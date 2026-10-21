# ClinicEase

ClinicEase is a Flask and MySQL web application for managing clinic appointments. It provides separate patient and clinic-staff workflows for registration, appointment booking, request review, recurring clinic hours, and slot administration.

Patients register with an initial appointment request, manage upcoming and past appointments, and can request another available time. Clinic staff review and update requests, manage appointment slots and clinic closures, and view dashboard summaries and reports.

Patient email addresses are required. Contact numbers are optional.

## Features

- Separate sign-in (`/login`) and registration (`/register`) pages.
- Role-based patient and clinic-staff dashboards.
- Appointment statuses with guarded transitions: Pending, Confirmed, Cancelled, and Completed.
- Configurable recurring clinic hours, 30-minute appointment slots, and one-off blocked dates.
- Transactional booking with a database row lock to prevent two requests from claiming the same slot.
- Staff dashboard with appointment statistics, charts, pending and confirmed request lists, and a responsive 14-day slot calendar.
- Optional email notifications for patients and clinic staff.
- Password hashing through Werkzeug, with successful-login upgrade of legacy SHA-256 password hashes.

## Technology

- Python and Flask
- MySQL with `mysql-connector-python`
- Jinja2 templates
- Vanilla JavaScript and CSS
- Chart.js loaded from a CDN for the staff dashboard

Python dependencies are listed in [`requirements.txt`](requirements.txt). Front-end assets are served from `static/`; Chart.js is not installed as a Python or npm dependency.

## Architecture and OOP Design

The application separates database-backed entities in `models/` from application services in `services/`.

| Principle or pattern | Implementation |
|---|---|
| Encapsulation | `Appointment.status` validates permitted lifecycle transitions against `ALLOWED_TRANSITIONS`. `AppointmentSlot.status` restricts valid slot states, and its methods control state changes. |
| Inheritance and polymorphism | `Patient` and `ClinicStaff` extend `User` and provide role-specific behavior. Dashboard implementations share the `BaseDashboard` contract. |
| Abstraction | `BaseDashboard`, `BaseNotificationService`, and `BookingValidationStrategy` define contracts for dashboard retrieval, notifications, and booking validation. |
| Factory | `DashboardFactory` chooses a dashboard by role. `NotificationServiceFactory` chooses console or email notification delivery. `SlotGeneratorFactory` selects a slot-generation strategy. |
| Strategy | `Standard30MinStrategy` implements slot generation. Booking validation is defined by `BookingValidationStrategy`; `RegistrationService` uses `StandardValidationStrategy` for slot availability and a registration-specific validation strategy for email and slot checks. `StrictValidationStrategy` is also available in the codebase. |
| Adapter | `PasswordHasherAdapter` provides a stable interface over Werkzeug password hashing and verification while supporting legacy SHA-256 hashes. |
| Generator | `generate_appointment_report()` in `models/reports.py` uses `yield` to provide formatted report lines lazily. The staff report API currently materializes those lines into a list for its JSON response. |

### Booking transaction

The patient booking endpoint starts a transaction with autocommit disabled, selects the requested `appointment_slots` row using `SELECT ... FOR UPDATE`, checks and updates its state, then creates the appointment. The slot update and appointment creation are committed together; failures roll back the transaction. The initial registration-and-booking flow also uses a transaction and locks the selected slot.

## Project Structure

```text
ClinicEase/
├── ClinicEase.sql
├── README.MD
├── requirements.txt
├── database.py
├── app.py
├── models/
│   ├── __init__.py
│   ├── appointment.py
│   ├── dashboard.py
│   ├── password.py
│   ├── reports.py
│   ├── slot.py
│   ├── user.py
│   └── users.py
├── services/
│   ├── __init__.py
│   ├── dashboard_service.py
│   ├── notification_service.py
│   ├── registration_service.py
│   ├── slot_generator_service.py
│   ├── validation_service.py
│   └── validation_strategy.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── landing_page.html
│   ├── login.html
│   ├── register.html
│   ├── patient/
│   │   └── patient_dashboard.html
│   └── clinic_staff/
│       └── staff_dashboard.html
└── static/
    ├── css/
    │   ├── base.css
    │   ├── components.css
    │   └── pages/
    └── js/
        ├── api-test.js
        ├── auth.js
        ├── base.js
        ├── patient-dashboard.js
        └── staff-dashboard.js
```

## Requirements

- Python version compatible with the packages in `requirements.txt`.
- MySQL Server.
- MySQL Workbench or the MySQL command-line client to initialize the schema.

## Setup

### 1. Create the database

> **Warning:** `ClinicEase.sql` starts with `DROP DATABASE IF EXISTS clinicease_db`. Running the complete script deletes and recreates that database, including its existing data. Back up any data you need before importing it. This script is intended for a fresh development setup.

Import `ClinicEase.sql` using MySQL Workbench, or from a Windows Command Prompt with the MySQL client installed:

```bat
mysql -u root -p < ClinicEase.sql
```

The schema creates `clinicease_db`, the user, slot, schedule, closure, and appointment tables, sample accounts, and appointment slots for the upcoming 30 days. The recurring schedule and date-based slot generation require a MySQL version that supports recursive common table expressions.

### 2. Configure the application

`database.py` loads environment variables from a `.env` file at the project root. Configure the database connection with:

```dotenv
CLINICEASE_DB_HOST=localhost
CLINICEASE_DB_PORT=3306
CLINICEASE_DB_NAME=clinicease_db
CLINICEASE_DB_USER=root
CLINICEASE_DB_PASSWORD=your_mysql_password
CLINICEASE_SECRET_KEY=replace_with_a_long_random_secret
```

The database connection defaults to host `localhost`, port `3306`, database `clinicease_db`, and user `root`. `CLINICEASE_DB_PASSWORD` must be set or the application cannot connect. Set a stable, private `CLINICEASE_SECRET_KEY`; the application generates a temporary fallback when it is unset, so sessions will not persist across restarts. For HTTPS deployments, set `CLINICEASE_HTTPS=true` to mark session cookies as Secure.

Do not commit `.env` or real credentials.

### 3. Install Python dependencies

In PowerShell from the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 4. Start the application

```powershell
python app.py
```

The development server listens on `http://localhost:5000`. On startup, it attempts to generate missing slots for today and the following 29 days from the active weekly clinic schedule. If slot generation fails, the application logs the failure and continues starting; no new slots will be available until the database or schedule issue is resolved and generation succeeds.

The current `app.py` runs Flask with debug mode enabled. Use a production WSGI server and production-appropriate settings for deployment; do not expose the development server publicly.

## Seed Accounts

The fresh-install SQL script creates the following development accounts. Each is seeded with the password `password123`.

| Role | Email | Name |
|---|---|---|
| Clinic Staff | `gaudenz@example.com` | Gaudenz Padullon |
| Clinic Staff | `staff.sarah@example.com` | Dr. Sarah Jenkins |
| Patient | `maria.patient@example.com` | Maria Santos |
| Patient | `juan.patient@example.com` | Juan Dela Cruz |

These are public sample credentials for local development only. Replace or remove them before deploying to any shared or production environment.

## Clinic Hours and Appointment Slots

The `clinic_schedule` table stores recurring clinic hours. Weekday values use Python's convention: Monday is `0` and Sunday is `6`. A fresh schema sets Monday through Friday to 08:00–17:00 and Saturday and Sunday to 08:00–12:00, using 30-minute appointments. The slot generator only creates appointments whose full 30-minute duration fits before closing; for a 12:00 weekend closing time, the final slot starts at 11:30.

Staff can generate missing slots for a selected month from the dashboard. The same operation is available through `POST /api/slots/generate` with integer `year` and `month` values. Generation reads active rows from `clinic_schedule`, skips dates in `blocked_dates`, and uses the unique `(slot_date, time)` key with `INSERT IGNORE` to avoid duplicates.

Changing clinic hours affects slots created by subsequent generation; it does not automatically rewrite slots already in `appointment_slots`. Review or manage existing slots using the staff dashboard.

Staff can add a one-off clinic closure using the Block a Date form or `POST /api/staff/blocked_dates` with a date and reason. The closure disables unbooked slots on that date and prevents new slots from being generated for it. Existing booked appointments are not cancelled.

The staff dashboard lists slots from today through 14 days ahead, initially showing the first seven days. Staff can expand the calendar and filter by date. The patient dashboard only retrieves slots with status `Available` and a date on or after the current date.

## Application Pages

| Path | Access | Description |
|---|---|---|
| `/` | Public | Landing page |
| `/login` | Public | Sign-in page |
| `/register` | Public | Patient registration and initial appointment request |
| `/signup` | Public | GET alias that opens the registration page |
| `/dashboard` | Signed-in user | Redirects to the dashboard for the user's role |
| `/patient/dashboard` | Patient | Book appointments and review upcoming and past appointments |
| `/staff/dashboard` | Clinic Staff | Review requests, manage clinic times, and view dashboard summaries |
| `/test-panel` | Public | Interactive API test panel |
| `/logout` | Signed-in user | Clears the session |

## API Endpoints

All endpoints use the session-based authentication implemented by the application. Staff-only and patient-only endpoints verify the caller's session role.

| Endpoint | Method | Access | Purpose |
|---|---|---|---|
| `/api/register` | POST | Public | Create a patient account and its initial pending appointment request. |
| `/api/register_and_book` | POST | Public | Create the same initial request and sign the patient in; returns a dashboard redirect URL. |
| `/api/login` | POST | Public | Authenticate and establish the user's session. |
| `/api/logout` | POST | Signed-in user | Clear the session. |
| `/api/dashboard/slots` | GET | Signed-in user | Retrieve slots appropriate to the user's role. |
| `/api/slots/book` | POST | Patient | Request an available appointment slot. |
| `/api/patient/appointments/<appt_id>/cancel` | POST | Patient | Cancel an eligible appointment belonging to the patient. |
| `/api/staff/appointments/pending` | GET | Clinic Staff | Retrieve pending appointment requests. |
| `/api/staff/dashboard/stats` | GET | Clinic Staff | Retrieve appointment counts, weekly bookings, and slot statistics for the staff dashboard. |
| `/api/staff/appointments/<appt_id>/action` | POST | Clinic Staff | Confirm, cancel, or complete an appointment, subject to allowed status transitions. |
| `/api/staff/blocked_dates` | POST | Clinic Staff | Add a clinic closure date and disable unbooked slots for it. |
| `/api/slots/generate` | POST | Clinic Staff | Generate missing appointment slots for a month from the clinic schedule. |
| `/api/staff/slots/<slot_id>` | PATCH, DELETE | Clinic Staff | Edit, enable, disable, or delete an eligible appointment slot. |
| `/api/staff/report` | GET | Clinic Staff | Return a JSON report containing formatted appointment lines. |

## Notifications

Appointment notifications are dispatched using `CLINICEASE_NOTIFICATION_MODE`. The application currently defaults this setting to `email`. Configure email delivery with:

```dotenv
CLINICEASE_NOTIFICATION_MODE=email
CLINICEASE_SMTP_HOST=your_smtp_host
CLINICEASE_SMTP_PORT=587
CLINICEASE_SMTP_SENDER=clinic@example.com
CLINICEASE_SMTP_USERNAME=your_smtp_username
CLINICEASE_SMTP_PASSWORD=your_smtp_password
```

SMTP username and password are only needed when the server requires authentication. For local development, `CLINICEASE_NOTIFICATION_MODE=console` prints notification contents to the application console instead of sending email. Notification errors are logged and reported as a warning; a booking that was already committed remains saved.

## Password Compatibility

New passwords are hashed with Werkzeug's password-hashing functions. The fresh-install seed accounts use SHA-256 values to match the application's legacy-hash compatibility path. After a successful login with a legacy hash, `User.login()` upgrades the stored hash to the configured Werkzeug format.

## Troubleshooting

- **Database connection fails:** Confirm that MySQL is running and that the `.env` database settings match the imported database. `CLINICEASE_DB_PASSWORD` is required.
- **No appointment times appear:** Confirm that active rows exist in `clinic_schedule`, that the selected date is not in `blocked_dates`, and that slot generation completed successfully. Staff can generate slots from the dashboard.
- **A dashboard API request returns 401:** Sign in with an account that has the required role. Patient and staff endpoints are role-protected.
- **Email notifications are not delivered:** Verify the SMTP host, port, sender, and any required credentials. In local development, use console mode to avoid depending on SMTP.
- **Charts do not load:** The staff dashboard loads Chart.js from jsDelivr. A network filter, content blocker, or browser privacy setting may prevent the CDN script from loading; the stats endpoint is independent of chart rendering.
- **Calendar schedule changes do not alter existing times:** Schedule rules control future slot generation; existing rows are retained to protect booked appointments and preserve slot records.

## Related Documentation

- [`TECHNICAL_EVIDENCE_KEY_CODE_EXCERPTS.md`](TECHNICAL_EVIDENCE_KEY_CODE_EXCERPTS.md) — source-backed descriptions and screenshot targets for selected OOP concepts and patterns.
