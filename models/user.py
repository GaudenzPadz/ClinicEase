import hashlib
import hmac
from typing import Optional

from database import get_connection
from werkzeug.security import check_password_hash, generate_password_hash


# Adapter: password hashing is isolated from the user entity.
class PasswordHasherAdapter:
    @staticmethod
    def hash_password(password: str) -> str:
        return generate_password_hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        if hashed_password.startswith(("scrypt:", "pbkdf2:")):
            return check_password_hash(hashed_password, plain_password)

        legacy_hash = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
        return hmac.compare_digest(legacy_hash, hashed_password)

    @staticmethod
    def needs_rehash(hashed_password: str) -> bool:
        return not hashed_password.startswith(("scrypt:", "pbkdf2:"))


# Inheritance and Polymorphism: Base user class with private password hash
class User:
    def __init__(
        self,
        user_id: int,
        name: str,
        email: str,
        password_hash: str,
        contact_number: Optional[str] = None,
    ):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.contact_number = contact_number or None
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

            if PasswordHasherAdapter.needs_rehash(stored_hash):
                upgraded_hash = PasswordHasherAdapter.hash_password(password)
                cursor.execute(
                    """
                    UPDATE users
                    SET password_hash = %s
                    WHERE user_id = %s AND password_hash = %s
                    """,
                    (upgraded_hash, user_data["user_id"], stored_hash),
                )
                conn.commit()
                stored_hash = upgraded_hash

            role = user_data["role"]
            if role == "Patient":
                return Patient(
                    user_id=user_data["user_id"],
                    name=user_data["name"],
                    email=user_data["email"],
                    password_hash=stored_hash,
                    contact_number=user_data.get(
                        "contact_number", user_data.get("phone_number")
                    ),
                )
            elif role == "Clinic Staff":
                return ClinicStaff(
                    user_id=user_data["user_id"],
                    name=user_data["name"],
                    email=user_data["email"],
                    password_hash=stored_hash,
                    contact_number=user_data.get(
                        "contact_number", user_data.get("phone_number")
                    ),
                )

            return None
        finally:
            cursor.close()
            conn.close()


class Patient(User):
    def __init__(
        self,
        user_id: int,
        name: str,
        email: str,
        password_hash: str,
        contact_number: Optional[str] = None,
    ):
        super().__init__(
            user_id=user_id,
            name=name,
            email=email,
            password_hash=password_hash,
            contact_number=contact_number,
        )

    def get_user_role(self) -> str:
        return "Patient"

    @classmethod
    def create(
        cls,
        cursor,
        name: str,
        email: str,
        contact_number: Optional[str],
        password: str,
    ) -> int:
        password_hash = PasswordHasherAdapter.hash_password(password)
        return cls.create_with_hash(
            cursor,
            name=name,
            email=email,
            contact_number=contact_number,
            password_hash=password_hash,
        )

    @classmethod
    def create_with_hash(
        cls,
        cursor,
        name: str,
        email: str,
        password_hash: str,
        contact_number: Optional[str] = None,
    ) -> int:
        cursor.execute(
            """
            INSERT INTO users (name, email, contact_number, password_hash, role)
            VALUES (%s, %s, %s, %s, 'Patient')
            """,
            (name, email, contact_number, password_hash),
        )
        return cursor.lastrowid


class ClinicStaff(User):
    def get_user_role(self) -> str:
        return "Clinic Staff"
