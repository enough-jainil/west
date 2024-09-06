import streamlit as st
from pycaret.classification import load_model
import pandas as pd
import numpy as np
import os

# Update the features to match those used during model training
features = {
    'pH': float,  # Keep it as 'pH' for user input
    'Hardness': float,
    'Solids': float,
    'Chloramines': float,
    'Sulfate': float,
    'Conductivity': float,
    'Organic_carbon': float,
    'Trihalomethanes': float,
    'Turbidity': float,
}

quality = []

def app2():
    st.title('Water Potability Test Model')
    
    # Set the correct working directory
    os.chdir(r'C:\Users\jaini\Downloads\UDT')
    
    # Load the pretrained model
    model_path = os.path.join('models', 'Water_Potability', 'waterpotability_model')
    
    if not os.path.exists(model_path + '.pkl'):
        st.error(f"Model file not found at {model_path + '.pkl'}. Please check the file path.")
        return

    try:
        model = load_model(model_path)
        st.success("Model loaded successfully!")
    except Exception as e:
        st.error(f"Error loading the model: {str(e)}")
        return

    # Create input widgets for each feature
    inputs = {}
    col1, col2, col3 = st.columns(3)
    for i, (feature, feature_type) in enumerate(features.items()):
        col = col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3
        with col:
            inputs[feature] = st.number_input(f'{feature}', value=0.0, step=0.1, format='%.2f', key=feature)

    # Add two buttons aligned in the center
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button('Predict Potability'):
            data = pd.DataFrame(inputs, index=[0])
            # Rename 'pH' to 'ph' before prediction
            data = data.rename(columns={'pH': 'ph'})
            prediction = model.predict(data)
            display_prediction(prediction[0])

    with col2:
        if st.button('Random Inputs Predict'):
            # Generate random data
            random_data = {feature: np.random.uniform(0, 10) for feature in features}
            data = pd.DataFrame(random_data, index=[0])
            # Rename 'pH' to 'ph' before prediction
            data = data.rename(columns={'pH': 'ph'})
            st.write("Random Input Data:")
            st.write(data)
            prediction = model.predict(data)
            display_prediction(prediction[0])

    # Display water quality information
    st.subheader("Water Quality Information:")
    col1, col2, col3 = st.columns(3)
    for i, (feature, value) in enumerate(inputs.items()):
        col = col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3
        with col:
            st.write(f"{feature}: {value}")

def display_prediction(prediction):
    # Convert numpy int to Python int
    prediction = int(prediction)
    quality.append(prediction)
    if prediction == 0:
        st.success('The Water is fit for drinking and also for irrigation purpose')
    else:
        st.error('The Water is not fit for drinking or for irrigation purpose')

def display_prediction(prediction):
    quality.append(prediction)
    if prediction == 0:
        st.success('The Water is fit for drinking and also for irrigation purpose')
    else:
        st.error('The Water is not fit for drinking or for irrigation purpose')

if __name__ == "__main__":
    app2()