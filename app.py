from datetime import date, datetime
import os
import secrets

from flask import (
    Flask,
    jsonify,
    session,
    request,
    render_template,
    redirect,
    url_for,
)
import mysql.connector
from database import get_connection
from models.user import User
from models.slot import AppointmentSlot
from models.appointment import Appointment
from models.reports import generate_appointment_report
from services.dashboard_service import DashboardFactory
from services.notification_service import NotificationServiceFactory
from services.registration_service import InitialRequestError, RegistrationService
from services.slot_generator_service import CalendarSlotService
from services.validation_service import ValidationService

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("CLINICEASE_SECRET_KEY") or secrets.token_hex(32)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = (
    os.getenv("CLINICEASE_HTTPS", "").strip().lower() in {"1", "true", "yes"}
)
if not os.getenv("CLINICEASE_SECRET_KEY"):
    app.logger.warning(
        "CLINICEASE_SECRET_KEY is unset; sessions will not persist across restarts."
    )


def send_notifications(notifications):
    if not notifications:
        return None

    try:
        mode = os.getenv("CLINICEASE_NOTIFICATION_MODE", "email")
        notifier = NotificationServiceFactory.create_service(mode=mode)
        for notification in notifications:
            notifier.send_notification(**notification)
    except Exception:
        app.logger.exception("Appointment notification delivery failed.")
        return "The appointment was saved, but an email notification could not be delivered."
    return None


def available_registration_slots():
    conn = get_connection()
    if not conn:
        return [], "Appointment times are temporarily unavailable. Please try again."

    try:
        dashboard = DashboardFactory.create_dashboard("Patient", conn)
        return dashboard.get_slots(), None
    except Exception:
        app.logger.exception("Failed to retrieve available registration slots.")
        return [], "Appointment times are temporarily unavailable. Please try again."
    finally:
        conn.close()


def render_auth_page(
    active_tab="",
    error=None,
    message=None,
    form_data=None,
    status_code=200,
):
    slots, slots_error = available_registration_slots()
    return (
        render_template(
            "login.html",
            active_tab=active_tab,
            error=error,
            message=message,
            form_data=form_data or {},
            initial_request_slots=slots,
            slots_error=slots_error,
        ),
        status_code,
    )


def create_initial_request(data):
    # Figure 2: registration and the first Pending appointment commit together.
    receipt = RegistrationService().create_initial_request(data)
    notifications = [
        {
            "recipient": receipt["email"],
            "subject": "ClinicEase account created and appointment request received",
            "body": (
                f"Hello {receipt['name']}, your ClinicEase account has been created. "
                f"Your appointment request for {receipt['slot_date']} at "
                f"{receipt['slot_time']} was received and is Pending review."
            ),
        },
        *[
            {
                "recipient": recipient,
                "subject": "New appointment request",
                "body": (
                    f"{receipt['name']} created a ClinicEase account and requested an "
                    f"appointment for {receipt['slot_date']} at {receipt['slot_time']}. "
                    "Please review it in ClinicEase."
                ),
            }
            for recipient in receipt["staff_recipients"]
        ],
    ]
    warning = send_notifications(notifications)
    return {
        "status": "success",
        "message": "Account created and appointment request saved as Pending.",
        "warning": warning,
        "patient_id": receipt["patient_id"],
        "name": receipt["name"],
        "email": receipt["email"],
        "contact_number": receipt["contact_number"],
    }


def start_patient_session(user_data):
    session.clear()
    session["user_id"] = user_data["patient_id"]
    session["role"] = "Patient"
    session["name"] = user_data["name"]
    session["email"] = user_data["email"]
    session["contact_number"] = user_data.get("contact_number")


# UI Views
@app.route("/")
def home():
    return render_template("landing_page.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        if "role" in session:
            return redirect(url_for("dashboard"))
        return render_auth_page()

    email = request.form.get("email")
    password = request.form.get("password")

    is_valid, err = ValidationService.validate_login({"email": email, "password": password})
    if not is_valid:
        return render_auth_page(error=err, status_code=400)

    user_obj = User.login(email, password)
    if user_obj:
        session["user_id"] = user_obj.user_id
        session["role"] = user_obj.get_user_role()
        session["name"] = user_obj.name
        session["email"] = user_obj.email
        session["contact_number"] = user_obj.contact_number
        return redirect(url_for("dashboard"))

    return render_auth_page(error="Invalid email or password.", status_code=401)


@app.route("/signup", methods=["GET"])
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "GET":
        if "role" in session:
            return redirect(url_for("dashboard"))
        return render_auth_page(active_tab="create")

    form_data = request.form.to_dict()
    try:
        result = create_initial_request(form_data)
    except InitialRequestError as error:
        return render_auth_page(
            active_tab="create",
            error=str(error),
            form_data=form_data,
            status_code=error.status_code,
        )
    except Exception:
        app.logger.exception("Failed to create initial patient request.")
        return render_auth_page(
            active_tab="create",
            error="The account and appointment request could not be saved. Please try again.",
            form_data=form_data,
            status_code=500,
        )

    message = result["message"]
    if result["warning"]:
        message = f"{message} {result['warning']}"
    start_patient_session(result)
    return redirect(url_for("patient_dashboard_view"))


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    if request.is_json or request.path.startswith("/api/"):
        return jsonify({"status": "success", "message": "Logged out successfully."}), 200
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    # Figure 2: the User subclass determines which dashboard is selected.
    role = session.get("role")
    if not role:
        return redirect(url_for("login_page"))
    if role == "Clinic Staff":
        return redirect(url_for("staff_dashboard_view"))
    return redirect(url_for("patient_dashboard_view"))


@app.route("/patient/dashboard")
def patient_dashboard_view():
    if session.get("role") != "Patient":
        return redirect(url_for("login_page"))

    conn = get_connection()
    if not conn:
        return "Database connection failed", 500

    try:
        dashboard_service = DashboardFactory.create_dashboard("Patient", conn)
        slots = dashboard_service.get_slots()

        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT a.appointment_id, a.purpose, a.status, a.created_at,
                   a.contact_number, s.slot_date, s.time
            FROM appointments a
            JOIN appointment_slots s ON a.slot_id = s.slot_id
            WHERE a.user_id = %s
            ORDER BY s.slot_date ASC, s.time ASC
            """,
            (session.get("user_id"),),
        )
        appointments = cursor.fetchall()
        cursor.close()

        upcoming_appointments = [
            appointment
            for appointment in appointments
            if appointment["status"] in ("Pending", "Confirmed")
            and appointment["slot_date"] >= date.today()
        ]
        upcoming_ids = {
            appointment["appointment_id"] for appointment in upcoming_appointments
        }
        past_appointments = [
            appointment
            for appointment in appointments
            if appointment["appointment_id"] not in upcoming_ids
        ]
        user = {
            "name": session.get("name", "Patient"),
            "email": session.get("email", ""),
            "contact_number": session.get("contact_number", ""),
        }
        return render_template(
            "patient/patient_dashboard.html",
            user=user,
            slots=slots,
            upcoming_appointments=upcoming_appointments,
            past_appointments=past_appointments,
        )
    finally:
        conn.close()


@app.route("/staff/dashboard")
def staff_dashboard_view():
    if session.get("role") != "Clinic Staff":
        return redirect(url_for("login_page"))

    conn = get_connection()
    if not conn:
        return "Database connection failed", 500

    try:
        dashboard_service = DashboardFactory.create_dashboard("Clinic Staff", conn)
        slots = dashboard_service.get_slots()

        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT a.appointment_id, a.purpose, a.status, a.created_at,
                   u.name as patient_name, u.email, a.contact_number,
                   s.slot_date, s.time
            FROM appointments a
            JOIN users u ON a.user_id = u.user_id
            JOIN appointment_slots s ON a.slot_id = s.slot_id
            WHERE a.status = 'Pending'
            ORDER BY a.created_at ASC
            """
        )
        pending_appointments = cursor.fetchall()
        cursor.execute(
            """
            SELECT a.appointment_id, a.purpose, a.status, a.created_at,
                   u.name as patient_name, u.email, a.contact_number,
                   s.slot_date, s.time
            FROM appointments a
            JOIN users u ON a.user_id = u.user_id
            JOIN appointment_slots s ON a.slot_id = s.slot_id
            WHERE a.status = 'Confirmed'
            ORDER BY s.slot_date ASC, s.time ASC
            """
        )
        confirmed_appointments = cursor.fetchall()
        cursor.close()

        for slot in slots:
            slot["slot_date_input"] = slot["slot_date"].isoformat()
            try:
                slot["time_input"] = datetime.strptime(
                    slot["time"], "%I:%M %p"
                ).strftime("%H:%M")
            except ValueError:
                slot["time_input"] = datetime.strptime(
                    slot["time"], "%H:%M"
                ).strftime("%H:%M")

        user = {
            "name": session.get("name", "Clinic Staff"),
            "email": session.get("email", ""),
        }
        return render_template(
            "clinic_staff/staff_dashboard.html",
            user=user,
            slots=slots,
            pending_appointments=pending_appointments,
            confirmed_appointments=confirmed_appointments,
            today=date.today(),
        )
    finally:
        conn.close()


@app.route("/test-panel")
def test_panel():
    return render_template("index.html")


# API Endpoints
@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Incomplete Information."}), 400

    try:
        return jsonify(create_initial_request(data)), 201
    except InitialRequestError as error:
        return jsonify({"status": "error", "message": str(error)}), error.status_code
    except Exception:
        app.logger.exception("Failed to create initial patient request.")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "The account and appointment request could not be saved. Please try again.",
                }
            ),
            500,
        )


@app.route("/api/register_and_book", methods=["POST"])
def api_register_and_book():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid request payload."}), 400

    try:
        result = create_initial_request(data)
    except InitialRequestError as error:
        return jsonify({"status": "error", "message": str(error)}), error.status_code
    except Exception:
        app.logger.exception("Failed to register patient and book initial appointment.")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "The account and appointment request could not be saved. Please try again.",
                }
            ),
            500,
        )

    start_patient_session(result)
    return (
        jsonify(
            {
                "status": "success",
                "message": result["message"],
                "warning": result["warning"],
                "redirect_url": url_for("patient_dashboard_view"),
            }
        ),
        201,
    )


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}

    is_valid, err = ValidationService.validate_login(data)
    if not is_valid:
        return jsonify({"status": "error", "message": err}), 400

    email = data.get("email")
    password = data.get("password")

    user_obj = User.login(email, password)
    if user_obj:
        session["user_id"] = user_obj.user_id
        session["role"] = user_obj.get_user_role()
        session["name"] = user_obj.name
        session["email"] = user_obj.email
        session["contact_number"] = user_obj.contact_number

        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"Welcome Back, {user_obj.name}",
                    "role": session["role"],
                }
            ),
            200,
        )

    return jsonify({"status": "error", "message": "Invalid email or password"}), 401


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"status": "success", "message": "Logged out successfully."}), 200


@app.route("/api/dashboard/slots", methods=["GET"])
def get_dashboard_slots():
    role = session.get("role")
    if not role:
        return (
            jsonify({"status": "error", "message": "Unauthorized. Please log in first."}),
            401,
        )

    conn = get_connection()
    if not conn:
        return jsonify({"status": "error", "message": "Database connection failed"}), 500

    try:
        dashboard_service = DashboardFactory.create_dashboard(role, conn)
        slots = dashboard_service.get_slots()
        return jsonify({"status": "success", "role": role, "slots": slots}), 200
    finally:
        conn.close()


@app.route("/api/slots/book", methods=["POST"])
def book_appointment_slot():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid request payload."}), 400
    patient_id = session.get("user_id")

    if not patient_id or session.get("role") != "Patient":
        return (
            jsonify({"status": "error", "message": "Unauthorized. Please log in as a patient."}),
            401,
        )

    is_valid_payload, err = ValidationService.validate_booking(data)
    if not is_valid_payload:
        return jsonify({"status": "error", "message": err}), 400

    slot_id = int(data.get("slot_id"))
    purpose = data.get("purpose")
    contact_number = data.get("contact_number")
    contact_number = (
        (contact_number.strip() or None)
        if isinstance(contact_number, str)
        else None
    )

    conn = get_connection()
    if not conn:
        return jsonify({"status": "error", "message": "Database connection failed"}), 500

    cursor = None
    try:
        # Pessimistic locking serializes patients competing for this slot.
        conn.autocommit = False
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT *
            FROM appointment_slots
            WHERE slot_id = %s
            FOR UPDATE
            """,
            (slot_id,),
        )
        slot_data = cursor.fetchone()
        if not slot_data:
            conn.rollback()
            return jsonify({"status": "error", "message": "Slot not found."}), 404

        slot = AppointmentSlot(
            slot_id=slot_data["slot_id"],
            slot_date=slot_data["slot_date"],
            time=slot_data["time"],
            status=slot_data["status"],
        )
        if slot.slot_date < date.today():
            conn.rollback()
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "This appointment slot is no longer available. Please select another slot.",
                    }
                ),
                409,
            )
        # Encapsulation: book() validates and updates the model's protected status.
        slot.book()
        cursor.execute(
            """
            UPDATE appointment_slots
            SET status = %s
            WHERE slot_id = %s AND status = 'Available'
            """,
            (slot.status, slot_id),
        )
        if cursor.rowcount != 1:
            raise ValueError(
                "This appointment slot is no longer available. Please select another slot."
            )

        Appointment.create_pending(
            cursor,
            patient_id=patient_id,
            slot_id=slot_id,
            purpose=purpose.strip(),
            contact_number=contact_number,
        )
        cursor.execute("SELECT email FROM users WHERE role = 'Clinic Staff'")
        staff_recipients = [row["email"] for row in cursor.fetchall()]
        conn.commit()

        notification_warning = send_notifications(
            [
                {
                    "recipient": session.get("email", ""),
                    "subject": "Appointment request received",
                    "body": (
                        f"Hello {session.get('name', 'Patient')}, your appointment request "
                        f"for {slot.slot_date} at {slot.time} was received and is Pending review."
                    ),
                },
                *[
                    {
                        "recipient": recipient,
                        "subject": "New appointment request",
                        "body": (
                            f"{session.get('name', 'A patient')} requested an appointment "
                            f"for {slot.slot_date} at {slot.time}. Please review it in ClinicEase."
                        ),
                    }
                    for recipient in staff_recipients
                ],
            ]
        )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Request saved as Pending. Slot status is now Booked.",
                    "warning": notification_warning,
                }
            ),
            200,
        )

    except ValueError as error:
        conn.rollback()
        return jsonify({"status": "error", "message": str(error)}), 409
    except Exception:
        conn.rollback()
        app.logger.exception("Failed to book appointment slot %s.", slot_id)
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "The appointment could not be saved. Please try again.",
                }
            ),
            500,
        )
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


@app.route("/api/staff/appointments/pending", methods=["GET"])
def get_pending_appointments():
    if session.get("role") != "Clinic Staff":
        return jsonify({"status": "error", "message": "Unauthorized."}), 401

    conn = get_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB failed"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT a.appointment_id, a.purpose, a.status, u.name as patient_name,
                   u.email, a.contact_number, s.slot_date, s.time
            FROM appointments a
            JOIN users u ON a.user_id = u.user_id
            JOIN appointment_slots s ON a.slot_id = s.slot_id
            WHERE a.status = 'Pending'
            ORDER BY a.created_at ASC
        """
        cursor.execute(query)
        appointments = cursor.fetchall()
        return jsonify({"status": "success", "appointments": appointments}), 200
    finally:
        cursor.close()
        conn.close()


@app.route("/api/staff/blocked_dates", methods=["POST"])
def create_blocked_date():
    if session.get("role") != "Clinic Staff":
        return jsonify({"status": "error", "message": "Unauthorized."}), 401

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid request payload."}), 400

    raw_date = data.get("blocked_date", data.get("date"))
    reason = data.get("reason", "Clinic closed")
    try:
        blocked_date = date.fromisoformat(raw_date)
    except (TypeError, ValueError):
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Enter the clinic closure date in YYYY-MM-DD format.",
                }
            ),
            400,
        )

    if not isinstance(reason, str) or not reason.strip() or len(reason.strip()) > 255:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Closure reason is required and must be 255 characters or fewer.",
                }
            ),
            400,
        )
    if blocked_date < date.today():
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "A past date cannot be added as a clinic closure.",
                }
            ),
            400,
        )

    conn = get_connection()
    if not conn:
        return jsonify({"status": "error", "message": "Database connection failed."}), 500

    cursor = None
    try:
        conn.autocommit = False
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO blocked_dates (blocked_date, reason)
            VALUES (%s, %s)
            """,
            (blocked_date, reason.strip()),
        )
        # Do not cancel booked appointments; remove newly-blocked open times from patient view.
        cursor.execute(
            """
            UPDATE appointment_slots
            SET status = 'Disabled'
            WHERE slot_date = %s AND status = 'Available'
            """,
            (blocked_date,),
        )
        disabled_count = cursor.rowcount
        conn.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Clinic closure saved.",
                    "disabled_slots": disabled_count,
                }
            ),
            201,
        )
    except mysql.connector.IntegrityError:
        conn.rollback()
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "That date is already marked as a clinic closure.",
                }
            ),
            409,
        )
    except Exception:
        conn.rollback()
        app.logger.exception("Failed to save clinic closure for %s.", blocked_date)
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "The clinic closure could not be saved.",
                }
            ),
            500,
        )
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


@app.route("/api/slots/generate", methods=["POST"])
def generate_monthly_slots():
    if session.get("role") != "Clinic Staff":
        return jsonify({"status": "error", "message": "Unauthorized."}), 401

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid request payload."}), 400

    year = data.get("year")
    month = data.get("month")
    if (
        isinstance(year, bool)
        or not isinstance(year, int)
        or isinstance(month, bool)
        or not isinstance(month, int)
    ):
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Year and month must be integers.",
                }
            ),
            400,
        )

    try:
        inserted_count = CalendarSlotService().generate_slots_for_month(year, month)
    except ValueError as error:
        return jsonify({"status": "error", "message": str(error)}), 400
    except RuntimeError as error:
        return jsonify({"status": "error", "message": str(error)}), 503
    except Exception:
        app.logger.exception("Failed to generate slots for %s-%02d.", year, month)
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Appointment slots could not be generated.",
                }
            ),
            500,
        )

    return (
        jsonify(
            {
                "status": "success",
                "message": f"Generated {inserted_count} new appointment slots.",
                "inserted": inserted_count,
            }
        ),
        200,
    )


@app.route("/api/staff/appointments/<int:appt_id>/action", methods=["POST"])
def staff_appointment_action(appt_id):
    if session.get("role") != "Clinic Staff":
        return jsonify({"status": "error", "message": "Unauthorized."}), 401

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid request payload."}), 400
    action = data.get("action")

    if action not in ["confirm", "cancel", "complete"]:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Invalid action. Choose confirm, cancel, or complete.",
                }
            ),
            400,
        )

    appt_data = Appointment.fetch_by_id(appt_id)
    if not appt_data:
        return jsonify({"status": "error", "message": "Appointment not found."}), 404

    conn = get_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB failed"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        # Figure 2: staff review branches to Confirmed or Cancelled; only Confirmed completes.
        appt = Appointment(
            appointment_id=appt_data["appointment_id"],
            patient_id=appt_data["user_id"],
            slot_id=appt_data["slot_id"],
            purpose=appt_data["purpose"],
            status=appt_data["status"],
        )

        if action == "confirm":
            appt.confirm()
            new_status = "Confirmed"
        elif action == "cancel":
            appt.cancel()
            new_status = "Cancelled"

            cursor.execute(
                "SELECT slot_date FROM appointment_slots WHERE slot_id = %s FOR UPDATE",
                (appt.slot_id,),
            )
            slot_data = cursor.fetchone()
            if not slot_data:
                raise ValueError("The appointment time no longer exists.")
            cursor.execute(
                """
                UPDATE appointment_slots
                SET status = CASE
                    WHEN EXISTS (
                        SELECT 1 FROM blocked_dates
                        WHERE blocked_date = %s
                    ) THEN 'Disabled'
                    ELSE 'Available'
                END
                WHERE slot_id = %s
                """,
                (slot_data["slot_date"], appt.slot_id),
            )
        else:
            appt.complete()
            new_status = "Completed"

        cursor.execute(
            """
            UPDATE appointments
            SET status = %s
            WHERE appointment_id = %s AND status = %s
            """,
            (new_status, appt_id, appt_data["status"]),
        )
        if cursor.rowcount != 1:
            conn.rollback()
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "This appointment was updated by someone else. Refresh and try again.",
                    }
                ),
                409,
            )
        conn.commit()

        notification_warning = send_notifications(
            [
                {
                    "recipient": appt_data["email"],
                    "subject": f"Appointment {new_status}",
                    "body": (
                        f"Dear {appt_data['patient_name']}, your appointment has been "
                        f"{new_status.lower()}."
                    ),
                }
            ]
        )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"Appointment {new_status} successfully.",
                    "warning": notification_warning,
                }
            ),
            200,
        )

    except ValueError as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/api/staff/slots/<int:slot_id>", methods=["PATCH", "DELETE"])
def manage_staff_slot(slot_id):
    if session.get("role") != "Clinic Staff":
        return jsonify({"status": "error", "message": "Unauthorized."}), 401

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid request payload."}), 400
    action = data.get("action")
    conn = get_connection()
    if not conn:
        return jsonify({"status": "error", "message": "Database connection failed."}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        if request.method == "PATCH" and action == "update":
            try:
                slot_date = date.fromisoformat(data.get("slot_date", ""))
                parsed_time = datetime.strptime(data.get("time", ""), "%H:%M")
                slot_time = parsed_time.strftime("%I:%M %p")
            except (TypeError, ValueError):
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "Enter a valid appointment date and time.",
                        }
                    ),
                    400,
                )

            if datetime.combine(slot_date, parsed_time.time()) < datetime.now():
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "Appointment times cannot be moved into the past.",
                        }
                    ),
                    400,
                )

            cursor.execute(
                "SELECT 1 FROM blocked_dates WHERE blocked_date = %s",
                (slot_date,),
            )
            if cursor.fetchone():
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "An appointment time cannot be moved onto a clinic closure date.",
                        }
                    ),
                    409,
                )

            cursor.execute(
                """
                SELECT slot_id FROM appointment_slots
                WHERE slot_date = %s AND time = %s AND slot_id != %s
                LIMIT 1
                """,
                (slot_date, slot_time, slot_id),
            )
            if cursor.fetchone():
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "An appointment time already exists at that date and time.",
                        }
                    ),
                    409,
                )

            cursor.execute(
                """
                UPDATE appointment_slots
                SET slot_date = %s, time = %s
                WHERE slot_id = %s
                  AND status IN ('Available', 'Unavailable', 'Disabled')
                  AND NOT EXISTS (
                      SELECT 1 FROM appointments WHERE appointments.slot_id = %s
                  )
                """,
                (slot_date, slot_time, slot_id, slot_id),
            )
            if cursor.rowcount != 1:
                conn.rollback()
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "This time cannot be changed because it is booked or has appointment history.",
                        }
                    ),
                    409,
                )
            conn.commit()
            return jsonify({"status": "success", "message": "Appointment time updated."}), 200

        if request.method == "DELETE" and action == "delete":
            cursor.execute(
                """
                DELETE FROM appointment_slots
                WHERE slot_id = %s
                  AND status IN ('Available', 'Unavailable', 'Disabled')
                  AND NOT EXISTS (
                      SELECT 1 FROM appointments WHERE appointments.slot_id = %s
                  )
                """,
                (slot_id, slot_id),
            )
            if cursor.rowcount != 1:
                conn.rollback()
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "This time cannot be removed because it is booked or has appointment history.",
                        }
                    ),
                    409,
                )
            conn.commit()
            return jsonify({"status": "success", "message": "Appointment time removed."}), 200

        if request.method == "PATCH" and action in ("enable", "disable"):
            new_status = "Available" if action == "enable" else "Disabled"
            if action == "enable":
                cursor.execute(
                    """
                    SELECT s.slot_date,
                           EXISTS (
                               SELECT 1 FROM blocked_dates b
                               WHERE b.blocked_date = s.slot_date
                           ) AS is_blocked
                    FROM appointment_slots s
                    WHERE s.slot_id = %s
                    FOR UPDATE
                    """,
                    (slot_id,),
                )
                slot_data = cursor.fetchone()
                if not slot_data:
                    conn.rollback()
                    return (
                        jsonify(
                            {"status": "error", "message": "Appointment time not found."}
                        ),
                        404,
                    )
                if slot_data["is_blocked"]:
                    conn.rollback()
                    return (
                        jsonify(
                            {
                                "status": "error",
                                "message": "A slot on a clinic closure date cannot be enabled.",
                            }
                        ),
                        409,
                    )
            cursor.execute(
                """
                UPDATE appointment_slots
                SET status = %s
                WHERE slot_id = %s AND status IN ('Available', 'Unavailable', 'Disabled')
                """,
                (new_status, slot_id),
            )
            if cursor.rowcount != 1:
                conn.rollback()
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "This appointment time cannot be changed.",
                        }
                    ),
                    409,
                )
            conn.commit()
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": f"Appointment time {new_status.lower()}.",
                    }
                ),
                200,
            )

        return (
            jsonify({"status": "error", "message": "Invalid appointment time action."}),
            400,
        )
    except Exception as error:
        conn.rollback()
        return jsonify({"status": "error", "message": str(error)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/api/staff/report", methods=["GET"])
def get_staff_appointment_report():
    if session.get("role") != "Clinic Staff":
        return jsonify({"status": "error", "message": "Unauthorized."}), 401

    conn = get_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB failed"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT a.appointment_id, a.purpose, a.status, u.name as patient_name,
                   s.slot_date, s.time
            FROM appointments a
            JOIN users u ON a.user_id = u.user_id
            JOIN appointment_slots s ON a.slot_id = s.slot_id
            ORDER BY a.appointment_id ASC
            """
        )
        appointments = cursor.fetchall()

        report_generator = generate_appointment_report(appointments)
        report_lines = list(report_generator)

        return (
            jsonify(
                {
                    "status": "success",
                    "total": len(report_lines),
                    "report": report_lines,
                }
            ),
            200,
        )
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
