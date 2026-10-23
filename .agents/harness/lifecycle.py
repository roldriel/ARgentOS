#!/usr/bin/env python3
"""ARgentOS adoption lifecycle CLI (RFC-81 / Plan 154, U1–U9 and U14).

One standard-library entry point, distributed with the payload inside the
``.agents/harness/`` family (D1), with four operations::

    install   materialize the payload into <project-root>/.argentos
    update    refresh managed artifacts without overwriting adopter changes
    uninstall remove only managed, non-diverged artifacts (preserve by default)
    doctor    report a deterministic diagnostic state

plus ``recover`` to resolve an interrupted operation from its journal.

Contract highlights (RFC-81 D1–D7, I1–I10):

* ``PROJECT_ROOT`` is an input (``--project-root`` or ``ARGENTOS_PROJECT_ROOT``).
* Ownership is provenance (``origin``) + verified state; a fingerprint only
  detects divergence and never proves authorship.
* The adapter ``<project-root>/AGENTS.md`` is generated only if absent; an
  existing one is preserved (manual integration) unless ``--replace-agents-md``.
* ``.gitignore`` is never modified; a documentary fragment is reported.
* ``uninstall`` preserves by default; ``--purge`` is limited to artifacts with
  ``origin == installed`` and ``state == present``.
* Recovery never silently overwrites changes the adopter made after an
  interruption: it stops with ``recovery pending`` and reports the conflict.
* Exit states are deterministic: success / no-op / conflict / recovery pending.

Usage::

    python lifecycle.py --project-root <p> install --payload <staged .agents>
    python lifecycle.py --project-root <p> update --payload <staged .agents>
    python lifecycle.py --project-root <p> uninstall [--purge] [--restore]
    python lifecycle.py --project-root <p> doctor
    python lifecycle.py --project-root <p> recover
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

import lifecycle_contract as contract  # noqa: E402
import lifecycle_root as root_binding  # noqa: E402
import lifecycle_staging as staging  # noqa: E402
import roots as _roots  # noqa: E402

# --- Exit states (deterministic; RFC-81 §"Estados de salida") -------------

SUCCESS = "success"
NOOP = "no-op"
CONFLICT = "conflict"
RECOVERY_PENDING = "recovery-pending"
EXIT_CODES = {SUCCESS: 0, NOOP: 10, CONFLICT: 20, RECOVERY_PENDING: 30}

#: The payload template that seeds the single active configuration.
FEATURES_FILENAME = "features.toml"


class LifecycleStop(Exception):
    """A fail-closed condition: the operation stops without deciding."""


class SimulatedCrash(Exception):
    """Test seam: an interruption injected after a phase for recovery tests."""


@dataclass
class Result:
    """Outcome of a lifecycle operation."""

    operation: str
    state: str
    message: str
    details: dict = field(default_factory=dict)

    @property
    def exit_code(self) -> int:
        return EXIT_CODES[self.state]

    def to_dict(self) -> dict:
        return {
            "operation": self.operation,
            "state": self.state,
            "message": self.message,
            "details": self.details,
        }


# --- Lock (mutual exclusion on ARGENTOS_ROOT) -----------------------------


class _Lock:
    def __init__(self, binding):
        self.binding = binding
        self._token = None

    def acquire(self) -> None:
        try:
            self._token = self.binding.lock_create()
        except root_binding.RootBindingError as exc:
            raise LifecycleStop(str(exc)) from exc

    def release(self) -> None:
        if self._token is not None:
            self.binding.lock_release(self._token)
            self._token = None


# --- Root identity (TOCTOU guard) -----------------------------------------

#: Cached Win32 function table; populated lazily only on Windows.
_WIN32 = None


def _win32():
    """Return the Win32 helpers, or ``None`` on non-Windows platforms."""
    global _WIN32
    if os.name != "nt":
        return None
    if _WIN32 is None:
        import ctypes
        from ctypes import wintypes

        class _BY_HANDLE_FILE_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("dwFileAttributes", wintypes.DWORD),
                ("ftCreationTime", wintypes.FILETIME),
                ("ftLastAccessTime", wintypes.FILETIME),
                ("ftLastWriteTime", wintypes.FILETIME),
                ("dwVolumeSerialNumber", wintypes.DWORD),
                ("nFileSizeHigh", wintypes.DWORD),
                ("nFileSizeLow", wintypes.DWORD),
                ("nNumberOfLinks", wintypes.DWORD),
                ("nFileIndexHigh", wintypes.DWORD),
                ("nFileIndexLow", wintypes.DWORD),
            ]

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateFileW.argtypes = [
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.HANDLE,
        ]
        kernel32.CreateFileW.restype = wintypes.HANDLE
        kernel32.GetFileInformationByHandle.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(_BY_HANDLE_FILE_INFORMATION),
        ]
        kernel32.GetFileInformationByHandle.restype = wintypes.BOOL
        kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel32.CloseHandle.restype = wintypes.BOOL
        _WIN32 = (ctypes, wintypes, kernel32, _BY_HANDLE_FILE_INFORMATION)
    return _WIN32


def _win_open_directory(path: Path):
    """Open a directory handle without delete sharing; ``None`` on failure."""
    lib = _win32()
    if lib is None:
        return None
    ctypes, _wintypes, kernel32, _info = lib
    handle = kernel32.CreateFileW(
        str(path),
        0x80000000,  # GENERIC_READ
        # FILE_SHARE_READ | FILE_SHARE_WRITE, deliberately WITHOUT
        # FILE_SHARE_DELETE: the open handle makes the directory and its
        # ancestors unrenamable/undeletable while the lifecycle holds it.
        0x1 | 0x2,
        None,
        3,  # OPEN_EXISTING
        0x02000000,  # FILE_FLAG_BACKUP_SEMANTICS (directories)
        None,
    )
    if handle == ctypes.c_void_p(-1).value:
        return None
    return handle


def _win_directory_id(handle):
    """Return ``(volume_serial, file_index)`` for a directory handle."""
    lib = _win32()
    if lib is None:
        return None
    ctypes, _wintypes, kernel32, info_type = lib
    info = info_type()
    if not kernel32.GetFileInformationByHandle(handle, ctypes.byref(info)):
        return None
    return (
        int(info.dwVolumeSerialNumber),
        (int(info.nFileIndexHigh) << 32) | int(info.nFileIndexLow),
    )


def _win_close(handle) -> None:
    lib = _win32()
    if lib is None:
        return
    _ctypes, _wintypes, kernel32, _info = lib
    kernel32.CloseHandle(handle)


# --- Engine ---------------------------------------------------------------


class LifecycleEngine:
    """Executes one lifecycle operation against an explicit ``PROJECT_ROOT``."""

    def __init__(
        self,
        project_root: str | os.PathLike[str],
        *,
        payload_dir: str | os.PathLike[str] | None = None,
        source_ref: str | None = None,
        repo: str | os.PathLike[str] | None = None,
        payload_subdir: str = "protocol/.agents",
        replace_agents_md: bool = False,
        purge: bool = False,
        restore: bool = False,
        force_restore: bool = False,
        staging_parent: str | os.PathLike[str] | None = None,
        fail_at: str | set[str] | None = None,
        crash_at: str | None = None,
        hook=None,
    ):
        self.roots = _roots.resolve(project_root)
        self.project_root = self.roots.project_root
        self.argentos_root = self.roots.argentos_root
        self.payload_dir = Path(payload_dir) if payload_dir else None
        self.source_ref = source_ref
        self.repo = Path(repo) if repo else None
        self.payload_subdir = payload_subdir
        self.replace_agents_md = replace_agents_md
        self.purge = purge
        self.restore = restore
        self.force_restore = force_restore
        self.staging_parent = Path(staging_parent) if staging_parent else None
        self.fail_at = (
            {fail_at}
            if isinstance(fail_at, str)
            else set(fail_at or ())
        )
        self.crash_at = crash_at
        self._hook = hook
        self._fired: set[str] = set()
        self._staging_root: Path | None = None
        self.binding = None
        self._binding_error: str | None = None
        try:
            self.binding = root_binding.open_root_binding(self.project_root)
        except root_binding.RootBindingError as exc:
            self._binding_error = str(exc)
        self._argentos_existed_before = False
        if self.binding is not None:
            try:
                self._argentos_existed_before = self.binding.exists(".argentos")
            except root_binding.RootBindingError:
                # The path is unsafe (for example a symlink). Do not mutate
                # during construction; the operation will fail closed later.
                self._argentos_existed_before = False
        self._adapter_inspection: dict | None = None

    # -- small helpers ----------------------------------------------------

    def _result(self, op: str, state: str, message: str, **details) -> Result:
        return Result(op, state, message, details)

    def _seam(self, name: str) -> None:
        """Testing/interruption seam fired once per phase name."""
        if name in self._fired:
            return
        self._fired.add(name)
        if self._hook is not None:
            self._hook(name, self)
        if name in self.fail_at:
            raise LifecycleStop(f"injected failure at phase {name!r}")
        if self.crash_at == name:
            raise SimulatedCrash(f"simulated interruption at phase {name!r}")

    def _assert_root_unchanged(self) -> None:
        binding = self._require_binding()
        if not binding.unchanged():
            raise LifecycleStop(
                "PROJECT_ROOT changed between validation and write (STOP)"
            )

    def _binding_failure(self, operation: str) -> Result | None:
        """Fail closed when no OS-level root binding could be established."""
        if self.binding is not None and self.binding.strong:
            return None
        detail = self._binding_error or "no strong root binding available"
        return self._result(
            operation,
            CONFLICT,
            f"strong root binding unavailable: {detail} (fail-closed)",
            root_guard="unavailable",
        )

    def _require_binding(self):
        if self.binding is None:
            raise LifecycleStop(
                "strong root binding unavailable; refusing the operation "
                "(fail-closed)"
            )
        return self.binding

    def close(self) -> None:
        """Release the root binding (idempotent)."""
        if self.binding is not None:
            self.binding.close()
            self.binding = None

    def _root_changed_result(self, operation: str) -> Result | None:
        """Return a CONFLICT result when the root changed, else ``None``."""
        try:
            self._assert_root_unchanged()
        except LifecycleStop as exc:
            return self._result(operation, CONFLICT, str(exc))
        return None

    def _write_file(self, rel: str, data: bytes) -> str:
        self._assert_root_unchanged()
        self._require_binding().write_atomic(rel, data)
        return contract.sha256_bytes(data)

    def _journal_then_write(
        self,
        rel: str,
        data,
        journal: dict,
        *,
        key: str = "created",
        extra: dict | None = None,
    ) -> str:
        """Record the intent, then write the file.

        The write used to precede the journal append, so a crash in between
        left a payload file that rollback could not see. Recording the intent
        first inverts the window: a crash now leaves a journal entry whose
        target does not exist yet, which ``_undo_create`` already tolerates.
        No file can exist without its journal record.
        """
        self._assert_root_unchanged()
        payload = data.encode("utf-8") if isinstance(data, str) else data
        digest = contract.sha256_bytes(payload)
        entry: dict = {"path": rel, "sha256": digest}
        if extra:
            entry.update(extra)
        journal[key].append(entry)
        self._journal_write(journal)
        self._write_file(rel, payload)
        return digest

    # -- staging ----------------------------------------------------------

    def _stage(self) -> tuple[Path, str, dict]:
        if self.payload_dir is not None and self.source_ref is not None:
            raise LifecycleStop("provide either --payload or --source, not both")
        if self.payload_dir is None and self.source_ref is None:
            raise LifecycleStop(
                "a payload source is required (--payload <dir> or --source <ref>)"
            )
        self._staging_root = staging.new_staging_root(self.staging_parent)
        if self.payload_dir is not None:
            # The payload origin must not be confusable with the project either.
            staging.ensure_staging_isolated(self.payload_dir, self.project_root)
            payload_root = staging.acquire_local_copy(
                self.payload_dir, self._staging_root
            )
            method = "local-copy"
            source = {"ref": None, "commit": None, "provenance": "local"}
        else:
            if self.repo is None:
                raise LifecycleStop("--source requires --repo <git repository>")
            payload_root, commit = staging.acquire_git_archive(
                self.repo, self.source_ref, self.payload_subdir, self._staging_root
            )
            method = "git-checkout"
            source = {
                "ref": self.source_ref,
                "commit": commit or None,
                "provenance": "git",
            }
        staging.ensure_staging_isolated(self._staging_root, self.project_root)
        problems = staging.validate_payload(payload_root)
        if problems:
            raise LifecycleStop("invalid payload: " + "; ".join(problems))
        return payload_root, method, source

    def _cleanup_staging(self) -> None:
        if self._staging_root is not None:
            import shutil

            shutil.rmtree(self._staging_root, ignore_errors=True)
            self._staging_root = None

    @staticmethod
    def _payload_version(payload_root: Path) -> str:
        return (payload_root / "VERSION").read_text(encoding="utf-8").strip()

    @staticmethod
    def _payload_files(payload_root: Path) -> list[Path]:
        return sorted(
            (p for p in payload_root.rglob("*") if p.is_file()),
            key=lambda p: p.as_posix().encode("utf-8"),
        )

    # -- journal ----------------------------------------------------------

    def _journal(self) -> dict | None:
        try:
            if not self._require_binding().exists(contract.JOURNAL_REL):
                return None
            raw = self._require_binding().read_bytes(contract.JOURNAL_REL)
            return json.loads(raw.decode("utf-8"))
        except root_binding.RootBindingError:
            return {"status": "corrupt", "phase": "unknown"}
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            return {"status": "corrupt", "phase": "unknown"}

    def _journal_write(self, journal: dict) -> None:
        journal["updated_at"] = contract.utc_now()
        data = json.dumps(journal, indent=2, ensure_ascii=False) + "\n"
        self._require_binding().write_atomic(
            contract.JOURNAL_REL, data.encode("utf-8")
        )

    def _new_journal(self, operation: str, version: str) -> dict:
        return {
            "journal_schema_version": contract.JOURNAL_SCHEMA_VERSION,
            "operation_id": uuid.uuid4().hex,
            "operation": operation,
            "phase": "journal",
            "status": "open",
            "project_root_realpath": self._require_binding().root_realpath,
            "argentos_root_existed": self._argentos_existed_before,
            "protocol_version": version,
            "started_at": contract.utc_now(),
            "updated_at": contract.utc_now(),
            "created": [],
            "replaced": [],
            "removed": [],
            "backups": [],
        }

    def _backup_file(self, rel: str, journal: dict) -> str:
        """Copy the current ``rel`` into ``.backup/<stamp>/<rel>``; return rel."""
        binding = self._require_binding()
        self._assert_root_unchanged()
        data = binding.read_bytes(rel)
        stamp = journal["operation_id"]
        backup_rel = f"{contract.BACKUP_DIR_REL}/{stamp}/{rel}"
        if binding.exists(backup_rel):
            raise LifecycleStop(f"backup entry already exists: {backup_rel}")
        binding.write_atomic(backup_rel, data)
        journal["backups"].append(
            {
                "path": backup_rel,
                "replaced": rel,
                "origin": "preexisting",
                "sha256": contract.sha256_bytes(data),
                "created_at": contract.utc_now(),
            }
        )
        return backup_rel

    # -- install ----------------------------------------------------------

    def install(self) -> Result:
        """Public entry point; staging is always cleaned up."""
        failure = self._binding_failure("install")
        if failure is not None:
            self.close()
            return failure
        try:
            return self._install_run()
        except SimulatedCrash as exc:
            return self._result(
                "install",
                RECOVERY_PENDING,
                "installation interrupted before committing",
                phase=str(exc),
            )
        except root_binding.RootBindingError as exc:
            return self._result(
                "install",
                CONFLICT,
                f"root binding refused a managed path: {exc}",
            )
        finally:
            self._cleanup_staging()
            self.close()

    def _install_run(self) -> Result:
        try:
            payload_root, method, source = self._stage()
            self._assert_root_unchanged()
        except (LifecycleStop, staging.StagingError) as exc:
            self._cleanup_staging()
            return self._result("install", CONFLICT, str(exc))
        self._seam("preflight")
        root_changed = self._root_changed_result("install")
        if root_changed is not None:
            self._cleanup_staging()
            return root_changed

        # An open journal means a previous operation never reached its commit
        # point. Reporting NOOP from a clean manifest would hide a half-applied
        # operation (the manifest is written just before the journal commits),
        # so the only safe answer is recovery-pending.
        open_journal = self._journal()
        if open_journal is not None and open_journal.get("status") != "committed":
            self._cleanup_staging()
            return self._result(
                "install",
                RECOVERY_PENDING,
                "a previous operation never reached its commit point "
                f"(open lifecycle journal, phase {open_journal.get('phase')!r}): "
                "run `recover` before installing again (STOP)",
            )

        try:
            manifest = self._require_binding().load_manifest()
        except contract.ManifestError as exc:
            self._cleanup_staging()
            return self._result(
                "install", CONFLICT, f"manifest invalid (fail-closed): {exc}"
            )

        if manifest is None and self._require_binding().exists(".argentos"):
            self._cleanup_staging()
            return self._result(
                "install",
                CONFLICT,
                "unrecognized .argentos/ without a manifest (STOP)",
            )

        version = self._payload_version(payload_root)
        if manifest is not None:
            self._cleanup_staging()
            managed = manifest.get("install", {}).get("managed")
            if managed is not True:
                # Previously uninstalled (managed=false): a reinstall is valid.
                return self._reinstall(version)
            if self._install_is_clean(manifest, version):
                return self._result(
                    "install",
                    NOOP,
                    "installation already present and unchanged (idempotent)",
                    protocol_version=version,
                )
            return self._result(
                "install",
                CONFLICT,
                "an installation already exists; use update",
                installed_version=manifest.get("protocol_version"),
                incoming_version=version,
            )

        lock = _Lock(self.binding)
        try:
            lock.acquire()
        except LifecycleStop as exc:
            self._cleanup_staging()
            return self._result("install", CONFLICT, str(exc))
        try:
            result = self._install_fresh(payload_root, method, source, version)
        finally:
            lock.release()
            self._cleanup_staging()
        self._cleanup_after_revert(result)
        return result

    def _install_is_clean(self, manifest: dict, version: str) -> bool:
        if manifest.get("protocol_version") != version:
            return False
        if not self._require_binding().is_file(
            f"{contract.PAYLOAD_ROOT_REL}/INDEX.md"
        ):
            return False
        return not self._divergences(manifest)

    def _reinstall(self, version: str) -> Result:
        """Reinstall over a manifest flagged ``managed=false`` (post-uninstall)."""
        try:
            payload_root, method, source = self._stage()
        except (LifecycleStop, staging.StagingError) as exc:
            self._cleanup_staging()
            return self._result("install", CONFLICT, str(exc))
        lock = _Lock(self.binding)
        try:
            lock.acquire()
        except LifecycleStop as exc:
            self._cleanup_staging()
            return self._result("install", CONFLICT, str(exc))
        try:
            result = self._install_fresh(payload_root, method, source, version)
        finally:
            lock.release()
            self._cleanup_staging()
        self._cleanup_after_revert(result)
        return result

    def _divergences(self, manifest: dict) -> list[dict]:
        binding = self._require_binding()
        out: list[dict] = []
        for entry in manifest.get("files", []):
            state = binding.classify_entry(entry)
            if state != contract.OWNERSHIP_MANAGED_UNCHANGED:
                out.append({"path": entry["path"], "state": state})
        for entry in manifest.get("generated", []):
            state = binding.classify_entry(entry)
            if state != contract.OWNERSHIP_MANAGED_UNCHANGED:
                out.append({"path": entry["path"], "state": state})
        return out

    def _install_fresh(
        self, payload_root: Path, method: str, source: dict, version: str
    ) -> Result:
        root_changed = self._root_changed_result("install")
        if root_changed is not None:
            return root_changed
        binding = self._require_binding()
        adapter_present = binding.exists(contract.ADAPTER_REL)
        adapter_hash = (
            binding.sha256(contract.ADAPTER_REL) if adapter_present else None
        )
        self._adapter_inspection = {
            "present": adapter_present,
            "sha256": adapter_hash,
        }
        historical_agents = binding.exists(".agents")
        gitignore_present = binding.exists(".gitignore")
        config_present = binding.exists(contract.ACTIVE_CONFIG_REL)
        self._seam("inventory")

        journal = self._new_journal("install", version)
        try:
            self._assert_root_unchanged()
        except LifecycleStop as exc:
            return self._result("install", CONFLICT, str(exc))
        self._journal_write(journal)
        self._seam("journal")

        try:
            # --- backup phase: replace the adapter only with explicit opt-in.
            self._assert_root_unchanged()
            adapter_origin = "installed"
            if adapter_present and self.replace_agents_md:
                if binding.sha256(contract.ADAPTER_REL) != adapter_hash:
                    raise LifecycleStop(
                        "AGENTS.md changed between inspection and operation (STOP)"
                    )
                self._backup_file(contract.ADAPTER_REL, journal)
                adapter_origin = "substituted-authorized"
            self._seam("backup")

            # --- apply phase: payload files, config seed, adapter.
            self._assert_root_unchanged()
            binding.mkdirs(contract.BACKUP_DIR_REL)
            written: dict[str, str] = {}
            for src in self._payload_files(payload_root):
                rel = f"{contract.PAYLOAD_ROOT_REL}/{src.relative_to(payload_root).as_posix()}"
                digest = self._journal_then_write(rel, src.read_bytes(), journal)
                written[rel] = digest
                self._seam("apply")

            if not config_present:
                template = payload_root / FEATURES_FILENAME
                if template.is_file():
                    self._journal_then_write(
                        contract.ACTIVE_CONFIG_REL, template.read_bytes(), journal
                    )

            adapter_generated = False
            if not adapter_present:
                self._journal_then_write(
                    contract.ADAPTER_REL, self._adapter_content(version), journal
                )
                adapter_generated = True
            elif self.replace_agents_md:
                self._journal_then_write(
                    contract.ADAPTER_REL, self._adapter_content(version), journal
                )
                adapter_generated = True
            self._seam("apply")

            # --- post-validation.
            problems = self._post_validate(written)
            if problems:
                raise LifecycleStop("post-validation failed: " + "; ".join(problems))
            self._seam("post_validate")

            # --- commit: build + atomically write the manifest.
            self._seam("commit")
            manifest = self._build_manifest(
                payload_root, method, source, version, journal, adapter_origin,
                adapter_generated, config_present,
            )
            self._assert_root_unchanged()
            binding.save_manifest(manifest)
            journal["status"] = "committed"
            journal["phase"] = "commit"
            self._journal_write(journal)
            self._assert_root_unchanged()
            return self._result(
                "install",
                SUCCESS,
                "installation completed",
                protocol_version=version,
                manifest=contract.MANIFEST_REL,
                gitignore_modified=False,
                historical_agents_detected=historical_agents,
                gitignore_present=gitignore_present,
                files_installed=len(written),
            )
        except SimulatedCrash:
            return self._result(
                "install",
                RECOVERY_PENDING,
                "installation interrupted; run recover",
                phase=journal.get("phase"),
            )
        except LifecycleStop as exc:
            return self._rollback(journal, str(exc))
        except Exception as exc:  # noqa: BLE001 — fail-closed, then roll back
            return self._rollback(journal, f"unexpected failure: {exc}")

    def _post_validate(self, written: dict[str, str]) -> list[str]:
        binding = self._require_binding()
        problems: list[str] = []
        for rel, digest in written.items():
            if not binding.exists(rel):
                problems.append(f"missing after write: {rel}")
            elif binding.sha256(rel) != digest:
                problems.append(f"hash mismatch after write: {rel}")
        return problems

    def _adapter_content(self, version: str) -> bytes:
        text = (
            "<!-- Generated by the ARgentOS adoption lifecycle. Non-normative"
            " adapter; do not treat as the protocol source. -->\n"
            "# AGENTS.md\n\n"
            "This project adopts **ARgentOS**. The normative bootstrap is:\n\n"
            "    .argentos/.agents/INDEX.md\n\n"
            "Read that file and follow the protocol it defines. This adapter is\n"
            "generated for discovery and is not the payload entry point.\n"
            f"\n<!-- protocol_version: {version} -->\n"
        )
        return text.encode("utf-8")

    def _build_manifest(
        self,
        payload_root: Path,
        method: str,
        source: dict,
        version: str,
        journal: dict,
        adapter_origin: str,
        adapter_generated: bool,
        config_present: bool,
    ) -> dict:
        binding = self._require_binding()
        files = []
        for src in self._payload_files(payload_root):
            rel = f"{contract.PAYLOAD_ROOT_REL}/{src.relative_to(payload_root).as_posix()}"
            files.append(binding.file_entry(rel, "installed"))
        if binding.exists(contract.ACTIVE_CONFIG_REL):
            files.append(
                binding.file_entry(
                    contract.ACTIVE_CONFIG_REL,
                    "preexisting" if config_present else "installed",
                )
            )
        generated = []
        if adapter_generated:
            generated.append(
                {
                    "path": contract.ADAPTER_REL,
                    "kind": "adapter",
                    "origin": adapter_origin,
                    "sha256": binding.sha256(contract.ADAPTER_REL),
                }
            )
        manifest = {
            "manifest_schema_version": contract.MANIFEST_SCHEMA_VERSION,
            "protocol_version": version,
            "install": {
                "manifest_path": contract.MANIFEST_REL,
                "method": method,
                "source": source,
                "installed_at": contract.utc_now(),
                "managed": True,
            },
            "config": {"active_path": contract.ACTIVE_CONFIG_REL},
            "files": sorted(files, key=lambda e: e["path"].encode("utf-8")),
            "generated": sorted(generated, key=lambda e: e["path"].encode("utf-8")),
            "backups": sorted(
                journal["backups"], key=lambda e: e["path"].encode("utf-8")
            ),
        }
        return manifest

    # -- rollback / recovery ---------------------------------------------

    def _rollback(
        self, journal: dict, reason: str, *, success_state: str = CONFLICT
    ) -> Result:
        op = journal.get("operation", "install")
        if not self._require_binding().unchanged():
            # The binding would keep an undo on the original object, but the
            # pathname no longer identifies the validated root. Stop rather
            # than mutate either root; the replacement is left untouched and
            # the original is preserved for manual recovery.
            return self._result(
                op,
                CONFLICT,
                f"{reason}; PROJECT_ROOT changed: rollback was NOT attempted "
                "on the replacement root",
                root_changed=True,
            )
        if "rollback" in self.fail_at:
            journal["status"] = "recovery-pending"
            journal["phase"] = "rollback"
            self._journal_write(journal)
            return self._result(
                op,
                RECOVERY_PENDING,
                f"rollback failed after {reason}; recovery pending",
                phase=journal.get("phase"),
            )
        conflicts: list[dict] = []
        for entry in reversed(journal.get("created", [])):
            conflict = self._undo_create(entry)
            if conflict:
                conflicts.append(conflict)
        for entry in reversed(journal.get("replaced", [])):
            conflict = self._undo_replace(entry)
            if conflict:
                conflicts.append(conflict)
        for entry in reversed(journal.get("removed", [])):
            conflict = self._undo_remove(entry)
            if conflict:
                conflicts.append(conflict)
        if conflicts:
            journal["status"] = "recovery-pending"
            journal["phase"] = "rollback"
            self._journal_write(journal)
            return self._result(
                op,
                RECOVERY_PENDING,
                f"{reason}; recovery pending — later changes detected",
                conflicts=conflicts,
            )
        self._prune_empty_dirs()
        journal["status"] = "rolled-back"
        journal["phase"] = "rollback"
        self._journal_write(journal)
        result = self._result(
            op, success_state, f"operation aborted and rolled back: {reason}"
        )
        result.details["operation_id"] = journal.get("operation_id")
        result.details["created_scaffolding"] = not journal.get(
            "argentos_root_existed"
        )
        return result

    def _cleanup_after_revert(self, result: Result) -> None:
        """Remove the ARgentOS scaffolding a reverted ``install`` created.

        Only reached after a *successful* rollback that restored every prior
        artifact, and only when ``.argentos/`` did not exist before the
        operation — so the adopter's data is never at risk. Called after the
        lock has been released (the lock file lives inside the scaffolding).
        """
        if not result.details.get("created_scaffolding"):
            return
        binding = self._require_binding()
        operation_id = result.details.get("operation_id")
        batch = f"{contract.BACKUP_DIR_REL}/{str(operation_id)}"
        if binding.is_dir(batch):
            binding.remove_tree(batch)
        for rel in (contract.JOURNAL_REL, contract.LOCK_REL):
            try:
                if binding.exists(rel):
                    binding.unlink(rel)
            except (OSError, root_binding.RootBindingError):
                pass
        for rel in (
            contract.PAYLOAD_ROOT_REL,
            contract.BACKUP_DIR_REL,
            contract.PROJECT_STATE_DIR_REL,
            ".argentos",
        ):
            binding.prune_empty(rel)

    def _undo_create(self, entry: dict) -> dict | None:
        binding = self._require_binding()
        rel = entry["path"]
        if not binding.exists(rel):
            return None
        current = binding.sha256(rel)
        if current != entry.get("sha256"):
            return {"path": rel, "reason": "modified after write"}
        binding.unlink(rel)
        return None

    def _undo_replace(self, entry: dict) -> dict | None:
        binding = self._require_binding()
        rel = entry["path"]
        if not binding.exists(rel):
            return {"path": rel, "reason": "removed after write"}
        if binding.sha256(rel) != entry.get("sha256"):
            return {"path": rel, "reason": "modified after write"}
        binding.write_atomic(rel, binding.read_bytes(entry["backup"]))
        return None

    def _undo_remove(self, entry: dict) -> dict | None:
        binding = self._require_binding()
        rel = entry["path"]
        backup = entry["backup"]
        if binding.exists(rel):
            # The intent is journaled before the unlink, so an existing target
            # that still matches its backup means the removal never happened:
            # nothing to undo. A different file was recreated after removal.
            try:
                unchanged = binding.read_bytes(rel) == binding.read_bytes(backup)
            except OSError:
                unchanged = False
            if unchanged:
                return None
            return {"path": rel, "reason": "recreated after removal"}
        binding.write_atomic(rel, binding.read_bytes(backup))
        return None

    def _prune_empty_dirs(self) -> None:
        binding = self._require_binding()
        for rel in (
            contract.PAYLOAD_ROOT_REL,
            contract.BACKUP_DIR_REL,
            contract.PROJECT_STATE_DIR_REL,
            ".argentos",
        ):
            binding.prune_empty(rel)

    def recover(self) -> Result:
        failure = self._binding_failure("recover")
        if failure is not None:
            self.close()
            return failure
        try:
            return self._recover_run()
        except root_binding.RootBindingError as exc:
            return self._result(
                "recover", CONFLICT, f"root binding refused a managed path: {exc}"
            )
        finally:
            self.close()

    def _recover_run(self) -> Result:
        journal = self._journal()
        if journal is None:
            return self._result(
                "recover", NOOP, "no operation journal present (nothing to recover)"
            )
        if journal.get("status") in ("committed", "rolled-back"):
            return self._result(
                "recover",
                NOOP,
                f"journal already closed ({journal.get('status')})",
            )
        lock = _Lock(self.binding)
        try:
            lock.acquire()
        except LifecycleStop as exc:
            return self._result("recover", CONFLICT, str(exc))
        try:
            result = self._rollback(
                journal, "recovery of interrupted operation", success_state=SUCCESS
            )
        finally:
            lock.release()
        self._cleanup_after_revert(result)
        return result

    # -- update -----------------------------------------------------------

    def update(self) -> Result:
        failure = self._binding_failure("update")
        if failure is not None:
            self.close()
            return failure
        try:
            return self._update_run()
        except SimulatedCrash as exc:
            return self._result(
                "update",
                RECOVERY_PENDING,
                "update interrupted before committing",
                phase=str(exc),
            )
        except root_binding.RootBindingError as exc:
            return self._result(
                "update",
                CONFLICT,
                f"root binding refused a managed path: {exc}",
            )
        finally:
            self.close()

    def _update_run(self) -> Result:
        try:
            manifest = self._require_binding().load_manifest()
        except contract.ManifestError as exc:
            return self._result("update", CONFLICT, f"manifest invalid: {exc}")
        if manifest is None:
            return self._result(
                "update", CONFLICT, "no installation manifest found (use install)"
            )
        try:
            payload_root, method, source = self._stage()
            self._assert_root_unchanged()
        except (LifecycleStop, staging.StagingError) as exc:
            self._cleanup_staging()
            return self._result("update", CONFLICT, str(exc))
        self._seam("preflight")
        root_changed = self._root_changed_result("update")
        if root_changed is not None:
            self._cleanup_staging()
            return root_changed
        version = self._payload_version(payload_root)

        divergences = self._divergences(manifest)
        if divergences:
            self._cleanup_staging()
            return self._result(
                "update",
                CONFLICT,
                "local divergence or missing managed artifacts (STOP; not a no-op)",
                divergences=divergences,
            )

        lock = _Lock(self.binding)
        try:
            lock.acquire()
        except LifecycleStop as exc:
            self._cleanup_staging()
            return self._result("update", CONFLICT, str(exc))
        try:
            result = self._update_apply(manifest, payload_root, method, source, version)
        finally:
            lock.release()
            self._cleanup_staging()
        self._cleanup_after_revert(result)
        return result

    def _update_apply(
        self,
        manifest: dict,
        payload_root: Path,
        method: str,
        source: dict,
        version: str,
    ) -> Result:
        root_changed = self._root_changed_result("update")
        if root_changed is not None:
            return root_changed
        binding = self._require_binding()
        known = {e["path"]: e for e in manifest.get("files", [])}
        target_files: list[tuple[str, Path, bytes]] = []
        for src in self._payload_files(payload_root):
            rel = f"{contract.PAYLOAD_ROOT_REL}/{src.relative_to(payload_root).as_posix()}"
            data = src.read_bytes()
            target_files.append((rel, src, data))
        removed_from_payload = [
            rel for rel in known if rel.startswith(contract.PAYLOAD_ROOT_REL + "/")
            and rel not in {r for r, _, _ in target_files}
        ]
        self._seam("inventory")

        journal = self._new_journal("update", version)
        try:
            self._assert_root_unchanged()
        except LifecycleStop as exc:
            return self._result("update", CONFLICT, str(exc))
        self._journal_write(journal)
        self._seam("journal")

        changed = False
        try:
            self._assert_root_unchanged()
            for rel, src, data in target_files:
                current = known.get(rel)
                if binding.exists(rel):
                    if binding.sha256(rel) == contract.sha256_bytes(data):
                        continue  # already identical: idempotent, no rewrite
                    backup = self._backup_file(rel, journal)
                    self._journal_then_write(
                        rel, data, journal, key="replaced", extra={"backup": backup}
                    )
                    changed = True
                else:
                    self._journal_then_write(rel, data, journal)
                    changed = True
                self._seam("apply")
            self._seam("apply")

            if not changed and manifest.get("protocol_version") == version:
                journal["status"] = "rolled-back"
                journal["phase"] = "noop"
                self._journal_write(journal)
                return self._result(
                    "update",
                    NOOP,
                    "already up to date (idempotent)",
                    protocol_version=version,
                )

            problems = self._post_validate(
                {rel: binding.sha256(rel) for rel, _, _ in target_files}
            )
            if problems:
                raise LifecycleStop("post-validation failed: " + "; ".join(problems))
            self._seam("post_validate")

            manifest["protocol_version"] = version
            manifest["install"]["method"] = method
            manifest["install"]["source"] = source
            manifest["install"]["installed_at"] = contract.utc_now()
            files = []
            for rel, _, _ in target_files:
                origin = known.get(rel, {}).get("origin", "installed")
                files.append(binding.file_entry(rel, origin))
            # Artifacts removed from the payload stay owned and reported, never
            # silently dropped from the manifest.
            files.extend(known[rel] for rel in removed_from_payload)
            if binding.exists(contract.ACTIVE_CONFIG_REL):
                files.append(
                    binding.file_entry(
                        contract.ACTIVE_CONFIG_REL,
                        known.get(contract.ACTIVE_CONFIG_REL, {}).get(
                            "origin", "installed"
                        ),
                    )
                )
            manifest["files"] = sorted(
                files, key=lambda e: e["path"].encode("utf-8")
            )
            manifest["backups"] = sorted(
                manifest.get("backups", []) + journal["backups"],
                key=lambda e: e["path"].encode("utf-8"),
            )
            self._seam("commit")
            self._assert_root_unchanged()
            binding.save_manifest(manifest)
            journal["status"] = "committed"
            journal["phase"] = "commit"
            self._journal_write(journal)
            self._assert_root_unchanged()
            return self._result(
                "update",
                SUCCESS,
                "update completed",
                protocol_version=version,
                removed_from_payload=removed_from_payload,
            )
        except SimulatedCrash:
            return self._result(
                "update",
                RECOVERY_PENDING,
                "update interrupted; run recover",
                phase=journal.get("phase"),
            )
        except LifecycleStop as exc:
            return self._rollback(journal, str(exc))
        except Exception as exc:  # noqa: BLE001
            return self._rollback(journal, f"unexpected failure: {exc}")

    # -- uninstall --------------------------------------------------------

    def uninstall(self) -> Result:
        failure = self._binding_failure("uninstall")
        if failure is not None:
            self.close()
            return failure
        try:
            return self._uninstall_run()
        except SimulatedCrash as exc:
            return self._result(
                "uninstall",
                RECOVERY_PENDING,
                "uninstall interrupted before committing",
                phase=str(exc),
            )
        except root_binding.RootBindingError as exc:
            return self._result(
                "uninstall",
                CONFLICT,
                f"root binding refused a managed path: {exc}",
            )
        finally:
            self.close()

    def _uninstall_run(self) -> Result:
        try:
            manifest = self._require_binding().load_manifest()
        except contract.ManifestError as exc:
            return self._result("uninstall", CONFLICT, f"manifest invalid: {exc}")
        if manifest is None:
            return self._result(
                "uninstall",
                CONFLICT,
                "no installation manifest found (fail-closed)",
            )
        lock = _Lock(self.binding)
        try:
            lock.acquire()
        except LifecycleStop as exc:
            return self._result("uninstall", CONFLICT, str(exc))
        try:
            result = self._uninstall_apply(manifest)
        finally:
            lock.release()
        self._cleanup_after_revert(result)
        return result

    def _uninstall_apply(self, manifest: dict) -> Result:
        root_changed = self._root_changed_result("uninstall")
        if root_changed is not None:
            return root_changed
        binding = self._require_binding()
        eligible: list[str] = []
        preserved: list[dict] = []
        for entry in manifest.get("files", []):
            state = binding.classify_entry(entry)
            if entry.get("origin") == "installed" and state == contract.OWNERSHIP_MANAGED_UNCHANGED:
                if entry["path"] == contract.ACTIVE_CONFIG_REL:
                    preserved.append({"path": entry["path"], "reason": "active config"})
                    continue
                eligible.append(entry["path"])
            else:
                preserved.append({"path": entry["path"], "state": state})
        adapter_remove: str | None = None
        for entry in manifest.get("generated", []):
            state = binding.classify_entry(entry)
            if entry.get("origin") == "installed" and state == contract.OWNERSHIP_MANAGED_UNCHANGED:
                adapter_remove = entry["path"]
            else:
                preserved.append({"path": entry["path"], "state": state})
        for rel in self._unknown_artifacts(manifest):
            preserved.append({"path": rel, "state": contract.OWNERSHIP_UNVERIFIED})
        self._seam("inventory")

        if not eligible and adapter_remove is None and not self.purge:
            return self._result(
                "uninstall",
                NOOP,
                "nothing eligible for removal (preserve by default)",
                preserved=preserved,
            )

        journal = self._new_journal("uninstall", manifest.get("protocol_version", ""))
        try:
            self._assert_root_unchanged()
        except LifecycleStop as exc:
            return self._result("uninstall", CONFLICT, str(exc))
        self._journal_write(journal)
        self._seam("journal")
        try:
            self._assert_root_unchanged()
            for rel in eligible + ([adapter_remove] if adapter_remove else []):
                backup = self._backup_file(rel, journal)
                self._assert_root_unchanged()
                # Record the removal before performing it: a crash after the
                # unlink and before the journal append used to leave a file
                # gone with no record of its removal.
                journal["removed"].append({"path": rel, "backup": backup})
                self._journal_write(journal)
                binding.unlink(rel)
                self._seam("apply")
            self._seam("apply")

            if self.restore or self.force_restore:
                self._restore_backups(manifest, journal)
            self._seam("post_validate")

            self._seam("commit")
            if self.purge:
                if binding.exists(contract.MANIFEST_REL):
                    self._assert_root_unchanged()
                    binding.unlink(contract.MANIFEST_REL)
            else:
                remaining = []
                for entry in manifest.get("files", []):
                    if entry["path"] in eligible:
                        continue
                    remaining.append(entry)
                manifest["files"] = remaining
                if adapter_remove is not None:
                    manifest["generated"] = [
                        entry
                        for entry in manifest.get("generated", [])
                        if entry["path"] != adapter_remove
                    ]
                manifest["install"]["managed"] = False
                manifest["install"]["uninstalled_at"] = contract.utc_now()
                manifest["backups"] = sorted(
                    manifest.get("backups", []) + journal["backups"],
                    key=lambda e: e["path"].encode("utf-8"),
                )
                self._assert_root_unchanged()
                binding.save_manifest(manifest)
            journal["status"] = "committed"
            journal["phase"] = "commit"
            self._journal_write(journal)
            self._assert_root_unchanged()
            return self._result(
                "uninstall",
                SUCCESS,
                "uninstall completed (preserve by default)"
                + (" [--purge]" if self.purge else ""),
                removed=eligible + ([adapter_remove] if adapter_remove else []),
                preserved=preserved,
                purge=self.purge,
            )
        except SimulatedCrash:
            return self._result(
                "uninstall",
                RECOVERY_PENDING,
                "uninstall interrupted; run recover",
                phase=journal.get("phase"),
            )
        except LifecycleStop as exc:
            return self._rollback(journal, str(exc))
        except Exception as exc:  # noqa: BLE001
            return self._rollback(journal, f"unexpected failure: {exc}")

    def _restore_backups(self, manifest: dict, journal: dict) -> None:
        binding = self._require_binding()
        for entry in manifest.get("backups", []):
            dest = entry["replaced"]
            if binding.exists(dest):
                continue  # never overwrite a later adopter file
            backup = entry["path"]
            if not binding.exists(backup):
                continue
            binding.write_atomic(dest, binding.read_bytes(backup))

    def _unknown_artifacts(self, manifest: dict) -> list[str]:
        """Project-relative files under ``.argentos/`` the manifest does not own.

        These are the adopter's — reported, never touched (I5, D3).
        """
        binding = self._require_binding()
        known: set[str] = set()
        for kind in ("files", "generated", "backups"):
            for entry in manifest.get(kind, []):
                known.add(entry.get("path"))
        known.add(contract.MANIFEST_REL)
        known.add(contract.JOURNAL_REL)
        known.add(contract.LOCK_REL)
        out: list[str] = []
        for rel in sorted(binding.walk_files(".argentos")):
            if rel in known:
                continue
            if rel.startswith(contract.BACKUP_DIR_REL + "/"):
                continue
            out.append(rel)
        return out

    # -- doctor -----------------------------------------------------------

    def doctor(self) -> Result:
        failure = self._binding_failure("doctor")
        if failure is not None:
            self.close()
            return failure
        try:
            return self._doctor_run()
        except root_binding.RootBindingError as exc:
            return self._result(
                "doctor", CONFLICT, f"root binding refused a managed path: {exc}"
            )
        finally:
            self.close()

    def _doctor_run(self) -> Result:
        journal = self._journal()
        if journal is not None and journal.get("status") not in (
            "committed",
            "rolled-back",
        ):
            state = (
                "backup-pending-restore"
                if journal.get("status") == "recovery-pending"
                else "incomplete-recoverable"
            )
            return self._doctor_result(state, journal=journal)

        try:
            manifest = self._require_binding().load_manifest()
        except contract.ManifestError as exc:
            return self._doctor_result("invalid-manifest", evidence=str(exc))

        if manifest is None:
            if self._require_binding().exists(".argentos"):
                if self._require_binding().is_dir(contract.PAYLOAD_ROOT_REL):
                    return self._doctor_result("needs-manual-intervention")
                return self._doctor_result("unrecognized")
            return self._doctor_result("installation-absent")

        if manifest.get("install", {}).get("managed") is False:
            return self._doctor_result("installation-absent")

        divergences = self._divergences(manifest)
        installed_version = None
        version_rel = f"{contract.PAYLOAD_ROOT_REL}/VERSION"
        if self._require_binding().is_file(version_rel):
            installed_version = (
                self._require_binding().read_bytes(version_rel).decode("utf-8").strip()
            )
        if installed_version and installed_version != manifest.get("protocol_version"):
            return self._doctor_result(
                "version-conflict",
                evidence={
                    "manifest": manifest.get("protocol_version"),
                    "payload": installed_version,
                },
            )
        if divergences:
            return self._doctor_result("local-divergence", evidence=divergences)
        if not self._require_binding().is_file(
            f"{contract.PAYLOAD_ROOT_REL}/INDEX.md"
        ):
            return self._doctor_result("needs-manual-intervention")
        return self._doctor_result("valid", evidence=contract.MANIFEST_REL)

    def _doctor_result(self, doctor_state: str, **extra) -> Result:
        if doctor_state in ("installation-absent", "valid"):
            state = SUCCESS
        elif doctor_state in ("incomplete-recoverable", "backup-pending-restore"):
            state = RECOVERY_PENDING
        else:
            state = CONFLICT
        return self._result(
            "doctor", state, doctor_state, doctor_state=doctor_state, **extra
        )


# --- CLI ------------------------------------------------------------------


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--project-root",
        "--root",
        dest="project_root",
        default=None,
        help=(
            "real project root (default: the "
            f"{_roots.ENV_PROJECT_ROOT} environment variable)"
        ),
    )
    parser.add_argument(
        "--staging-parent",
        dest="staging_parent",
        default=None,
        help="directory that hosts the temporary staging root (default: system temp)",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ARgentOS adoption lifecycle")
    _add_common(parser)
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("install", "update"):
        p = sub.add_parser(name)
        p.add_argument("--payload", dest="payload_dir", default=None)
        p.add_argument("--source", dest="source_ref", default=None)
        p.add_argument("--repo", dest="repo", default=None)
        p.add_argument("--payload-subdir", dest="payload_subdir", default="protocol/.agents")
        if name == "install":
            p.add_argument("--replace-agents-md", action="store_true")

    p_un = sub.add_parser("uninstall")
    p_un.add_argument("--purge", action="store_true")
    p_un.add_argument("--restore", action="store_true")
    p_un.add_argument("--force-restore", action="store_true")

    sub.add_parser("doctor")
    sub.add_parser("recover")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    project_root = args.project_root or os.environ.get(_roots.ENV_PROJECT_ROOT)
    try:
        engine = LifecycleEngine(
            project_root,
            payload_dir=getattr(args, "payload_dir", None),
            source_ref=getattr(args, "source_ref", None),
            repo=getattr(args, "repo", None),
            payload_subdir=getattr(args, "payload_subdir", "protocol/.agents"),
            replace_agents_md=getattr(args, "replace_agents_md", False),
            purge=getattr(args, "purge", False),
            restore=getattr(args, "restore", False),
            force_restore=getattr(args, "force_restore", False),
            staging_parent=getattr(args, "staging_parent", None),
        )
    except _roots.RootResolutionError as exc:
        print(json.dumps({"state": CONFLICT, "message": str(exc)}, indent=2))
        return EXIT_CODES[CONFLICT]

    command = args.command
    if command == "install":
        result = engine.install()
    elif command == "update":
        result = engine.update()
    elif command == "uninstall":
        result = engine.uninstall()
    elif command == "doctor":
        result = engine.doctor()
    else:
        result = engine.recover()
    print(json.dumps(result.to_dict(), indent=2))
    return result.exit_code


if __name__ == "__main__":
    sys.exit(main())
