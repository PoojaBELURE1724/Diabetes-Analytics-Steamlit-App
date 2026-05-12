import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.markdown("""
<style>

/* KPI container */
div[data-testid="stMetric"] {
    padding: 0.1rem 0.1rem;
}

/* KPI label (title text) */
div[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    font-weight: 500;
}

/* KPI value (big number) */
div[data-testid="stMetricValue"] {
    font-size: 16px !important;
    font-weight: 600;
}

/* KPI delta (if any) */
div[data-testid="stMetricDelta"] {
    font-size: 11px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Race-wise Hourly Glucose Trend",
    layout="wide"
)

#st.title("📊 Race-wise Hourly Glucose Trend Dashboard")
st.markdown(
    "<h3 style='text-align:center; margin-bottom:5px;'>📊 Race-wise Hourly Glucose Trend Dashboard</h3>",
    unsafe_allow_html=True
)

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    return pd.read_excel(
        "Team6_DataDynamos_Python-Hackathon_MAY2026_V2.xlsx"
    )

df = load_data()

# =========================================================
# PREPROCESSING
# =========================================================
df['Time'] = pd.to_datetime(df['time']).dt.hour

race_col = 'race'
df = df.dropna(subset=[race_col])

# =========================================================
# FILTERS
# =========================================================
race_groups = sorted(df[race_col].unique())

st.sidebar.header("Filters")

selected_race = st.sidebar.multiselect(
    "Select Race Groups",
    options=race_groups,
    default=race_groups
)

filtered_df = df[df[race_col].isin(selected_race)]

# =========================================================
# AGGREGATION
# =========================================================
hourly_trend = (
    filtered_df.groupby(['Time', race_col])['glucose']
    .mean()
    .unstack()
)

# =========================================================
# KPI SECTION
# =========================================================

# =========================================================
# CHART SECTION (BRIGHT + THIN LINES)
# =========================================================
with st.container(border=True):

    #st.subheader("📈 Hourly Glucose Pattern by Race Group")

    fig, ax = plt.subplots(figsize=(9, 4.8))

    # Bright color palette
    colors = [
        '#FF3B30',  # red
        '#34C759',  # green
        '#FF9500',  # orange
        '#007AFF',  # blue
        '#AF52DE',  # purple
        '#FF2D55'   # pink
    ]

    offsets = [6, -8, 6, -8, 6, -8]

    for i, col in enumerate(hourly_trend.columns):

        ax.plot(
            hourly_trend.index,
            hourly_trend[col],
            marker='o',
            linewidth=1.2,   # ✔ THINNER LINE
            color=colors[i % len(colors)],
            label=col
        )

        # annotations (small + clean)
        for hour, value in hourly_trend[col].items():
            ax.annotate(
                f'{value:.1f}',
                xy=(hour, value),
                xytext=(0, offsets[i % len(offsets)]),
                textcoords='offset points',
                ha='center',
		va='center',   # ✅ vertical alignment fix
                fontsize=7,
                color=colors[i % len(colors)],
		fontweight = 'bold',
		rotation=30
            )

    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Average Glucose Level")
    ax.set_xticks(hourly_trend.index)
    ax.tick_params(axis='x', rotation=45)

    ax.legend(title="Race Group", fontsize=8)
    ax.grid(alpha=0.25)

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

# =========================================================
# DATA VIEW
# =========================================================
with st.expander("View Aggregated Data"):
    st.dataframe(hourly_trend)