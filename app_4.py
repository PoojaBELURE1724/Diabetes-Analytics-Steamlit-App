# =========================================================
# COLOR ENCODED + ANNOTATED DASHBOARD CHARTS
# =========================================================

# ---------------------------------------------------------
# DISTINCT PATIENT COUNT BY BLOOD SUGAR CATEGORY
# ---------------------------------------------------------

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

        # Custom Colors
        color_map = {
            "Low": "red",
            "Normal": "green",
            "High": "orange",
            "Very High": "brown"
        }

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

        # Annotate Bars
        for bar in bars:

            height = bar.get_height()

            ax.annotate(
                f'{int(height)}',
                xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0,5),
                textcoords="offset points",
                ha='center',
                fontsize=10,
                fontweight='bold'
            )

        st.pyplot(fig)

# ---------------------------------------------------------
# DISTINCT PATIENT PERCENTAGE PIE CHART
# ---------------------------------------------------------

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

        # Make annotation bold
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')

        ax.set_title("Patient Percentage by Sugar Category")

        st.pyplot(fig)

# ---------------------------------------------------------
# COMPOSITE RISK SCORE BY GENDER
# ---------------------------------------------------------

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

        # Annotate Bars
        for bar in bars:

            height = bar.get_height()

            ax.annotate(
                f'{height:.1f}',
                xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0,5),
                textcoords="offset points",
                ha='center',
                fontsize=10,
                fontweight='bold'
            )

        st.pyplot(fig)

# ---------------------------------------------------------
# COMPOSITE RISK SCORE BY AGE GROUP
# ---------------------------------------------------------

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

        # Annotate Bars
        for bar in bars:

            height = bar.get_height()

            ax.annotate(
                f'{height:.1f}',
                xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0,5),
                textcoords="offset points",
                ha='center',
                fontsize=10,
                fontweight='bold'
            )

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