import os
import time
import hashlib

def cpu_worker():
    # Infinite CPU load loop
    while True:
        data = os.urandom(1024 * 1024)
        hashlib.sha256(data).hexdigest()

def mem_worker():
    # Aggressive memory allocation
    memory_hog = []
    try:
        while True:
            memory_hog.append(bytearray(100 * 1024 * 1024))
            time.sleep(0.1)
    except MemoryError:
        pass

def io_worker():
    # Direct I/O write bypassing OS cache
    temp_file = f"io_stress_{os.getpid()}.tmp"
    data = os.urandom(1024 * 1024 * 10)
    try:
        with open(temp_file, "wb") as f:
            while True:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)