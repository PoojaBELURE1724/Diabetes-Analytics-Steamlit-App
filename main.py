# =========================================================
# MULTIPAGE STREAMLIT APP STRUCTURE
# =========================================================

# Folder Structure:
#
# my_streamlit_app/
# │
# ├── app.py
# ├── pages/
# │     ├── 1_Dashboard.py
# │     ├── 2_Analytics.py
# │     ├── 3_ML_Prediction.py
# │     └── 4_Recommendations.py
# │
# ├── data/
# │     └── diabetes.csv
# │
# └── requirements.txt


# =========================================================
# STEP 1: INSTALL STREAMLIT
# =========================================================
# pip install streamlit pandas matplotlib seaborn scikit-learn


# =========================================================
# STEP 2: MAIN FILE -> app.py
# =========================================================

import streamlit as st

st.set_page_config(
    page_title="Diabetes Analytics App",
    page_icon="📊",
    layout="wide"
)

st.title("🏥 Diabetes Analytics System")

st.markdown("""
Welcome to the Diabetes Analytics Platform.

Use the sidebar to navigate between pages:
- Dashboard
- Analytics
- ML Prediction
- Recommendations
""")


# =========================================================
# STEP 3: CREATE pages/1_Dashboard.py
# =========================================================

import streamlit as st
import pandas as pd

st.title("📈 Dashboard")

# Load data
df = pd.read_csv("data/diabetes.csv")

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Total Patients", len(df))
col2.metric("Average Glucose", round(df['glucose'].mean(),2))
col3.metric("Average Insulin", round(df['insulin'].mean(),2))

st.dataframe(df.head())


# =========================================================
# STEP 4: CREATE pages/2_Analytics.py
# =========================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Analytics")

df = pd.read_csv("data/diabetes.csv")

# Glucose category function
def glucose_category(x):
    if x < 70:
        return "Low"
    elif x <= 140:
        return "Normal"
    elif x <= 180:
        return "High"
    else:
        return "Very High"

df['glucose_category'] = df['glucose'].apply(glucose_category)

# Count plot
category_counts = df['glucose_category'].value_counts()

fig, ax = plt.subplots(figsize=(8,5))

bars = ax.bar(
    category_counts.index,
    category_counts.values
)

ax.set_title("Blood Sugar Category Distribution")
ax.set_xlabel("Category")
ax.set_ylabel("Count")

# Annotate bars
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2,
        height,
        str(height),
        ha='center',
        va='bottom'
    )

st.pyplot(fig)


# =========================================================
# STEP 5: CREATE pages/3_ML_Prediction.py
# =========================================================

import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

st.title("🤖 ML Prediction")

df = pd.read_csv("data/diabetes.csv")

# Example target
df['target'] = (df['glucose'] > 180).astype(int)

features = ['age', 'insulin', 'calories', 'heart_rate']
X = df[features]
y = df['target']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Train
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Accuracy
pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)

st.success(f"Model Accuracy: {accuracy:.2f}")

# User Inputs
st.subheader("Predict Hyperglycemia")

age = st.number_input("Age", 1, 100, 40)
insulin = st.number_input("Insulin", 0.0, 100.0, 20.0)
calories = st.number_input("Calories", 0.0, 5000.0, 2000.0)
heart_rate = st.number_input("Heart Rate", 40, 200, 80)

if st.button("Predict"):

    input_df = pd.DataFrame({
        'age': [age],
        'insulin': [insulin],
        'calories': [calories],
        'heart_rate': [heart_rate]
    })

    prediction = model.predict(input_df)[0]

    if prediction == 1:
        st.error("⚠ High Risk of Hyperglycemia")
    else:
        st.success("✅ Normal Risk")


# =========================================================
# STEP 6: CREATE pages/4_Recommendations.py
# =========================================================

import streamlit as st

st.title("💡 Recommendations")

glucose = st.slider("Current Glucose Level", 40, 350, 120)

if glucose < 70:
    st.warning("""
    Recommendations:
    - Consume fast-acting carbohydrates
    - Monitor glucose every 15 minutes
    - Avoid strenuous activity
    """)

elif glucose <= 140:
    st.success("""
    Recommendations:
    - Maintain current diet
    - Continue regular exercise
    - Monitor regularly
    """)

elif glucose <= 180:
    st.warning("""
    Recommendations:
    - Reduce sugar intake
    - Increase water intake
    - Add light physical activity
    """)

else:
    st.error("""
    Recommendations:
    - Consult physician
    - Adjust insulin dosage
    - Monitor continuously
    """)


# =========================================================
# STEP 7: RUN APPLICATION
# =========================================================

# Open terminal and run:
#
# streamlit run app.py