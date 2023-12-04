import os
import sys
import time
import ctypes
import gc

from threading import Event


def consume_mem(size: int, seconds: int | None = None):
    print(f"Consuming {size} bytes for {seconds} seconds...")
    buffer = ctypes.create_string_buffer(int(size))
    if seconds is None:
      Event().wait() # Wait forever
    time.sleep(seconds)
    buffer = None
    gc.collect(generation=0)
    print("Done")


def mebibytes_to_bytes(mebibytes: int) -> int:
    return mebibytes * 1024 * 1024


def main() -> int:
    config = {
      "st_mib": os.getenv("STARTUP_CONSUME_MEBIBYTES", default="512"),
      "st_sec": os.getenv("STARTUP_CONSUME_SECONDS",   default="1"),
      "rt_mib": os.getenv("RUNTIME_CONSUME_MEBIBYTES", default="4"),
      "rt_sec": os.getenv("RUNTIME_CONSUME_SECONDS",   default=None),
    }

    for key, val in config.items():
        try:
            config[key] = float(val)
        except:
            config[key] = None

    consume_mem(size=mebibytes_to_bytes(config["st_mib"]), seconds=config["st_sec"])
    consume_mem(size=mebibytes_to_bytes(config["rt_mib"]), seconds=config["rt_sec"])
    return 0


if __name__ == '__main__':
    sys.exit(main())

