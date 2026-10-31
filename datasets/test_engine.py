import sys
sys.path.insert(0, "notebooks")
import pandas as pd, engine as e
def test_no_double_counting():
    a = e.evaluate(e.load())
    seen = set()
    for _, x in a[a.device == "AC"].iterrows():
        for i in range(int(x.hours)):
            t = x.time + pd.Timedelta(hours=i)
            assert t not in seen, f"AC hour {t} counted twice"; seen.add(t)
def test_savings_never_exceed_bill():
    df = e.load(); assert e.evaluate(df).saving_inr.sum() < df.cost.sum()
def test_priority_range():
    a = e.evaluate(e.load()); assert a.priority.between(0, 100).all()
