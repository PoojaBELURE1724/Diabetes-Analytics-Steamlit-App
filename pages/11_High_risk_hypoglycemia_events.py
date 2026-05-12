import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="High-Risk Dashboard",
    layout="wide"
)

# ---------------------------------------------------------
# SMALL KPI STYLE
# ---------------------------------------------------------
st.markdown("""
<style>
div[data-testid="stMetric"] {
    padding: 0.2rem 0.2rem;
}

div[data-testid="stMetricLabel"] {
    font-size: 11px;
}

div[data-testid="stMetricValue"] {
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# TITLE (H3 STYLE)
# ---------------------------------------------------------
st.markdown(
    "<h3 style='text-align:center; margin-bottom:5px;'>🚨 High-Risk Hypoglycemia Events</h3>",
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

df_all = load_data()

# ---------------------------------------------------------
# HIGH-RISK FLAG
# ---------------------------------------------------------
df_all['high_risk_flag'] = (
    (df_all['glucose'] < 70) &
    (df_all['heart_rate'] > 100)
)

# ---------------------------------------------------------
# RISK SUMMARY
# ---------------------------------------------------------
risk_summary = (
    df_all[df_all['high_risk_flag']]
    .groupby('patient_id')
    .size()
    .reset_index(name='risk_count')
    .sort_values(by='risk_count', ascending=False)
)

# ---------------------------------------------------------
# KPI METRICS (SMALL)
# ---------------------------------------------------------
col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.metric("High-Risk Events", len(df_all[df_all['high_risk_flag']]))

with col2:
    st.metric("Patients at Risk", risk_summary['patient_id'].nunique())

with col3:
    st.metric("Max Risk Count", risk_summary['risk_count'].max())

# ---------------------------------------------------------
# CHART (FIT SCREEN)
# ---------------------------------------------------------
with st.container(border=True):

    #st.subheader("📊 Risk Events per Patient")

    fig, ax = plt.subplots(figsize=(12, 4))  # 🔥 compact height for screen fit

    sns.barplot(
        data=risk_summary,
        x='patient_id',
        y='risk_count',
        palette='Reds_r',
        ax=ax
    )

    ax.set_xlabel("Patient ID", fontsize=10)
    ax.set_ylabel("Risk Event Count", fontsize=10)

    ax.tick_params(axis='x', rotation=45, labelsize=8)
    ax.tick_params(axis='y', labelsize=8)

    #ax.set_title("High-Risk Hypoglycemia Events", fontsize=11, fontweight='bold')

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

# ---------------------------------------------------------
# TABLE
# ---------------------------------------------------------
with st.expander("📋 Top Risk Patients"):

    st.dataframe(risk_summary.head(10), use_container_width=True)