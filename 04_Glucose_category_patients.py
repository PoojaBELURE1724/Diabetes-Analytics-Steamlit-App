import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Glucose Risk Analysis",
    layout="wide"
)

st.title("🩸 Glucose Risk Categories (Distinct Patients)")

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
# CATEGORIZATION FUNCTION
# ---------------------------------------------------------
def categorize_glucose(x):
    if x < 70:
        return "Hypoglycemia"
    elif x < 140:
        return "Normal"
    elif x < 180:
        return "Elevated"
    else:
        return "High"

df['glucose_category'] = df['glucose'].apply(categorize_glucose)

# ---------------------------------------------------------
# DISTINCT PATIENTS PER CATEGORY
# ---------------------------------------------------------
category_counts = (
    df.groupby('glucose_category')['patient_id']
    .nunique()
    .reindex(["Hypoglycemia", "Normal", "Elevated", "High"])
)

plot_df = category_counts.reset_index()
plot_df.columns = ["glucose_category", "distinct_patients"]

# ---------------------------------------------------------
# COLOR MAP
# ---------------------------------------------------------
palette = {
    "Hypoglycemia": "#4C78A8",  # blue
    "Normal": "#54A24B",        # green
    "Elevated": "#F58518",      # orange
    "High": "#E45756"           # red
}

# ---------------------------------------------------------
# CENTERED CHART
# ---------------------------------------------------------
left, center, right = st.columns([1, 2, 1])

with center:

    with st.container(border=True):

        st.markdown(
            "<h3 style='text-align:center;'>🧪 Distinct Patient Glucose Risk Distribution</h3>",
            unsafe_allow_html=True
        )

        fig, ax = plt.subplots(figsize=(6, 4))

        sns.barplot(
            data=plot_df,
            x="glucose_category",
            y="distinct_patients",
            palette=palette,
            ax=ax
        )

        # Add labels on bars
        for container in ax.containers:
            ax.bar_label(container, fontsize=10, fontweight='bold')

        ax.set_xlabel("Glucose Category")
        ax.set_ylabel("Distinct Patients")
        ax.set_title("")

        plt.xticks(rotation=20)
        plt.tight_layout()

        st.pyplot(fig)