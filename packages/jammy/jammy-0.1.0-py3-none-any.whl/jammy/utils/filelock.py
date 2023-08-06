import stackprinter
from filelock import FileLock, SoftFileLock

# pylint: disable=broad-except

__all__ = [
    "try_filelock",
]


def try_filelock(
    fn,
    target_file,
    is_soft=False,
    timeout=20,
):
    lock_obj = SoftFileLock if is_soft else FileLock
    try:
        with lock_obj(f"{target_file}._lock", timeout) as flock:
            if flock.is_locked:
                fn()
            else:
                print(f"try_filelock Timeout!!! {target_file}")
    except Exception as exc:
        stackprinter.show(exc, style="darkbg2")
