import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Health Correlation Dashboard",
    layout="wide"
)

#st.title("🔥 Health Variable Correlation Dashboard")
st.markdown(
    "<h3 style='text-align:center; margin-bottom:5px;'>🔥 Health Variable Correlation Dashboard</h3>",
    unsafe_allow_html=True
)
# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_excel(
        "Team6_DataDynamos_Python-Hackathon_MAY2026_V2.xlsx"
    )

df = load_data()

# ---------------------------------------------------------
# CORRELATION MATRIX
# ---------------------------------------------------------
corr_cols = [
    'glucose',
    'heart_rate',
    'steps',
    'calories',
    'sleep_quality_(1-10)',
    '%_with_sleep_disturbances'
]

corr = df[corr_cols].corr()

# ---------------------------------------------------------
# CENTERED LAYOUT
# ---------------------------------------------------------
col1, col2, col3 = st.columns([1, 3.5, 1])

with col2:

    fig, ax = plt.subplots(figsize=(12, 10))  # 🔥 BIGGER CHART

    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        linewidths=0.5,
        annot_kws={"size": 11, "fontweight": "bold"},  # 🔥 BIG LABELS
        ax=ax
    )

    # bigger axis labels
    ax.tick_params(axis='x', labelsize=12, rotation=30)
    ax.set_xticklabels(ax.get_xticklabels(), fontweight='bold')
    ax.tick_params(axis='y', labelsize=12)
    ax.set_yticklabels(ax.get_yticklabels(), fontweight='bold')

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

# ---------------------------------------------------------
# OPTIONAL TABLE
# ---------------------------------------------------------
with st.expander("View Correlation Table"):

    st.dataframe(corr, use_container_width=True)