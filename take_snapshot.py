"""
This script is meant to be run periodically to store latest
bus coordinates in a local file.
"""
import time

from snapshot import fetch_store_snapshot


if __name__ == "__main__":
    while True:
        print(f"Snapshot taken at {time.time()}")
        fetch_store_snapshot()
        time.sleep(120)
