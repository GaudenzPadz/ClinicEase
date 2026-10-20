from abc import ABC, abstractmethod


# Abstraction: Base dashboard service contract
class BaseDashboard(ABC):
    def __init__(self, db_connection):
        self.db = db_connection

    @abstractmethod
    def get_slots(self):
        pass


# Concrete dashboard implementations
class PatientDashboard(BaseDashboard):
    def get_slots(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM appointment_slots WHERE status = 'Available'")
        slots = cursor.fetchall()
        cursor.close()
        return slots


class StaffDashboard(BaseDashboard):
    def get_slots(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM appointment_slots")
        slots = cursor.fetchall()
        cursor.close()
        return slots


# Factory Pattern: Instantiates dashboard service based on user role
class DashboardFactory:
    @staticmethod
    def create_dashboard(user_role: str, db_connection) -> BaseDashboard:
        if user_role == "Patient":
            return PatientDashboard(db_connection)
        elif user_role == "Clinic Staff":
            return StaffDashboard(db_connection)
        else:
            raise ValueError(f"Unknown user role: '{user_role}'")
