"""Root binding for the adoption lifecycle (RFC-81, GATE 3 #32).

The lifecycle must never mutate a filesystem object other than the
``PROJECT_ROOT`` it validated. A pathname is not a binding: between a check and
a path-based mutation the directory can be replaced. This module provides the
binding primitive used by ``lifecycle.py``:

* ``PosixRootBinding`` keeps an ``O_DIRECTORY`` descriptor and performs every
  mutation relative to it with ``dir_fd``. The descriptor pins the validated
  directory object; a replacement of the pathname cannot redirect the
  operation. Managed paths are traversed component by component with
  ``O_NOFOLLOW``; a symlink is refused (stricter than escape rejection, and
  safe for the binding).
* ``WindowsRootBinding`` opens a directory handle **without**
  ``FILE_SHARE_DELETE``. While it is open Windows refuses to rename or delete
  the directory, including through an ancestor directory, so the pathname is
  stable for the life of the operation. Mutations can therefore stay
  path-based without being redirectable. The handle is also the identity pin.
  This guarantee is verified for local volumes whose sharing modes are honored
  by the filesystem; remote/UNC volumes are not assumed and should be treated
  as unsupported until verified (the lifecycle still fails closed if the
  handle cannot be opened).
* If a strong binding cannot be established, ``open_root_binding`` raises
  ``RootBindingUnavailable`` and the lifecycle fails closed; it never falls
  back to the weak ``realpath + st_dev + st_ino`` identity for mutations.

The module is standard-library only and ships inside the payload.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat as stat_module
import uuid
from contextlib import contextmanager
from pathlib import Path, PurePosixPath
from typing import Any, Iterator

import lifecycle_contract as contract


class RootBindingError(RuntimeError):
    """A managed path cannot be operated on safely through the binding."""


class RootBindingUnavailable(RootBindingError):
    """No strong root binding could be established; mutating calls must stop."""


def _parts(rel: str) -> tuple[str, ...]:
    """Validate a project-relative POSIX path and return its components."""
    if not contract.is_safe_relpath(rel):
        raise RootBindingError(f"unsafe managed path: {rel!r}")
    return PurePosixPath(rel).parts


def _read_all(fd: int) -> bytes:
    chunks: list[bytes] = []
    while True:
        chunk = os.read(fd, 1024 * 1024)
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)


def _write_all(fd: int, data: bytes) -> None:
    view = memoryview(data)
    while view:
        written = os.write(fd, view)
        if written <= 0:
            raise OSError("short write")
        view = view[written:]


class RootBinding:
    """Common relative-path API over the bound root object."""

    root: Path
    strong = True

    def __init__(self, root: Path, token: Any):
        self.root = Path(root)
        self._token = token
        self._root_realpath = os.path.realpath(str(self.root))
        self._closed = False

    # -- abstract primitive: relative I/O --------------------------------

    def read_bytes(self, rel: str) -> bytes:  # pragma: no cover - abstract
        raise NotImplementedError

    def write_bytes(self, rel: str, data: bytes) -> None:  # pragma: no cover
        raise NotImplementedError

    def exists(self, rel: str) -> bool:  # pragma: no cover - abstract
        raise NotImplementedError

    def is_file(self, rel: str) -> bool:  # pragma: no cover - abstract
        raise NotImplementedError

    def is_dir(self, rel: str) -> bool:  # pragma: no cover - abstract
        raise NotImplementedError

    def listdir(self, rel: str) -> list[str]:  # pragma: no cover - abstract
        raise NotImplementedError

    def mkdirs(self, rel: str) -> None:  # pragma: no cover - abstract
        raise NotImplementedError

    def unlink(self, rel: str) -> None:  # pragma: no cover - abstract
        raise NotImplementedError

    def rmdir(self, rel: str) -> None:  # pragma: no cover - abstract
        raise NotImplementedError

    def rename(self, src: str, dst: str, *, replace: bool = False) -> None:
        raise NotImplementedError

    def lock_create(self) -> Any:  # pragma: no cover - abstract
        raise NotImplementedError

    def lock_release(self, token: Any) -> None:  # pragma: no cover - abstract
        raise NotImplementedError

    def close(self) -> None:  # pragma: no cover - abstract
        raise NotImplementedError

    def unchanged(self) -> bool:  # pragma: no cover - abstract
        """Whether ``root`` still resolves to the object held by the binding."""
        raise NotImplementedError

    def __del__(self) -> None:  # pragma: no cover - finalization safety net
        try:
            self.close()
        except Exception:  # noqa: BLE001 - never fail during finalization
            pass

    @property
    def root_realpath(self) -> str:
        return self._root_realpath

    # -- derived operations ----------------------------------------------

    def sha256(self, rel: str) -> str:
        return hashlib.sha256(self.read_bytes(rel)).hexdigest()

    def write_atomic(self, rel: str, data: bytes) -> None:
        """Atomically replace ``rel`` inside the bound root."""
        parent = str(PurePosixPath(rel).parent)
        if parent not in ("", "."):
            self.mkdirs(parent)
        name = PurePosixPath(rel).name
        self._atomic(rel, data, name)

    def _atomic(self, rel: str, data: bytes, name: str) -> None:
        # Implemented by concrete bindings.
        raise NotImplementedError

    def copy(self, src: str, dst: str) -> None:
        self.write_atomic(dst, self.read_bytes(src))

    def remove_tree(self, rel: str) -> None:
        if not self.exists(rel):
            return
        if self.is_dir(rel):
            for name in self.listdir(rel):
                self.remove_tree(f"{rel}/{name}")
            self.rmdir(rel)
        else:
            self.unlink(rel)

    def prune_empty(self, rel: str) -> None:
        if not self.is_dir(rel):
            return
        for name in self.listdir(rel):
            self.prune_empty(f"{rel}/{name}")
        if not self.listdir(rel):
            self.rmdir(rel)

    def walk_files(self, rel: str) -> list[str]:
        if not self.is_dir(rel):
            return []
        out: list[str] = []
        for name in self.listdir(rel):
            child = f"{rel}/{name}"
            if self.is_dir(child):
                out.extend(self.walk_files(child))
            elif self.is_file(child):
                out.append(child)
        return out

    def file_entry(self, rel: str, origin: str) -> dict:
        if not self.exists(rel):
            return {
                "path": rel,
                "origin": origin,
                "state": "missing",
                "sha256": None,
            }
        return {
            "path": rel,
            "origin": origin,
            "state": "present",
            "sha256": self.sha256(rel),
        }

    def classify_entry(self, entry: dict) -> str:
        rel = entry["path"]
        if not self.exists(rel):
            return contract.OWNERSHIP_MISSING
        origin = entry.get("origin")
        if origin == "installed":
            digest = entry.get("sha256")
            if isinstance(digest, str) and self.sha256(rel) == digest:
                return contract.OWNERSHIP_MANAGED_UNCHANGED
            return contract.OWNERSHIP_MANAGED_MODIFIED
        return contract.OWNERSHIP_PREEXISTING

    def load_manifest(self) -> dict | None:
        if not self.exists(contract.MANIFEST_REL):
            return None
        raw = self.read_bytes(contract.MANIFEST_REL)
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise contract.ManifestError(f"manifest is not valid JSON: {exc}") from exc
        problems = contract.validate_manifest(data, self.root)
        if problems:
            raise contract.ManifestError("; ".join(problems))
        return data

    def save_manifest(self, manifest: dict) -> None:
        stamp = contract.backup_stamp()
        if self.exists(contract.MANIFEST_REL):
            snapshot = f"{contract.BACKUP_DIR_REL}/{stamp}/{PurePosixPath(contract.MANIFEST_REL).name}"
            self.write_atomic(snapshot, self.read_bytes(contract.MANIFEST_REL))
        payload = json.dumps(manifest, indent=2, sort_keys=False, ensure_ascii=False) + "\n"
        self.write_atomic(contract.MANIFEST_REL, payload.encode("utf-8"))


class PosixRootBinding(RootBinding):
    """Directory-descriptor binding; every managed operation is relative."""

    def __init__(self, root: Path):
        if not hasattr(os, "O_DIRECTORY") or not hasattr(os, "O_NOFOLLOW"):
            raise RootBindingUnavailable(
                "POSIX root binding requires O_DIRECTORY and O_NOFOLLOW"
            )
        fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
        super().__init__(root, fd)
        self.fd = fd

    def _open_dir(self, current: int, name: str, opened: list[int]) -> int:
        try:
            fd = os.open(
                name,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=current,
            )
        except FileNotFoundError:
            raise
        except OSError as exc:
            raise RootBindingError(
                f"managed path component is not a safe directory: {name!r} ({exc})"
            ) from exc
        opened.append(fd)
        return fd

    @contextmanager
    def _parent(self, rel: str) -> Iterator[tuple[int, str]]:
        parts = _parts(rel)
        current = self.fd
        opened: list[int] = []
        try:
            for component in parts[:-1]:
                current = self._open_dir(current, component, opened)
            yield current, parts[-1]
        finally:
            for fd in reversed(opened):
                try:
                    os.close(fd)
                except OSError:
                    pass

    def _lstat(self, rel: str) -> os.stat_result | None:
        try:
            with self._parent(rel) as (parent, name):
                try:
                    st = os.stat(name, dir_fd=parent, follow_symlinks=False)
                except FileNotFoundError:
                    return None
        except FileNotFoundError:
            return None
        if stat_module.S_ISLNK(st.st_mode):
            raise RootBindingError(f"symlink in managed path: {rel!r}")
        return st

    def read_bytes(self, rel: str) -> bytes:
        with self._parent(rel) as (parent, name):
            fd = os.open(
                name,
                os.O_RDONLY | os.O_NOFOLLOW,
                dir_fd=parent,
            )
            try:
                return _read_all(fd)
            finally:
                os.close(fd)

    def write_bytes(self, rel: str, data: bytes) -> None:
        self.write_atomic(rel, data)

    def _atomic(self, rel: str, data: bytes, name: str) -> None:
        with self._parent(rel) as (parent, name):
            tmp = f".{name}.tmp-{os.getpid()}-{uuid.uuid4().hex}"
            fd = os.open(
                tmp,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600,
                dir_fd=parent,
            )
            try:
                _write_all(fd, data)
                os.fsync(fd)
            except Exception:
                os.close(fd)
                try:
                    os.unlink(tmp, dir_fd=parent)
                except OSError:
                    pass
                raise
            os.close(fd)
            try:
                os.replace(tmp, name, src_dir_fd=parent, dst_dir_fd=parent)
            except Exception:
                try:
                    os.unlink(tmp, dir_fd=parent)
                except OSError:
                    pass
                raise
            try:
                os.fsync(parent)
            except OSError:
                pass

    def exists(self, rel: str) -> bool:
        return self._lstat(rel) is not None

    def is_file(self, rel: str) -> bool:
        st = self._lstat(rel)
        return st is not None and stat_module.S_ISREG(st.st_mode)

    def is_dir(self, rel: str) -> bool:
        st = self._lstat(rel)
        return st is not None and stat_module.S_ISDIR(st.st_mode)

    def listdir(self, rel: str) -> list[str]:
        with self._parent(rel) as (parent, name):
            try:
                fd = os.open(
                    name,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=parent,
                )
            except OSError as exc:
                raise RootBindingError(f"not a directory: {rel!r}") from exc
            try:
                return sorted(os.listdir(fd))
            finally:
                os.close(fd)

    def mkdirs(self, rel: str) -> None:
        parts = _parts(rel)
        current = self.fd
        opened: list[int] = []
        try:
            for component in parts:
                try:
                    st = os.stat(component, dir_fd=current, follow_symlinks=False)
                except FileNotFoundError:
                    try:
                        os.mkdir(component, dir_fd=current)
                    except FileExistsError:
                        pass
                    st = os.stat(component, dir_fd=current, follow_symlinks=False)
                if stat_module.S_ISLNK(st.st_mode) or not stat_module.S_ISDIR(st.st_mode):
                    raise RootBindingError(
                        f"managed path component is not a directory: {component!r}"
                    )
                current = self._open_dir(current, component, opened)
        finally:
            for fd in reversed(opened):
                try:
                    os.close(fd)
                except OSError:
                    pass

    def unlink(self, rel: str) -> None:
        with self._parent(rel) as (parent, name):
            try:
                os.unlink(name, dir_fd=parent)
            except FileNotFoundError as exc:
                raise RootBindingError(f"missing managed file: {rel!r}") from exc

    def rmdir(self, rel: str) -> None:
        with self._parent(rel) as (parent, name):
            os.rmdir(name, dir_fd=parent)

    def rename(self, src: str, dst: str, *, replace: bool = False) -> None:
        with self._parent(src) as (src_parent, src_name):
            with self._parent(dst) as (dst_parent, dst_name):
                if replace:
                    os.replace(src_name, dst_name, src_dir_fd=src_parent, dst_dir_fd=dst_parent)
                else:
                    os.rename(src_name, dst_name, src_dir_fd=src_parent, dst_dir_fd=dst_parent)

    def lock_create(self) -> int:
        self.mkdirs(contract.PROJECT_STATE_DIR_REL)
        with self._parent(contract.LOCK_REL) as (parent, name):
            try:
                fd = os.open(
                    name,
                    os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                    dir_fd=parent,
                )
            except FileExistsError as exc:
                raise RootBindingError(
                    "another lifecycle operation holds the lock on this root"
                ) from exc
            _write_all(fd, f"{os.getpid()} {contract.utc_now()}\n".encode("utf-8"))
            return fd

    def lock_release(self, token: int) -> None:
        try:
            os.close(token)
        except OSError:
            pass
        try:
            self.unlink(contract.LOCK_REL)
        except (RootBindingError, FileNotFoundError):
            pass

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            os.close(self.fd)
        except OSError:
            pass

    def unchanged(self) -> bool:
        try:
            path_stat = os.stat(self.root)
            fd_stat = os.fstat(self.fd)
        except OSError:
            return False
        return (path_stat.st_dev, path_stat.st_ino) == (
            fd_stat.st_dev,
            fd_stat.st_ino,
        )


def _windows_drive_type(root: Path) -> int | None:
    """Return the Win32 drive type for ``root`` (``None`` if unavailable)."""
    try:
        import ctypes

        drive, _tail = os.path.splitdrive(str(root))
        if not drive:
            return None
        volume = drive if drive.endswith("\\") else drive + "\\"
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.GetDriveTypeW.argtypes = [ctypes.c_wchar_p]
        kernel32.GetDriveTypeW.restype = ctypes.c_uint
        return int(kernel32.GetDriveTypeW(volume))
    except Exception:  # noqa: BLE001 - any failure means "not verified"
        return None


class WindowsRootBinding(RootBinding):
    """Path-stable binding via a directory handle without delete sharing."""

    def __init__(self, root: Path):
        from lifecycle import _win_open_directory  # local, no cycle at import

        drive_type = _windows_drive_type(root)
        if drive_type not in (2, 3, 6):
            # DRIVE_REMOVABLE/FIXED/RAM. Remote/unknown volumes do not have a
            # verified sharing-mode guarantee; refuse rather than claim one.
            raise RootBindingUnavailable(
                "Windows root binding is verified only for local volumes "
                f"(drive type {drive_type!r})"
            )
        handle = _win_open_directory(root)
        if handle is None:
            raise RootBindingUnavailable(
                "cannot open a directory handle without FILE_SHARE_DELETE"
            )
        super().__init__(root, handle)
        self.handle = handle

    def _path(self, rel: str) -> Path:
        try:
            return contract.resolve_manifest_path(self.root, rel)
        except contract.ManifestError as exc:
            raise RootBindingError(str(exc)) from exc

    def read_bytes(self, rel: str) -> bytes:
        return self._path(rel).read_bytes()

    def write_bytes(self, rel: str, data: bytes) -> None:
        self.write_atomic(rel, data)

    def _atomic(self, rel: str, data: bytes, name: str) -> None:
        target = self._path(rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_name(target.name + f".tmp-{uuid.uuid4().hex}")
        with open(tmp, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, target)

    def exists(self, rel: str) -> bool:
        return self._path(rel).exists()

    def is_file(self, rel: str) -> bool:
        return self._path(rel).is_file()

    def is_dir(self, rel: str) -> bool:
        return self._path(rel).is_dir()

    def listdir(self, rel: str) -> list[str]:
        return sorted(p.name for p in self._path(rel).iterdir())

    def mkdirs(self, rel: str) -> None:
        self._path(rel).mkdir(parents=True, exist_ok=True)

    def unlink(self, rel: str) -> None:
        self._path(rel).unlink()

    def rmdir(self, rel: str) -> None:
        self._path(rel).rmdir()

    def rename(self, src: str, dst: str, *, replace: bool = False) -> None:
        source = self._path(src)
        target = self._path(dst)
        if replace:
            os.replace(source, target)
        else:
            os.rename(source, target)

    def lock_create(self) -> int:
        self.mkdirs(contract.PROJECT_STATE_DIR_REL)
        path = self._path(contract.LOCK_REL)
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as exc:
            raise RootBindingError(
                "another lifecycle operation holds the lock on this root"
            ) from exc
        os.write(fd, f"{os.getpid()} {contract.utc_now()}\n".encode("utf-8"))
        return fd

    def lock_release(self, token: int) -> None:
        try:
            os.close(token)
        except OSError:
            pass
        try:
            self._path(contract.LOCK_REL).unlink()
        except FileNotFoundError:
            pass

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        from lifecycle import _win_close

        _win_close(self.handle)

    def unchanged(self) -> bool:
        from lifecycle import _win_close, _win_directory_id, _win_open_directory

        fresh = _win_open_directory(self.root)
        if fresh is None:
            return False
        try:
            return _win_directory_id(fresh) == _win_directory_id(self.handle)
        finally:
            _win_close(fresh)


def open_root_binding(root: Path) -> RootBinding:
    """Open a strong binding for ``root`` or fail closed."""
    try:
        if os.name == "posix":
            return PosixRootBinding(Path(root))
        if os.name == "nt":
            return WindowsRootBinding(Path(root))
    except RootBindingError:
        raise
    except OSError as exc:
        raise RootBindingUnavailable(str(exc)) from exc
    raise RootBindingUnavailable(
        f"no strong root binding for platform {os.name!r}"
    )
