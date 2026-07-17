# Setup

All files below go in the same folder — repo root, alongside the CSVs already there.

```
hospital_database_project/
├── project_hospital.sql          (original)
├── Sample_doctors.csv            (already in repo)
├── Sample_patients.csv           (already in repo)
├── Sample_Appointments.csv       (already in repo)
├── data_utils.py                 (new — shared load/clean/merge logic)
├── hospital_eda_ml.ipynb         (new — EDA + ML training)
├── app.py                        (new — Streamlit deployment)
└── requirements.txt              (new)
```

## Run order

```bash
pip install -r requirements.txt

# 1. Run the notebook once, top to bottom — trains the model and saves
#    hospital_model.pkl + model_features.pkl
jupyter notebook hospital_eda_ml.ipynb

# 2. Launch the deployed app (reads the CSVs + the saved model)
streamlit run app.py
```

## Deploy for free
Push the whole folder to `hospital_database_project` on GitHub (including the two `.pkl`
files created by the notebook), then deploy at [share.streamlit.io](https://share.streamlit.io)
pointing at `app.py`. You get a public URL for your resume/LinkedIn/GitHub README.

## What each new file does
- **`data_utils.py`** — the single source of truth for loading and cleaning the 3 CSVs. Both
  the notebook and `app.py` import from it, so they can never disagree on what "clean data" means.
- **`hospital_eda_ml.ipynb`** — import → data quality check → cleaning (with reasoning for every
  decision) → EDA (doctor/patient/appointment patterns) → ML (predict appointment completion,
  Logistic Regression vs Random Forest, cross-validated) → saves the model.
- **`app.py`** — Streamlit app with 4 tabs: overview metrics, EDA charts, a live prediction form
  (feed in a hypothetical patient/doctor/appointment and get a completion prediction), and the
  raw tables.
