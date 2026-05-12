import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Risk Matrix Dashboard",
    layout="wide"
)

st.title("📊 Risk Matrix: Race × Gender × Age Group")

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
# RISK CATEGORY (based on glucose)
# ---------------------------------------------------------
def risk_category(x):
    if x < 70:
        return "Hypoglycemia"
    elif x < 140:
        return "Normal"
    elif x < 180:
        return "Elevated"
    else:
        return "High"

df["risk"] = df["glucose"].apply(risk_category)

# ---------------------------------------------------------
# AGE GROUPS
# ---------------------------------------------------------
age_bins = [0, 18, 35, 50, 65, 120]
age_labels = ["0-18", "19-35", "36-50", "51-65", "65+"]

df["age_group"] = pd.cut(df["age"], bins=age_bins, labels=age_labels)

# ---------------------------------------------------------
# CREATE RISK SCORE (numeric for heatmap)
# ---------------------------------------------------------
risk_map = {
    "Hypoglycemia": 1,
    "Normal": 2,
    "Elevated": 3,
    "High": 4
}

df["risk_score"] = df["risk"].map(risk_map)

# ---------------------------------------------------------
# AGGREGATE: DISTINCT PATIENT RISK SCORE
# ---------------------------------------------------------
matrix = df.groupby(
    ["race", "gender", "age_group"]
)["risk_score"].mean().reset_index()

# Pivot for heatmap (Race × Gender, averaged across age groups)
heatmap_data = matrix.pivot_table(
    index=["race", "gender"],
    columns="age_group",
    values="risk_score"
)

# ---------------------------------------------------------
# CENTER LAYOUT
# ---------------------------------------------------------
left, center, right = st.columns([1, 2, 1])

with center:

    with st.container(border=True):

        st.markdown(
            "<h3 style='text-align:center;'>🔥 Risk Matrix (Race × Gender × Age Group)</h3>",
            unsafe_allow_html=True
        )

        fig, ax = plt.subplots(figsize=(9, 5))

        sns.heatmap(
            heatmap_data,
            annot=True,
            cmap="RdYlGn_r",   # green = low risk, red = high risk
            linewidths=0.5,
            linecolor="white",
            cbar_kws={"label": "Risk Level (1=Low, 4=High)"},
            ax=ax
        )

        ax.set_xlabel("Age Group")
        ax.set_ylabel("Race / Gender")
        ax.set_title("")

        plt.tight_layout()

        st.pyplot(fig)