<p align="center">
  <img src="https://img.shields.io/badge/SQL-MySQL-blue?logo=mysql&logoColor=white" alt="MySQL Badge" />
  <img src="https://img.shields.io/badge/Status-Completed-success" alt="Completed Badge" />
  <img src="https://img.shields.io/badge/Lines%20of%20SQL-200+-informational" alt="LOC Badge" />
</p>

<h1 align="center">🏥 Hospital Management System – SQL Mini Project</h1>
<p align="center"><em>Graded assignment for the Data Science &amp; Business Analytics Program by IIT Guwahati</em></p>

---

## 🎯 Project Overview

This repository simulates a real-world hospital database using MySQL.  
You'll find:

- ✍️ A normalized **relational schema**  
- 🔄 Sample **data insertions & updates**  
- 🔗 Complex **JOINs** & **subqueries**  
- 📊 Aggregations & **window functions**  

---

## 📑 Table of Contents

1. [Schema Design](#schema-design)  
2. [Key Concepts](#key-concepts)  
3. [Sample Queries](#sample-queries)  
4. [Getting Started](#getting-started)  

---

## 🏗️ Schema Design

<details>
  <summary>👨‍⚕️ Doctors <code>Doctors(doctor_id, doctor_name, specialization, experience_years)</code></summary>

| Column            | Type       | 
|-------------------|------------|
| doctor_id         | INT        |
| doctor_name       | VARCHAR(50)|
| specialization    | VARCHAR(50)|      
| experience_years  | INT        |      
</details>

<details>
  <summary>🧑‍🤝‍🧑 Patients <code>Patients(patient_id, patient_name, age, gender, doctor_id, contact)</code></summary>

| Column          | Type         | 
|-----------------|--------------|
| patient_id      | INT          |
| patient_name    | VARCHAR(50)  |
| age             | INT          |
| gender          | ENUM('M','F')|
| doctor_id       | INT          |
| contact         | VARCHAR(15)  |
</details>

<details>
  <summary>📆 Appointments <code>Appointments(appointment_id, patient_id, doctor_id, date_time, status)</code></summary>

| Column           | Type       | 
|------------------|------------|
| appointment_id   | INT(PK)        |
| patient_id       | INT(FK)        | 
| doctor_id        | INT(FK)        | 
| date_time        | DATETIME   |     
| status           | ENUM('scheduled','completed','cancelled') | 
</details>

---

## 🧠 Key Concepts Used

- 🔹 **Table Creation** with PRIMARY & FOREIGN KEY constraints  
- 🔹 **INSERT/UPDATE/DELETE** operations  
- 🔹 **INNER & LEFT JOINs** to combine tables  
- 🔹 **Aggregate Functions**: `COUNT()`, `AVG()`  
- 🔹 **Window Functions**: `RANK() OVER`, `COUNT() OVER`  
- 🔹 **Subqueries** for nested filtering  

---

## 💻 Sample Queries

> **Doctors with >5 years of experience**  
```sql
SELECT d.doctor_id, d.doctor_name, d.experience_years
FROM Doctors d
WHERE d.experience_years > 5;
```

> **Doctors without patients**  
```sql
SELECT d.doctor_id, d.doctor_name
FROM Doctors d
LEFT JOIN Patients p 
  ON d.doctor_id = p.doctor_id
WHERE p.patient_id IS NULL;
```

> **Rank doctors by experience**  
```sql
SELECT 
  doctor_id, 
  doctor_name, 
  experience_years,
  RANK() OVER (ORDER BY experience_years DESC) AS experience_rank
FROM Doctors;
```
---

<p align="center">
  <em>Built with ❤️ by Kanak Baghel | <a href="https://www.linkedin.com/in/kanakbaghel">LinkedIn</a></em>
</p>
