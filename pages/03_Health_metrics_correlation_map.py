import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# PAGE CONFIG (wide = single dashboard feel)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Health Correlation Dashboard",
    layout="wide"
)

st.title("🔥 Health Variable Correlation Dashboard")

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
# SINGLE PAGE DASHBOARD LAYOUT (CENTERED)
# ---------------------------------------------------------
col1, col2, col3 = st.columns([1, 3, 1])

with col2:

    st.subheader("Correlation Heatmap")

    fig, ax = plt.subplots(figsize=(5.5, 4.5))  # compact size

    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        linewidths=0.4,
        annot_kws={"size": 8},   # smaller annotation font
        ax=ax
    )

    ax.set_title(
        "Health Variable Correlation",
        fontsize=11,
        fontweight='bold'
    )

    plt.tight_layout()

    st.pyplot(fig)

# ---------------------------------------------------------
# OPTIONAL DATA VIEW
# ---------------------------------------------------------
with st.expander("View Correlation Table"):
    st.dataframe(corr, use_container_width=True)