import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Telecom Churn Prediction",
                   layout='wide',
                   initial_sidebar_state='collapsed',
                   page_icon="📞")

models_dict = {
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

vars_container = st.container(border=True,
                              height="content")

model_column1, model_column2, model_column3 = vars_container.columns([1, 1, 1],
                                                         gap='small',
                                                         border=False)

select_model = model_column2.selectbox('Model',
                     tuple(models_dict.keys()),
                     index=5,
                     help="Select the machine learning model you want to use for churn prediction.")

model = load_model(select_model)

var_column1, var_column2, var_column3 = vars_container.columns([1, 1, 1],
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

if internet_disabled:
    internet_options = []
    internet_help="Select the online services the customer subscribes to (if internet is available)."
else:
    internet_options = ["Online Security", "Online Backup", "Device Protection", "Tech Support",
                        "Streaming TV", "Streaming Movies"]
    internet_help="Internet unavailable."

OnlineServices = var_column2.multiselect("Online Services",
                                         internet_options,
                                         default=[],
                                         key="OnlineServices_if",
                                         help=internet_help)

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


data={
    "gender" : 1 if gender == "Male" else 2,
    "SeniorCitizen" : 1 if SeniorCitizen == "Yes" else 0,
    "Partner" : 1 if Partner == "Yes" else 0,
    "Dependents" : 1 if Dependents == "Yes" else 0,
    "tenure" : Tenure,
    "MultipleLines" : 0 if PhoneServices == "No phone service" else 1 if PhoneServices == "One phone" else 2,
    "OnlineSecurity": 1 if "Online Security" in OnlineServices else 0,
    "OnlineBackup": 1 if "Online Backup" in OnlineServices else 0,
    "DeviceProtection": 1 if "Device Protection" in OnlineServices else 0,
    "TechSupport": 1 if "Tech Support" in OnlineServices else 0,
    "StreamingTV": 1 if "Streaming TV" in OnlineServices else 0,
    "StreamingMovies": 1 if "Streaming Movies" in OnlineServices else 0,
    "Contract" : 0 if Contract == "Month-to-month" else 1 if Contract == "One Year" else 2,
    "PaperlessBilling" : 1 if PaperlessBilling == "Yes" else 0,
    "MonthlyCharges" : MonthlyCharges,
    "HasInternet" : 1 if InternetService != "No internet service" else 0,
    "automatic_pay" : 1 if PaymentMethod in ["Bank transfer (automatic)","Credit card (automatic)"] else 0,
    "DSL" : 1 if InternetService == "DSL" else 0,
    "Fiber optic" : 1 if InternetService == "Fiber optic" else 0,
    "Bank transfer (automatic)" : 1 if PaymentMethod == "Bank transfer (automatic)" else 0,
    "Credit card (automatic)" : 1 if PaymentMethod == "Credit card (automatic)" else 0,
    "Electronic check" : 1 if PaymentMethod == "Electronic check" else 0}

df = pd.DataFrame([data])

var_column2.caption("""<div style="text-align:center">
                    <p>Click the button below to calculate the churn %</p></div>""", unsafe_allow_html=True)

col1, col2, col3 = var_column2.columns([1, 1, 1])

result1, result2 = st.columns([1, 2])

if col2.button("Predict Churn",use_container_width=True):
    pred = model.predict(df)[0]
    proba = model.predict_proba(df)[0][1]

    if pred == 1:
        result1.error(f"🔴 Prediction: **Churn**")
    else:
        result1.success(f"🟢 Prediction: **No Churn**")

    result2.metric(label="Churn Probability", value=f"{proba:.2%}")