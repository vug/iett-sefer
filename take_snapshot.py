"""
This script is meant to be run periodically to store latest
bus coordinates in a local file.

According to https://stackoverflow.com/questions/50465106/attributeerror-when-reading-a-pickle-file
the function that creates the pickle shouldn't be in the main module
hence I placed this script outside of snapshot.py module.
"""
import time

from snapshot import fetch_store_snapshot


if __name__ == "__main__":
    while True:
        print(f"Snapshot taken at {time.time()}")
        fetch_store_snapshot()
        time.sleep(120)
