import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#st.title("🩺 Diagnostic: Basal Rate by Age Group")
st.markdown(
    "<h3 style='margin-bottom:5px;'>🩺 Diagnostic: Basal Rate by Age Group</h3>",
    unsafe_allow_html=True
)

# =========================
# FAST DATA LOADING (IMPORTANT FIX)
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("Team6_DataDynamos_Python-Hackathon_MAY2026_V2.xlsx")

df = load_data()

# =========================
# PRECOMPUTE AGE GROUP (OPTIMIZED)
# =========================
bins = [20, 30, 40, 50, 60, 70, 80]
labels = ['20-30', '30-40', '40-50', '50-60', '60-70', '70-80']

df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)

# =========================
# PRECOMPUTE AGGREGATION (FASTER)
# =========================
basal_avg = (
    df.groupby('age_group', observed=True)['basal_rate']
    .mean()
    .reset_index()
)

# =========================
# PLOT
# =========================
fig, ax = plt.subplots(figsize=(8, 4.5))  # smaller = faster render

ax.bar(
    basal_avg['age_group'],
    basal_avg['basal_rate'],
    color='#6ee7b7'   # lighter but optimized green
)

# value labels (lightweight)
for i, v in enumerate(basal_avg['basal_rate']):
    ax.text(i, v, f"{v:.2f}", ha='center', fontsize=8)

#ax.set_title("Average Basal Rate by Age Group")
ax.set_xlabel("Age Group")
ax.set_ylabel("Basal Rate (units/hr)")
ax.grid(axis='y', alpha=0.2)

plt.tight_layout()

# =========================
# STREAMLIT OUTPUT
# =========================
st.pyplot(fig, use_container_width=True)