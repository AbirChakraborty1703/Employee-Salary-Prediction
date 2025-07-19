import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.data_prep import load_and_preprocess
from src.model import load_model, predict

# Page configuration
st.set_page_config(
    page_title="Employee Salary Predictor", 
    page_icon="💼",
    layout="wide"
)

st.title("💼 Employee Salary Predictor")
st.markdown("### Predict if an employee's salary is above or below $50K")

# Sidebar inputs
st.sidebar.header("Enter Employee Details")

# Add preset examples
st.sidebar.subheader("🚀 Quick Test Examples")
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("👔 High Income", help="CEO/Executive profile", key="high_income_btn"):
        st.session_state.use_high_income = True
        
with col2:
    if st.button("👤 Low Income", help="Entry-level profile", key="low_income_btn"):
        st.session_state.use_low_income = True

def user_input_features():
    """Create input form for user to enter employee details"""
    
    # Check for preset examples and set session state values
    if 'use_high_income' in st.session_state and st.session_state.use_high_income:
        # High income defaults
        st.session_state.age_slider = 45
        st.session_state.education_select = "Masters"
        st.session_state.occupation_select = "Exec-managerial"
        st.session_state.hours_slider = 50
        st.session_state.capital_gain_input = 15000
        st.session_state.marital_select = "Married-civ-spouse"
        st.session_state.relationship_select = "Husband"
        st.session_state.gender_select = "Male"
        st.session_state.race_select = "White"
        st.session_state.workclass_select = "Private"
        st.session_state.education_num_slider = 14
        st.session_state.capital_loss_input = 0
        st.session_state.native_country_select = "United-States"
        st.session_state.fnlwgt_input = 200000
        st.session_state.use_high_income = False
    elif 'use_low_income' in st.session_state and st.session_state.use_low_income:
        # Low income defaults
        st.session_state.age_slider = 22
        st.session_state.education_select = "HS-grad"
        st.session_state.occupation_select = "Handlers-cleaners"
        st.session_state.hours_slider = 25
        st.session_state.capital_gain_input = 0
        st.session_state.marital_select = "Never-married"
        st.session_state.relationship_select = "Own-child"
        st.session_state.gender_select = "Male"
        st.session_state.race_select = "White"
        st.session_state.workclass_select = "Private"
        st.session_state.education_num_slider = 9
        st.session_state.capital_loss_input = 0
        st.session_state.native_country_select = "United-States"
        st.session_state.fnlwgt_input = 150000
        st.session_state.use_low_income = False
    
    # Personal Information
    st.sidebar.subheader("👤 Personal Information")
    age = st.sidebar.slider("Age", 17, 90, value=st.session_state.get('age_slider', 35), key="age_slider")
    gender = st.sidebar.selectbox("Gender", ["Male", "Female"], index=0 if st.session_state.get('gender_select', 'Male') == 'Male' else 1, key="gender_select")
    race = st.sidebar.selectbox("Race", [
        "White", "Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other"
    ], index=["White", "Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other"].index(st.session_state.get('race_select', 'White')), key="race_select")
    
    # Work Information
    st.sidebar.subheader("💼 Work Information")
    workclass = st.sidebar.selectbox("Work Class", [
        "Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", 
        "Local-gov", "State-gov", "Without-pay", "Never-worked"
    ], index=["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", 
              "Local-gov", "State-gov", "Without-pay", "Never-worked"].index(st.session_state.get('workclass_select', 'Private')), key="workclass_select")
    
    occupation_list = ["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial",
                      "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical",
                      "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv",
                      "Armed-Forces"]
    occupation = st.sidebar.selectbox("Occupation", occupation_list, 
                                    index=occupation_list.index(st.session_state.get('occupation_select', 'Tech-support')), key="occupation_select")
    
    hours_per_week = st.sidebar.slider("Hours per Week", 1, 99, value=st.session_state.get('hours_slider', 40), key="hours_slider")
    
    # Education Information
    st.sidebar.subheader("🎓 Education Information")
    education_list = ["Bachelors", "HS-grad", "11th", "Masters", "9th", "Some-college",
                     "Assoc-acdm", "Assoc-voc", "7th-8th", "Doctorate", "Prof-school",
                     "5th-6th", "10th", "1st-4th", "Preschool", "12th"]
    education = st.sidebar.selectbox("Education Level", education_list,
                                   index=education_list.index(st.session_state.get('education_select', 'Bachelors')), key="education_select")
    
    education_num = st.sidebar.slider("Years of Education", 1, 16, value=st.session_state.get('education_num_slider', 13), key="education_num_slider")
    
    # Family Information
    st.sidebar.subheader("👨‍👩‍👧‍👦 Family Information")
    marital_list = ["Married-civ-spouse", "Divorced", "Never-married", "Separated", 
                   "Widowed", "Married-spouse-absent", "Married-AF-spouse"]
    marital_status = st.sidebar.selectbox("Marital Status", marital_list,
                                        index=marital_list.index(st.session_state.get('marital_select', 'Married-civ-spouse')), key="marital_select")
    
    relationship_list = ["Wife", "Own-child", "Husband", "Not-in-family", "Other-relative", "Unmarried"]
    relationship = st.sidebar.selectbox("Relationship", relationship_list,
                                      index=relationship_list.index(st.session_state.get('relationship_select', 'Husband')), key="relationship_select")
    
    # Financial Information
    st.sidebar.subheader("💰 Financial Information")
    capital_gain = st.sidebar.number_input("Capital Gain", 0, 100000, value=st.session_state.get('capital_gain_input', 0), step=100, key="capital_gain_input")
    capital_loss = st.sidebar.number_input("Capital Loss", 0, 5000, value=st.session_state.get('capital_loss_input', 0), step=50, key="capital_loss_input")
    
    # Location Information
    st.sidebar.subheader("🌍 Location Information")
    country_list = ["United-States", "Cambodia", "England", "Puerto-Rico", "Canada", "Germany",
                   "Outlying-US(Guam-USVI-etc)", "India", "Japan", "Greece", "South", "China",
                   "Cuba", "Iran", "Honduras", "Philippines", "Italy", "Poland", "Jamaica",
                   "Vietnam", "Mexico", "Portugal", "Ireland", "France", "Dominican-Republic",
                   "Laos", "Ecuador", "Taiwan", "Haiti", "Columbia", "Hungary", "Guatemala",
                   "Nicaragua", "Scotland", "Thailand", "Yugoslavia", "El-Salvador",
                   "Trinadad&Tobago", "Peru", "Hong", "Holand-Netherlands"]
    native_country = st.sidebar.selectbox("Native Country", country_list,
                                        index=country_list.index(st.session_state.get('native_country_select', 'United-States')), key="native_country_select")
    
    # Create a weight value (this is typically not user input but required for the model)
    fnlwgt = st.sidebar.number_input("Final Weight (Census)", 12285, 1484705, value=st.session_state.get('fnlwgt_input', 200000), key="fnlwgt_input")
    
    # Create input dictionary
    data = {
        "age": age,
        "workclass": workclass,
        "fnlwgt": fnlwgt,
        "education": education,
        "educational-num": education_num,  # ⚠️ FIXED: Changed from 'education-num' to 'educational-num'
        "marital-status": marital_status,
        "occupation": occupation,
        "relationship": relationship,
        "race": race,
        "gender": gender,
        "capital-gain": capital_gain,
        "capital-loss": capital_loss,
        "hours-per-week": hours_per_week,
        "native-country": native_country
    }
    
    return pd.DataFrame([data])

# Get user input
input_df = user_input_features()

# Display user input
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 User Input Parameters")
    # Display in a more readable format
    display_df = input_df.T
    display_df.columns = ['Value']
    st.write(display_df)

with col2:
    st.subheader("📊 Quick Stats")
    st.metric("Age", input_df['age'].iloc[0])
    st.metric("Hours/Week", input_df['hours-per-week'].iloc[0])
    st.metric("Education Level", input_df['educational-num'].iloc[0])
    
    # Add some prediction hints
    if input_df['educational-num'].iloc[0] >= 13 and input_df['hours-per-week'].iloc[0] >= 40:
        st.success("Higher income indicators")
    elif input_df['educational-num'].iloc[0] <= 9 and input_df['hours-per-week'].iloc[0] <= 30:
        st.info("Lower income indicators")

# Load and display sample data if requested
if st.sidebar.checkbox("Show sample data", key="show_sample_checkbox"):
    try:
        X, y = load_and_preprocess("data/adult.csv")
        st.subheader("📁 Dataset Sample")
        sample_data = pd.concat([X.head(), y.head()], axis=1)
        st.write(sample_data)
        
        # Dataset statistics
        st.subheader("📈 Dataset Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", len(X))
        with col2:
            st.metric("Features", len(X.columns))
        with col3:
            st.metric("≤50K Count", (y == "<=50K").sum())
        with col4:
            st.metric(">50K Count", (y == ">50K").sum())
            
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Load model and make prediction
try:
    # Add debug mode toggle in sidebar
    debug_mode = st.sidebar.checkbox("🐛 Debug Mode", value=False, help="Show detailed debugging information")
    st.session_state['debug_mode'] = debug_mode
    
    if debug_mode:
        # Show debugging information only when debug mode is enabled
        st.subheader("🔍 Current Input Values")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Age**: {input_df['age'].iloc[0]}")
            st.write(f"**Hours/Week**: {input_df['hours-per-week'].iloc[0]}")
            st.write(f"**Education**: {input_df['education'].iloc[0]}")
        with col2:
            st.write(f"**Education Years**: {input_df['educational-num'].iloc[0]}")
            st.write(f"**Occupation**: {input_df['occupation'].iloc[0]}")
            st.write(f"**Marital Status**: {input_df['marital-status'].iloc[0]}")
        with col3:
            st.write(f"**Capital Gain**: ${input_df['capital-gain'].iloc[0]:,}")
            st.write(f"**Workclass**: {input_df['workclass'].iloc[0]}")
            st.write(f"**Gender**: {input_df['gender'].iloc[0]}")
        
        # Show session state values in debug mode
        st.subheader("🐛 SESSION STATE DEBUG")
        st.write("**Button States:**")
        st.write(f"- use_high_income: {st.session_state.get('use_high_income', 'Not set')}")
        st.write(f"- use_low_income: {st.session_state.get('use_low_income', 'Not set')}")
        st.write("**Form Widget Values:**")
        st.write(f"- age_slider: {st.session_state.get('age_slider', 'Not set')}")
        st.write(f"- occupation_select: {st.session_state.get('occupation_select', 'Not set')}")
        st.write(f"- capital_gain_input: {st.session_state.get('capital_gain_input', 'Not set')}")
    
    # Load the trained model
    model_package = load_model("model/salary_model.pkl")
    
    # Make prediction
    result = predict(model_package, input_df)
    
    # Check if we're getting the fallback result only in debug mode
    if debug_mode and result['confidence'] == 50.0 and result['probabilities']['<=50K'] == 0.5:
        st.error("🚨 **PREDICTION ERROR DETECTED!**")
        st.error("The model is returning fallback values, which means there's an error in the prediction process.")
        st.error("Check the terminal/console for error messages.")
    
    # Display prediction results
    st.subheader("🎯 Prediction Results")
    
    # Main prediction display
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if result['prediction'] == ">50K":
            st.success(f"💰 **Predicted Salary: {result['prediction']}**")
            st.balloons()
        else:
            st.info(f" **Predicted Salary: {result['prediction']}**")
        
        st.write(f"**Confidence:** {result['confidence']:.1f}%")
    
    with col2:
        # Probability chart
        prob_data = pd.DataFrame({
            'Income Level': list(result['probabilities'].keys()),
            'Probability': list(result['probabilities'].values())
        })
        
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(prob_data['Income Level'], prob_data['Probability'], 
                     color=['lightcoral', 'lightgreen'])
        ax.set_ylabel('Probability')
        ax.set_title('Prediction Probabilities')
        ax.set_ylim(0, 1)
        
        # Add value labels on bars
        for bar, prob in zip(bars, prob_data['Probability']):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{prob:.3f}', ha='center', va='bottom')
        
        st.pyplot(fig)
    
    # Model information
    with st.expander("🔍 Model Information"):
        st.write(f"**Model Type:** {model_package.get('model_name', 'Random Forest')}")
        st.write(f"**Model Accuracy:** {model_package.get('test_accuracy', 0.86):.4f}")
        st.write(f"**Features Used:** {len(model_package['feature_columns'])}")
        if debug_mode:
            st.write("**Feature List:**")
            for i, feature in enumerate(model_package['feature_columns'], 1):
                st.write(f"{i}. {feature}")
        
        # Show advanced debug information only in debug mode
        if debug_mode:
            st.write("**Complete Input DataFrame:**")
            st.dataframe(input_df)

except FileNotFoundError as e:
    st.error("🔗 **Model Not Found**")
    st.error(str(e))
    st.info("**To fix this:**")
    st.info("1. Open the Jupyter notebook: `notebooks/Employee Salary Prediction.ipynb`")
    st.info("2. Run all cells to train and save the model")
    st.info("3. The model will be saved to `model/salary_model.pkl`")
except Exception as e:
    st.error(f"**Error loading model or making prediction:** {e}")
    if debug_mode:
        import traceback
        st.code(traceback.format_exc())

# Additional visualizations if requested
if st.sidebar.checkbox("Show data visualizations", key="show_viz_checkbox"):
    try:
        X, y = load_and_preprocess("data/adult.csv")
        
        st.subheader("📊 Data Visualizations")
        
        # Income distribution
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 5))
            y.value_counts().plot(kind='bar', ax=ax, color=['lightcoral', 'lightgreen'])
            ax.set_title('Income Distribution')
            ax.set_xlabel('Income Level')
            ax.set_ylabel('Count')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(8, 5))
            X['age'].hist(bins=30, ax=ax, alpha=0.7, color='skyblue')
            ax.set_title('Age Distribution')
            ax.set_xlabel('Age')
            ax.set_ylabel('Frequency')
            st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Error creating visualizations: {e}")

# Footer
st.markdown("---")
st.markdown("**Note:** This prediction is based on the Adult Census Income dataset and should be used for educational purposes only.")
