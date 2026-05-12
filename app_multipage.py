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
- Demographic glucose categories and risks
- Sleep related parameters effect on glucose
- Bolus volume vs glucose
- Correlation metrics
- conclusion
""")
