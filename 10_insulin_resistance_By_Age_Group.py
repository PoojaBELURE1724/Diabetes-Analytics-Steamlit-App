import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Insulin Resistance Dashboard",
    layout="wide"
)

st.markdown(
    "<h3 style='text-align:center; margin-bottom:5px;'>🩺 Diagnostic: Insulin Resistance</h3>",
    unsafe_allow_html=True
)
# =========================
# FAST DATA LOADING (IMPORTANT FIX)
# =========================
@st.cache_data
def load_data():
    df = pd.read_excel(
        "Team6_DataDynamos_Python-Hackathon_MAY2026_V2.xlsx"
    )

    # Precompute age group once (FAST FIX)
    df['age_group'] = pd.cut(
        df['age'],
        bins=[20, 30, 40, 50, 60, 70, 80],
        labels=['20-30', '30-40', '40-50', '50-60', '60-70', '70-80']
    )

    df['age_category'] = df['age'].apply(
        lambda x: 'Younger' if x < 50 else 'Older'
    )

    return df

df = load_data()

# =========================
# FAST PRECOMPUTED AGGREGATION
# =========================
@st.cache_data
def compute_data(df):
    basal_avg = (
        df.groupby(['age_group', 'age_category'])['basal_rate']
        .mean()
        .reset_index()
    )

    pivot_df = basal_avg.pivot(
        index='age_group',
        columns='age_category',
        values='basal_rate'
    )

    return pivot_df

pivot_df = compute_data(df)

# =========================
# PLOT (OPTIMIZED)
# =========================
fig, ax = plt.subplots(figsize=(8, 4))  # smaller = faster

colors = {
    'Younger': '#34c759',
    'Older': '#007aff'
}

x = range(len(pivot_df.index))
width = 0.35

# Younger bars
if 'Younger' in pivot_df:
    ax.bar(
        [i - width/2 for i in x],
        pivot_df['Younger'],
        width=width,
        color=colors['Younger'],
        label='Younger (<50)'
    )

# Older bars
if 'Older' in pivot_df:
    ax.bar(
        [i + width/2 for i in x],
        pivot_df['Older'],
        width=width,
        color=colors['Older'],
        label='Older (50+)'
    )

# =========================
# LABELS (LIGHTWEIGHT FIX)
# =========================
for i in x:
    if 'Younger' in pivot_df:
        val = pivot_df['Younger'].iloc[i]
        ax.text(i - width/2, val, f"{val:.2f}", ha='center', fontsize=7)

    if 'Older' in pivot_df:
        val = pivot_df['Older'].iloc[i]
        ax.text(i + width/2, val, f"{val:.2f}", ha='center', fontsize=7)

# =========================
# STYLING
# =========================
#ax.set_title("Basal Rate by Age Group (Younger vs Older)")
ax.set_xlabel("Age Group")
ax.set_ylabel("Avg Basal Rate")
ax.set_xticks(list(x))
ax.set_xticklabels(pivot_df.index)

ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()

# =========================
# STREAMLIT OUTPUT (FAST)
# =========================
st.pyplot(fig, use_container_width=True)