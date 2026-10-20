DROP DATABASE IF EXISTS clinicease_db;
CREATE DATABASE clinicease_db;
USE clinicease_db;

-- ============================================================================
-- 1. USERS TABLE
-- Encapsulates core user account information with role-based segregation.
-- ============================================================================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Patient', 'Clinic Staff') NOT NULL
);

-- Seed Data: All test accounts have the password 'password123'
-- MySQL's SHA2('password123', 256) exactly matches Python's hashlib.sha256
INSERT INTO users (name, email, password_hash, role) VALUES 
('Gaudenz Padullon', 'gaudenz@example.com', SHA2('password123', 256), 'Clinic Staff'),
('Dr. Sarah Jenkins', 'staff.sarah@example.com', SHA2('password123', 256), 'Clinic Staff'),
('Maria Santos', 'maria.patient@example.com', SHA2('password123', 256), 'Patient'),
('Juan Dela Cruz', 'juan.patient@example.com', SHA2('password123', 256), 'Patient');

-- ============================================================================
-- 2. APPOINTMENT SLOTS TABLE
-- Manages time slots with availability status.
-- ============================================================================
CREATE TABLE IF NOT EXISTS appointment_slots (
    slot_id INT AUTO_INCREMENT PRIMARY KEY,
    slot_date DATE NOT NULL,
    time VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'Available'
);

-- Seed Data: Sample appointment slots
INSERT INTO appointment_slots (slot_date, time, status) VALUES 
('2026-10-15', '09:00 AM', 'Available'),
('2026-10-15', '10:00 AM', 'Available'),
('2026-10-15', '11:00 AM', 'Booked'), -- Pre-linked to Maria Santos
('2026-10-16', '01:30 PM', 'Available'),
('2026-10-16', '03:00 PM', 'Available'),
('2026-10-17', '08:30 AM', 'Booked'), -- Pre-linked to Juan Dela Cruz
('2026-10-17', '10:00 AM', 'Available');

-- ============================================================================
-- 3. APPOINTMENTS TABLE
-- Tracks appointment records, patient assignments, and lifecycle statuses.
-- ============================================================================
DROP TABLE IF EXISTS appointments;

CREATE TABLE appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    slot_id INT NOT NULL,
    user_id INT NOT NULL,
    purpose VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (slot_id) REFERENCES appointment_slots(slot_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Seed Data: Sample initial appointments
INSERT INTO appointments (slot_id, user_id, purpose, status) VALUES 
(3, 3, 'General Medical Checkup - Maria Santos', 'Pending'),
(6, 4, 'Dental Consultation - Juan Dela Cruz', 'Pending');
