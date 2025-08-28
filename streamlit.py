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
                               ["Male", "Female"],
                               help="Select the customer's gender.")

PhoneServices = var_column1.selectbox('Phone Service',
                                      ["No phone service", "One phone", "Multiple phones"],
                                      help="Select the type of phone service the customer has.")

InternetService = var_column1.selectbox('Internet Service',
                                        ["No internet service", "DSL", "Fiber optic"],
                                        help="Select the type of internet service the customer has, if any.")

PaymentMethod = var_column1.selectbox('Payment Method',
                                      ["Mailed check", "Electronic check",
                                       "Bank transfer (automatic)", "Credit card (automatic)"],
                                      help="Select the method the customer uses to pay their bills.")

Contract = var_column2.selectbox('Contract Type',
                                 ["Month-to-month", "One year", "Two year"],
                                 help="Select the type of contract the customer has with the company.")

Tenure = var_column2.number_input('Tenure',
                                  min_value=0,
                                  max_value=100,
                                  value="min",
                                  step=1,
                                  help="Enter the number of months the customer has been with the company.")

MonthlyCharges = var_column2.number_input('Monthly Charges',
                                          min_value=5.0,
                                          max_value=200.0,
                                          value="min",
                                          step=0.05,
                                          help="Enter the monthly charges billed to the customer.")

internet_disabled = True if InternetService == "No internet service" else False

default_services = [] if internet_disabled else []

OnlineServices = var_column2.multiselect("Online Services",
                                         ["Online Security", "OnlineBackup", "DeviceProtection", "TechSupport",
                                          "StreamingTV", "StreamingMovies"],
                                         default=default_services,
                                         disabled=internet_disabled,
                                         help="Select the online services the customer subscribes to (if internet is available).")

if internet_disabled:
    OnlineServices = []

SeniorCitizen = var_column3.radio('Senior Citizen',
                                  ["Yes", "No"],
                                  horizontal=True,
                                  help="Indicate if the customer is a senior citizen.")

Partner = var_column3.radio('Partner',
                            ["Yes", "No"],
                            horizontal=True,
                            help="Indicate if the customer has a partner.")

Dependents = var_column3.radio('Dependents',
                               ["Yes", "No"],
                               horizontal=True,
                               help="Indicate if the customer has dependents.")

PaperlessBilling = var_column3.radio('Paperless Billing',
                                     ["Yes", "No"],
                                     horizontal=True,
                                     help="Select whether the customer uses paperless billing.")