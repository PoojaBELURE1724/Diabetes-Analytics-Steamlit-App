import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🩺 Diagnostic: Basal Rate by Age Group")

# =========================
# LOAD DATA
# =========================
df = pd.read_excel("Team6_DataDynamos_Python-Hackathon_MAY2026_V2.xlsx")

# =========================
# AGE GROUP CREATION
# =========================
df['age_group'] = pd.cut(
    df['age'],
    bins=[20, 30, 40, 50, 60, 70, 80],
    labels=['20-30', '30-40', '40-50', '50-60', '60-70', '70-80']
)

# =========================
# AGGREGATION
# =========================
basal_avg = df.groupby('age_group')['basal_rate'].mean().reset_index()

# =========================
# PLOT
# =========================
fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(
    basal_avg['age_group'],
    basal_avg['basal_rate'],
    color='#90ee90'   # ✔ light green bars
)

# value labels on bars
for i, v in enumerate(basal_avg['basal_rate']):
    ax.text(i, v + 0.01, f"{v:.2f}", ha='center', fontsize=9)

# =========================
# STYLING
# =========================
ax.set_title("Diagnostic: Average Basal Rate by Age Group")
ax.set_xlabel("Age Group (Years)")
ax.set_ylabel("Average Basal Rate (units/hr)")
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()

# =========================
# STREAMLIT OUTPUT
# =========================
st.pyplot(fig, use_container_width=True)