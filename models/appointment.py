from database import get_connection


# Encapsulation: Status management with property and validation setter
class Appointment:
    VALID_STATUSES = ["Pending", "Confirmed", "Cancelled", "Completed"]
    ALLOWED_TRANSITIONS = {
        "Pending": {"Confirmed", "Cancelled"},
        "Confirmed": {"Completed", "Cancelled"},
        "Cancelled": set(),
        "Completed": set(),
    }

    def __init__(
        self,
        appointment_id: int = None,
        patient_id: int = None,
        slot_id: int = None,
        purpose: str = None,
        status: str = "Pending",
    ):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.slot_id = slot_id
        self.purpose = purpose
        self.__status = None
        self.status = status

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, new_status: str):
        if new_status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status: '{new_status}'. Allowed values: {self.VALID_STATUSES}"
            )

        if (
            self.__status is not None
            and new_status != self.__status
            and new_status not in self.ALLOWED_TRANSITIONS[self.__status]
        ):
            raise ValueError(
                f"Appointment cannot transition from {self.__status} to {new_status}."
            )

        self.__status = new_status

    def confirm(self):
        if self.__status != "Pending":
            raise ValueError("Only Pending appointments can be confirmed.")
        self.status = "Confirmed"

    def cancel(self):
        if self.__status not in ("Pending", "Confirmed"):
            raise ValueError("Only Pending or Confirmed appointments can be cancelled.")
        self.status = "Cancelled"

    def complete(self):
        if self.__status != "Confirmed":
            raise ValueError("Only Confirmed appointments can be marked as Completed.")
        self.status = "Completed"

    @classmethod
    def create_pending(
        cls,
        cursor,
        patient_id: int,
        slot_id: int,
        purpose: str,
        contact_number=None,
    ) -> int:
        appointment = cls(
            patient_id=patient_id,
            slot_id=slot_id,
            purpose=purpose,
            status="Pending",
        )
        cursor.execute(
            """
            INSERT INTO appointments (user_id, slot_id, purpose, contact_number, status)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (patient_id, slot_id, purpose, contact_number, appointment.status),
        )
        return cursor.lastrowid

    @staticmethod
    def fetch_by_id(appointment_id: int):
        conn = get_connection()
        if not conn:
            return None

        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT a.*, u.email, u.name as patient_name 
                FROM appointments a 
                JOIN users u ON a.user_id = u.user_id 
                WHERE a.appointment_id = %s
            """
            cursor.execute(query, (appointment_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
