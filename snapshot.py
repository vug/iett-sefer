from datetime import datetime
import os
import pickle
import time
from typing import List

from ibb import get_arac_konum, AracKonum


class Snapshot(object):
    def __init__(
        self, vehicles: List[AracKonum], request_time: float, response_time: float
    ):
        self.vehicles = vehicles
        self.request_time = request_time
        self.response_time = response_time
        self.duration = response_time - request_time
        self.dt = datetime.fromtimestamp(request_time)
        self.ts = self.dt.strftime("%Y-%m-%dT%H-%M-%S")


def fetch_store_snapshot():
    t1 = time.time()
    araclar = get_arac_konum()
    t2 = time.time()

    snapshot = Snapshot(vehicles=araclar, request_time=t1, response_time=t2)
    with open(f"snapshot-{snapshot.ts}.pkl", "wb") as f:
        pickle.dump(snapshot, f)


def load_latest_snapshot():
    snapshot_files = [
        fn for fn in os.listdir() if fn.startswith("snapshot") and fn.endswith(".pkl")
    ]
    if not snapshot_files:
        raise Exception("No snapshot exist.")
    latest_file = snapshot_files[-1]
    with open(latest_file, "rb") as f:
        snapshot = pickle.load(f)
    return snapshot
