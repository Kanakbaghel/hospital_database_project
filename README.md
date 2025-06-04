# hospital_database_project
Graded SQL Mini Project - Hospital Database using MYSQL | Data Science Course

# 🏥 Hospital Management System – SQL Project

This repository contains a graded *SQL Mini Project* developed for the *Data Science & Business Analytics Program by IIT Guwahati*.

The project simulates a real-world *hospital database* and uses *MySQL* to perform data modeling, insertions, joins, aggregations, and window functions.

---

## 📚 Overview

This project demonstrates:
- Designing relational schema for a hospital system
- Using SQL to insert, retrieve, and analyze data
- Exploring relationships between doctors, patients, and appointments

---

## 🧱 Database Schema

### 👨‍⚕ Doctors Table
| Column         | Type       |
|----------------|------------|
| doctor_id      | INT (PK)   |
| doctor_name    | VARCHAR    |
| specialization | VARCHAR    |
| experience_years | INT      |

### 🧑‍🤝‍🧑 Patients Table
| Column         | Type       |
|----------------|------------|
| patient_id     | INT (PK)   |
| patient_name   | VARCHAR    |
| age            | INT        |
| gender         | VARCHAR    |
| doctor_id      | INT (FK)   |
| contact_number | VARCHAR    |

### 📅 Appointments Table
| Column           | Type       |
|------------------|------------|
| appointment_id   | INT (PK)   |
| patient_id       | INT (FK)   |
| doctor_id        | INT (FK)   |
| appointment_date | DATETIME   |
| status           | TEXT       |

---

## 🧠 Key Concepts Used

- ✅ Table creation with constraints
- ✅ Foreign Key relationships
- ✅ SQL Joins (INNER, LEFT)
- ✅ Aggregate Functions (COUNT, AVG)
- ✅ Window Functions (RANK(), COUNT() OVER)
- ✅ Subqueries

---

## 💻 Sample Queries

🔹 Doctors with more than 5 years of experience:
```sql
SELECT p.*
FROM Patients p
JOIN Doctors d ON p.doctor_id = d.doctor_id
WHERE d.experience_years > 5;
```
🔹 Find doctors who have no patients:
```sql
SELECT d.doctor_id, d.doctor_name
FROM Doctors d
LEFT JOIN Patients p ON d.doctor_id = p.doctor_id
WHERE p.patient_id IS NULL;
```
🔹 Rank doctors by experience:
```sql
SELECT doctor_id, doctor_name, experience_years,
RANK() OVER(ORDER BY experience_years DESC) AS experience_rank
FROM Doctors;
```

---

👩‍💻 Developed by

Kanak Baghel
📫 kanak.bgl704@gmail.com
🔗 GitHub Profile

