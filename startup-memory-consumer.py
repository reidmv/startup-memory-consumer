import os
import sys
import time
import ctypes
import gc

from threading import Event


def consume_mem(size: int, seconds: int | None = None):
    print(f"Consuming {size} bytes for {seconds} seconds...")
    buffer = ctypes.create_string_buffer(size)
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
      "start_mib": os.getenv("STARTUP_CONSUME_MEBIBYTES", default="512"),
      "start_sec": os.getenv("STARTUP_CONSUME_SECONDS",   default="1"),
      "other_mib": os.getenv("RUNTIME_CONSUME_MEBIBYTES", default="4"),
      "other_sec": os.getenv("RUNTIME_CONSUME_SECONDS",   default=None),
    }

    for key, val in config.items():
        try:
            config[key] = int(val)
        except:
            config[key] = None

    consume_mem(size=mebibytes_to_bytes(config["start_mib"]), seconds=config["start_sec"])
    consume_mem(size=mebibytes_to_bytes(config["other_mib"]), seconds=config["other_sec"])
    return 0


if __name__ == '__main__':
    sys.exit(main())

