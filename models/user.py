import hashlib
from database import get_connection


# Adapter Pattern: Encapsulates password hashing and verification
class PasswordHasherAdapter:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PasswordHasherAdapter.hash_password(plain_password) == hashed_password


# Inheritance and Polymorphism: Base user class with private password hash
class User:
    def __init__(self, user_id: int, name: str, email: str, password_hash: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.__password_hash = password_hash

    @property
    def password_hash(self) -> str:
        return self.__password_hash

    def get_user_role(self) -> str:
        return "Base User"

    @staticmethod
    def login(email: str, password: str):
        conn = get_connection()
        if not conn:
            return None

        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user_data = cursor.fetchone()

            if not user_data:
                return None

            stored_hash = user_data["password_hash"]
            if not PasswordHasherAdapter.verify_password(password, stored_hash):
                return None

            role = user_data["role"]
            if role == "Patient":
                return Patient(
                    user_id=user_data["user_id"],
                    name=user_data["name"],
                    email=user_data["email"],
                    password_hash=stored_hash,
                )
            elif role == "Clinic Staff":
                return ClinicStaff(
                    user_id=user_data["user_id"],
                    name=user_data["name"],
                    email=user_data["email"],
                    password_hash=stored_hash,
                )

            return None
        finally:
            cursor.close()
            conn.close()


class Patient(User):
    def get_user_role(self) -> str:
        return "Patient"


class ClinicStaff(User):
    def get_user_role(self) -> str:
        return "Clinic Staff"
