DROP DATABASE IF EXISTS clinicease_db;
CREATE DATABASE clinicease_db;
USE clinicease_db;

-- 1. Users table (Supports role-based dashboard factory logic)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Patient', 'Clinic Staff') NOT NULL
);

-- Insert multiple test users (all passwords are set to 'password123' via SHA2)
INSERT INTO users (name, email, password_hash, role) VALUES 
('Gaudenz Padullon', 'gaudenz@example.com', SHA2('password123', 256), 'Clinic Staff'),
('Maria Santos', 'maria.patient@example.com', SHA2('password123', 256), 'Patient'),
('Juan Dela Cruz', 'juan.patient@example.com', SHA2('password123', 256), 'Patient'),
('Dr. Sarah Jenkins', 'staff.sarah@example.com', SHA2('password123', 256), 'Clinic Staff');

-- 2. Appointment slots table (Supports state protection & dashboard services)
CREATE TABLE IF NOT EXISTS appointment_slots (
    slot_id INT AUTO_INCREMENT PRIMARY KEY,
    slot_date DATE NOT NULL,
    time VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'Available'
);

-- Insert multiple sample slots with varied dates, times, and statuses
INSERT INTO appointment_slots (slot_date, time, status) VALUES 
('2026-10-15', '09:00 AM', 'Available'),
('2026-10-15', '10:00 AM', 'Available'),
('2026-10-15', '11:00 AM', 'Booked'), -- Linked to an appointment below
('2026-10-16', '01:30 PM', 'Available'),
('2026-10-16', '03:00 PM', 'Available'),
('2026-10-17', '08:30 AM', 'Booked'), -- Linked to an appointment below
('2026-10-17', '10:00 AM', 'Available');

-- 3. Appointments table (Tracks confirmed bookings, purposes, and relations)
DROP TABLE IF EXISTS appointments;

CREATE TABLE appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    slot_id INT NOT NULL,
    user_id INT NOT NULL,
    purpose VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (slot_id) REFERENCES appointment_slots(slot_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Insert sample appointments matching the new columns
INSERT INTO appointments (slot_id, user_id, purpose, status) VALUES 
(3, 2, 'General Medical Checkup - Maria Santos', 'Pending'),
(6, 3, 'Dental Consultation - Juan Dela Cruz', 'Pending');