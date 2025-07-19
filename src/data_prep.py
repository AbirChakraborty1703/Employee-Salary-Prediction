import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import LabelEncoder, StandardScaler

@st.cache_data
def load_and_preprocess(path: str):
    """
    Reads the Adult CSV dataset, preprocesses it, and returns feature matrix X and target y.
    This matches the preprocessing done in the Jupyter notebook.
    """
    # Load the dataset
    df = pd.read_csv(path)
    
    # Handle missing values (replace '?' with NaN and fill with mode)
    df_clean = df.replace('?', np.nan)
    
    # Define categorical columns (same as in notebook)
    categorical_columns = ['workclass', 'education', 'marital-status', 'occupation', 
                          'relationship', 'race', 'gender', 'native-country']
    
    # Fill missing values with mode for categorical variables
    for col in categorical_columns:
        if col in df_clean.columns and df_clean[col].isnull().sum() > 0:
            mode_value = df_clean[col].mode()[0]
            df_clean[col].fillna(mode_value, inplace=True)
    
    # Separate features and target
    X = df_clean.drop(['income'], axis=1)
    y = df_clean['income']
    
    return X, y

def preprocess_input_for_prediction(input_data, label_encoders, scaler, numerical_features):
    """
    Preprocesses user input data for prediction using saved encoders and scaler.
    
    Args:
        input_data (pd.DataFrame): Raw input data from user
        label_encoders (dict): Dictionary of fitted label encoders
        scaler: Fitted scaler for numerical features
        numerical_features (list): List of numerical feature names
    
    Returns:
        pd.DataFrame: Preprocessed data ready for prediction
    """
    # Create a copy of input data
    processed_data = input_data.copy()
    
    # Apply label encoders to categorical columns
    for col, encoder in label_encoders.items():
        if col in processed_data.columns:
            try:
                processed_data[col] = encoder.transform(processed_data[col])
            except ValueError:
                # Handle unseen categories by using the first category
                processed_data[col] = 0
    
    # Apply scaler to numerical features
    if numerical_features:
        processed_data[numerical_features] = scaler.transform(processed_data[numerical_features])
    
    return processed_data
