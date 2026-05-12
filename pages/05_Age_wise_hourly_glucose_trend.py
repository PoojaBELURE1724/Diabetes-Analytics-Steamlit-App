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
    page_title="Age-wise Hourly Glucose Trend",
    layout="wide"
)

#st.title("📊 Age-wise Hourly Glucose Trend Dashboard")
st.markdown(
    "<h3 style='text-align:center; margin-bottom:5px;'>📊 Age-wise Hourly Glucose Trend Dashboard</h3>",
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

df['Age_Group'] = pd.cut(
    df['age'],
    bins=[0, 30, 45, 60, 100],
    labels=['18-30', '31-45', '46-60', '60+']
)

# =========================================================
# FILTERS (DEFAULT ALL AGE GROUPS)
# =========================================================
age_groups = ['18-30', '31-45', '46-60', '60+']

st.sidebar.header("Filters")

selected_age = st.sidebar.multiselect(
    "Select Age Groups",
    options=age_groups,
    default=age_groups
)

filtered_df = df[df['Age_Group'].isin(selected_age)]

# =========================================================
# AGGREGATION
# =========================================================
hourly_trend = (
    filtered_df.groupby(['Time', 'Age_Group'])['glucose']
    .mean()
    .unstack()
)

# =========================================================
# KPI SECTION
# =========================================================
with st.container(border=True):
    st.markdown(
    "<h4 style='margin-bottom:5px;'>📌 Key Insights</h4>",
    unsafe_allow_html=True
)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Active Age Groups", len(hourly_trend.columns))

    with col2:
        st.metric(
            "Peak Glucose Hour",
            int(hourly_trend.mean(axis=1).idxmax())
        )

    with col3:
        st.metric(
            "Max Glucose Level",
            f"{hourly_trend.max().max():.1f}"
        )

# =========================================================
# CHART SECTION (BRIGHT + THIN LINES)
# =========================================================
with st.container(border=True):

    st.subheader("📈 Hourly Glucose Pattern by Age Group")

    fig, ax = plt.subplots(figsize=(9, 4.8))

    # Bright color palette
    colors = [
        '#ff3b30',  # red
        '#34c759',  # green
        '#007aff',  # blue
        '#ff9500'   # orange
    ]

    offsets = [6, -8, 6, -8]

    for i, col in enumerate(hourly_trend.columns):

        ax.plot(
            hourly_trend.index,
            hourly_trend[col],
            marker='o',
            linewidth=1.1,   # thin lines
            color=colors[i % len(colors)],
            label=col
        )

        # annotations
        for hour, value in hourly_trend[col].items():
            ax.annotate(
                f'{value:.1f}',
                xy=(hour, value),
                xytext=(0, offsets[i % len(offsets)]),
                textcoords='offset points',
                ha='center',
                fontsize=6,
                color=colors[i % len(colors)]
            )

    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Average Glucose Level")
    ax.set_xticks(hourly_trend.index)
    ax.tick_params(axis='x', rotation=45)

    ax.legend(title="Age Group", fontsize=8)

    ax.grid(alpha=0.2)

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

# =========================================================
# DATA VIEW
# =========================================================
with st.expander("View Aggregated Data"):
    st.dataframe(hourly_trend)