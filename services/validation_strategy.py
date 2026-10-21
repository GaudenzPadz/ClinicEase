from abc import ABC, abstractmethod
from typing import Tuple, Optional
from models.slot import AppointmentSlot
from database import get_connection


# Strategy Pattern: Validation contract for booking attempts
class BookingValidationStrategy(ABC):
    @abstractmethod
    def validate(
        self, patient_id: Optional[int], slot: Optional[AppointmentSlot], db_connection=None
    ) -> Tuple[bool, Optional[str]]:
        pass


class StandardValidationStrategy(BookingValidationStrategy):
    def validate(
        self, patient_id: Optional[int], slot: Optional[AppointmentSlot], db_connection=None
    ) -> Tuple[bool, Optional[str]]:
        if not slot or not slot.is_available():
            return False, "This appointment slot is no longer available. Please select another slot."
        return True, None


class RegistrationBookingValidationStrategy:
    """Validates the database-dependent branches of the combined sign-up flow."""

    def validate(
        self, email_available: bool, slot: Optional[AppointmentSlot]
    ) -> Tuple[bool, Optional[str]]:
        if not email_available:
            return False, "This email is already registered."
        if not slot or not slot.is_available():
            return (
                False,
                "This appointment slot is no longer available. Please select another slot.",
            )
        return True, None


class StrictValidationStrategy(BookingValidationStrategy):
    def validate(
        self, patient_id: Optional[int], slot: Optional[AppointmentSlot], db_connection=None
    ) -> Tuple[bool, Optional[str]]:
        if not slot or not slot.is_available():
            return False, "This appointment slot is no longer available. Please select another slot."
        if patient_id is None:
            return False, "Patient information is required for booking validation."

        conn = db_connection or get_connection()
        if not conn:
            return False, "Database connection unavailable for validation."

        should_close = db_connection is None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT appointment_id FROM appointments 
                WHERE user_id = %s AND status = 'Pending'
                """,
                (patient_id,),
            )
            existing_pending = cursor.fetchone()
            if existing_pending:
                return (
                    False,
                    "You already have a Pending appointment request. Please wait for staff review before requesting another.",
                )
            return True, None
        finally:
            cursor.close()
            if should_close:
                conn.close()
