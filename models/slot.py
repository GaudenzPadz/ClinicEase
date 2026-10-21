from database import get_connection


# Encapsulation: State protection and concurrency control
class AppointmentSlot:
    VALID_STATUSES = ["Available", "Booked", "Unavailable", "Disabled"]

    def __init__(
        self,
        slot_id: int = None,
        slot_date: str = None,
        time: str = None,
        status: str = "Available",
    ):
        self.slot_id = slot_id
        self.slot_date = slot_date
        self.time = time
        self.__status = None
        self.status = status

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, value: str):
        if value not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid slot status: '{value}'. Must be one of {self.VALID_STATUSES}."
            )
        self.__status = value

    def is_available(self) -> bool:
        return self.__status == "Available"

    def book(self) -> bool:
        if not self.is_available():
            raise ValueError(
                "This appointment slot is no longer available. Please select another slot."
            )
        self.status = "Booked"
        return True

    def book_atomically(self, cursor) -> bool:
        """Claim the slot only if it is still Available in the database."""
        if not self.is_available():
            raise ValueError(
                "This appointment slot is no longer available. Please select another slot."
            )

        cursor.execute(
            """
            UPDATE appointment_slots
            SET status = 'Booked'
            WHERE slot_id = %s
              AND status = 'Available'
              AND slot_date >= CURRENT_DATE
            """,
            (self.slot_id,),
        )
        if cursor.rowcount != 1:
            raise ValueError(
                "This appointment slot is no longer available. Please select another slot."
            )

        self.status = "Booked"
        return True

    def release(self) -> bool:
        self.status = "Available"
        return True

    def disable(self) -> bool:
        self.status = "Disabled"
        return True

    def to_dict(self) -> dict:
        return {
            "slot_id": self.slot_id,
            "slot_date": str(self.slot_date) if self.slot_date else None,
            "time": self.time,
            "status": self.status,
        }

    @staticmethod
    def fetch_by_id(slot_id: int):
        conn = get_connection()
        if not conn:
            return None

        cursor = conn.cursor(dictionary=True)
        try:
            return AppointmentSlot.fetch_with_cursor(cursor, slot_id)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def fetch_with_cursor(cursor, slot_id: int):
        cursor.execute(
            """
            SELECT slot_id, slot_date, time, status
            FROM appointment_slots
            WHERE slot_id = %s
            """,
            (slot_id,),
        )
        slot_data = cursor.fetchone()
        if not slot_data:
            return None

        return AppointmentSlot(
            slot_id=slot_data["slot_id"],
            slot_date=slot_data["slot_date"],
            time=slot_data["time"],
            status=slot_data["status"],
        )
