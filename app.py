import streamlit as st
import pandas as pd
import numpy as np
import joblib

model = joblib.load("model.pkl")
columns = joblib.load("columns.pkl")
df = pd.read_csv("student_project.csv")
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
        st.markdown("---")

    prediction = model.predict(input_data)[0]

    st.success(f"Predicted Marks: {round(prediction,2)}")
   # Performance Message
if prediction < 40:
    st.error("⚠️ Student is At Risk! Needs immediate attention.")
elif prediction < 70:
    st.warning("📊 Average performance. Can improve with effort.")
else:
    st.success("🌟 Great performance! Keep it up!")

# Smart Recommendations
st.subheader("📌 Recommendations")

if study_hours < 2:
    st.write("👉 Increase study time to at least 2–3 hours daily.")

if attendance < 75:
    st.write("👉 Improve attendance to above 75%.")

if internet == "No":
    st.write("👉 Access to internet can significantly improve learning.")

if family == "Low Income":
    st.write("👉 Seek academic support programs or scholarships.")

if prediction > 70:
    st.write("👉 Maintain consistency and keep practicing!")
st.markdown("---")
st.header("📊 Data Insights Dashboard")

import matplotlib.pyplot as plt
import seaborn as sns

fig1, ax1 = plt.subplots()
sns.histplot(df['Marks'], bins=10, ax=ax1)
ax1.set_title("Marks Distribution")
st.pyplot(fig1)
fig2, ax2 = plt.subplots()
sns.scatterplot(x=df['Study_hours'], y=df['Marks'], ax=ax2)
ax2.set_title("Study Hours vs Marks")
st.pyplot(fig2)
fig3, ax3 = plt.subplots()
sns.heatmap(df[['Study_hours','Attendance','Marks']].corr(), annot=True, ax=ax3)
ax3.set_title("Correlation Heatmap")
st.pyplot(fig3)
