import streamlit as st
import numpy as np
from joblib import load

st.set_page_config(page_title="Credit Pulse — Churn Predictor", page_icon="💳", layout="centered")

# -------------------------------------------------
# Load model (same joblib format used in app.py)
# -------------------------------------------------
@st.cache_resource
def load_model():
    return load("XGBoost_model")

model = load_model()

# Top-10 feature importances from the notebook (used for the "why" explanation)
FEATURE_IMPORTANCE = {
    "NumOfProducts": 0.425,
    "IsActiveMember": 0.175,
    "Age": 0.168,
    "Is_Germany": 0.086,
    "Is_Male": 0.071,
    "Balance": 0.031,
    "HasCrCard": 0.011,
    "CreditScore": 0.008,
    "Tenure": 0.007,
    "Is_Spain": 0.007,
}

st.title("💳 Credit Pulse")
st.caption("Bank customer churn predictor — XGBoost model (ROC-AUC 0.890, F1 0.640)")

st.divider()

# -------------------------------------------------
# Input form
# -------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    credit_score = st.slider("Credit Score", 300, 900, 650)
    age = st.slider("Age", 18, 92, 38)
    tenure = st.slider("Tenure (years with bank)", 0, 10, 5)
    balance = st.number_input("Balance ($)", min_value=0.0, value=75000.0, step=1000.0)

with col2:
    num_products = st.selectbox("Number of Products", [1, 2, 3, 4], index=1)
    estimated_salary = st.number_input("Estimated Salary ($)", min_value=0.0, value=100000.0, step=1000.0)
    has_cr_card = st.radio("Has Credit Card?", ["Yes", "No"], horizontal=True)
    is_active = st.radio("Active Member?", ["Yes", "No"], horizontal=True)

col3, col4 = st.columns(2)
with col3:
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
with col4:
    geography = st.selectbox("Geography", ["France", "Germany", "Spain"])

threshold = st.slider(
    "Decision threshold",
    0.1, 0.9, 0.5, 0.05,
    help="Lower threshold = catch more churners (higher recall) but more false alarms. "
         "See the Threshold Tuning table in the README for the precision/recall tradeoff.",
)

st.divider()

# -------------------------------------------------
# Predict
# -------------------------------------------------
if st.button("Predict Churn Risk", type="primary", use_container_width=True):
    Is_Male = 1 if gender == "Male" else 0
    Is_Female = 1 - Is_Male
    Is_Germany = 1 if geography == "Germany" else 0
    Is_Spain = 1 if geography == "Spain" else 0
    Is_France = 1 if geography == "France" else 0
    HasCrCard = 1 if has_cr_card == "Yes" else 0
    IsActiveMember = 1 if is_active == "Yes" else 0

    features = np.array([[
        credit_score, age, tenure, balance, num_products,
        HasCrCard, IsActiveMember, estimated_salary,
        Is_Male, Is_Female, Is_Germany, Is_Spain, Is_France
    ]])

    proba = model.predict_proba(features)[0][1]
    will_churn = proba >= threshold

    st.subheader("Result")
    r1, r2 = st.columns([1, 2])
    with r1:
        st.metric("Churn Probability", f"{proba:.1%}")
    with r2:
        if will_churn:
            st.error(f"⚠️ High churn risk (threshold: {threshold:.0%})")
        else:
            st.success(f"✅ Likely to stay (threshold: {threshold:.0%})")

    st.progress(min(float(proba), 1.0))

    # -------------------------------------------------
    # Explainability: which inputs drove this the most
    # -------------------------------------------------
    st.subheader("What's driving this prediction")
    st.caption("Based on global feature importance from the trained XGBoost model — "
               "not a per-prediction SHAP value, but shows which inputs the model weighs most.")

    flags = []
    if num_products <= 1 or num_products >= 3:
        flags.append(("Number of Products", FEATURE_IMPORTANCE["NumOfProducts"],
                       "1 or 3+ products correlates with higher churn in this dataset"))
    if is_active == "No":
        flags.append(("Inactive Member", FEATURE_IMPORTANCE["IsActiveMember"],
                       "Inactive members churn at a notably higher rate"))
    if age >= 45:
        flags.append(("Age", FEATURE_IMPORTANCE["Age"],
                       "Older customers show higher churn likelihood in this dataset"))
    if geography == "Germany":
        flags.append(("Geography: Germany", FEATURE_IMPORTANCE["Is_Germany"],
                       "German customers churn at a higher rate than France/Spain"))

    if flags:
        for name, importance, note in flags:
            st.write(f"**{name}** (model weight: {importance:.1%}) — {note}")
    else:
        st.write("No major risk flags — inputs align with the model's lower-risk profile.")

    with st.expander("Full feature importance (XGBoost)"):
        st.bar_chart(FEATURE_IMPORTANCE)

st.divider()
st.caption("Model trained on the Kaggle Bank Customer Churn dataset · "
           "[View source on GitHub](https://github.com/paradise2580/CREDIT-PULSE)")