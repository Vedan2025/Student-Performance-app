import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load files
importance = joblib.load("importance.pkl")
model = joblib.load("model.pkl")
columns = joblib.load("columns.pkl")
df = pd.read_csv("student_project.csv")

# Title
st.title("🎓 Student Performance Predictor")

# Inputs
st.markdown("## 📋 Student Inputs")

col1, col2 = st.columns(2)

with col1:
    study_hours = st.slider("Study Hours", 0.0, 10.0, 2.0)

with col2:
    attendance = st.slider("Attendance %", 0, 100, 70)

gender = st.selectbox("Gender", ["Male", "Female"])
internet = st.selectbox("Internet Access", ["Yes", "No"])
family = st.selectbox("Family Background", ["Low Income", "Middle Income", "High Income"])

st.info("👆 Enter details and click Predict to see results")

# Predict button
if st.button("Predict"):

    # 🔥 STUDENT SEGMENTATION
    if study_hours > 3 and attendance > 80:
        segment = "High Effort Student"
    elif study_hours < 2 and attendance < 60:
        segment = "Low Effort Student"
    else:
        segment = "Average Student"

    st.markdown("---")
    st.subheader("🧠 Student Type")
    st.info(f"Detected: {segment}")

    # 🔥 CONFIDENCE LEVEL
    if segment == "Average Student":
        st.success("✅ Prediction Confidence: High")
    else:
        st.warning("⚠️ Prediction Confidence: Moderate (pattern varies)")

    # Prepare input
    input_data = pd.DataFrame(0, index=[0], columns=columns)

    input_data['Study_hours'] = study_hours
    input_data['Attendance'] = attendance
    input_data['Gender_Male'] = 1 if gender == "Male" else 0
    input_data['Internet_access_Yes'] = 1 if internet == "Yes" else 0

    if 'Family Background_Low Income' in columns:
        input_data['Family Background_Low Income'] = 1 if family == "Low Income" else 0

    if 'Family Background_Middle Income' in columns:
        input_data['Family Background_Middle Income'] = 1 if family == "Middle Income" else 0

    if 'Family Background_High Income' in columns:
        input_data['Family Background_High Income'] = 1 if family == "High Income" else 0

    # Prediction
    prediction = model.predict(input_data)[0]

    # Output
    st.success(f"🎯 Predicted Marks: {round(prediction,2)}")

    # Student Category
    st.markdown("---")
    st.subheader("🎯 Student Category")

    if prediction < 40:
        st.error("🔴 At Risk Student")
    elif prediction < 70:
        st.warning("🟡 Average Student")
    else:
        st.success("🟢 Top Performer")

    # Performance Message
    if prediction < 40:
        st.error("⚠️ Student is At Risk! Needs immediate attention.")
    elif prediction < 70:
        st.warning("📊 Average performance. Can improve with effort.")
    else:
        st.success("🌟 Great performance! Keep it up!")

    # Recommendations
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

    # Final Insight
    st.markdown("---")
    st.subheader("🧠 Final Insight Summary")

    if prediction < 40:
        st.write("🔴 High risk student. Immediate intervention needed.")
    elif prediction < 70:
        st.write("🟡 Moderate performance. Improvement required.")
    else:
        st.write("🟢 Strong performance. Maintain consistency.")

    st.write("📌 Key influencing factors:")
    st.write("• Study Hours and Attendance have highest impact")

    # Dashboard
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

    # Feature Importance
    st.markdown("---")
    st.header("📊 Feature Importance")

    fig, ax = plt.subplots()
    ax.barh(importance['Feature'], importance['Importance'])
    ax.set_title("Feature Importance")
    st.pyplot(fig)
