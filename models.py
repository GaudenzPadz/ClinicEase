from database import get_connection
import hashlib
from abc import ABC, abstractmethod


class PasswordHasherAdapter:
    """
    Adapter Pattern: Encapsulates and standardizes password hashing
    and verification logic, separating it from the core User entity.
    """

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


class User:
    def __init__(self, user_id, name, email, password_hashed):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.__password_hashed = password_hashed  # Private attribute

    def get_password_hash(self):
        return self.__password_hashed

    def set_password(self, password):
        self.__password_hashed = PasswordHasherAdapter.hash_password(password)

    def get_user_role(self):
        return "TEST USER"

    @staticmethod
    def login(email, password):
        conn = get_connection()
        if conn is None:
            return None

        cursor = conn.cursor(dictionary=True)
        password_hash = PasswordHasherAdapter.hash_password(password)

        query = "SELECT * FROM users WHERE email = %s AND password_hash = %s"
        cursor.execute(query, (email, password_hash))
        user_data = cursor.fetchone()

        cursor.close()
        conn.close()

        if user_data:
            role = user_data["role"]
            if role == "Patient":
                return Patient(
                    user_data["user_id"],
                    user_data["name"],
                    user_data["email"],
                    user_data["password_hash"],
                )
            elif role == "Clinic Staff":
                return ClinicStaff(
                    user_data["user_id"],
                    user_data["name"],
                    user_data["email"],
                    user_data["password_hash"],
                )

        return None


class Patient(User):
    def get_user_role(self):
        return "Patient"


class ClinicStaff(User):
    def get_user_role(self):
        return "Clinic Staff"


class AppointmentSlot:
    """
    Encapsulates slot data and protects state changes.
    Invalid state transitions (e.g., booking an already booked slot) are rejected.
    """

    def __init__(self, slot_id, slot_date, time, status="Available"):
        self.slot_id = slot_id
        self.slot_date = slot_date
        self.time = time
        self.__status = status  # Protected/private attribute

    @property
    def status(self):
        return self.__status

    def book(self):
        """
        Controlled method to protect object state.
        Rejects invalid state changes if the slot is no longer available.
        """
        if self.__status != "Available":
            raise ValueError(
                "This appointment slot is no longer available. Please select another slot."
            )

        self.__status = "Booked"
        return True


class Appointment:
    def __init__(
        self,
        appointment_id=None,
        patient_id=None,
        slot_id=None,
        purpose=None,
        status="Pending",
    ):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.slot_id = slot_id
        self.purpose = purpose
        self.status = status

    def send_notification(self, message_type):
        print(
            f"Sending email notification ({message_type}) to patient... DEBUG FEATURE"
        )


class BaseDashboard(ABC):
    """
    Abstract Base Class defining the service layer contract
    for fetching appointment slots based on user privileges.
    """

    @abstractmethod
    def get_slots(self):
        pass


class PatientDashboard(BaseDashboard):
    """Concrete implementation for Patients: returns only Available slots."""

    def __init__(self, db_connection):
        self.db = db_connection

    def get_slots(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM appointment_slots WHERE status = 'Available'")
        slots = cursor.fetchall()
        cursor.close()
        return slots


class StaffDashboard(BaseDashboard):
    """Concrete implementation for Clinic Staff: returns all slots and their statuses."""

    def __init__(self, db_connection):
        self.db = db_connection

    def get_slots(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM appointment_slots")
        slots = cursor.fetchall()
        cursor.close()
        return slots


class DashboardFactory:
    """
    Factory Pattern: Dynamically creates and returns the correct
    dashboard object based on the user's role.
    """

    @staticmethod
    def create_dashboard(user_role, db_connection):
        if user_role == "Patient":
            return PatientDashboard(db_connection)
        elif user_role == "Clinic Staff":
            return StaffDashboard(db_connection)
        else:
            raise ValueError(f"Unknown user role: {user_role}")
