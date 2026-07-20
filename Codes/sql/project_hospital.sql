CREATE DATABASE hospital_db;
USE hospital_db;
CREATE TABLE Doctors (
doctor_id INT Auto_increment PRIMARY KEY,
doctor_name VARCHAR(100),
specialization VARCHAR(100),
experience_years INT);
SELECT * FROM Doctors;
INSERT INTO Doctors (doctor_name, specialization, experience_years)
VALUES
('Dr. Jessica', 'Pathology', 5),  
('Dr. Karen', 'Gastroenterology', 8), 
('Dr. Brian', 'Endocrinology', 4),  
('Dr. George', 'Nephrology', 6),  
('Dr. Amanda', 'Psychiatry', 9);
CREATE TABLE Patients (
patient_id INT PRIMARY KEY auto_increment,
patient_name VARCHAR(100),
age INT,
gender VARCHAR(10),
doctor_id INT,
contact_number VARCHAR(20),
FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id));
drop table if exists Patients;
SELECT * FROM Patients;
INSERT INTO Patients (patient_name, age, gender, doctor_id, contact_number)
VALUES
('Jada Pinkett Smith', 53, 'Female', 16, '9601234567'), 
('Rita Ora', 33, 'Female', 17, '9612345678'),  
('Ryan Gosling', 42, 'Male', 18, '9623456789'),  
('Emma Stone', 36, 'Female', 19, '9634567890'),  
('Rachel McAdams', 47, 'Female', 20, '9645678901');
CREATE TABLE Appointments (
appointment_id INT PRIMARY KEY auto_increment,
patient_id INT,
doctor_id INT,
appointment_date DATETIME,
status TEXT,
FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id));
SELECT * FROM Appointments;
INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status)
VALUES
(37, 15, '2025-03-07', 'Pending'),   
(38, 16, '2025-03-08', 'Completed'),  
(39, 17, '2025-03-09', 'Pending'),  
(40, 18, '2025-03-10', 'Completed'), 
(41, 19, '2025-03-11', 'Pending');
-- QUESTION 1
SELECT p.*
FROM Patients p
JOIN Doctors d ON p.doctor_id = d.doctor_id
WHERE d.experience_years > 5;
-- QUESTION 2
SELECT doctor_id, doctor_name, specialization, experience_years
FROM Doctors
WHERE experience_years > 10
-- QUESTION 3
select d.doctor_id, d.doctor_name
FROM Doctors d
LEFT JOIN Patients p ON d.doctor_id = p.doctor_id
WHERE p.patient_id IS NULL;
-- QUESTION 4
SELECT doctor_id, COUNT(*) AS appointment_count
FROM Appointments
GROUP BY doctor_id;
-- QUESTION 5.
SELECT COUNT(distinct patient_id) AS unique_patients
FROM Appointments;
SELECT d.doctor_id, d.doctor_name, AVG(p.age) AS avg_patient_age
FROM Doctors d
JOIN Patients p ON d.doctor_id = p.doctor_id
GROUP BY d.doctor_id, d.doctor_name;
select doctor_id, doctor_name, experience_years, RANK() OVER(ORDER BY experience_years DESC) AS
experience_rank
FROM Doctors;
SELECT appointment_id, appointment_date, COUNT(*) OVER (PARTITION BY appointment_date) AS
appointments_on_same_day
FROM Appointments;
SELECT d.doctor_id, d.doctor_name, d.specialization, d.experience_years, p.patient_id, p.patient_name,
p.age, p.gender, p.contact_number
FROM Doctors d
LEFT JOIN Patients p ON d.doctor_id = p.doctor_id;

