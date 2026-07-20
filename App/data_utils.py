"""
data_utils.py
--------------
Shared load + clean + merge logic for the Hospital project.
Used by both hospital_eda_ml.ipynb (analysis/training) and app.py (deployment),
so the two never drift out of sync.

Expects Sample_doctors.csv, Sample_patients.csv, Sample_Appointments.csv to sit
in the same folder as this file (that's how they are in the GitHub repo).
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DOCTORS_CSV = os.path.join(BASE_DIR, "Sample_doctors.csv")
PATIENTS_CSV = os.path.join(BASE_DIR, "Sample_patients.csv")
APPOINTMENTS_CSV = os.path.join(BASE_DIR, "Sample_Appointments.csv")

NA_VALUES = ["NULL", "null", "NaN", ""]


def load_raw():
    """Load the three CSVs exactly as they are in the repo, treating the literal
    string 'NULL' (present in the source files) as a real missing value."""
    doctors = pd.read_csv(DOCTORS_CSV, na_values=NA_VALUES)
    patients = pd.read_csv(PATIENTS_CSV, na_values=NA_VALUES)
    appointments = pd.read_csv(APPOINTMENTS_CSV, na_values=NA_VALUES)
    return doctors, patients, appointments


def clean(doctors: pd.DataFrame, patients: pd.DataFrame, appointments: pd.DataFrame):
    """Clean each table. Every decision is explicit and non-destructive where possible
    (we add flag columns instead of silently dropping data, except where a row can't
    be used for modeling)."""
    doctors = doctors.copy()
    patients = patients.copy()
    appointments = appointments.copy()

    # --- Doctors ---
    # 2 doctors (Dr. Alice, Dr. Mary) have missing experience_years.
    # Impute with the median experience across doctors, and flag it so the
    # imputation is transparent rather than hidden.
    doctors["experience_years_missing"] = doctors["experience_years"].isna()
    median_exp = doctors["experience_years"].median()
    doctors["experience_years"] = doctors["experience_years"].fillna(median_exp)

    # --- Patients ---
    # 1 patient (Jane Roe) has no doctor_id assigned yet -> keep as "Unassigned"
    patients["doctor_id"] = patients["doctor_id"]  # keep NaN, handled at merge time
    patients["contact_number"] = patients["contact_number"].fillna("Not Provided")

    # --- Appointments ---
    # status has one literal 'NULL' row (appointment_id 3) -> mark as 'Unknown'
    appointments["status"] = appointments["status"].fillna("Unknown")
    appointments["appointment_date"] = pd.to_datetime(appointments["appointment_date"])
    appointments["appointment_month"] = appointments["appointment_date"].dt.month_name()
    appointments["appointment_weekday"] = appointments["appointment_date"].dt.day_name()

    return doctors, patients, appointments


def build_master_table(doctors: pd.DataFrame, patients: pd.DataFrame, appointments: pd.DataFrame) -> pd.DataFrame:
    """One flat analytical table: every appointment enriched with patient + doctor info."""
    df = appointments.merge(patients, on="patient_id", how="left", suffixes=("", "_patient"))
    df = df.merge(doctors, on="doctor_id", how="left", suffixes=("", "_doctor"))
    return df


def load_clean_master():
    """Convenience one-call entry point used by app.py."""
    doctors, patients, appointments = load_raw()
    doctors, patients, appointments = clean(doctors, patients, appointments)
    master = build_master_table(doctors, patients, appointments)
    return doctors, patients, appointments, master
