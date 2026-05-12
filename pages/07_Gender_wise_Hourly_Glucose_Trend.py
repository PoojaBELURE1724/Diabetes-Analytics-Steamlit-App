import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Gender-wise Hourly Glucose Trend",
    layout="wide"
)

#st.title("📊 Gender-wise Hourly Glucose Trend Dashboard")
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

# Normalize gender values (optional safety)
df['gender'] = df['gender'].str.lower()

# =========================================================
# FILTERS (DEFAULT ALL GENDERS)
# =========================================================
gender_groups = df['gender'].dropna().unique()

st.sidebar.header("Filters")

selected_gender = st.sidebar.multiselect(
    "Select Gender",
    options=gender_groups,
    default=gender_groups
)

filtered_df = df[df['gender'].isin(selected_gender)]

# =========================================================
# AGGREGATION
# =========================================================
hourly_trend = (
    filtered_df.groupby(['Time', 'gender'])['glucose']
    .mean()
    .unstack()
)

# =========================================================
# CHART SECTION (GENDER COLOR ENCODING)
# =========================================================
with st.container(border=True):

    #st.subheader("📈 Hourly Glucose Pattern by Gender")

    fig, ax = plt.subplots(figsize=(9, 4.8))

    # Gender-based colors
    gender_colors = {
        'male': '#007aff',    # blue
        'female': '#ff2d55'   # pink
    }

    offsets = [6, -8]

    for i, col in enumerate(hourly_trend.columns):

        color = gender_colors.get(col, '#6b7280')  # fallback gray

        ax.plot(
            hourly_trend.index,
            hourly_trend[col],
            marker='o',
            linewidth=1.1,   # thin lines
            color=color,
            label=col.capitalize()
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
                color=color
            )

    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Average Glucose Level")
    ax.set_xticks(hourly_trend.index)
    ax.tick_params(axis='x', rotation=45)

    ax.legend(title="Gender", fontsize=8)

    ax.grid(alpha=0.2)

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

# =========================================================
# DATA VIEW
# =========================================================
with st.expander("View Aggregated Data"):
    st.dataframe(hourly_trend)