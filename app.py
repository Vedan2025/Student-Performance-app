import streamlit as st
import pandas as pd
import numpy as np
import joblib

model = joblib.load("model.pkl")
columns = joblib.load("columns.pkl")
# Title
st.title("🎓 Student Performance Predictor")

# Inputs
study_hours = st.slider("Study Hours", 0.0, 10.0, 2.0)
attendance = st.slider("Attendance %", 0, 100, 70)
gender = st.selectbox("Gender", ["Male", "Female"])
internet = st.selectbox("Internet Access", ["Yes", "No"])
family = st.selectbox("Family Background", ["Low Income", "Middle Income", "High Income"])

# Convert input to model format
gender_male = 1 if gender == "Male" else 0
internet_yes = 1 if internet == "Yes" else 0

low = 1 if family == "Low Income" else 0
middle = 1 if family == "Middle Income" else 0
high = 1 if family == "High Income" else 0

if st.button("Predict"):

    input_data = pd.DataFrame(0, index=[0], columns=columns)

    input_data['Study_hours'] = study_hours
    input_data['Attendance'] = attendance
    input_data['Gender_Male'] = gender_male
    input_data['Internet_access_Yes'] = internet_yes

    if 'Family Background_Low Income' in columns:
        input_data['Family Background_Low Income'] = 1 if family == "Low Income" else 0

    if 'Family Background_Middle Income' in columns:
        input_data['Family Background_Middle Income'] = 1 if family == "Middle Income" else 0

    if 'Family Background_High Income' in columns:
        input_data['Family Background_High Income'] = 1 if family == "High Income" else 0

    prediction = model.predict(input_data)[0]

    st.success(f"Predicted Marks: {round(prediction,2)}")
    # Predict
    prediction = model.predict(input_data)[0]

    # Show result
    st.success(f"Predicted Marks: {round(prediction,2)}")