"""If-Then rule engine with weighted priority scoring."""
import pandas as pd
def tariff(h):  # Rs per kWh (time-of-day tariff)
    return 9.0 if 18 <= h < 22 else 4.0 if (h >= 23 or h < 5) else 6.0
# Priority weights (key design decision): savings matter most, then low comfort impact, then confidence
W = {"savings": 0.5, "comfort": 0.3, "confidence": 0.2}
RULES = {  # id: (if-condition text, then-action, comfort_ease 0-1, confidence 0-1)
    "R1": ("AC ON and bedroom empty for 2+ hours", "Turn AC off", 0.9, 0.95),
    "R2": ("Lights ON and room empty for 1+ hour", "Turn lights off", 1.0, 0.9),
    "R3": ("TV ON and room empty for 1+ hour", "Turn TV off", 1.0, 0.9),
    "R4": ("Washing machine runs in peak hours (6-10 PM)", "Shift to off-peak (after 11 PM)", 0.7, 0.85),
    "R5": ("Geyser ON in peak hours (6-10 PM)", "Heat in morning / use timer", 0.6, 0.8),
    "R6": ("AC ON 7+ continuous hours", "Set sleep timer / 24C", 0.5, 0.7)}
def load(path="datasets/usage.csv"):
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df["hour"] = df.timestamp.dt.hour
    df["cost"] = df.kwh * df.hour.map(tariff)
    return df
def _runs(mask):  # lengths of consecutive True runs -> list of (start_idx, length)
    out, start = [], None
    for i, m in enumerate(list(mask) + [False]):
        if m and start is None: start = i
        if not m and start is not None: out.append((start, i - start)); start = None
    return out
def evaluate(df):
    alerts = []
    for dev, g in df.groupby("device"):
        g = g.sort_values("timestamp").reset_index(drop=True)
        on, empty = g.is_on == 1, g.room_occupied == 0
        def add(rid, rows):
            kwh, rs = rows.kwh.sum(), RULES[rid]
            alerts.append(dict(rule=rid, device=dev, time=rows.timestamp.iloc[0], hours=len(rows), kwh_wasted=round(kwh, 2),
                               saving_inr=round(rows.cost.sum() * (0.3 if rid in ("R4", "R5") else 1) if rid != "R6" else rows.cost.sum() * .15, 2),
                               condition=rs[0], action=rs[1], _ce=rs[2], _cf=rs[3]))
        if dev == "AC":
            for s, n in _runs(on & empty):
                if n >= 2: add("R1", g.iloc[s:s + n])
            for s, n in _runs(on & ~empty):  # exclude hours already flagged by R1 (no double counting)
                if n >= 7: add("R6", g.iloc[s:s + n])
        if dev == "Lights":
            for s, n in _runs(on & empty):
                if n >= 1: add("R2", g.iloc[s:s + n])
        if dev == "TV":
            for s, n in _runs(on & empty):
                if n >= 1: add("R3", g.iloc[s:s + n])
        if dev == "Washing Machine":
            for s, n in _runs(on & g.hour.between(18, 21)): add("R4", g.iloc[s:s + n])
        if dev == "Geyser":
            for s, n in _runs(on & g.hour.between(18, 21)): add("R5", g.iloc[s:s + n])
    a = pd.DataFrame(alerts)
    if a.empty: return a
    sav = a.saving_inr / a.saving_inr.max()
    a["priority"] = (100 * (W["savings"] * sav + W["comfort"] * a._ce + W["confidence"] * a._cf)).round(1)
    a["level"] = pd.cut(a.priority, [0, 55, 75, 101], labels=["Low", "Medium", "High"])
    return a.drop(columns=["_ce", "_cf"]).sort_values("priority", ascending=False).reset_index(drop=True)
if __name__ == "__main__":
    df = load(); a = evaluate(df)
    a.to_csv("outputs/alerts.csv", index=False)
    print("total bill Rs", round(df.cost.sum(), 2), "| alerts", len(a), "| potential saving Rs", round(a.saving_inr.sum(), 2))
    print(a.groupby("rule").agg(n=("rule", "size"), inr=("saving_inr", "sum")).round(1))
