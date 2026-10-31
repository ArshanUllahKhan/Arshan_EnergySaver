"""Simulate 7 days of hourly smart-home usage for an Indian 2BHK (seeded, reproducible)."""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
DEV = {  # device: (room, kW when on)
    "AC": ("Bedroom", 1.5), "Geyser": ("Bathroom", 2.0), "Lights": ("Living Room", 0.12),
    "Washing Machine": ("Utility", 0.5), "TV": ("Living Room", 0.15)}
rows = []
for ts in pd.date_range("2026-10-19", periods=7 * 24, freq="h"):
    h = ts.hour
    bed_occ = h >= 23 or h < 7
    liv_occ = 18 <= h <= 23 or 7 <= h <= 9
    for d, (room, kw) in DEV.items():
        occ = {"Bedroom": bed_occ, "Living Room": liv_occ}.get(room, rng.random() < .3)
        if d == "AC": on = (h >= 21 or h < 8) and rng.random() < .9 or (13 <= h <= 16 and rng.random() < .5)
        elif d == "Geyser": on = (h in (6, 7) and rng.random() < .9) or (h in (19, 20) and rng.random() < .5)
        elif d == "Lights": on = (h >= 18 or h < 1 or 6 <= h <= 8) and rng.random() < .85
        elif d == "Washing Machine": on = h in (19, 20) and ts.weekday() in (1, 4, 6)
        else: on = (19 <= h <= 23 or 14 <= h <= 16) and rng.random() < .7
        rows.append((ts, d, room, int(on), int(occ), round(kw * on, 3)))
pd.DataFrame(rows, columns=["timestamp", "device", "room", "is_on", "room_occupied", "kwh"]).to_csv("datasets/usage.csv", index=False)
print("rows:", len(rows))
