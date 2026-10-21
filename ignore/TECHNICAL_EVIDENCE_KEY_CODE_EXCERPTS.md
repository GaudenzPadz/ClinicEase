# Technical Evidence: Key Code Excerpts

## 1. Encapsulation — Appointment Status

**File Location:** `models/appointment.py`

**What to Screenshot:** The `Appointment` class, especially `ALLOWED_TRANSITIONS`, the `status` property and `@status.setter`, and the `confirm()`, `cancel()`, and `complete()` methods.

**Academic Description:** The `Appointment` class encapsulated its status in the name-mangled `__status` attribute and exposed controlled access through a property. Its setter checked valid statuses and enforced `ALLOWED_TRANSITIONS`, preventing invalid lifecycle changes while the dedicated methods provided explicit operations for confirming, cancelling, and completing appointments.

## 2. Strategy Pattern — Booking Validation

**File Location:** `services/validation_strategy.py`

**What to Screenshot:** The `BookingValidationStrategy` abstract base class and the `StandardValidationStrategy.validate()` method. To show where the strategy was selected and used, include `RegistrationService.__init__()` and the call to `self.slot_validation_strategy.validate()` in `services/registration_service.py`.

**Academic Description:** The system defined a common `validate()` contract in `BookingValidationStrategy` and implemented the standard slot-availability check in `StandardValidationStrategy`. `RegistrationService` accepted a slot-validation strategy and invoked it during the initial registration-and-booking flow, allowing validation behavior to be supplied through a strategy object rather than embedded in that service.

## 3. Adapter Pattern — Password Security

**File Location:** `models/user.py`

**What to Screenshot:** The `PasswordHasherAdapter` class, particularly `hash_password()`, `verify_password()`, and `needs_rehash()`. Optionally include the calls to these methods in `User.login()`.

**Academic Description:** The `PasswordHasherAdapter` provided the application with a consistent interface for password hashing and verification while delegating modern password operations to Werkzeug. It also verified legacy SHA-256 digests using a constant-time comparison and identified them for rehashing, allowing existing credentials to be upgraded during login.

## 4. Factory Pattern — Role-Based Dashboards

**File Location:** `services/dashboard_service.py`

**What to Screenshot:** The `DashboardFactory` class and its `create_dashboard()` static method, together with the `PatientDashboard` and `StaffDashboard` classes.

**Academic Description:** The `DashboardFactory.create_dashboard()` method selected and instantiated a dashboard implementation according to the supplied user role. This centralized object creation and returned implementations of the shared `BaseDashboard` contract, so callers could request role-specific dashboard behavior without constructing the concrete dashboard classes themselves.

## 5. Race-Condition Prevention — Pessimistic Locking

**File Location:** `app.py`

**What to Screenshot:** The `book_appointment_slot()` route registered at `/api/slots/book`, from `conn.autocommit = False` through the `SELECT ... FOR UPDATE`, slot update, appointment creation, `conn.commit()`, and the rollback handling.

**Academic Description:** The booking route disabled autocommit and selected the requested appointment-slot row with `FOR UPDATE`, locking it within the transaction while availability was checked and the booking was saved. The route committed the slot update and appointment together on success and rolled back on failure, preventing concurrent requests from successfully booking the same available slot.

## 6. Generator Pattern — Appointment Report Generation

**File Location:** `models/reports.py`

**What to Screenshot:** The `generate_appointment_report()` function, highlighting its `for` loop and `yield` statement. For context, the report route `get_staff_appointment_report()` in `app.py` calls the function and converts its result with `list(report_generator)`.

**Academic Description:** The `generate_appointment_report()` function used `yield` to produce each formatted appointment-report line lazily, rather than constructing and returning the complete sequence inside the function. The current staff-report route subsequently materialized those yielded lines into a list for its JSON response, so the generator itself supported lazy iteration even though that route did not stream the final response.
