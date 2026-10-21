import mysql.connector

from database import get_connection
from models.appointment import Appointment
from models.slot import AppointmentSlot
from models.user import PasswordHasherAdapter, Patient
from services.validation_service import ValidationService
from services.validation_strategy import (
    RegistrationBookingValidationStrategy,
    StandardValidationStrategy,
)


class InitialRequestError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


class RegistrationService:
    """Creates a patient account and its first appointment in one transaction."""

    def __init__(
        self,
        connection_factory=None,
        validation_strategy=None,
        slot_validation_strategy=None,
    ):
        self.connection_factory = connection_factory or get_connection
        self.validation_strategy = (
            validation_strategy or RegistrationBookingValidationStrategy()
        )
        self.slot_validation_strategy = (
            slot_validation_strategy or StandardValidationStrategy()
        )

    def create_initial_request(self, data):
        is_valid, error = ValidationService.validate_initial_request(data)
        if not is_valid:
            raise InitialRequestError(error or "Incomplete Information.")

        name = data["name"].strip()
        email = data["email"].strip()
        password = data["password"]
        purpose = data["purpose"].strip()
        slot_id = int(data["slot_id"])
        raw_contact_number = data.get("contact_number")
        contact_number = (
            raw_contact_number.strip()
            if isinstance(raw_contact_number, str) and raw_contact_number.strip()
            else None
        )
        password_hash = PasswordHasherAdapter.hash_password(password)

        conn = self.connection_factory()
        if not conn:
            raise InitialRequestError(
                "The appointment service is temporarily unavailable. Please try again.",
                503,
            )

        cursor = None
        try:
            conn.autocommit = False
            conn.start_transaction()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            email_available = cursor.fetchone() is None

            # Lock the database row before validating or changing its encapsulated state.
            cursor.execute(
                """
                SELECT slot_id, slot_date, time, status
                FROM appointment_slots
                WHERE slot_id = %s
                FOR UPDATE
                """,
                (slot_id,),
            )
            slot_data = cursor.fetchone()
            if not slot_data:
                raise InitialRequestError(
                    "This appointment slot is no longer available. Please select another slot.",
                    409,
                )
            slot = AppointmentSlot(
                slot_id=slot_data["slot_id"],
                slot_date=slot_data["slot_date"],
                time=slot_data["time"],
                status=slot_data["status"],
            )

            is_valid, error = self.validation_strategy.validate(
                email_available=email_available,
                slot=slot,
            )
            if not is_valid:
                raise InitialRequestError(error or "The request could not be validated.", 409)

            is_valid, error = self.slot_validation_strategy.validate(
                patient_id=None,
                slot=slot,
            )
            if not is_valid:
                raise InitialRequestError(
                    error or "The appointment slot is not available.",
                    409,
                )

            # Encapsulation: update the model's protected state only through book().
            slot.book()

            try:
                patient_id = Patient.create_with_hash(
                    cursor,
                    name=name,
                    email=email,
                    contact_number=contact_number,
                    password_hash=password_hash,
                )
            except mysql.connector.IntegrityError as error:
                raise InitialRequestError(
                    "This email is already registered.",
                    409,
                ) from error

            Appointment.create_pending(
                cursor,
                patient_id=patient_id,
                slot_id=slot.slot_id,
                purpose=purpose,
                contact_number=contact_number,
            )
            cursor.execute(
                """
                UPDATE appointment_slots
                SET status = %s
                WHERE slot_id = %s AND status = 'Available'
                """,
                (slot.status, slot.slot_id),
            )
            if cursor.rowcount != 1:
                raise InitialRequestError(
                    "This appointment slot is no longer available. Please select another slot.",
                    409,
                )

            cursor.execute("SELECT email FROM users WHERE role = 'Clinic Staff'")
            staff_recipients = [row["email"] for row in cursor.fetchall()]
            conn.commit()

            return {
                "patient_id": patient_id,
                "name": name,
                "email": email,
                "contact_number": contact_number,
                "slot_date": slot.slot_date,
                "slot_time": slot.time,
                "staff_recipients": staff_recipients,
            }
        except InitialRequestError:
            conn.rollback()
            raise
        except ValueError as error:
            conn.rollback()
            raise InitialRequestError(str(error), 409) from error
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()
