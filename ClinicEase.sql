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
    contact_number VARCHAR(20) NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Patient', 'Clinic Staff') NOT NULL
) ENGINE=InnoDB;

-- Existing database migration (run only when the column is still named
-- phone_number): ALTER TABLE users CHANGE COLUMN phone_number contact_number VARCHAR(20) NULL;

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
    status VARCHAR(50) DEFAULT 'Available',
    UNIQUE KEY uq_appointment_slots_date_time (slot_date, time)
) ENGINE=InnoDB;

-- ============================================================================
-- 2A. RECURRING CLINIC HOURS AND CLOSED DATES
-- weekday uses Python's weekday convention: Monday=0 through Sunday=6.
-- ============================================================================
CREATE TABLE IF NOT EXISTS clinic_schedule (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    weekday TINYINT UNSIGNED NOT NULL,
    open_time TIME NOT NULL,
    close_time TIME NOT NULL,
    slot_duration_minutes SMALLINT UNSIGNED NOT NULL DEFAULT 30,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT chk_clinic_schedule_weekday CHECK (weekday BETWEEN 0 AND 6),
    CONSTRAINT chk_clinic_schedule_duration CHECK (slot_duration_minutes = 30),
    CONSTRAINT chk_clinic_schedule_hours CHECK (open_time < close_time),
    UNIQUE KEY uq_clinic_schedule_hours (weekday, open_time, close_time)
);

CREATE TABLE IF NOT EXISTS blocked_dates (
    blocked_date DATE PRIMARY KEY,
    reason VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Default clinic hours: weekdays 08:00–17:00 and weekends 08:00–12:00,
-- with 30-minute slots. The generator creates the final slot only when its
-- full duration ends by the configured closing time.
INSERT IGNORE INTO clinic_schedule
    (weekday, open_time, close_time, slot_duration_minutes, is_active)
VALUES
    (0, '08:00:00', '17:00:00', 30, TRUE),
    (1, '08:00:00', '17:00:00', 30, TRUE),
    (2, '08:00:00', '17:00:00', 30, TRUE),
    (3, '08:00:00', '17:00:00', 30, TRUE),
    (4, '08:00:00', '17:00:00', 30, TRUE),
    (5, '08:00:00', '12:00:00', 30, TRUE),
    (6, '08:00:00', '12:00:00', 30, TRUE);

INSERT IGNORE INTO blocked_dates (blocked_date, reason)
VALUES ('2026-12-25', 'Christmas Day');

-- Seed selectable appointment times for the next 30 days so the calendar is usable
-- immediately after a fresh install. This uses the same weekly hours and closures
-- as the monthly slot-generation service; rerunning it does not duplicate slots.
INSERT IGNORE INTO appointment_slots (slot_date, time, status)
WITH RECURSIVE
calendar_days AS (
    SELECT DATE_ADD(CURRENT_DATE, INTERVAL 1 DAY) AS slot_date
    UNION ALL
    SELECT DATE_ADD(slot_date, INTERVAL 1 DAY)
    FROM calendar_days
    WHERE slot_date < DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY)
),
schedule_times AS (
    SELECT
        weekday,
        close_time,
        slot_duration_minutes,
        open_time AS slot_start
    FROM clinic_schedule
    WHERE is_active = TRUE

    UNION ALL

    SELECT
        weekday,
        close_time,
        slot_duration_minutes,
        ADDTIME(slot_start, SEC_TO_TIME(slot_duration_minutes * 60))
    FROM schedule_times
    WHERE ADDTIME(slot_start, SEC_TO_TIME(slot_duration_minutes * 60)) < close_time
)
SELECT
    calendar_days.slot_date,
    DATE_FORMAT(schedule_times.slot_start, '%h:%i %p'),
    'Available'
FROM calendar_days
JOIN schedule_times
    ON WEEKDAY(calendar_days.slot_date) = schedule_times.weekday
WHERE ADDTIME(
          schedule_times.slot_start,
          SEC_TO_TIME(schedule_times.slot_duration_minutes * 60)
      ) <= schedule_times.close_time
  AND NOT EXISTS (
      SELECT 1
      FROM blocked_dates
      WHERE blocked_dates.blocked_date = calendar_days.slot_date
  );

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
    contact_number VARCHAR(30) NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (slot_id) REFERENCES appointment_slots(slot_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;
