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
from models.user import User, PasswordHasherAdapter
from models.slot import AppointmentSlot
from models.appointment import Appointment
from models.reports import generate_appointment_report
from services.dashboard_service import DashboardFactory
from services.notification_service import NotificationServiceFactory
from services.validation_strategy import (
    StandardValidationStrategy,
    StrictValidationStrategy,
)
from services.validation_service import ValidationService

app = Flask(__name__)
app.secret_key = "secured_key_for_clinicease_system"


# UI Views
@app.route("/")
def home():
    return render_template("landing_page.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        if "role" in session:
            return redirect(url_for("dashboard"))
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    is_valid, err = ValidationService.validate_login({"email": email, "password": password})
    if not is_valid:
        return render_template("login.html", error=err), 400

    user_obj = User.login(email, password)
    if user_obj:
        session["user_id"] = user_obj.user_id
        session["role"] = user_obj.get_user_role()
        session["name"] = user_obj.name
        session["email"] = user_obj.email
        return redirect(url_for("dashboard"))

    return render_template("login.html", error="Invalid email or password."), 401


@app.route("/signup", methods=["GET"])
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "GET":
        if "role" in session:
            return redirect(url_for("dashboard"))
        return render_template("signup.html")

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    is_valid, err = ValidationService.validate_registration(
        {"name": name, "email": email, "password": password}
    )
    if not is_valid:
        return render_template("signup.html", error=err), 400

    conn = get_connection()
    if not conn:
        return render_template("signup.html", error="Database connection failed."), 500

    cursor = conn.cursor()
    try:
        hashed_password = PasswordHasherAdapter.hash_password(password)
        query = """
            INSERT INTO users (name, email, password_hash, role) 
            VALUES (%s, %s, %s, 'Patient')
        """
        cursor.execute(query, (name, email, hashed_password))
        conn.commit()

        return render_template(
            "login.html",
            message="Account created successfully! Please sign in with your credentials.",
        )
    except mysql.connector.IntegrityError:
        return render_template(
            "signup.html", error="An account with this email already exists."
        ), 409
    except Exception as e:
        return render_template("signup.html", error=str(e)), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    if request.is_json or request.path.startswith("/api/"):
        return jsonify({"status": "success", "message": "Logged out successfully."}), 200
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
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
                   s.slot_date, s.time
            FROM appointments a
            JOIN appointment_slots s ON a.slot_id = s.slot_id
            WHERE a.user_id = %s
            ORDER BY a.created_at DESC
            """,
            (session.get("user_id"),),
        )
        appointments = cursor.fetchall()
        cursor.close()

        user = {
            "name": session.get("name", "Patient"),
            "email": session.get("email", ""),
        }
        return render_template(
            "patient_dashboard.html", user=user, slots=slots, appointments=appointments
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
                   u.name as patient_name, u.email,
                   s.slot_date, s.time
            FROM appointments a
            JOIN users u ON a.user_id = u.user_id
            JOIN appointment_slots s ON a.slot_id = s.slot_id
            WHERE a.status = 'Pending'
            ORDER BY a.created_at ASC
            """
        )
        pending_appointments = cursor.fetchall()
        cursor.close()

        user = {
            "name": session.get("name", "Clinic Staff"),
            "email": session.get("email", ""),
        }
        return render_template(
            "staff_dashboard.html",
            user=user,
            slots=slots,
            pending_appointments=pending_appointments,
        )
    finally:
        conn.close()


@app.route("/test-panel")
def test_panel():
    return render_template("index.html")


# API Endpoints
@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json() or {}

    is_valid, err = ValidationService.validate_registration(data)
    if not is_valid:
        return jsonify({"status": "error", "message": err}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    if not conn:
        return jsonify({"status": "error", "message": "Database connection failed."}), 500

    cursor = conn.cursor()
    try:
        hashed_password = PasswordHasherAdapter.hash_password(password)
        query = """
            INSERT INTO users (name, email, password_hash, role) 
            VALUES (%s, %s, %s, 'Patient')
        """
        cursor.execute(query, (name, email, hashed_password))
        conn.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Account created successfully! Please log in.",
                }
            ),
            201,
        )

    except mysql.connector.IntegrityError:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "An account with this email already exists.",
                }
            ),
            409,
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


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
    data = request.get_json() or {}
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
    purpose = data.get("purpose", "General Checkup") or "General Checkup"

    slot = AppointmentSlot.fetch_by_id(slot_id)
    if not slot:
        return jsonify({"status": "error", "message": "Slot not found."}), 404

    validation_strategy = StandardValidationStrategy()
    is_valid, validation_msg = validation_strategy.validate(patient_id, slot)
    if not is_valid:
        return jsonify({"status": "error", "message": validation_msg}), 400

    conn = get_connection()
    if not conn:
        return jsonify({"status": "error", "message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        slot.book()

        cursor.execute(
            "UPDATE appointment_slots SET status = 'Booked' WHERE slot_id = %s",
            (slot_id,),
        )

        cursor.execute(
            """
            INSERT INTO appointments (user_id, slot_id, purpose, status) 
            VALUES (%s, %s, %s, 'Pending')
            """,
            (patient_id, slot_id, purpose),
        )
        conn.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Request saved as Pending. Slot status is now Booked.",
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
            SELECT a.appointment_id, a.purpose, a.status, u.name as patient_name, u.email, 
                   s.slot_date, s.time 
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


@app.route("/api/staff/appointments/<int:appt_id>/action", methods=["POST"])
def staff_appointment_action(appt_id):
    if session.get("role") != "Clinic Staff":
        return jsonify({"status": "error", "message": "Unauthorized."}), 401

    data = request.get_json() or {}
    action = data.get("action")

    if action not in ["confirm", "cancel"]:
        return jsonify({"status": "error", "message": "Invalid action. Must be 'confirm' or 'cancel'."}), 400

    appt_data = Appointment.fetch_by_id(appt_id)
    if not appt_data:
        return jsonify({"status": "error", "message": "Appointment not found."}), 404

    conn = get_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB failed"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
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
        else:
            appt.cancel()
            new_status = "Cancelled"

            cursor.execute(
                "UPDATE appointment_slots SET status = 'Available' WHERE slot_id = %s",
                (appt.slot_id,),
            )

        cursor.execute(
            "UPDATE appointments SET status = %s WHERE appointment_id = %s",
            (new_status, appt_id),
        )
        conn.commit()

        notifier = NotificationServiceFactory.create_service(mode="console")
        notifier.send_notification(
            recipient=appt_data["email"],
            subject=f"Appointment {new_status}",
            body=f"Dear {appt_data['patient_name']}, your appointment has been {new_status.lower()}.",
        )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"Appointment {new_status} successfully.",
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
