import os
import gc
import platform

def auto_clean_ram():
    # Python garbage collection
    gc.collect()

    system = platform.system()

    if system == "Linux":
        os.system("sync; echo 3 > /proc/sys/vm/drop_caches")

    return {
        "status": "safe_clean_done",
        "note": "Garbage collected, cache cleaned safely"
    }
