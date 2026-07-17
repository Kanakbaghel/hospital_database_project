"""
Hospital Management System — Deployment App
--------------------------------------------
Streamlit front-end for the Hospital SQL Mini Project (IIT Guwahati DSBA).

Run locally:
    pip install -r requirements.txt
    streamlit run app.py

Deploy free on Streamlit Community Cloud:
    1. Push this repo (app.py, requirements.txt, hospital_project.ipynb) to GitHub.
    2. Go to share.streamlit.io -> "New app" -> point it at app.py.
    3. Done — you get a shareable public URL for your resume / LinkedIn.

If hospital.db doesn't exist yet (e.g. first deploy), this script builds it
automatically from the same schema/data used in the notebook, so the app
never depends on you having run the notebook first.
"""

import os
import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "hospital.db"

st.set_page_config(page_title="Hospital SQL Mini Project", page_icon="🏥", layout="wide")


# ---------------------------------------------------------------------------
# Database bootstrap (self-healing: builds the DB if it isn't there yet)
# ---------------------------------------------------------------------------
def build_database(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript("""
    DROP TABLE IF EXISTS Appointments;
    DROP TABLE IF EXISTS Patients;
    DROP TABLE IF EXISTS Doctors;

    CREATE TABLE Doctors (
        doctor_id         INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_name       VARCHAR(100) NOT NULL,
        specialization    VARCHAR(100) NOT NULL,
        experience_years  INTEGER NOT NULL
    );

    CREATE TABLE Patients (
        patient_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name    VARCHAR(100) NOT NULL,
        age             INTEGER NOT NULL,
        gender          VARCHAR(10) NOT NULL,
        doctor_id       INTEGER,
        contact_number  VARCHAR(20),
        FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
    );

    CREATE TABLE Appointments (
        appointment_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id         INTEGER,
        doctor_id          INTEGER,
        appointment_date   DATETIME NOT NULL,
        status             VARCHAR(20) NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
        FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
    );
    """)

    doctors = [
        ('Dr. Jessica Fernandes', 'Pathology', 5),
        ('Dr. Karen Mehta', 'Gastroenterology', 8),
        ('Dr. Brian Dsouza', 'Endocrinology', 4),
        ('Dr. George Thomas', 'Nephrology', 6),
        ('Dr. Amanda Rao', 'Psychiatry', 9),
        ('Dr. Nikhil Sharma', 'Cardiology', 12),
        ('Dr. Priya Nair', 'Orthopedics', 15),
        ('Dr. Sameer Khan', 'Dermatology', 3),
        ('Dr. Anita Verma', 'Pediatrics', 11),
        ('Dr. Rahul Gupta', 'Neurology', 2),
    ]
    cur.executemany(
        "INSERT INTO Doctors (doctor_name, specialization, experience_years) VALUES (?,?,?)",
        doctors,
    )

    patients = [
        ('Jada Pinkett', 53, 'Female', 1, '9601234567'),
        ('Rita Ora', 33, 'Female', 2, '9612345678'),
        ('Ryan Gosling', 42, 'Male', 6, '9623456789'),
        ('Emma Stone', 36, 'Female', 7, '9634567890'),
        ('Rachel McAdams', 47, 'Female', 9, '9645678901'),
        ('Tom Holland', 29, 'Male', 6, '9656789012'),
        ('Zendaya Coleman', 27, 'Female', 7, '9667890123'),
        ('Chris Evans', 44, 'Male', 4, '9678901234'),
        ('Ana de Armas', 37, 'Female', 5, '9689012345'),
        ('John Cho', 51, 'Male', 9, '9690123456'),
        ('Priyanka Chopra', 42, 'Female', 2, '9701234567'),
        ('Dev Patel', 34, 'Male', 6, '9712345678'),
    ]
    cur.executemany(
        "INSERT INTO Patients (patient_name, age, gender, doctor_id, contact_number) VALUES (?,?,?,?,?)",
        patients,
    )

    appointments = [
        (1, 1, '2025-03-01 10:00', 'Completed'),
        (2, 2, '2025-03-02 11:30', 'Completed'),
        (3, 6, '2025-03-03 09:00', 'Pending'),
        (4, 7, '2025-03-04 15:00', 'Completed'),
        (5, 9, '2025-03-04 16:00', 'Cancelled'),
        (6, 6, '2025-03-05 10:30', 'Pending'),
        (7, 7, '2025-03-05 12:00', 'Completed'),
        (8, 4, '2025-03-06 09:30', 'Pending'),
        (9, 5, '2025-03-06 14:00', 'Completed'),
        (10, 9, '2025-03-07 11:00', 'Pending'),
        (3, 6, '2025-03-10 10:00', 'Completed'),
        (11, 2, '2025-03-11 13:00', 'Completed'),
        (12, 6, '2025-03-12 09:00', 'Pending'),
        (1, 1, '2025-03-15 10:00', 'Completed'),
        (7, 7, '2025-03-18 15:30', 'Cancelled'),
    ]
    cur.executemany(
        "INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status) VALUES (?,?,?,?)",
        appointments,
    )
    conn.commit()
    conn.close()


@st.cache_resource
def get_connection() -> sqlite3.Connection:
    if not os.path.exists(DB_PATH):
        build_database(DB_PATH)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def run_query(sql: str) -> pd.DataFrame:
    return pd.read_sql_query(sql, get_connection())


# ---------------------------------------------------------------------------
# Predefined graded queries (same ones answered in the notebook)
# ---------------------------------------------------------------------------
QUERIES = {
    "Q1: Patients treated by doctors with > 5 yrs experience": """
        SELECT p.patient_id, p.patient_name, d.doctor_name, d.specialization, d.experience_years
        FROM Patients p
        JOIN Doctors d ON p.doctor_id = d.doctor_id
        WHERE d.experience_years > 5
        ORDER BY d.experience_years DESC;
    """,
    "Q2: Senior doctors (> 10 yrs experience)": """
        SELECT doctor_id, doctor_name, specialization, experience_years
        FROM Doctors
        WHERE experience_years > 10
        ORDER BY experience_years DESC;
    """,
    "Q3: Doctors with no patients assigned": """
        SELECT d.doctor_id, d.doctor_name, d.specialization
        FROM Doctors d
        LEFT JOIN Patients p ON d.doctor_id = p.doctor_id
        WHERE p.patient_id IS NULL;
    """,
    "Q4: Appointments handled per doctor": """
        SELECT d.doctor_id, d.doctor_name, COUNT(a.appointment_id) AS appointment_count
        FROM Doctors d
        LEFT JOIN Appointments a ON d.doctor_id = a.doctor_id
        GROUP BY d.doctor_id, d.doctor_name
        ORDER BY appointment_count DESC;
    """,
    "Q5a: Unique patients with at least one appointment": """
        SELECT COUNT(DISTINCT patient_id) AS unique_patients_with_appointments
        FROM Appointments;
    """,
    "Q5b: Average patient age per doctor": """
        SELECT d.doctor_id, d.doctor_name, ROUND(AVG(p.age), 1) AS avg_patient_age
        FROM Doctors d
        JOIN Patients p ON d.doctor_id = p.doctor_id
        GROUP BY d.doctor_id, d.doctor_name
        ORDER BY avg_patient_age DESC;
    """,
    "Q5c: Doctors ranked by experience (window function)": """
        SELECT doctor_id, doctor_name, experience_years,
               RANK() OVER (ORDER BY experience_years DESC) AS experience_rank
        FROM Doctors;
    """,
    "Q5d: Appointments happening on the same day (window function)": """
        SELECT appointment_id, appointment_date,
               COUNT(*) OVER (PARTITION BY DATE(appointment_date)) AS appointments_on_same_day
        FROM Appointments
        ORDER BY appointment_date;
    """,
    "Q5e: Full doctor -> patient roster (LEFT JOIN)": """
        SELECT d.doctor_id, d.doctor_name, d.specialization, d.experience_years,
               p.patient_id, p.patient_name, p.age, p.gender, p.contact_number
        FROM Doctors d
        LEFT JOIN Patients p ON d.doctor_id = p.doctor_id
        ORDER BY d.doctor_id;
    """,
    "Bonus: Patients under doctors with above-average experience (subquery)": """
        SELECT p.patient_name, d.doctor_name, d.experience_years
        FROM Patients p
        JOIN Doctors d ON p.doctor_id = d.doctor_id
        WHERE d.experience_years > (SELECT AVG(experience_years) FROM Doctors)
        ORDER BY d.experience_years DESC;
    """,
}


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
st.title("🏥 Hospital Management System — SQL Mini Project")
st.caption(
    "IIT Guwahati DSBA Graded Project · Kanak Baghel · "
    "[GitHub repo](https://github.com/Kanakbaghel/hospital_database_project)"
)

tab_overview, tab_queries, tab_custom, tab_charts = st.tabs(
    ["📋 Overview", "📊 Graded Queries", "🧠 Custom SQL", "📈 Charts"]
)

with tab_overview:
    st.subheader("Schema")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Doctors**")
        st.dataframe(run_query("SELECT * FROM Doctors;"), use_container_width=True, hide_index=True)
    with col2:
        st.markdown("**Patients**")
        st.dataframe(run_query("SELECT * FROM Patients;"), use_container_width=True, hide_index=True)
    with col3:
        st.markdown("**Appointments**")
        st.dataframe(run_query("SELECT * FROM Appointments;"), use_container_width=True, hide_index=True)

with tab_queries:
    st.subheader("Run a graded query")
    choice = st.selectbox("Pick a question", list(QUERIES.keys()))
    sql = QUERIES[choice]
    with st.expander("Show SQL"):
        st.code(sql.strip(), language="sql")
    result = run_query(sql)
    st.dataframe(result, use_container_width=True, hide_index=True)
    st.download_button(
        "Download result as CSV",
        result.to_csv(index=False).encode("utf-8"),
        file_name="query_result.csv",
        mime="text/csv",
    )

with tab_custom:
    st.subheader("Write your own SELECT query")
    st.caption("Read-only sandbox — only SELECT statements are allowed against Doctors, Patients, and Appointments.")
    default_sql = "SELECT * FROM Doctors WHERE experience_years > 5;"
    user_sql = st.text_area("SQL", value=default_sql, height=120)
    if st.button("Run query"):
        cleaned = user_sql.strip().rstrip(";")
        if not cleaned.lower().startswith("select"):
            st.error("Only SELECT statements are allowed in this sandbox.")
        else:
            try:
                st.dataframe(run_query(cleaned), use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"Query failed: {e}")

with tab_charts:
    st.subheader("Doctors ranked by experience")
    exp_df = run_query("SELECT doctor_name, experience_years FROM Doctors ORDER BY experience_years DESC;")
    st.bar_chart(exp_df.set_index("doctor_name"))

    st.subheader("Appointments handled per doctor")
    appt_df = run_query("""
        SELECT d.doctor_name, COUNT(a.appointment_id) AS appointment_count
        FROM Doctors d LEFT JOIN Appointments a ON d.doctor_id = a.doctor_id
        GROUP BY d.doctor_name
        ORDER BY appointment_count DESC;
    """)
    st.bar_chart(appt_df.set_index("doctor_name"))

    st.subheader("Appointment status breakdown")
    status_df = run_query("SELECT status, COUNT(*) AS n FROM Appointments GROUP BY status;")
    st.dataframe(status_df, use_container_width=True, hide_index=True)
    st.bar_chart(status_df.set_index("status"))
