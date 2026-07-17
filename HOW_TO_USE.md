# How to use these files

## 1. `hospital_project.ipynb` — the graded notebook
Open in Jupyter (`jupyter notebook hospital_project.ipynb`) or upload to Google Colab.
Run all cells top to bottom. It:
- creates the `Doctors` / `Patients` / `Appointments` schema
- inserts consistent sample data (fixes the orphaned foreign keys from the original `project_hospital.sql`)
- answers every graded question (JOINs, aggregates, subqueries, `RANK()`, `COUNT() OVER (PARTITION BY ...)`)
- plots 3 charts
- writes `hospital.db` (SQLite) and CSV exports to `./exports/`

No installs needed beyond `pandas` and `matplotlib` — it uses Python's built-in `sqlite3`, so it runs
with zero setup. A commented-out MySQL connection snippet is included in Section 1 if your
grader specifically wants MySQL.

## 2. `app.py` — the deployment app
A Streamlit app that turns the project into something you can actually click through and share
a link to (good for your resume / LinkedIn / GitHub README).

```bash
pip install -r requirements.txt
streamlit run app.py
```

It self-builds `hospital.db` if it doesn't already exist, so `app.py` works standalone even without
running the notebook first.

**Free deployment:** push this folder to your `hospital_database_project` GitHub repo, then deploy at
[share.streamlit.io](https://share.streamlit.io) pointing at `app.py`. You'll get a public URL to put
in your resume/README, e.g. `https://kanakbaghel-hospital-db.streamlit.app`.

## 3. Suggested repo structure after adding these
```
hospital_database_project/
├── project_hospital.sql          (original)
├── hospital_project.ipynb        (new — full analysis)
├── app.py                        (new — deployment)
├── requirements.txt              (new)
├── Sample_doctors.csv / Sample_patients.csv / Sample_Appointments.csv
└── README.md
```
Update the README's "Getting Started" section to mention both the notebook and the live app link
once deployed — that's what makes this stand out over a plain `.sql` file on a fresher resume.
