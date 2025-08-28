import streamlit as st
import pandas as pd
import joblib
import time

st.set_page_config(page_title="Telecom Churn Prediction",
                   layout='wide',
                   initial_sidebar_state='collapsed')

models_dict ={
    'GradientBoosting':'gbc',
    'KNN':'knn',
    'Logistic Regression':'logreg',
    'Neural Networks':'nn',
    'Random Forest':'rft',
    'XGBoost':'xgb'
}

@st.cache_resource
def load_model(model):
    return joblib.load(f'model/{models_dict[model]}_model.pkl')

model_column1, model_column2, model_column3 = st.columns([1, 1, 1],
                                                         gap='small',
                                                         border=False)

select_model = model_column2.selectbox('Model',
                     tuple(models_dict.keys()),
                     index=2)

model = load_model(select_model)

var_column1, var_column2, var_column3 = st.columns([1, 1, 1],
                                                   gap='large',
                                                   border=False)

gender = var_column1.selectbox('Gender',
                               (["Male", "Female"]))

PhoneServices = var_column1.selectbox('Phone Service',
                                        (["No phone service", "One phone", "Multiple phones"]))

InternetService = var_column1.selectbox('Internet Service',
                                        (["No internet service", "DSL", "Fiber optic"]))

PaymentMethod = var_column1.selectbox('Payment Method',
                                        (["Mailed check", "Electronic check",
                                          "Bank transfer (automatic)", "Credit card (automatic)"]))

SeniorCitizen = var_column2.radio('Senior Citizen',
                                  (["Yes", "No"]),
                                  horizontal=True)

Partner = var_column2.radio('Partner',
                            (["Yes", "No"]),
                            horizontal=True)

Dependents = var_column2.radio('Dependents',
                               (["Yes", "No"]),
                               horizontal=True)

PaperlessBilling = var_column2.radio('Paperless Billing',
                                     (["Yes", "No"]),
                                     horizontal=True)

Tenure = var_column3.number_input('Tenure',
                                  min_value=0,
                                  max_value=100,
                                  value="min",
                                  step=1)

MonthlyCharges = var_column3.number_input('Monthly Charges',
                                          min_value=5.0,
                                          max_value=200.0,
                                          value="min",
                                          step=0.05)

OnlineServices = var_column3.multiselect("Online Services",
                                         ("Online Security", "OnlineBackup", "DeviceProtection", "TechSupport",
                                          "StreamingTV", "StreamingMovies"))

Contract = var_column3.selectbox('Contract Type',
                                 (["Month-to-month", "One year", "Two year"]))

