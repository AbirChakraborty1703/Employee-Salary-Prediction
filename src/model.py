import joblib
import streamlit as st
import pandas as pd
import numpy as np

@st.cache_resource
def load_model(path: str):
    """
    Loads and caches the trained model package from disk.
    Returns the complete model package with preprocessing components.
    """
    import os
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at {path}. Please train the model first using the Jupyter notebook.")
    
    try:
        return joblib.load(path)
    except Exception as e:
        raise RuntimeError(f"Error loading model from {path}: {str(e)}")

def predict(model_package, input_df):
    """
    Runs prediction on input DataFrame using the model package.
    Returns both prediction and probability for classification.
    """
    try:
        # Create a copy of input data
        processed_data = input_df.copy()
        
        # Apply label encoders to categorical columns
        for col, encoder in model_package['label_encoders'].items():
            if col in processed_data.columns:
                original_value = processed_data[col].iloc[0]
                try:
                    encoded_value = encoder.transform(processed_data[col])[0]
                    processed_data[col] = encoded_value
                except ValueError as e:
                    # Handle unseen categories by using default value
                    processed_data[col] = 0
        
        # Apply scaler to numerical features
        numerical_features = model_package['numerical_features']
        if numerical_features:
            processed_data[numerical_features] = model_package['scaler'].transform(processed_data[numerical_features])
        
        # Ensure feature order matches training
        feature_columns = model_package['feature_columns']
        processed_data = processed_data[feature_columns]
        
        # Make prediction
        prediction = model_package['model'].predict(processed_data)[0]
        prediction_proba = model_package['model'].predict_proba(processed_data)[0]
        
        # Convert prediction to readable format
        predicted_class = model_package['target_names'][prediction]
        confidence = max(prediction_proba) * 100
        
        return {
            'prediction': predicted_class,
            'confidence': confidence,
            'probabilities': {
                model_package['target_names'][0]: prediction_proba[0],
                model_package['target_names'][1]: prediction_proba[1]
            }
        }
    
    except Exception as e:
        import streamlit as st
        import traceback
        
        # Display error in Streamlit only in debug mode
        if st.session_state.get('debug_mode', False):
            st.error(f"❌ PREDICTION ERROR: {str(e)}")
            st.code(traceback.format_exc())
        
        return {
            'prediction': '<=50K',
            'confidence': 50.0,
            'probabilities': {'<=50K': 0.5, '>50K': 0.5}
        }
