import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Student Virtual Lab", layout="centered")

# ------------------ TITLE ------------------
st.title("🧪 Student Performance Virtual Lab")
st.write("Experiment with different factors and observe how they affect student performance.")

# ------------------ INPUT CONTROLS ------------------
st.header("🎛️ Experiment Controls")

study_hours = st.slider("📚 Study Hours per Day", 0, 12, 5)
attendance = st.slider("🏫 Attendance (%)", 0, 100, 75)
sleep = st.slider("😴 Sleep Hours", 0, 10, 6)
previous_score = st.slider("📊 Previous Exam Score", 0, 100, 60)

# ------------------ PREDICTION FUNCTION ------------------
def predict_performance(study, attend, sleep, prev):
    score = (study * 4) + (attend * 0.3) + (sleep * 2) + (prev * 0.2)
    return min(score, 100)

# ------------------ RUN EXPERIMENT ------------------
if st.button("▶️ Run Experiment"):

    result = predict_performance(study_hours, attendance, sleep, previous_score)

    # ------------------ RESULT ------------------
    st.header("📊 Result")
    st.subheader(f"Predicted Score: {result:.2f}")

    if result > 75:
        st.success("🌟 Performance: Excellent")
    elif result > 50:
        st.warning("⚖️ Performance: Average")
    else:
        st.error("⚠️ Performance: At Risk")

    # ------------------ GRAPH ------------------
    st.header("📈 Experiment Visualization")

    hours = np.arange(0, 12, 1)
    scores = [predict_performance(h, attendance, sleep, previous_score) for h in hours]

    fig, ax = plt.subplots()
    ax.plot(hours, scores)
    ax.set_xlabel("Study Hours")
    ax.set_ylabel("Performance Score")
    ax.set_title("Effect of Study Hours on Performance")

    st.pyplot(fig)

    # ------------------ OBSERVATIONS ------------------
    st.header("📌 Observations & Insights")

    if study_hours < 3:
        st.write("🔻 Low study hours negatively affect performance.")

    if attendance < 50:
        st.write("🔻 Low attendance significantly reduces performance.")

    if sleep < 5:
        st.write("🔻 Lack of sleep impacts learning efficiency.")

    if result > previous_score:
        st.write("✅ Improvement observed compared to previous performance.")
    else:
        st.write("⚠️ Performance has not improved. Consider increasing study hours.")

# ------------------ COMPARE MODE ------------------
st.header("⚔️ Compare Two Students")

if st.checkbox("Enable Comparison Mode"):

    st.subheader("Student 1")
    s1_study = st.slider("Study Hours (S1)", 0, 12, 5, key="s1")
    s1_att = st.slider("Attendance (S1)", 0, 100, 70, key="s2")

    st.subheader("Student 2")
    s2_study = st.slider("Study Hours (S2)", 0, 12, 6, key="s3")
    s2_att = st.slider("Attendance (S2)", 0, 100, 80, key="s4")

    s1_score = predict_performance(s1_study, s1_att, sleep, previous_score)
    s2_score = predict_performance(s2_study, s2_att, sleep, previous_score)

    st.write(f"📊 Student 1 Score: {s1_score:.2f}")
    st.write(f"📊 Student 2 Score: {s2_score:.2f}")

# ------------------ RESET BUTTON ------------------
if st.button("🔄 Reset Experiment"):
    st.session_state.clear()
    st.rerun()
