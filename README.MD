# ClinicEase: Web-Based Appointment Management System

ClinicEase is a web-based clinic appointment management system built with Flask and MySQL. It provides appointment scheduling, slot management, and role-based access for patients and clinic staff.

---

## Architecture and Design Patterns

The backend follows Object-Oriented Programming (OOP) principles and design patterns.

### 1. Object-Oriented Principles

* **Encapsulation:**
  * `User`: Private attribute `__password_hash` accessible only through the `password_hash` property getter.
  * `Appointment`: Private `__status` attribute managed via `@property` and `@status.setter` with validation on permitted state transitions (`Pending` -> `Confirmed` -> `Completed` or `Cancelled`).
  * `AppointmentSlot`: Private `__status` attribute managed via `@property` and `@status.setter` with concurrency protection in `book()`, `release()`, and `disable()`.

* **Inheritance and Polymorphism:**
  * Base class `User` defines the polymorphic method `get_user_role()`.
  * `Patient` inherits from `User` and overrides `get_user_role()` to return `"Patient"`.
  * `ClinicStaff` inherits from `User` and overrides `get_user_role()` to return `"Clinic Staff"`.
  * `User.login()` returns polymorphic subclasses (`Patient` or `ClinicStaff`) based on the database record.

* **Abstraction:**
  * `BaseDashboard` defines abstract contract `get_slots()` for role-based slot retrieval.
  * `BaseNotificationService` defines abstract contract `send_notification(recipient, subject, body)`.
  * `BookingValidationStrategy` defines abstract contract `validate(patient_id, slot, db_connection)`.

### 2. Design Patterns

* **Adapter Pattern (Structural):**
  * `PasswordHasherAdapter` encapsulates SHA-256 password hashing and verification (`hash_password`, `verify_password`), decoupling cryptography from entity classes.

* **Factory Method Pattern (Creational):**
  * `DashboardFactory`: Instantiates `PatientDashboard` or `StaffDashboard` based on the user's role.
  * `NotificationServiceFactory`: Instantiates `ConsoleNotificationService` or `EmailNotificationService` based on dispatch mode.

* **Strategy Pattern (Behavioral):**
  * `StandardValidationStrategy`: Validates slot availability.
  * `StrictValidationStrategy`: Validates slot availability and prevents concurrent duplicate pending bookings for the same patient.

* **Generator Pattern (Behavioral):**
  * `generate_appointment_report(appointments_list)`: Uses `yield` to stream formatted appointment summary rows without loading full report structures into memory.

---

## Project Structure

```
ClinicEase/
├── ClinicEase.sql                  # Database schema, table definitions, and seed data
├── database.py                     # Centralized MySQL connection provider
├── app.py                          # Flask application routes, session handling, and API
├── README.MD                       # Project documentation
├── models/
│   ├── __init__.py                 # Package exports
│   ├── user.py                     # User, Patient, ClinicStaff, PasswordHasherAdapter
│   ├── appointment.py              # Appointment model with status transition guards
│   ├── slot.py                     # AppointmentSlot model with concurrency control
│   └── reports.py                  # Generator function for appointment reporting
├── services/
│   ├── __init__.py                 # Package exports
│   ├── dashboard_service.py        # BaseDashboard, PatientDashboard, StaffDashboard, DashboardFactory
│   ├── notification_service.py     # BaseNotificationService, ConsoleNotificationService, EmailNotificationService, NotificationServiceFactory
│   ├── validation_strategy.py      # BookingValidationStrategy, StandardValidationStrategy, StrictValidationStrategy
│   └── validation_service.py       # Input validation facade for login, registration, and booking
├── templates/
│   ├── base.html                   # Base layout template
│   ├── landing_page.html           # Initial landing page
│   ├── login.html                  # User login view
│   ├── signup.html                 # Patient registration view
│   ├── patient_dashboard.html      # Patient appointment booking and history view
│   ├── staff_dashboard.html        # Staff slot management and review view
│   └── index.html                  # Backend API interactive test panel
└── static/
    └── css/                        # Stylesheets
```

---

## Database Setup

1. Ensure MySQL Server is running.
2. Import `ClinicEase.sql` into MySQL:
   ```bash
   mysql -u root -p < ClinicEase.sql
   ```
3. Update connection credentials in `database.py` if needed:
   ```python
   DB_CONFIG = {
       "host": "localhost",
       "database": "clinicease_db",
       "user": "root",
       "password": "your_mysql_password",
   }
   ```

### Default Seed Accounts

* **Clinic Staff Accounts (Password: `password123`):**
  * `gaudenz@example.com` (Gaudenz Padullon)
  * `staff.sarah@example.com` (Dr. Sarah Jenkins)
* **Patient Accounts (Password: `password123`):**
  * `maria.patient@example.com` (Maria Santos)
  * `juan.patient@example.com` (Juan Dela Cruz)

---

## Installation and Execution

1. Install Python dependencies:
   ```bash
   pip install flask mysql-connector-python
   ```
2. Start the Flask application:
   ```bash
   python app.py
   ```
3. Access the application:
   * Landing Page: `http://localhost:5000/`
   * Login: `http://localhost:5000/login`
   * Register: `http://localhost:5000/register`
   * Interactive API Test Panel: `http://localhost:5000/test-panel`

---

## Endpoints

### UI Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Landing page |
| `/login` | GET, POST | User login page and form submission |
| `/register` / `/signup` | GET, POST | Patient registration page and form submission |
| `/logout` | GET, POST | Clears session and redirects |
| `/dashboard` | GET | Role-based dashboard redirect |
| `/patient/dashboard` | GET | Patient dashboard view |
| `/staff/dashboard` | GET | Clinic staff dashboard view |
| `/test-panel` | GET | Interactive API testing panel |

### REST API Endpoints

| Endpoint | Method | Role | Description |
|---|---|---|---|
| `/api/register` | POST | Public | Register new patient account |
| `/api/login` | POST | Public | Authenticate user and initialize session |
| `/api/logout` | POST | Authenticated | Terminate session |
| `/api/dashboard/slots` | GET | Authenticated | Retrieve slots (Available only for Patient, All for Staff) |
| `/api/slots/book` | POST | Patient | Book an available slot |
| `/api/staff/appointments/pending` | GET | Clinic Staff | Fetch pending appointment requests |
| `/api/staff/appointments/<id>/action` | POST | Clinic Staff | Confirm or cancel an appointment |
| `/api/staff/report` | GET | Clinic Staff | Generate streaming appointment report |
