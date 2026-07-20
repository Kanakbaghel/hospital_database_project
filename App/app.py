import os
import joblib
import pandas as pd
import streamlit as st
from App.data_utils import load_clean_master

st.set_page_config(page_title="Hospital Project", page_icon="🏥", layout="wide")

# Update this path if your single pkl file has a different name
MODEL_PATH = "hospital_model.pkl" 

@st.cache_data
def get_data():
    return load_clean_master()

@st.cache_resource
def get_model():
    if not os.path.exists(MODEL_PATH):
        return None
    
    # Load the single consolidated pickle file
    model_data = joblib.load(MODEL_PATH)
    
    # If your single pkl is a dictionary containing both the model and features:
    if isinstance(model_data, dict):
        return model_data.get("model"), model_data.get("features")
    
    # If your single pkl is just the trained model/pipeline itself:
    return model_data, None

doctors, patients, appointments, master = get_data()
model, feature_cols = get_model()

st.title("🏥 Hospital Project — EDA & Appointment Prediction")
st.caption("Kanak Baghel · IIT Guwahati DSBA · [GitHub repo](https://github.com/Kanakbaghel/hospital_database_project)")

tab_overview, tab_eda, tab_predict, tab_data = st.tabs(
    ["📋 Overview", "📊 EDA", "🔮 Predict Appointment Outcome", "🗂️ Raw Tables"]
)

# ---------------------------------------------------------------------------
with tab_overview:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Doctors", len(doctors))
    c2.metric("Patients", len(patients))
    c3.metric("Appointments", len(appointments))
    completion_rate = (appointments["status"] == "Completed").mean()
    c4.metric("Completion rate", f"{completion_rate:.0%}")
    
    st.markdown("""
    This app deploys the pipeline built in `hospital_eda_ml.ipynb`: the same three CSVs from the repo → cleaned → explored → used to train a model that predicts whether a booked appointment will be **Completed** or stay **Pending**.
    """)

# ---------------------------------------------------------------------------
with tab_eda:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Doctors by specialization")
        st.bar_chart(doctors["specialization"].value_counts())
    with col2:
        st.subheader("Patient age distribution")
        st.bar_chart(patients["age"].value_counts().sort_index())
        
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Appointment status breakdown")
        st.bar_chart(appointments["status"].value_counts())
    with col4:
        st.subheader("Appointments per month")
        monthly = appointments.groupby(appointments["appointment_date"].dt.to_period("M")).size()
        monthly.index = monthly.index.astype(str)
        st.line_chart(monthly)
        
    st.subheader("Doctor workload (appointments handled)")
    workload = (master.groupby(["doctor_name", "specialization", "experience_years"])
                .size()
                .reset_index(name="appointment_count")
                .sort_values("appointment_count", ascending=False))
    st.dataframe(workload, use_container_width=True, hide_index=True)
    
    st.subheader("Completion rate by specialization")
    comp_rate = (master[master["status"] != "Unknown"]
                 .groupby("specialization")["status"]
                 .apply(lambda s: (s == "Completed").mean())
                 .sort_values(ascending=False))
    st.bar_chart(comp_rate)

# ---------------------------------------------------------------------------
with tab_predict:
    st.subheader("Predict whether a new appointment will be completed")
    if model is None:
        st.warning("No trained model found yet. Ensure your single `.pkl` file is generated and placed in the correct path.")
    else:
        st.caption("This uses the Random Forest pipeline trained in the notebook.")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.slider("Patient age", 18, 90, 40)
            gender = st.selectbox("Patient gender", sorted(patients["gender"].dropna().unique()))
            specialization = st.selectbox("Doctor specialization", sorted(doctors["specialization"].unique()))
        with col2:
            experience_years = st.slider("Doctor's experience (years)", 1, 25, 10)
            appointment_month = st.selectbox("Appointment month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
            appointment_weekday = st.selectbox("Appointment weekday", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            
        if st.button("Predict"):
            input_dict = {
                "age": age,
                "gender": gender,
                "specialization": specialization,
                "experience_years": experience_years,
                "appointment_month": appointment_month,
                "appointment_weekday": appointment_weekday,
            }
            
            # Create DataFrame
            input_df = pd.DataFrame([input_dict])
            
            # Reorder columns ONLY if specific features list was saved, otherwise use input order
            if feature_cols is not None:
                input_df = input_df[feature_cols]
                
            pred = model.predict(input_df)[0]
            proba = model.predict_proba(input_df)[0][1]
            
            if pred == 1:
                st.success(f"Likely **Completed** — model confidence {proba:.0%}")
            else:
                st.warning(f"Likely to stay **Pending** — model confidence {1 - proba:.0%}")
                
            st.caption("This is a small-sample demo model — treat the probability as illustrative.")

# ---------------------------------------------------------------------------
with tab_data:
    st.subheader("Doctors")
    st.dataframe(doctors, use_container_width=True, hide_index=True)
    st.subheader("Patients")
    st.dataframe(patients, use_container_width=True, hide_index=True)
    st.subheader("Appointments")
    st.dataframe(appointments, use_container_width=True, hide_index=True)
