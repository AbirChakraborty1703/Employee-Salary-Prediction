import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def encode_categorical_features(df, categorical_columns, label_encoders=None):
    """
    Encode categorical features using LabelEncoder.
    
    Args:
        df: DataFrame with categorical features
        categorical_columns: List of categorical column names
        label_encoders: Dict of pre-fitted encoders (for prediction)
    
    Returns:
        Encoded DataFrame and label encoders dict
    """
    df_encoded = df.copy()
    
    if label_encoders is None:
        label_encoders = {}
        # Fit new encoders
        for col in categorical_columns:
            if col in df_encoded.columns:
                le = LabelEncoder()
                df_encoded[col] = le.fit_transform(df_encoded[col])
                label_encoders[col] = le
    else:
        # Use existing encoders
        for col in categorical_columns:
            if col in df_encoded.columns and col in label_encoders:
                try:
                    df_encoded[col] = label_encoders[col].transform(df_encoded[col])
                except ValueError:
                    # Handle unseen categories
                    df_encoded[col] = 0
    
    return df_encoded, label_encoders

def scale_numerical_features(X_train, X_test=None, numerical_features=None, scaler=None):
    """
    Scale numerical features using StandardScaler.
    
    Args:
        X_train: Training data
        X_test: Test data (optional)
        numerical_features: List of numerical column names
        scaler: Pre-fitted scaler (for prediction)
    
    Returns:
        Scaled data and fitted scaler
    """
    if numerical_features is None:
        numerical_features = ['age', 'fnlwgt', 'educational-num', 'capital-gain', 
                             'capital-loss', 'hours-per-week']
    
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy() if X_test is not None else None
    
    if scaler is None:
        scaler = StandardScaler()
        X_train_scaled[numerical_features] = scaler.fit_transform(X_train[numerical_features])
    else:
        X_train_scaled[numerical_features] = scaler.transform(X_train[numerical_features])
    
    if X_test is not None:
        X_test_scaled[numerical_features] = scaler.transform(X_test[numerical_features])
        return X_train_scaled, X_test_scaled, scaler
    
    return X_train_scaled, scaler

def create_feature_mappings():
    """
    Create mappings for categorical features in the Adult dataset.
    """
    return {
        'workclass': [
            'Private', 'Self-emp-not-inc', 'Self-emp-inc', 'Federal-gov',
            'Local-gov', 'State-gov', 'Without-pay', 'Never-worked'
        ],
        'education': [
            'Bachelors', 'HS-grad', '11th', 'Masters', '9th', 'Some-college',
            'Assoc-acdm', 'Assoc-voc', '7th-8th', 'Doctorate', 'Prof-school',
            '5th-6th', '10th', '1st-4th', 'Preschool', '12th'
        ],
        'marital-status': [
            'Married-civ-spouse', 'Divorced', 'Never-married', 'Separated',
            'Widowed', 'Married-spouse-absent', 'Married-AF-spouse'
        ],
        'occupation': [
            'Tech-support', 'Craft-repair', 'Other-service', 'Sales', 'Exec-managerial',
            'Prof-specialty', 'Handlers-cleaners', 'Machine-op-inspct', 'Adm-clerical',
            'Farming-fishing', 'Transport-moving', 'Priv-house-serv', 'Protective-serv',
            'Armed-Forces'
        ],
        'relationship': [
            'Husband', 'Not-in-family', 'Wife', 'Own-child', 'Unmarried', 'Other-relative'
        ],
        'race': [
            'White', 'Black', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other'
        ],
        'gender': ['Male', 'Female'],
        'native-country': [
            'United-States', 'Cambodia', 'England', 'Puerto-Rico', 'Canada', 'Germany',
            'Outlying-US(Guam-USVI-etc)', 'India', 'Japan', 'Greece', 'South', 'China',
            'Cuba', 'Iran', 'Honduras', 'Philippines', 'Italy', 'Poland', 'Jamaica',
            'Vietnam', 'Mexico', 'Portugal', 'Ireland', 'France', 'Dominican-Republic',
            'Laos', 'Ecuador', 'Taiwan', 'Haiti', 'Columbia', 'Hungary', 'Guatemala',
            'Nicaragua', 'Scotland', 'Thailand', 'Yugoslavia', 'El-Salvador',
            'Trinadad&Tobago', 'Peru', 'Hong', 'Holand-Netherlands'
        ]
    }
