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
    def __init__(self, path: Path):
        self.path = path
        self._fd: int | None = None

    def acquire(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self._fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as exc:
            raise LifecycleStop(
                "another lifecycle operation holds the lock on this root"
            ) from exc
        os.write(self._fd, f"{os.getpid()} {contract.utc_now()}\n".encode("utf-8"))

    def release(self) -> None:
        if self._fd is not None:
            os.close(self._fd)
            self._fd = None
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


def _identify(root: Path) -> tuple[str, int, int] | None:
    try:
        stat = os.stat(root)
    except OSError:
        return None
    return (os.path.realpath(str(root)), stat.st_dev, stat.st_ino)


def _prune_empty_tree(base: Path) -> None:
    """Remove ``base`` and any now-empty descendants (bottom-up)."""
    if not base.is_dir():
        return
    for dirpath, _dirnames, _filenames in os.walk(base, topdown=False):
        try:
            if not os.listdir(dirpath):
                os.rmdir(dirpath)
        except OSError:
            pass


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
        self._root_identity = _identify(self.project_root)
        self._argentos_existed_before = self.argentos_root.exists()
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
        if _identify(self.project_root) != self._root_identity:
            raise LifecycleStop(
                "PROJECT_ROOT changed between validation and write (STOP)"
            )

    def _assert_within(self, target: Path) -> None:
        contract.ensure_within_project(self.project_root, target)

    def _write_file(self, rel: str, data: bytes) -> str:
        self._assert_root_unchanged()
        target = contract.resolve_manifest_path(self.project_root, rel)
        self._assert_within(target)
        contract.atomic_write(target, data)
        return contract.sha256_bytes(data)

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
        path = contract.journal_path(self.project_root)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"status": "corrupt", "phase": "unknown"}

    def _journal_write(self, journal: dict) -> None:
        journal["updated_at"] = contract.utc_now()
        data = json.dumps(journal, indent=2, ensure_ascii=False) + "\n"
        contract.atomic_write(contract.journal_path(self.project_root), data.encode("utf-8"))

    def _new_journal(self, operation: str, version: str) -> dict:
        return {
            "journal_schema_version": contract.JOURNAL_SCHEMA_VERSION,
            "operation_id": uuid.uuid4().hex,
            "operation": operation,
            "phase": "journal",
            "status": "open",
            "project_root_realpath": os.path.realpath(str(self.project_root)),
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
        self._assert_root_unchanged()
        source = contract.resolve_manifest_path(self.project_root, rel)
        stamp = journal["operation_id"]
        backup_rel = f"{contract.BACKUP_DIR_REL}/{stamp}/{rel}"
        dest = contract.resolve_manifest_path(self.project_root, backup_rel)
        if dest.exists():
            raise LifecycleStop(f"backup entry already exists: {backup_rel}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(source.read_bytes())
        journal["backups"].append(
            {
                "path": backup_rel,
                "replaced": rel,
                "origin": "preexisting",
                "sha256": contract.sha256_file(source),
                "created_at": contract.utc_now(),
            }
        )
        return backup_rel

    # -- install ----------------------------------------------------------

    def install(self) -> Result:
        """Public entry point; staging is always cleaned up."""
        try:
            return self._install_run()
        except SimulatedCrash as exc:
            return self._result(
                "install",
                RECOVERY_PENDING,
                "installation interrupted before committing",
                phase=str(exc),
            )
        finally:
            self._cleanup_staging()

    def _install_run(self) -> Result:
        try:
            payload_root, method, source = self._stage()
            self._assert_root_unchanged()
        except (LifecycleStop, staging.StagingError) as exc:
            self._cleanup_staging()
            return self._result("install", CONFLICT, str(exc))
        self._seam("preflight")

        try:
            manifest = contract.load_manifest(self.project_root)
        except contract.ManifestError as exc:
            self._cleanup_staging()
            return self._result(
                "install", CONFLICT, f"manifest invalid (fail-closed): {exc}"
            )

        if manifest is None and self.argentos_root.exists():
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

        lock = _Lock(contract.lock_path(self.project_root))
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
        if not (self.roots.payload_root / "INDEX.md").is_file():
            return False
        return not self._divergences(manifest)

    def _reinstall(self, version: str) -> Result:
        """Reinstall over a manifest flagged ``managed=false`` (post-uninstall)."""
        try:
            payload_root, method, source = self._stage()
        except (LifecycleStop, staging.StagingError) as exc:
            self._cleanup_staging()
            return self._result("install", CONFLICT, str(exc))
        lock = _Lock(contract.lock_path(self.project_root))
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
        out: list[dict] = []
        for entry in manifest.get("files", []):
            state = contract.classify_entry(entry, self.project_root)
            if state != contract.OWNERSHIP_MANAGED_UNCHANGED:
                out.append({"path": entry["path"], "state": state})
        for entry in manifest.get("generated", []):
            state = contract.classify_entry(entry, self.project_root)
            if state != contract.OWNERSHIP_MANAGED_UNCHANGED:
                out.append({"path": entry["path"], "state": state})
        return out

    def _install_fresh(
        self, payload_root: Path, method: str, source: dict, version: str
    ) -> Result:
        adapter_path = self.project_root / contract.ADAPTER_REL
        adapter_present = adapter_path.exists()
        adapter_hash = (
            contract.sha256_file(adapter_path) if adapter_present else None
        )
        self._adapter_inspection = {
            "present": adapter_present,
            "sha256": adapter_hash,
        }
        historical_agents = (self.project_root / ".agents").exists()
        gitignore_present = (self.project_root / ".gitignore").exists()
        config_present = contract.active_config_path(self.project_root).exists()
        self._seam("inventory")

        journal = self._new_journal("install", version)
        self._journal_write(journal)
        self._seam("journal")

        try:
            # --- backup phase: replace the adapter only with explicit opt-in.
            adapter_origin = "installed"
            if adapter_present and self.replace_agents_md:
                if contract.sha256_file(adapter_path) != adapter_hash:
                    raise LifecycleStop(
                        "AGENTS.md changed between inspection and operation (STOP)"
                    )
                self._backup_file(contract.ADAPTER_REL, journal)
                adapter_origin = "substituted-authorized"
            self._seam("backup")

            # --- apply phase: payload files, config seed, adapter.
            contract.backup_root(self.project_root).mkdir(parents=True, exist_ok=True)
            written: dict[str, str] = {}
            for src in self._payload_files(payload_root):
                rel = f"{contract.PAYLOAD_ROOT_REL}/{src.relative_to(payload_root).as_posix()}"
                digest = self._write_file(rel, src.read_bytes())
                written[rel] = digest
                journal["created"].append({"path": rel, "sha256": digest})
                self._journal_write(journal)
                self._seam("apply")

            if not config_present:
                template = payload_root / FEATURES_FILENAME
                if template.is_file():
                    digest = self._write_file(
                        contract.ACTIVE_CONFIG_REL, template.read_bytes()
                    )
                    journal["created"].append(
                        {"path": contract.ACTIVE_CONFIG_REL, "sha256": digest}
                    )
                    self._journal_write(journal)

            adapter_generated = False
            if not adapter_present:
                self._write_file(
                    contract.ADAPTER_REL, self._adapter_content(version)
                )
                journal["created"].append(
                    {
                        "path": contract.ADAPTER_REL,
                        "sha256": contract.sha256_file(adapter_path),
                    }
                )
                self._journal_write(journal)
                adapter_generated = True
            elif self.replace_agents_md:
                self._write_file(contract.ADAPTER_REL, self._adapter_content(version))
                journal["created"].append(
                    {
                        "path": contract.ADAPTER_REL,
                        "sha256": contract.sha256_file(adapter_path),
                    }
                )
                self._journal_write(journal)
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
            contract.save_manifest_atomic(self.project_root, manifest)
            journal["status"] = "committed"
            journal["phase"] = "commit"
            self._journal_write(journal)
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
        problems: list[str] = []
        for rel, digest in written.items():
            target = contract.resolve_manifest_path(self.project_root, rel)
            if not target.exists():
                problems.append(f"missing after write: {rel}")
            elif contract.sha256_file(target) != digest:
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
        files = []
        for src in self._payload_files(payload_root):
            rel = f"{contract.PAYLOAD_ROOT_REL}/{src.relative_to(payload_root).as_posix()}"
            files.append(contract.file_entry(rel, "installed", self.project_root))
        config = contract.active_config_path(self.project_root)
        if config.exists():
            files.append(
                contract.file_entry(
                    contract.ACTIVE_CONFIG_REL,
                    "preexisting" if config_present else "installed",
                    self.project_root,
                )
            )
        generated = []
        if adapter_generated:
            generated.append(
                {
                    "path": contract.ADAPTER_REL,
                    "kind": "adapter",
                    "origin": adapter_origin,
                    "sha256": contract.sha256_file(
                        self.project_root / contract.ADAPTER_REL
                    ),
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
        import shutil

        operation_id = result.details.get("operation_id")
        batch = contract.backup_root(self.project_root) / str(operation_id)
        if batch.is_dir():
            shutil.rmtree(batch, ignore_errors=True)
        for owned in (
            contract.journal_path(self.project_root),
            contract.lock_path(self.project_root),
        ):
            try:
                owned.unlink()
            except FileNotFoundError:
                pass
        for base in (
            self.roots.payload_root,
            contract.backup_root(self.project_root),
            self.roots.project_dir,
            self.argentos_root,
        ):
            _prune_empty_tree(base)

    def _undo_create(self, entry: dict) -> dict | None:
        target = contract.resolve_manifest_path(self.project_root, entry["path"])
        if not target.exists():
            return None
        current = contract.sha256_file(target)
        if current != entry.get("sha256"):
            return {"path": entry["path"], "reason": "modified after write"}
        target.unlink()
        return None

    def _undo_replace(self, entry: dict) -> dict | None:
        target = contract.resolve_manifest_path(self.project_root, entry["path"])
        if not target.exists():
            return {"path": entry["path"], "reason": "removed after write"}
        if contract.sha256_file(target) != entry.get("sha256"):
            return {"path": entry["path"], "reason": "modified after write"}
        backup = contract.resolve_manifest_path(self.project_root, entry["backup"])
        target.write_bytes(backup.read_bytes())
        return None

    def _undo_remove(self, entry: dict) -> dict | None:
        target = contract.resolve_manifest_path(self.project_root, entry["path"])
        if target.exists():
            return {"path": entry["path"], "reason": "recreated after removal"}
        backup = contract.resolve_manifest_path(self.project_root, entry["backup"])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(backup.read_bytes())
        return None

    def _prune_empty_dirs(self) -> None:
        for base in (
            self.roots.payload_root,
            self.roots.project_dir,
            self.argentos_root,
        ):
            _prune_empty_tree(base)

    def recover(self) -> Result:
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
        lock = _Lock(contract.lock_path(self.project_root))
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
        try:
            return self._update_run()
        except SimulatedCrash as exc:
            return self._result(
                "update",
                RECOVERY_PENDING,
                "update interrupted before committing",
                phase=str(exc),
            )
        finally:
            self._cleanup_staging()

    def _update_run(self) -> Result:
        try:
            manifest = contract.load_manifest(self.project_root)
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

        lock = _Lock(contract.lock_path(self.project_root))
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
        self._journal_write(journal)
        self._seam("journal")

        changed = False
        try:
            for rel, src, data in target_files:
                current = known.get(rel)
                target = contract.resolve_manifest_path(self.project_root, rel)
                if current is not None and target.exists():
                    if contract.sha256_file(target) == contract.sha256_bytes(data):
                        continue  # already identical: idempotent, no rewrite
                    backup = self._backup_file(rel, journal)
                    digest = self._write_file(rel, data)
                    journal["replaced"].append(
                        {"path": rel, "backup": backup, "sha256": digest}
                    )
                    changed = True
                else:
                    digest = self._write_file(rel, data)
                    journal["created"].append({"path": rel, "sha256": digest})
                    changed = True
                self._journal_write(journal)
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
                {rel: contract.sha256_file(
                    contract.resolve_manifest_path(self.project_root, rel))
                 for rel, _, _ in target_files}
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
                files.append(contract.file_entry(rel, origin, self.project_root))
            # Artifacts removed from the payload stay owned and reported, never
            # silently dropped from the manifest.
            files.extend(known[rel] for rel in removed_from_payload)
            config = contract.active_config_path(self.project_root)
            if config.exists():
                files.append(
                    contract.file_entry(
                        contract.ACTIVE_CONFIG_REL,
                        known.get(contract.ACTIVE_CONFIG_REL, {}).get(
                            "origin", "installed"
                        ),
                        self.project_root,
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
            contract.save_manifest_atomic(self.project_root, manifest)
            journal["status"] = "committed"
            journal["phase"] = "commit"
            self._journal_write(journal)
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
        try:
            return self._uninstall_run()
        except SimulatedCrash as exc:
            return self._result(
                "uninstall",
                RECOVERY_PENDING,
                "uninstall interrupted before committing",
                phase=str(exc),
            )

    def _uninstall_run(self) -> Result:
        try:
            manifest = contract.load_manifest(self.project_root)
        except contract.ManifestError as exc:
            return self._result("uninstall", CONFLICT, f"manifest invalid: {exc}")
        if manifest is None:
            return self._result(
                "uninstall",
                CONFLICT,
                "no installation manifest found (fail-closed)",
            )
        lock = _Lock(contract.lock_path(self.project_root))
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
        eligible: list[str] = []
        preserved: list[dict] = []
        for entry in manifest.get("files", []):
            state = contract.classify_entry(entry, self.project_root)
            if entry.get("origin") == "installed" and state == contract.OWNERSHIP_MANAGED_UNCHANGED:
                if entry["path"] == contract.ACTIVE_CONFIG_REL:
                    preserved.append({"path": entry["path"], "reason": "active config"})
                    continue
                eligible.append(entry["path"])
            else:
                preserved.append({"path": entry["path"], "state": state})
        adapter_remove: str | None = None
        for entry in manifest.get("generated", []):
            state = contract.classify_entry(entry, self.project_root)
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
        self._journal_write(journal)
        self._seam("journal")
        try:
            for rel in eligible + ([adapter_remove] if adapter_remove else []):
                backup = self._backup_file(rel, journal)
                target = contract.resolve_manifest_path(self.project_root, rel)
                self._assert_root_unchanged()
                target.unlink()
                journal["removed"].append({"path": rel, "backup": backup})
                self._journal_write(journal)
                self._seam("apply")
            self._seam("apply")

            if self.restore or self.force_restore:
                self._restore_backups(manifest, journal)
            self._seam("post_validate")

            self._seam("commit")
            if self.purge:
                manifest_file = contract.manifest_path(self.project_root)
                if manifest_file.exists():
                    self._assert_root_unchanged()
                    manifest_file.unlink()
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
                contract.save_manifest_atomic(self.project_root, manifest)
            journal["status"] = "committed"
            journal["phase"] = "commit"
            self._journal_write(journal)
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
        for entry in manifest.get("backups", []):
            dest = contract.resolve_manifest_path(self.project_root, entry["replaced"])
            if dest.exists():
                continue  # never overwrite a later adopter file
            backup = contract.resolve_manifest_path(self.project_root, entry["path"])
            if not backup.exists():
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(backup.read_bytes())

    def _unknown_artifacts(self, manifest: dict) -> list[str]:
        """Project-relative files under ``.argentos/`` the manifest does not own.

        These are the adopter's — reported, never touched (I5, D3).
        """
        known: set[str] = set()
        for kind in ("files", "generated", "backups"):
            for entry in manifest.get(kind, []):
                known.add(entry.get("path"))
        known.add(contract.MANIFEST_REL)
        known.add(contract.JOURNAL_REL)
        known.add(contract.LOCK_REL)
        root = self.argentos_root
        out: list[str] = []
        if not root.is_dir():
            return out
        for path in sorted(root.rglob("*"), key=lambda p: p.as_posix()):
            if not path.is_file():
                continue
            rel = path.relative_to(self.project_root).as_posix()
            if rel in known:
                continue
            if rel.startswith(contract.BACKUP_DIR_REL + "/"):
                continue
            out.append(rel)
        return out

    # -- doctor -----------------------------------------------------------

    def doctor(self) -> Result:
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
            manifest = contract.load_manifest(self.project_root)
        except contract.ManifestError as exc:
            return self._doctor_result("invalid-manifest", evidence=str(exc))

        if manifest is None:
            if self.argentos_root.exists():
                if (self.roots.payload_root).exists():
                    return self._doctor_result("needs-manual-intervention")
                return self._doctor_result("unrecognized")
            return self._doctor_result("installation-absent")

        if manifest.get("install", {}).get("managed") is False:
            return self._doctor_result("installation-absent")

        divergences = self._divergences(manifest)
        installed_version = None
        version_file = self.roots.payload_root / "VERSION"
        if version_file.is_file():
            installed_version = version_file.read_text(encoding="utf-8").strip()
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
        bootstrap = self.roots.payload_root / "INDEX.md"
        if not bootstrap.is_file():
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
