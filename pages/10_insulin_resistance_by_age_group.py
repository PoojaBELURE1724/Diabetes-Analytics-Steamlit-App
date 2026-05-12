import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🩺 Diagnostic: Insuline resi")

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

# Define age category (✔ encoding logic)
df['age_category'] = df['age'].apply(
    lambda x: 'Younger' if x < 50 else 'Older'
)

# =========================
# AGGREGATION
# =========================
basal_avg = df.groupby(['age_group', 'age_category'])['basal_rate'].mean().reset_index()

# Pivot for plotting
pivot_df = basal_avg.pivot(index='age_group', columns='age_category', values='basal_rate')

# =========================
# PLOT
# =========================
fig, ax = plt.subplots(figsize=(9, 5))

colors = {
    'Younger': '#34c759',  # green
    'Older': '#007aff'     # blue
}

x = range(len(pivot_df.index))

width = 0.35

# Younger bars
ax.bar(
    [i - width/2 for i in x],
    pivot_df['Younger'],
    width=width,
    color=colors['Younger'],
    label='Younger (<50)'
)

# Older bars
ax.bar(
    [i + width/2 for i in x],
    pivot_df['Older'],
    width=width,
    color=colors['Older'],
    label='Older (50+)'
)

# =========================
# VALUE LABELS
# =========================
for i, v in enumerate(pivot_df['Younger']):
    ax.text(i - width/2, v, f"{v:.2f}", ha='center', fontsize=8)

for i, v in enumerate(pivot_df['Older']):
    ax.text(i + width/2, v, f"{v:.2f}", ha='center', fontsize=8)

# =========================
# STYLING
# =========================
ax.set_title("Basal Rate by Age Group (Younger vs Older)")
ax.set_xlabel("Age Group")
ax.set_ylabel("Average Basal Rate (units/hr)")
ax.set_xticks(x)
ax.set_xticklabels(pivot_df.index)
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()

st.pyplot(fig, use_container_width=True)