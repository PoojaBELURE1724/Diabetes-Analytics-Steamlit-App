# =========================================================
# INTERACTIVE DIABETES ANALYTICS DASHBOARD
# COLOR ENCODED + ANNOTATED + DISTINCT PATIENT COUNTS
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Diabetes Analytics Dashboard",
    layout="wide"
)

st.title("📊 Diabetes Health Analytics Dashboard")

# =========================================================
# LOAD DATA
# =========================================================

# Replace with your file name
df = pd.read_excel("Team6_DataDynamos_Python-Hackathon_MAY2026_V2.xlsx")

# =========================================================
# CREATE BLOOD SUGAR CATEGORY
# =========================================================

def categorize_glucose(x):

    if x < 70:
        return "Low"

    elif x < 140:
        return "Normal"

    elif x < 180:
        return "High"

    else:
        return "Very High"

df['blood_sugar_category'] = df['glucose'].apply(categorize_glucose)

# =========================================================
# CREATE COMPOSITE RISK SCORE
# =========================================================

df['composite_risk_score'] = (
    (df['glucose'] * 0.4) +
    (df['heart_rate'] * 0.2) +
    (df['%_with_sleep_disturbances'] * 0.2) -
    (df['sleep_quality_(1-10)'] * 2) -
    (df['steps'] * 0.001)
)

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔍 Dashboard Filters")

# Gender Filter
gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=df['gender'].unique(),
    default=df['gender'].unique()
)

# Age Filter
age_range = st.sidebar.slider(
    "Select Age Range",
    int(df['age'].min()),
    int(df['age'].max()),
    (
        int(df['age'].min()),
        int(df['age'].max())
    )
)

# Blood Sugar Category Filter
sugar_filter = st.sidebar.multiselect(
    "Select Blood Sugar Category",
    options=df['blood_sugar_category'].unique(),
    default=df['blood_sugar_category'].unique()
)

# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    (df['gender'].isin(gender_filter)) &
    (df['age'] >= age_range[0]) &
    (df['age'] <= age_range[1]) &
    (df['blood_sugar_category'].isin(sugar_filter))
]

# =========================================================
# DISTINCT PATIENT DATA
# =========================================================

# Important for 5-minute repeated records
patient_df = filtered_df.drop_duplicates(subset='patient_id')

# =========================================================
# KPI METRICS
# =========================================================

st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Distinct Patients",
        patient_df['patient_id'].nunique()
    )

with col2:
    st.metric(
        "Average Glucose",
        round(filtered_df['glucose'].mean(), 2)
    )

with col3:
    st.metric(
        "Average Risk Score",
        round(filtered_df['composite_risk_score'].mean(), 2)
    )

with col4:
    st.metric(
        "Average Steps",
        round(filtered_df['steps'].mean(), 2)
    )

# =========================================================
# COLOR MAP
# =========================================================

color_map = {
    "Low": "red",
    "Normal": "green",
    "High": "orange",
    "Very High": "brown"
}

# =========================================================
# ROW 1
# =========================================================

col1, col2 = st.columns(2)

# =========================================================
# DISTINCT PATIENT COUNT BY BLOOD SUGAR CATEGORY
# =========================================================

with col1:

    with st.container(border=True):

        st.subheader(
            "🩸 Distinct Patient Count by Blood Sugar Category"
        )

        sugar_counts = (
            filtered_df
            .groupby('blood_sugar_category')['patient_id']
            .nunique()
            .reset_index()
        )

        colors = [
            color_map[i]
            for i in sugar_counts['blood_sugar_category']
        ]

        fig, ax = plt.subplots(figsize=(7,5))

        bars = ax.bar(
            sugar_counts['blood_sugar_category'],
            sugar_counts['patient_id'],
            color=colors
        )

        ax.set_xlabel("Blood Sugar Category")
        ax.set_ylabel("Distinct Patients")
        ax.set_title("Distinct Patient Distribution")

        # Annotation
        for bar in bars:

            height = bar.get_height()

            ax.annotate(
                f'{int(height)}',
                xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0,5),
                textcoords='offset points',
                ha='center',
                fontsize=10,
                fontweight='bold'
            )

        st.pyplot(fig)

# =========================================================
# PERCENTAGE OF DISTINCT PATIENTS
# =========================================================

with col2:

    with st.container(border=True):

        st.subheader(
            "📊 Percentage of Distinct Patients by Sugar Level"
        )

        sugar_percent = (
            filtered_df
            .groupby('blood_sugar_category')['patient_id']
            .nunique()
        )

        pie_colors = [
            color_map[i]
            for i in sugar_percent.index
        ]

        fig, ax = plt.subplots(figsize=(7,5))

        wedges, texts, autotexts = ax.pie(
            sugar_percent.values,
            labels=sugar_percent.index,
            autopct='%1.1f%%',
            colors=pie_colors,
            startangle=90
        )

        # Style annotation text
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')

        ax.set_title("Patient Percentage by Sugar Category")

        st.pyplot(fig)

# =========================================================
# ROW 2
# =========================================================

col3, col4 = st.columns(2)

# =========================================================
# COMPOSITE RISK SCORE BY GENDER
# =========================================================

with col3:

    with st.container(border=True):

        st.subheader(
            "⚠ Average Composite Risk Score by Gender"
        )

        gender_risk = (
            patient_df
            .groupby('gender')['composite_risk_score']
            .mean()
            .reset_index()
        )

        gender_colors = ['skyblue', 'purple']

        fig, ax = plt.subplots(figsize=(7,5))

        bars = ax.bar(
            gender_risk['gender'],
            gender_risk['composite_risk_score'],
            color=gender_colors
        )

        ax.set_xlabel("Gender")
        ax.set_ylabel("Average Risk Score")
        ax.set_title("Risk Score Comparison by Gender")

        # Annotation
        for bar in bars:

            height = bar.get_height()

            ax.annotate(
                f'{height:.1f}',
                xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0,5),
                textcoords='offset points',
                ha='center',
                fontsize=10,
                fontweight='bold'
            )

        st.pyplot(fig)

# =========================================================
# COMPOSITE RISK SCORE BY AGE GROUP
# =========================================================

with col4:

    with st.container(border=True):

        st.subheader(
            "👥 Average Composite Risk Score by Age Group"
        )

        bins = [0, 20, 40, 60, 80, 100]

        labels = [
            "0-20",
            "21-40",
            "41-60",
            "61-80",
            "81+"
        ]

        patient_df['age_group'] = pd.cut(
            patient_df['age'],
            bins=bins,
            labels=labels
        )

        age_risk = (
            patient_df
            .groupby('age_group')['composite_risk_score']
            .mean()
            .reset_index()
        )

        age_colors = [
            'lightgreen',
            'gold',
            'orange',
            'tomato',
            'darkred'
        ]

        fig, ax = plt.subplots(figsize=(7,5))

        bars = ax.bar(
            age_risk['age_group'].astype(str),
            age_risk['composite_risk_score'],
            color=age_colors
        )

        ax.set_xlabel("Age Group")
        ax.set_ylabel("Average Risk Score")
        ax.set_title("Composite Risk by Age Group")

        # Annotation
        for bar in bars:

            height = bar.get_height()

            ax.annotate(
                f'{height:.1f}',
                xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0,5),
                textcoords='offset points',
                ha='center',
                fontsize=10,
                fontweight='bold'
            )

        st.pyplot(fig)

# =========================================================
# CORRELATION HEATMAP
# =========================================================

st.subheader("🔥 Correlation Heatmap")

with st.container(border=True):

    corr = filtered_df[
        [
            'glucose',
            'heart_rate',
            'steps',
            'calories',
            'sleep_quality_(1-10)',
            '%_with_sleep_disturbances',
            'composite_risk_score'
        ]
    ].corr()

    fig, ax = plt.subplots(figsize=(10,7))

    sns.heatmap(
        corr,
        annot=True,
        cmap='coolwarm',
        linewidths=1,
        fmt=".2f",
        ax=ax
    )

    ax.set_title("Health Variable Correlation Matrix")

    st.pyplot(fig)

# =========================================================
# FILTERED DATA TABLE
# =========================================================

st.subheader("📄 Filtered Dataset")

with st.container(border=True):

    st.dataframe(filtered_df)

# =========================================================
# DOWNLOAD BUTTON
# =========================================================

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name='filtered_diabetes_data.csv',
    mime='text/csv'
)