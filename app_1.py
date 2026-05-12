import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Page CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="HUPA Diabetes Analytics Dashboard",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("HUPA Diabetes Data Analytics Dashboard")
st.markdown("Interactive dashboard for diabetes descriptive analytics using Streamlit.")

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Diabetes Dataset excel",
    type=["xlsx"]
)

if uploaded_file is not None:

    # Load dataset
    df = pd.read_excel(uploaded_file)

    st.success("Dataset uploaded successfully!")

    # -----------------------------
    # DATA PREVIEW
    # -----------------------------
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # -----------------------------
    # SIDEBAR FILTERS
    # -----------------------------
    st.sidebar.header("Filters")

    # age filter
    if 'age' in df.columns:
        age_range = st.sidebar.slider(
            "Select age Range",
            int(df['age'].min()),
            int(df['age'].max()),
            (
                int(df['age'].min()),
                int(df['age'].max())
            )
        )

        df = df[
            (df['age'] >= age_range[0]) &
            (df['age'] <= age_range[1])
        ]

    # gender filter
    if 'gender' in df.columns:
        gender = st.sidebar.multiselect(
            "Select gender",
            options=df['gender'].unique(),
            default=df['gender'].unique()
        )

        df = df[df['gender'].isin(gender)]

    # -----------------------------
    # KPI METRICS
    # -----------------------------
    st.subheader("Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Average Glucose",
            round(df['glucose'].mean(), 2)
        )

    with col2:
        st.metric(
            "Average Heart Rate",
            round(df['heart_rate'].mean(), 2)
        )

    with col3:
        st.metric(
            "Average Steps",
            round(df['steps'].mean(), 2)
        )

    with col4:
        hyper = df[df['glucose'] > 140]

        hyper_percentage = (
            hyper['patient_id'].nunique() /
            df['patient_id'].nunique()
        ) * 100

        st.metric(
            "Hyperglycemia %",
            f"{hyper_percentage:.1f}%"
        )

    # -----------------------------
    # GLUCOSE DISTRIBUTION
    # -----------------------------
    st.subheader("Glucose Distribution")

    fig1, ax1 = plt.subplots(figsize=(8, 4))

    sns.histplot(df['glucose'], bins=20, kde=True, ax=ax1)

    ax1.set_title("Distribution of Glucose Levels")

    st.pyplot(fig1)

    # -----------------------------
    # GLUCOSE VARIABILITY
    # -----------------------------
    st.subheader("Top Patients with Highest Glucose Variability")

    variability = (
        df.groupby('patient_id')['glucose']
        .std()
        .sort_values(ascending=False)
        .head(10)
    )

    fig2, ax2 = plt.subplots(figsize=(10, 5))

    sns.barplot(
        x=variability.index.astype(str),
        y=variability.values,
        ax=ax2
    )

    ax2.set_title("Highest Glucose Variability")
    ax2.set_xlabel("Patient ID")
    ax2.set_ylabel("Standard Deviation")

    st.pyplot(fig2)

    # -----------------------------
    # STEPS BY age GROUP
    # -----------------------------
    st.subheader("Average Steps by age Group")

    df['age_Group'] = pd.cut(
        df['age'],
        bins=[0, 20, 40, 60, 100],
        labels=['0-20', '21-40', '41-60', '60+']
    )

    steps_by_age = (
        df.groupby('age_Group')['steps']
        .mean()
    )

    fig3, ax3 = plt.subplots(figsize=(8, 5))

    steps_by_age.plot(kind='bar', ax=ax3)

    ax3.set_title("Average Steps by age Group")
    ax3.set_xlabel("age Group")
    ax3.set_ylabel("Average Steps")

    st.pyplot(fig3)

    # -----------------------------
    # CALORIES VS GLUCOSE
    # -----------------------------
    st.subheader("Calories Burned vs Glucose")

    fig4, ax4 = plt.subplots(figsize=(8, 5))

    sns.scatterplot(
        x='calories',
        y='glucose',
        data=df,
        ax=ax4
    )

    ax4.set_title("Calories Burned vs Glucose")

    st.pyplot(fig4)

    # -----------------------------
    # SLEEP QUALITY VS GLUCOSE
    # -----------------------------
    st.subheader("Sleep Quality vs Glucose")

    fig5, ax5 = plt.subplots(figsize=(8, 5))

    sns.boxplot(
        x='sleep_quality_(1-10)',
        y='glucose',
        data=df,
        ax=ax5
    )

    ax5.set_title("Sleep Quality Impact on Glucose")

    st.pyplot(fig5)

    # -----------------------------
    # INSULIN DELIVERY BY HOUR
    # -----------------------------
    st.subheader("Insulin Delivery by Hour")

    if 'time' in df.columns:

        df['time'] = pd.to_datetime(df['time'])
        df['Hour'] = df['time'].dt.hour

        insulin_by_hour = (
            df.groupby('Hour')['bolus_volume_delivered']
            .mean()
        )

        fig6, ax6 = plt.subplots(figsize=(10, 5))

        insulin_by_hour.plot(marker='o', ax=ax6)

        ax6.set_title("Average Insulin Delivery by Hour")
        ax6.set_xlabel("Hour")
        ax6.set_ylabel("Bolus Insulin")

        st.pyplot(fig6)

    # -----------------------------
    # GLUCOSE SPIKES BY HOUR
    # -----------------------------
    st.subheader("Glucose Spikes by Hour")

    if 'Hour' in df.columns:

        spikes = df[df['glucose'] > 180]

        spike_hours = spikes.groupby('Hour').size()

        fig7, ax7 = plt.subplots(figsize=(10, 5))

        spike_hours.plot(kind='bar', ax=ax7)

        ax7.set_title("Glucose Spikes by Hour")
        ax7.set_xlabel("Hour")
        ax7.set_ylabel("Spike Count")

        st.pyplot(fig7)

    # -----------------------------
    # CORRELATION HEATMAP
    # -----------------------------
    st.subheader("Correlation Heatmap")

    numeric_cols = [
        'glucose',
        'heart_rate',
        'steps',
        'calories',
        'basal_rate',
        'bolus_volume_delivered',
        'carb_input'
    ]

    available_cols = [
        col for col in numeric_cols
        if col in df.columns
    ]

    corr = df[available_cols].corr()

    fig8, ax8 = plt.subplots(figsize=(10, 6))

    sns.heatmap(
        corr,
        annot=True,
        cmap='coolwarm',
        ax=ax8
    )

    ax8.set_title("Feature Correlation Heatmap")

    st.pyplot(fig8)

    # -----------------------------
    # DOWNLOAD FILTERED DATA
    # -----------------------------
    st.subheader("Download Filtered Dataset")

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='filtered_diabetes_data.csv',
        mime='text/csv'
    )

else:
    st.info("Please upload a CSV dataset to begin analysis.")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("Developed using Streamlit, Pandas, Matplotlib, and Seaborn")
