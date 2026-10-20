from database import get_connection


# Encapsulation: Status management with property and validation setter
class Appointment:
    VALID_STATUSES = ["Pending", "Confirmed", "Cancelled", "Completed"]

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

        if self.__status is not None:
            if self.__status == "Completed":
                raise ValueError("Cannot modify an appointment that is already Completed.")
            if self.__status == "Cancelled":
                raise ValueError("Cannot modify an appointment that is already Cancelled.")
            if self.__status == "Pending" and new_status == "Completed":
                raise ValueError("Pending appointments must be Confirmed before being marked Completed.")

        self.__status = new_status

    def confirm(self):
        if self.__status != "Pending":
            raise ValueError("Only Pending appointments can be confirmed.")
        self.status = "Confirmed"

    def cancel(self):
        if self.__status == "Completed":
            raise ValueError("Cannot cancel a completed appointment.")
        self.status = "Cancelled"

    def complete(self):
        if self.__status != "Confirmed":
            raise ValueError("Only Confirmed appointments can be marked as Completed.")
        self.status = "Completed"

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
