CREATE DATABASE IF NOT EXISTS AMC;
CREATE DATABASE IF NOT EXISTS hospital_service;
CREATE DATABASE IF NOT EXISTS financial_services;

USE AMC;
DROP TABLE IF EXISTS muncipdata13;
DROP TABLE IF EXISTS officialdata1;

CREATE TABLE officialdata1 (
    Name VARCHAR(50) NOT NULL,
    OfficialID INT NOT NULL PRIMARY KEY,
    Age VARCHAR(50) NOT NULL
);

CREATE TABLE muncipdata13 (
    Name VARCHAR(50) NOT NULL,
    UNIQUEID INT NOT NULL PRIMARY KEY,
    Age VARCHAR(50) NOT NULL,
    Area VARCHAR(100) NOT NULL,
    Ward INT NOT NULL,
    Gender VARCHAR(10) NOT NULL,
    Complains VARCHAR(100),
    Complainapp VARCHAR(100),
    Other VARCHAR(100),
    Otherapp VARCHAR(100)
);

INSERT INTO officialdata1 VALUES
('Rajesh Parad',1125001,'50'),
('Shalini Chattaraj',1125002,'25'),
('Sanjoy Basu',1125003,'34'),
('Tanmoy Das',1125004,'21');

INSERT INTO muncipdata13 VALUES
('Anish Rai',202545,'35','BNR More, G.T. Road',22,'Male','Road not repaired','Waiting',NULL,NULL),
('Manoj Verma',202553,'65','Kalipahari',80,'Male','Water not coming','Approved',NULL,NULL),
('Sneha Chatterjee',202525,'just born','Tribeni More, Burnpur',78,'Female',NULL,NULL,'Apply for birth certificate','Approved'),
('Subhash Prasad',202520,'66','Raniganj',36,'Male','Road not repaired','Approved',NULL,NULL),
('Tanya Das',202555,'21','BNR More, G.T. Road',28,'Female',NULL,NULL,'Trade licence','Waiting');

USE hospital_service;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS hospitals;

CREATE TABLE hospitals (
    hospital_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL
);

CREATE TABLE doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    hospital_id INT,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id)
);

CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(10),
    phone VARCHAR(15)
);

CREATE TABLE appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

INSERT INTO hospitals (name,address) VALUES
('Asansol District Hospital','G.T. Road, Asansol'),
('Burnpur Sub-Divisional Hospital','Burnpur Road'),
('Durgapur Sub-Divisional Hospital','Benachity, Durgapur'),
('Kulti State General Hospital','Kulti More'),
('Raniganj Block Primary Health Center','Main Road, Raniganj'),
('Jamuria Rural Hospital','Jamuria Main Road');

INSERT INTO doctors (name,specialty,hospital_id) VALUES
('Dr. Anupam Ghosh','Cardiologist',1),
('Dr. Rakesh Mitra','Cardiologist',2),
('Dr. Sneha Sen','Pediatrician',1),
('Dr. Alok Jain','Pediatrician',5),
('Dr. Ritwik Basu','Dermatologist',2),
('Dr. Reema Banerjee','Dermatologist',6),
('Dr. Rina Dey','Orthopedic',2),
('Dr. Ajit Das','Orthopedic',4),
('Dr. Surajit Pal','ENT Specialist',3),
('Dr. Namrata Ghosh','ENT Specialist',6),
('Dr. Nusrat Jahan','Gynecologist',3),
('Dr. Ipsita Dey','Gynecologist',5);

USE financial_services;
DROP TABLE IF EXISTS bank_accounts;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS banks;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    aadhar VARCHAR(12) UNIQUE NOT NULL
);

CREATE TABLE banks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE bank_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    bank_id INT NOT NULL,
    balance DECIMAL(10,2) DEFAULT 0.00,
    last_transaction DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (bank_id) REFERENCES banks(id)
);

INSERT INTO banks (name) VALUES
('State Bank of India'),
('Punjab National Bank'),
('Canara Bank'),
('Bank of Baroda'),
('Union Bank of India'),
('Indian Bank'),
('Central Bank of India'),
('UCO Bank');
