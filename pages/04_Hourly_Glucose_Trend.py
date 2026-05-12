import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.markdown(
    "<h3 style='text-align:center; margin-bottom:5px;'>📊 Average Glucose Trend by Hour</h3>",
    unsafe_allow_html=True
)
# =========================
# DATA PREPARATION
# =========================
@st.cache_data
def load_data():
    return pd.read_excel(
        "Team6_DataDynamos_Python-Hackathon_MAY2026_V2.xlsx"
    )

df = load_data()

df['Time'] = pd.to_datetime(df['time'])
df['hour'] = df['Time'].dt.hour

hourly_glucose = df.groupby('hour')['glucose'].mean()

# =========================
# PLOT
# =========================
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    hourly_glucose.index,
    hourly_glucose.values,
    marker='o',
    color='red',   # red color
    linewidth=1.5
)

# value labels
for x, y in zip(hourly_glucose.index, hourly_glucose.values):
    ax.text(
        x,
        y + 0.8,
        round(y, 1),
        ha='center',
        fontsize=8
    )

# =========================
# STYLING
# =========================
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Average Glucose")
ax.set_xticks(range(0, 24))
ax.grid(alpha=0.3)

plt.tight_layout()

# =========================
# STREAMLIT RENDER
# =========================
st.pyplot(fig, use_container_width=True)