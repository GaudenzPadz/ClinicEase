# ClinicEase: Web-Based Appointment Management System

ClinicEase is a web-based clinic appointment management system built with Flask and MySQL. It provides appointment scheduling, slot management, and role-based access for patients and clinic staff.

Patient email addresses are required for accounts and appointment updates. Contact numbers are optional during sign-up and appointment booking.

---

## Architecture and Design Patterns

The backend follows Object-Oriented Programming (OOP) principles and design patterns.

### 1. Object-Oriented Principles

* **Encapsulation:**
  * `User`: Stores its password hash privately. New passwords use Werkzeug's password hashing; legacy SHA-256 hashes are upgraded after successful login.
  * `Appointment`: Private `__status` attribute managed via `@property` and `@status.setter` with validation on permitted state transitions (`Pending` -> `Confirmed` -> `Completed` or `Cancelled`).
  * `AppointmentSlot`: Private `__status` attribute managed via `@property` and `@status.setter`. `book_atomically()` claims an Available, future slot with a conditional SQL update.

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
  * `PasswordHasherAdapter` encapsulates password hashing and verification (`hash_password`, `verify_password`), decoupling password handling from entity classes.

* **Factory Method Pattern (Creational):**
  * `DashboardFactory`: Instantiates `PatientDashboard` or `StaffDashboard` based on the user's role.
  * `NotificationServiceFactory`: Instantiates `ConsoleNotificationService` or `EmailNotificationService` based on dispatch mode.

* **Strategy Pattern (Behavioral):**
  * `StandardValidationStrategy`: Validates slot availability.
  * `StrictValidationStrategy`: Validates slot availability and prevents concurrent duplicate pending bookings for the same patient.
  * `RegistrationBookingValidationStrategy`: Checks account-email and selected-slot availability during the combined first-request flow.

* **Generator Pattern (Behavioral):**
  * `generate_appointment_report(appointments_list)`: Uses `yield` to stream formatted appointment summary rows without loading full report structures into memory.

---

## Project Structure

```
ClinicEase/
├── ClinicEase.sql                  # Database schema, table definitions, and seed data
├── migrations/
│   ├── 20261021_add_contact_numbers.sql # Adds registration and booking contact fields
│   └── 20261021_add_dynamic_calendar.sql # Schedule, closures, and unique slot keys
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
│   ├── registration_service.py     # Transactional account creation and initial appointment request
│   ├── slot_generator_service.py   # Calendar generation strategy, factory, and monthly slot service
│   ├── validation_strategy.py      # Booking and registration validation strategies
│   └── validation_service.py       # Input validation facade for login, registration, and booking
├── templates/
│   ├── base.html                   # Base layout template
│   ├── landing_page.html           # Initial landing page
│   ├── login.html                  # Combined sign-in and patient registration
│   ├── patient/
│   │   └── patient_dashboard.html  # Patient booking and appointment history
│   ├── clinic_staff/
│   │   └── staff_dashboard.html    # Staff request and slot management
│   └── index.html                  # Backend API interactive test panel
└── static/
    ├── css/
    │   ├── base.css                # Design tokens, reset, shared shell
    │   ├── components.css          # Shared buttons, cards, forms, tables, badges
    │   └── pages/                  # Landing, auth, dashboard, test-panel styles
    └── js/
        ├── base.js                 # Shared request and toast utilities
        ├── auth.js                 # Login and account creation
        ├── patient-dashboard.js    # Appointment booking interactions
        ├── staff-dashboard.js      # Staff actions and slot management
        └── api-test.js             # Developer test-panel interactions
```

---

## Database Setup

1. Ensure MySQL Server is running.
2. Import `ClinicEase.sql` into MySQL:
   ```bash
   mysql -u root -p < ClinicEase.sql
   ```
   For an existing database whose `users` table still has `phone_number`, migrate the
   optional field with:
   ```sql
   ALTER TABLE users CHANGE COLUMN phone_number contact_number VARCHAR(20) NULL;
   ```
   For an existing database, apply `migrations/20261021_add_dynamic_calendar.sql`.
   If the contact-number migration has not been applied yet, apply
   `migrations/20261021_add_contact_numbers.sql` first.
   If the existing `appointment_slots` table contains duplicate date/time pairs, resolve
   those conflicts first; the migration requires the unique key used for idempotent generation.
3. Configure the connection through `CLINICEASE_DB_HOST`, `CLINICEASE_DB_NAME`,
   `CLINICEASE_DB_USER`, and `CLINICEASE_DB_PASSWORD`. Set a stable, private
   `CLINICEASE_SECRET_KEY` for Flask sessions. For HTTPS deployments, set
   `CLINICEASE_HTTPS=true` so session cookies are marked Secure.
4. For SMTP delivery, set `CLINICEASE_NOTIFICATION_MODE=email`, `CLINICEASE_SMTP_HOST`,
   `CLINICEASE_SMTP_SENDER`, and (when required) `CLINICEASE_SMTP_USERNAME`,
   `CLINICEASE_SMTP_PASSWORD`, and `CLINICEASE_SMTP_PORT` in the environment.
   Email mode is the default. Set `CLINICEASE_NOTIFICATION_MODE=console` only for local
   development; the app reports a warning if an email cannot be delivered.

### Dynamic Calendar

The fresh-install schema and `migrations/20261021_add_dynamic_calendar.sql` create
`clinic_schedule` (Monday=0 through Sunday=6), `blocked_dates`, and the unique
`appointment_slots(slot_date, time)` key. The sample weekly schedule is Monday–Friday,
08:00–17:00 in 30-minute increments; Christmas Day 2026 is seeded as a closure.
Staff can generate slots from the dashboard or POST `{"year": 2027, "month": 1}` to
`/api/slots/generate`. Generated values are normalized to the existing `HH:MM AM/PM`
time format. `INSERT IGNORE` plus the unique key makes generation idempotent.

To change clinic hours, update `clinic_schedule` rows and run generation again. To block
a date, staff POST `{"blocked_date": "2027-01-01", "reason": "Holiday"}` to
`/api/staff/blocked_dates`; this disables unbooked slots already generated for that date.
Existing booked appointments are left intact.

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
   pip install -r requirements.txt
   ```
2. Start the Flask application:
   ```bash
   python app.py
   ```
3. Access the application:
   * Landing Page: `http://localhost:5000/`
   * Sign in or create an account and request its first appointment: `http://localhost:5000/login`
   * Interactive API Test Panel: `http://localhost:5000/test-panel`

---

## Endpoints

### UI Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Landing page |
| `/login` | GET, POST | Sign-in and combined patient registration/appointment request page |
| `/register` / `/signup` | GET, POST | Combined patient account and initial appointment request |
| `/logout` | GET, POST | Clears session and redirects |
| `/dashboard` | GET | Role-based dashboard redirect |
| `/patient/dashboard` | GET | Patient dashboard view |
| `/staff/dashboard` | GET | Clinic staff dashboard view |
| `/test-panel` | GET | Interactive API testing panel |

### REST API Endpoints

| Endpoint | Method | Role | Description |
|---|---|---|---|
| `/api/register` | POST | Public | Create a patient account and first Pending appointment atomically |
| `/api/register_and_book` | POST | Public | Atomically create the account and Pending request, then sign the patient in |
| `/api/login` | POST | Public | Authenticate user and initialize session |
| `/api/logout` | POST | Authenticated | Terminate session |
| `/api/dashboard/slots` | GET | Authenticated | Retrieve slots (Available only for Patient, All for Staff) |
| `/api/slots/book` | POST | Patient | Book an available slot |
| `/api/staff/blocked_dates` | POST | Clinic Staff | Add a closure date and disable unbooked slots on it |
| `/api/slots/generate` | POST | Clinic Staff | Generate missing slots from clinic hours for a month |
| `/api/staff/appointments/pending` | GET | Clinic Staff | Fetch pending appointment requests |
| `/api/staff/appointments/<id>/action` | POST | Clinic Staff | Confirm, cancel, or complete an appointment |
| `/api/staff/slots/<id>` | PATCH, DELETE | Clinic Staff | Update, enable, disable, or remove an unused appointment time |
| `/api/staff/report` | GET | Clinic Staff | Generate streaming appointment report |

### Activity Diagram Execution Mapping

1. **Register & Book:** The sign-up tab collects name, email, password, a preferred available slot, and purpose; contact number is optional. `RegistrationService` checks required fields, email uniqueness, and slot availability. It creates the account, conditionally claims the slot, and inserts a Pending appointment in one MySQL transaction. Any failure rolls back all three writes. Notifications are attempted only after commit.
2. **Authenticate & Route:** `User.login()` returns a `Patient` or `ClinicStaff`. The dashboard route reads `get_user_role()` and redirects to that role's dashboard.
   Staff can generate a month of 30-minute slots from active `clinic_schedule` rows.
   `blocked_dates` prevents generation on closures and disables unbooked slots already created for those dates; existing booked appointments are preserved.
3. **Request a Visit:** Patient booking uses `SELECT ... FOR UPDATE`, then calls the encapsulated `AppointmentSlot.book()` while holding the row lock. The slot update and Pending appointment insert commit together; a competing request sees the updated status and is rejected without creating an appointment.
4. **Review & Complete:** Staff can confirm or cancel a Pending appointment. Cancellation returns its slot to Available in the same transaction. Only Confirmed appointments may transition to Completed.

The model classes remain in the repository's `models/` package instead of a monolithic
`models.py`; `models/__init__.py` exports the public classes. This preserves the established
module boundaries while keeping each class focused.

### Workflow Tests

Run the diagram-specific validation, transaction, lifecycle, and password-hash tests with:

```bash
python -m unittest discover -s tests -v
```

Monthly generation accepts a JSON payload such as
`{"year": 2027, "month": 1}`. A closure request accepts
`{"blocked_date": "2027-01-01", "reason": "New Year's Day"}`.
Generation skips blocked dates and uses `INSERT IGNORE` with the unique
`(slot_date, time)` key so rerunning a month does not create duplicate slots.
