# =========================================================
# INTERACTIVE DIABETES ANALYTICS DASHBOARD (STREAMLIT)
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
    page_title="Diabetes Health Dashboard",
    layout="wide"
)

st.title("📊 Interactive Diabetes Analytics Dashboard")

# =========================================================
# LOAD DATA
# =========================================================

# Replace with your file
df = pd.read_excel("Team6_DataDynamos_Python-Hackathon_MAY2026_V2.xlsx")

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔍 Filters")

# Glucose Filter
glucose_range = st.sidebar.slider(
    "Select Glucose Range",
    int(df['glucose'].min()),
    int(df['glucose'].max()),
    (
        int(df['glucose'].min()),
        int(df['glucose'].max())
    )
)

# Heart Rate Filter
heart_range = st.sidebar.slider(
    "Select Heart Rate Range",
    int(df['heart_rate'].min()),
    int(df['heart_rate'].max()),
    (
        int(df['heart_rate'].min()),
        int(df['heart_rate'].max())
    )
)

# Steps Filter
steps_range = st.sidebar.slider(
    "Select Steps Range",
    int(df['steps'].min()),
    int(df['steps'].max()),
    (
        int(df['steps'].min()),
        int(df['steps'].max())
    )
)

# Calories Filter
calorie_range = st.sidebar.slider(
    "Select Calories Range",
    int(df['calories'].min()),
    int(df['calories'].max()),
    (
        int(df['calories'].min()),
        int(df['calories'].max())
    )
)

# Sleep Quality Filter
sleep_range = st.sidebar.slider(
    "Select Sleep Quality Range",
    float(df['sleep_quality_(1-10)'].min()),
    float(df['sleep_quality_(1-10)'].max()),
    (
        float(df['sleep_quality_(1-10)'].min()),
        float(df['sleep_quality_(1-10)'].max())
    )
)

# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    (df['glucose'] >= glucose_range[0]) &
    (df['glucose'] <= glucose_range[1]) &
    
    (df['heart_rate'] >= heart_range[0]) &
    (df['heart_rate'] <= heart_range[1]) &
    
    (df['steps'] >= steps_range[0]) &
    (df['steps'] <= steps_range[1]) &
    
    (df['calories'] >= calorie_range[0]) &
    (df['calories'] <= calorie_range[1]) &
    
    (df['sleep_quality_(1-10)'] >= sleep_range[0]) &
    (df['sleep_quality_(1-10)'] <= sleep_range[1])
]

# =========================================================
# KPI METRICS
# =========================================================

st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Average Glucose", round(filtered_df['glucose'].mean(), 2))

with col2:
    st.metric("Average Heart Rate", round(filtered_df['heart_rate'].mean(), 2))

with col3:
    st.metric("Average Steps", round(filtered_df['steps'].mean(), 2))

with col4:
    st.metric("Average Calories", round(filtered_df['calories'].mean(), 2))

# =========================================================
# CHARTS
# =========================================================

# ---------------------------------------------------------
# ROW 1
# ---------------------------------------------------------

col1, col2 = st.columns(2)

# =========================================================
# GLUCOSE DISTRIBUTION
# =========================================================

with col1:
    with st.container(border=True):
        st.subheader("🩸 Glucose Distribution")

        fig, ax = plt.subplots(figsize=(6,4))

        ax.hist(filtered_df['glucose'], bins=20)

        ax.set_xlabel("Glucose")
        ax.set_ylabel("Frequency")

        st.pyplot(fig)

# =========================================================
# HEART RATE VS CALORIES
# =========================================================

with col2:
    with st.container(border=True):
        st.subheader("❤️ Heart Rate vs Calories")

        fig, ax = plt.subplots(figsize=(6,4))

        ax.scatter(
            filtered_df['heart_rate'],
            filtered_df['calories']
        )

        ax.set_xlabel("Heart Rate")
        ax.set_ylabel("Calories")

        st.pyplot(fig)

# ---------------------------------------------------------
# ROW 2
# ---------------------------------------------------------

col3, col4 = st.columns(2)

# =========================================================
# STEPS VS CALORIES
# =========================================================

with col3:
    with st.container(border=True):
        st.subheader("🚶 Steps vs Calories")

        fig, ax = plt.subplots(figsize=(6,4))

        ax.scatter(
            filtered_df['steps'],
            filtered_df['calories']
        )

        ax.set_xlabel("Steps")
        ax.set_ylabel("Calories")

        st.pyplot(fig)

# =========================================================
# SLEEP QUALITY DISTRIBUTION
# =========================================================

with col4:
    with st.container(border=True):
        st.subheader("😴 Sleep Quality Distribution")

        fig, ax = plt.subplots(figsize=(6,4))

        ax.hist(filtered_df['sleep_quality_(1-10)'], bins=10)

        ax.set_xlabel("Sleep Quality")
        ax.set_ylabel("Frequency")

        st.pyplot(fig)

# ---------------------------------------------------------
# CORRELATION HEATMAP
# ---------------------------------------------------------

st.subheader("🔥 Correlation Heatmap")

with st.container(border=True):

    corr = filtered_df[
        [
            'glucose',
            'heart_rate',
            'steps',
            'calories',
            'sleep_quality_(1-10)',
            '%_with_sleep_disturbances'
        ]
    ].corr()

    fig, ax = plt.subplots(figsize=(10,6))

    sns.heatmap(
        corr,
        annot=True,
        cmap='coolwarm',
        ax=ax
    )

    st.pyplot(fig)

# ---------------------------------------------------------
# DATA PREVIEW
# ---------------------------------------------------------

st.subheader("📄 Filtered Dataset")

with st.container(border=True):
    st.dataframe(filtered_df)

# =========================================================
# DOWNLOAD FILTERED DATA
# =========================================================

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name='filtered_diabetes_data.csv',
    mime='text/csv'
)