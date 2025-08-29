import streamlit as st
import pandas as pd
import src.funcs as funcs

# Configure page
st.set_page_config(
    page_title="Telecom Churn Prediction",
    layout='wide',
    initial_sidebar_state='collapsed',
    page_icon="📞")

def main():
    """Main application function."""
    # Custom CSS to reduce top margin and compact layout
    st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    .main > div {
        padding-top: 1rem;
    }
    h1 {
        padding-top: 0rem;
        margin-top: 0rem;
    }
    </style>
    """, unsafe_allow_html=True)
    st.title("📞 Telecom Customer Churn Prediction")
    
    # Model selection container
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            selected_model = st.selectbox(
                'Choose Prediction Model',
                options=list(funcs.MODELS_CONFIG.keys()),
                index=0,  # Default to XGBoost
                help="Select the machine learning model for churn prediction"
            )
        
        # Load selected model
        model = funcs.load_model(selected_model)
        if model is None:
            st.stop()
    
    # Input form
    with st.container():        
        # Create three columns for inputs
        col1, col2, col3 = st.columns(3, gap="large")
        
        with col1:
            st.markdown("**Demographics**")
            gender = st.selectbox('Gender', ["Male", "Female"])
            senior_citizen = st.radio('Senior Citizen', ["Yes", "No"], horizontal=True)
            partner = st.radio('Partner', ["Yes", "No"], horizontal=True)
            dependents = st.radio('Dependents', ["Yes", "No"], horizontal=True)
        
        with col2:
            st.markdown("**Services & Contract**")
            phone_service = st.selectbox(
                'Phone Service',
                ["No phone service", "One phone", "Multiple phones"])
            
            internet_service = st.selectbox(
                'Internet Service',
                ["No internet service", "DSL", "Fiber optic"])
            
            contract = st.selectbox(
                'Contract Type',
                ["Month-to-month", "One year", "Two year"])
            
            # Dynamic online services based on internet availability
            internet_available = internet_service != "No internet service"
            online_services = st.multiselect(
                "Online Services",
                options=funcs.INTERNET_SERVICES if internet_available else [],
                disabled=not internet_available,
                help="Available only with internet service" if not internet_available else None)
        
        with col3:
            st.markdown("**Billing & Charges**")
            tenure = st.number_input(
                'Tenure (months)',
                min_value=0,
                max_value=100,
                value=1,
                help="Number of months with the company")
            
            monthly_charges = st.number_input(
                'Monthly Charges ($)',
                min_value=5.0,
                max_value=200.0,
                value=50.0,
                step=0.50)
            
            payment_method = st.selectbox(
                'Payment Method',
                ["Mailed check", "Electronic check", 
                 "Bank transfer (automatic)", "Credit card (automatic)"])
            
            paperless_billing = st.radio(
                'Paperless Billing',
                ["Yes", "No"],
                horizontal=True)
    
    # Prediction section
    with st.container():        
        # Center the predict button
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            predict_button = st.button(
                "🎯 Predict Churn Risk",
                type="primary",
                use_container_width=True)
        
        if predict_button:
            # Collect all inputs
            inputs = (
                gender, phone_service, internet_service, payment_method, 
                contract, tenure, monthly_charges, online_services,
                senior_citizen, partner, dependents, paperless_billing)
            
            # Create feature dictionary and DataFrame
            features = funcs.create_feature_dict(inputs)
            df = pd.DataFrame([features])
            
            # Make prediction
            try:
                with st.spinner("Making prediction..."):
                    prediction = model.predict(df)[0]
                    probability = model.predict_proba(df)[0][1]
                
                # Display results
                funcs.display_prediction_results(prediction, probability)
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")

if __name__ == "__main__":
    main()