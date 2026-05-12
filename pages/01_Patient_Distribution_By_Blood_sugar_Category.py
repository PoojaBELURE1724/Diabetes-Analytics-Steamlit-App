import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Blood Sugar Distribution",
    layout="wide"
)

# ---------------------------------------------------------
# SMALL KPI CSS
# ---------------------------------------------------------
st.markdown("""
<style>

div[data-testid="stMetric"] {
    padding: 0.2rem 0.2rem;
    border-radius: 6px;
}

div[data-testid="stMetricLabel"] {
    font-size: 12px;
}

div[data-testid="stMetricValue"] {
    font-size: 20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.markdown(
    "<h3 style='text-align: center; margin-bottom: 0.2rem;'>🩸 Distinct Patient Distribution by Blood Sugar Level</h3>",
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
# CREATE BLOOD SUGAR CATEGORIES
# ---------------------------------------------------------
bins = [0, 70, 140, 200, 500]

labels = ['Low', 'Normal', 'High', 'Very High']

df['Blood_Sugar_Category'] = pd.cut(
    df['glucose'],
    bins=bins,
    labels=labels
)

# ---------------------------------------------------------
# DISTINCT PATIENT COUNT
# ---------------------------------------------------------
category_counts = (
    df.groupby('Blood_Sugar_Category')['patient_id']
    .nunique()
    .reindex(labels)
    .dropna()
)

# ---------------------------------------------------------
# KPI METRICS
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Distinct Patients",
        df['patient_id'].nunique()
    )

with col2:
    st.metric(
        "Average Glucose",
        f"{df['glucose'].mean():.1f}"
    )

# ---------------------------------------------------------
# WIDE PIE CHART SECTION
# ---------------------------------------------------------
left, center, right = st.columns([0.5, 3, 0.5])

with center:

    with st.container(border=True):

        # ✔ WIDER FIGURE
        fig, ax = plt.subplots(figsize=(8, 5.5))

        colors = [
            'Orange',
            'Green',
            'Tomato',
            'Brown'
        ]

        wedges, texts, autotexts = ax.pie(
            category_counts,
            labels=category_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            textprops={
                'fontsize': 10,
                'fontweight': 'bold'
            },
            pctdistance=0.75
        )

        # Percentage styling
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontsize(9)
            autotext.set_fontweight("bold")

        # Legend
        ax.legend(
            wedges,
            category_counts.index,
            title="Blood Sugar Levels",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize=9,
            title_fontsize=10
        )

        ax.axis('equal')

        plt.tight_layout()

        st.pyplot(fig, use_container_width=False)

# ---------------------------------------------------------
# DATA TABLE
# ---------------------------------------------------------
with st.expander("📊 View Distinct Patient Counts"):

    summary_df = pd.DataFrame({
        'Blood Sugar Category': category_counts.index,
        'Distinct Patient Count': category_counts.values
    })

    st.dataframe(summary_df, use_container_width=True)