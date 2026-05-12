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

# ---------------------------------------------------------
# TITLE (H3 STYLE)
# ---------------------------------------------------------
st.markdown(
    "<h3 style='text-align:center; margin-bottom:5px;'>📊 Risk Matrix: Race × Gender × Age Group</h3>",
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
# RISK CATEGORY
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
# RISK SCORE MAP
# ---------------------------------------------------------
risk_map = {
    "Hypoglycemia": 1,
    "Normal": 2,
    "Elevated": 3,
    "High": 4
}

df["risk_score"] = df["risk"].map(risk_map)

# ---------------------------------------------------------
# AGGREGATION
# ---------------------------------------------------------
matrix = df.groupby(
    ["race", "gender", "age_group"]
)["risk_score"].mean().reset_index()

heatmap_data = matrix.pivot_table(
    index=["race", "gender"],
    columns="age_group",
    values="risk_score"
)

# ---------------------------------------------------------
# CENTER LAYOUT
# ---------------------------------------------------------
left, center, right = st.columns([1, 3, 1])

with center:

    with st.container(border=True):

        fig, ax = plt.subplots(figsize=(16, 12))  # 🔥 BIGGER HEATMAP

        hm = sns.heatmap(
            heatmap_data,
            annot=True,
            fmt=".2f",
            cmap="RdYlGn_r",
            linewidths=0.7,
            linecolor="white",
            annot_kws={
                "size": 16,
                "weight": "bold",
                "color": "black"
            },
            cbar_kws={
                "label": "Risk Level (1=Low, 4=High)",
                "shrink": 0.9
            },
            ax=ax
        )

        # -----------------------------------------------------
        # COLORBAR (LEGEND FONT FIX)
        # -----------------------------------------------------
        cbar = hm.collections[0].colorbar
        cbar.ax.tick_params(labelsize=14)
        cbar.set_label(
            "Risk Level (1=Low, 4=High)",
            fontsize=18,
            fontweight="bold"
        )

        # -----------------------------------------------------
        # AXIS LABELS (BOLD)
        # -----------------------------------------------------
        ax.set_xlabel("Age Group", fontsize=22, fontweight="bold")
        ax.set_ylabel("Race / Gender", fontsize=22, fontweight="bold")

        # -----------------------------------------------------
        # TICK LABELS (BOLD)
        # -----------------------------------------------------
        ax.tick_params(axis='x', labelsize=18)
        ax.tick_params(axis='y', labelsize=18)

        for label in ax.get_xticklabels():
            label.set_fontweight("bold")

        for label in ax.get_yticklabels():
            label.set_fontweight("bold")

        ax.set_title("")

        plt.tight_layout()

        st.pyplot(fig, use_container_width=True)

# ---------------------------------------------------------
# DATA TABLE
# ---------------------------------------------------------
with st.expander("📊 View Aggregated Risk Matrix Data"):

    st.dataframe(heatmap_data, use_container_width=True)