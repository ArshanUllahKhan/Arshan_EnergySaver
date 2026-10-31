import streamlit as st, pandas as pd
from engine import load, evaluate, RULES, W
from llm_tips import tips
st.set_page_config(page_title="Smart Energy Saver", page_icon="⚡", layout="wide")
df = load(); a = evaluate(df)
st.title("⚡ Smart Home Energy Saving Assistant")
st.caption("If-Then rules + weighted priority + Gen AI tips | simulated 7-day data")
c1, c2, c3, c4 = st.columns(4)
bill, save = df.cost.sum(), a.saving_inr.sum()
c1.metric("Weekly bill", f"₹{bill:,.0f}"); c2.metric("Potential saving", f"₹{save:,.0f}", f"{save/bill:.0%}")
c3.metric("Alerts", len(a)); c4.metric("High priority", int((a.level == "High").sum()))
l, r = st.columns([3, 2])
with l:
    st.subheader("Usage by device (kWh)")
    st.bar_chart(df.groupby("device").kwh.sum())
    st.subheader("Hourly load profile")
    st.line_chart(df.groupby("hour").kwh.mean())
with r:
    st.subheader("🔔 Alerts")
    lvl = st.multiselect("Priority", ["High", "Medium", "Low"], default=["High", "Medium"])
    for _, x in a[a.level.isin(lvl)].head(8).iterrows():
        icon = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}[x.level]
        st.info(f"{icon} **{x.device}** - {x.action}\n\n_{x.condition}_ | Score {x.priority} | Save ₹{x.saving_inr}")
st.subheader("🤖 AI tips")
for t in tips(a): st.success(t)
with st.expander("Rules & weights used"):
    st.write("Priority = " + " + ".join(f"{v:.0%} {k}" for k, v in W.items()))
    st.table(pd.DataFrame(RULES, index=["If", "Then", "Comfort ease", "Confidence"]).T)
