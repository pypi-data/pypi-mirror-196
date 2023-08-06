import torch
import stackprinter
from filelock import FileLock, SoftFileLock
from .basic import get_rank, get_world_size, print0

# pylint: disable=broad-except

def try_filelock(
    fn,
    target_file,
    is_soft=False,
    timeout=20,
):
    lock_obj = SoftFileLock if is_soft else FileLock
    try:
        if get_rank() == 0:
            lock = lock_obj(f"{target_file}._lock", timeout)
            lock.acquire()
            flag = lock.is_locked
        else:
            flag = False
        # create a one element tensor and broadcast it from rank 0
        flag = torch.tensor(flag, device="cuda")
        if get_world_size() > 1:
            torch.distributed.broadcast(flag, src=0)
        if flag.item():
            fn()
        else:
            print0(f"try_filelock Timeout!!! {target_file}")
    except Exception as exc:
        stackprinter.show(exc, style="darkbg2")
    finally:
        if get_rank() == 0:
            lock.release()