# =========================================================
# pages/1_Dashboard.py
# STREAMLIT VERSION
# =========================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Glucose vs Sleep Disturbance",
    layout="wide"
)

st.title("📊 Average Glucose vs Sleep Disturbance %")

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("Team6_DataDynamos_Python-Hackathon_MAY2026_V2.xlsx")

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

selected_groups = st.sidebar.multiselect(
    "Select Age Groups",
    options=df['Age_Group'].dropna().unique(),
    default=df['Age_Group'].dropna().unique()
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
# KPIs
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Overall Avg Glucose",
        f"{filtered_df['glucose'].mean():.1f}"
    )

with col2:
    st.metric(
        "Avg Sleep Disturbance %",
        f"{filtered_df['%_with_sleep_disturbances'].mean():.1f}%"
    )

# ---------------------------------------------------------
# CHART CONTAINER
# ---------------------------------------------------------
with st.container(border=True):

    st.subheader("Average Glucose vs Sleep Disturbance by Age Group")

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # -----------------------------------------------------
    # BAR CHART
    # -----------------------------------------------------
    bars = ax1.bar(
        avg_glucose.index.astype(str),
        avg_glucose.values,
        color='pink',
        width=0.6
    )

    ax1.set_xlabel("Age Group", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Average Glucose", fontsize=12, fontweight='bold')

    # Bar labels
    for bar in bars:
        height = bar.get_height()

        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            height - 8,
            f'{height:.1f}',
            ha='center',
            va='top',
            fontsize=10,
            color='white',
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
        color='maroon',
        linewidth=3,
        markersize=10
    )

    ax2.set_ylabel(
        "Sleep Disturbance %",
        fontsize=12,
        fontweight='bold'
    )

    # -----------------------------------------------------
    # ANNOTATIONS
    # -----------------------------------------------------
    x_positions = list(range(len(sleep_disturbance)))

    for i, (x, y) in enumerate(
        zip(x_positions, sleep_disturbance.values)
    ):

        ax2.annotate(
            f'{y:.1f}%',
            xy=(x, y),
            xytext=(x + 0.10, y + 1.5),
            fontsize=10,
            color='white',
            fontweight='bold',
            arrowprops=dict(
                arrowstyle='->',
                color='steelblue',
                lw=1.5
            ),
            bbox=dict(
                boxstyle='round,pad=0.3',
                facecolor='steelblue',
                edgecolor='white',
                alpha=0.9
            )
        )

    # -----------------------------------------------------
    # TITLE + GRID
    # -----------------------------------------------------
    plt.title(
        "Average Glucose vs Sleep Disturbance %",
        fontsize=16,
        fontweight='bold'
    )

    ax1.grid(
        axis='y',
        linestyle='--',
        alpha=0.4
    )

    plt.tight_layout()

    # -----------------------------------------------------
    # STREAMLIT DISPLAY
    # -----------------------------------------------------
    st.pyplot(fig, use_container_width=True)

# ---------------------------------------------------------
# DATA TABLE
# ---------------------------------------------------------
with st.expander("View Aggregated Data"):

    summary_df = pd.DataFrame({
        "Average Glucose": avg_glucose,
        "Sleep Disturbance %": sleep_disturbance
    })

    st.dataframe(summary_df)