from flask import Flask, jsonify, session, request, render_template
from database import get_connection
from models import User, DashboardFactory, AppointmentSlot

app = Flask(__name__)
app.secret_key = "secured_key_for_some_reasons"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Authenticate user using the User model and PasswordHasherAdapter
    user_obj = User.login(email, password)
    if user_obj:
        session["user_id"] = user_obj.user_id
        session["role"] = user_obj.get_user_role()

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


@app.route("/api/dashboard/slots", methods=["GET"])
def get_dashboard_slots():
    """
    Demonstrates the DashboardFactory and Service Layer:
    Uses the role stored in the session to fetch the appropriate slots.
    """
    role = session.get("role")
    if not role:
        return (
            jsonify(
                {"status": "error", "message": "Unauthorized. Please log in first."}
            ),
            401,
        )

    conn = get_connection()
    if not conn:
        return (
            jsonify({"status": "error", "message": "Database connection failed"}),
            500,
        )

    try:
        # Creational Pattern in action: Factory creates the matching dashboard
        dashboard = DashboardFactory.create_dashboard(role, conn)
        slots = dashboard.get_slots()

        return jsonify({"status": "success", "role": role, "slots": slots}), 200
    finally:
        conn.close()


@app.route("/api/slots/book", methods=["POST"])
def book_appointment_slot():
    """
    Demonstrates protected state change and error handling:
    1. Fetches the slot from the database.
    2. Instantiates the AppointmentSlot object.
    3. Calls slot.book() which protects object state and rejects invalid changes.
    """
    data = request.get_json()
    slot_id = data.get("slot_id")
    patient_id = session.get("user_id")

    # Ensure user is logged in
    if not patient_id or session.get("role") != "Patient":
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Unauthorized. Please log in as a patient.",
                }
            ),
            401,
        )

    conn = get_connection()
    if not conn:
        return (
            jsonify({"status": "error", "message": "Database connection failed"}),
            500,
        )

    cursor = conn.cursor(dictionary=True)

    try:
        # 1. Fetch the slot from the database
        cursor.execute("SELECT * FROM appointment_slots WHERE slot_id = %s", (slot_id,))
        slot_data = cursor.fetchone()

        if not slot_data:
            return jsonify({"status": "error", "message": "Slot not found."}), 404

        # 2. Instantiate the AppointmentSlot object
        slot = AppointmentSlot(
            slot_id=slot_data["slot_id"],
            slot_date=slot_data["slot_date"],
            time=slot_data["time"],
            status=slot_data["status"],
        )

        # 3. Attempt to book (triggers state protection logic)
        # This will raise a ValueError if the slot is no longer "Available"
        slot.book()

        # 4. If valid, update the database state and save appointment as Pending
        update_query = (
            "UPDATE appointment_slots SET status = 'Booked' WHERE slot_id = %s"
        )
        cursor.execute(update_query, (slot_id,))

        insert_appt_query = """
            INSERT INTO appointments (user_id, slot_id, purpose, status) 
            VALUES (%s, %s, %s, 'Pending')
        """
        cursor.execute(
            insert_appt_query,
            (patient_id, slot_id, data.get("purpose", "General Checkup")),
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
        return jsonify({"status": "error", "message": str(e)}), 400

    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
