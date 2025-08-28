import streamlit as st
import pandas as pd
import joblib

@st.cache_resource
def load_model():
    return joblib.load("model/logreg_model.pkl")

model = load_model()

st.set_page_config(page_title="Telecom Churn Prediction",
                   layout='wide',
                   initial_sidebar_state='collapsed')

col1, col2 = st.columns([1,1], gap='small', border=True)

col1.title('Insert Client Info')

co1, co2, co3 = col1.columns([1,1,1], gap='small')

gender = co1.selectbox("Gender",
                    ('Male','Female'))

SeniorCitizen = co2.radio('Senior Citizen',
                        ('Yes', 'No'),
                        horizontal=True)

InternetService = co1.selectbox("Internet Service",
                            ("No internet service", "DSL", "Fibre optic"),
                            0)
if InternetService!='No internet service':    
    MultipleLines = co2.selectbox("Multiple Lines",
                            ("No phone service", "No", "Yes"),
                            0)

c1, c2, c3 = st.columns([1.5, 1, 1.5])
