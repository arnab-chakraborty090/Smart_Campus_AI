
import streamlit as st
import pandas as pd
import joblib

model = joblib.load("student_risk_model.pkl")

FEATURES = [
    "age",
    "studytime",
    "failures",
    "absences",
    "schoolsup",
    "famsup",
    "paid",
    "activities",
    "internet",
    "health",
    "goout",
    "freetime"
]


def generate_recommendations(student):
    recommendations = []

    if student["studytime"] <= 2:
        recommendations.append(
            "Build a regular study timetable."
        )

    if student["absences"] >= 10:
        recommendations.append(
            "Review missed lessons and discuss "
            "attendance barriers with a teacher."
        )

    if student["failures"] >= 1:
        recommendations.append(
            "Seek help with difficult topics."
        )

    if student["schoolsup"] == "no":
        recommendations.append(
            "Explore available school support."
        )

    if student["famsup"] == "no":
        recommendations.append(
            "Consider a study partner or mentor."
        )

    if student["internet"] == "no":
        recommendations.append(
            "Ask about offline learning resources."
        )

    if student["health"] <= 2:
        recommendations.append(
            "Seek appropriate support if health "
            "difficulties affect your studies."
        )

    if not recommendations:
        recommendations.append(
            "Continue regular revision and "
            "weekly progress reviews."
        )

    return recommendations


st.set_page_config(
    page_title="Smart Campus AI",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Smart Campus AI")
st.subheader("Academic Risk & Study Planner")

st.write(
    "Enter student information to estimate the "
    "likelihood of a low final grade and obtain "
    "practical study recommendations."
)

st.info(
    "This is an educational prototype, not a "
    "definitive assessment of student ability."
)

with st.form("student_form"):

    st.header("Student Information")

    age = st.number_input(
        "Age",
        min_value=15,
        max_value=22,
        value=18
    )

    studytime = st.selectbox(
        "Weekly study-time category",
        options=[1, 2, 3, 4],
        format_func=lambda x: {
            1: "1: Less than 2 hours",
            2: "2: 2 to 5 hours",
            3: "3: 5 to 10 hours",
            4: "4: More than 10 hours"
        }[x]
    )

    failures = st.number_input(
        "Previous class failures",
        min_value=0,
        max_value=4,
        value=0
    )

    absences = st.number_input(
        "Number of absences",
        min_value=0,
        max_value=100,
        value=0
    )

    schoolsup = st.selectbox(
        "Extra school support",
        ["yes", "no"]
    )

    famsup = st.selectbox(
        "Family educational support",
        ["yes", "no"]
    )

    paid = st.selectbox(
        "Extra paid classes",
        ["yes", "no"]
    )

    activities = st.selectbox(
        "Extracurricular activities",
        ["yes", "no"]
    )

    internet = st.selectbox(
        "Internet access at home",
        ["yes", "no"]
    )

    health = st.slider(
        "Self-reported health (1 to 5)",
        min_value=1,
        max_value=5,
        value=3
    )

    goout = st.slider(
        "Frequency of going out (1 to 5)",
        min_value=1,
        max_value=5,
        value=3
    )

    freetime = st.slider(
        "Free time after school (1 to 5)",
        min_value=1,
        max_value=5,
        value=3
    )

    submitted = st.form_submit_button(
        "Analyze Student"
    )


if submitted:

    student = {
        "age": age,
        "studytime": studytime,
        "failures": failures,
        "absences": absences,
        "schoolsup": schoolsup,
        "famsup": famsup,
        "paid": paid,
        "activities": activities,
        "internet": internet,
        "health": health,
        "goout": goout,
        "freetime": freetime
    }

    student_df = pd.DataFrame(
        [student],
        columns=FEATURES
    )

    prediction = int(model.predict(student_df)[0])

    probability = float(
        model.predict_proba(student_df)[0, 1]
    )

    st.divider()
    st.header("Analysis Results")

    st.metric(
        "Estimated probability of a low final grade",
        f"{probability:.1%}"
    )

    if prediction == 1:
        st.warning(
            "The model flags this profile as potentially needing additional support."
        )
    else:
        st.success(
            "The model does not currently flag this profile for additional support."
        )

    st.caption(
        "This estimate is based on historical data. "
        "It is not a guarantee of future performance."
    )

    st.subheader("Personalized Study Recommendations")

    recommendations = generate_recommendations(student)

    for item in recommendations:
        st.write("•", item)
