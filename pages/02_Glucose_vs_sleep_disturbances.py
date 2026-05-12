# =========================================================
# COMPACT NO-SCROLL STREAMLIT DASHBOARD
# =========================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Glucose vs Sleep Disturbance",
    #layout="wide"
)

# ---------------------------------------------------------
# TITLE (SHIFTED UP)
# ---------------------------------------------------------
st.markdown(
    "<h3 style='margin-top:0px;'>📊 Average Glucose vs Sleep Disturbance</h3>",
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
# CREATE AGE GROUPS
# ---------------------------------------------------------
df['Age_Group'] = pd.cut(
    df['age'],
    bins=[0, 20, 40, 60, 80],
    labels=['0-20', '21-40', '41-60', '61-80']
)

# ---------------------------------------------------------
# SIDEBAR FILTER
# ---------------------------------------------------------
st.sidebar.header("Filters")

age_groups = ['0-20', '21-40', '41-60', '61-80']

selected_groups = st.sidebar.multiselect(
    "Select Age Groups",
    options=age_groups,
    default=age_groups
)

filtered_df = df[df['Age_Group'].isin(selected_groups)]

# ---------------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------------
avg_glucose = (
    filtered_df.groupby('Age_Group')['glucose']
    .mean()
)

sleep_disturbance = (
    filtered_df.groupby('Age_Group')['%_with_sleep_disturbances']
    .mean()
)

# ---------------------------------------------------------
# KPI ROW (VERY COMPACT)
# ---------------------------------------------------------
kpi1, kpi2 = st.columns(2)

with kpi1:
    st.metric(
        "Avg Glucose",
        f"{filtered_df['glucose'].mean():.1f}"
    )

with kpi2:
    st.metric(
        "Sleep %",
        f"{filtered_df['%_with_sleep_disturbances'].mean():.1f}%"
    )

# ---------------------------------------------------------
# CHART SECTION
# ---------------------------------------------------------
with st.container(border=True):

    # SMALLER HEIGHT TO FIT FULL SCREEN
    fig, ax1 = plt.subplots(figsize=(6.8, 3.0))

    # -----------------------------------------------------
    # BAR CHART
    # -----------------------------------------------------
    bars = ax1.bar(
        avg_glucose.index.astype(str),
        avg_glucose.values,
        color='pink',
        width=0.5
    )

    ax1.set_xlabel("Age Group", fontsize=8)
    ax1.set_ylabel("Avg Glucose", fontsize=8)

    # Compact labels
    for bar in bars:

        height = bar.get_height()

        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            height - 5,
            f'{height:.1f}',
            ha='center',
            va='top',
            fontsize=6,
            color='black',
            fontweight='bold'
        )

    # -----------------------------------------------------
    # SECOND AXIS
    # -----------------------------------------------------
    ax2 = ax1.twinx()

    ax2.plot(
        sleep_disturbance.index.astype(str),
        sleep_disturbance.values,
        marker='o',
        color='red',
        linewidth=1.2,
        markersize=4
    )

    ax2.set_ylabel("Sleep %", fontsize=8)

    # Compact annotations
    x_positions = list(range(len(sleep_disturbance)))

    for x, y in zip(x_positions, sleep_disturbance.values):

        ax2.annotate(
            f'{y:.1f}%',
            xy=(x, y),
            xytext=(0, 4),
            textcoords='offset points',
            ha='center',
            fontsize=5.5,
            color='red'
        )

    # -----------------------------------------------------
    # STYLING
    # -----------------------------------------------------
    ax1.grid(
        axis='y',
        linestyle='--',
        alpha=0.2
    )

    ax1.tick_params(axis='x', labelsize=7)
    ax1.tick_params(axis='y', labelsize=7)
    ax2.tick_params(axis='y', labelsize=7)

    plt.tight_layout(pad=0.5)

    st.pyplot(fig)

# ---------------------------------------------------------
# OPTIONAL TABLE
# ---------------------------------------------------------
with st.expander("View Aggregated Data"):

    summary_df = pd.DataFrame({
        "Average Glucose": avg_glucose,
        "Sleep Disturbance %": sleep_disturbance
    })

    st.dataframe(
        summary_df,
        use_container_width=True
    )

# ---------------------------------------------------------
# REDUCE KPI SIZE
# ---------------------------------------------------------
st.markdown("""
<style>

/* Reduce KPI container size */
div[data-testid="stMetric"] {
    background-color: transparent;
    padding: 0.2rem 0.2rem;
    border-radius: 6px;
}

/* KPI label */
div[data-testid="stMetricLabel"] {
    font-size: 12px;
}

/* KPI value */
div[data-testid="stMetricValue"] {
    font-size: 20px;
}

</style>
""", unsafe_allow_html=True)