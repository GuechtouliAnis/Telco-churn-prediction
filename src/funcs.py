import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# Constants
MODELS_CONFIG = {
    'XGBoost': 'xgb',
    'Random Forest': 'rft',
    'Gradient Boosting': 'gbc',
    'Neural Networks': 'nn',
    'Logistic Regression': 'logreg',
    'KNN': 'knn'
}

INTERNET_SERVICES = [
    "Online Security", "Online Backup", "Device Protection", 
    "Tech Support", "Streaming TV", "Streaming Movies"]

# Optimized model loading with error handling
@st.cache_resource
def load_model(model_name):
    """Load model with error handling and validation."""
    try:
        model_path = Path(f'model/{MODELS_CONFIG[model_name]}_model.pkl')
        if not model_path.exists():
            st.error(f"Model file not found: {model_path}")
            return None
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"Error loading model {model_name}: {str(e)}")
        return None

def create_feature_dict(inputs):
    """Create feature dictionary from user inputs."""
    gender, phone_service, internet_service, payment_method, contract, \
    tenure, monthly_charges, online_services, senior_citizen, partner, \
    dependents, paperless_billing = inputs
    
    return {
        "gender": 1 if gender == "Male" else 2,
        "SeniorCitizen": 1 if senior_citizen == "Yes" else 0,
        "Partner": 1 if partner == "Yes" else 0,
        "Dependents": 1 if dependents == "Yes" else 0,
        "tenure": tenure,
        "MultipleLines": {
            "No phone service": 0,
            "One phone": 1,
            "Multiple phones": 2
        }[phone_service],
        "OnlineSecurity": 1 if "Online Security" in online_services else 0,
        "OnlineBackup": 1 if "Online Backup" in online_services else 0,
        "DeviceProtection": 1 if "Device Protection" in online_services else 0,
        "TechSupport": 1 if "Tech Support" in online_services else 0,
        "StreamingTV": 1 if "Streaming TV" in online_services else 0,
        "StreamingMovies": 1 if "Streaming Movies" in online_services else 0,
        "Contract": {
            "Month-to-month": 0,
            "One year": 1,
            "Two year": 2
        }[contract],
        "PaperlessBilling": 1 if paperless_billing == "Yes" else 0,
        "MonthlyCharges": monthly_charges,
        "HasInternet": 1 if internet_service != "No internet service" else 0,
        "automatic_pay": 1 if payment_method in ["Bank transfer (automatic)", "Credit card (automatic)"] else 0,
        "DSL": 1 if internet_service == "DSL" else 0,
        "Fiber optic": 1 if internet_service == "Fiber optic" else 0,
        "Bank transfer (automatic)": 1 if payment_method == "Bank transfer (automatic)" else 0,
        "Credit card (automatic)": 1 if payment_method == "Credit card (automatic)" else 0,
        "Electronic check": 1 if payment_method == "Electronic check" else 0}

def display_prediction_results(prediction, probability):
    """Display prediction results with enhanced styling."""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if prediction == 1:
            st.error("🔴 **High Churn Risk**")
            st.caption("This customer is likely to churn")
        else:
            st.success("🟢 **Low Churn Risk**")
            st.caption("This customer is likely to stay")
    
    with col2:
        # Color-coded probability display
        color = "red" if probability > 0.7 else "orange" if probability > 0.4 else "green"
        st.metric(
            label="Churn Probability",
            value=f"{probability:.1%}",
            help=f"The model confidence is {probability:.1%}"
        )