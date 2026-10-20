import re
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple


class BaseValidator(ABC):
    """
    Abstract Base Class defining the contract for input validation.
    Demonstrates Abstraction and Single Responsibility Principle.
    """

    @abstractmethod
    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate input value.

        :param value: Value or payload to validate
        :return: (is_valid: bool, error_message: Optional[str])
        """
        pass


class EmailValidator(BaseValidator):
    """
    Validates standard email format and ensures non-empty value.
    """

    EMAIL_REGEX = re.compile(
        r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        if not value or not isinstance(value, str) or not value.strip():
            return False, "Email address is required."

        email = value.strip()
        if not self.EMAIL_REGEX.match(email):
            return False, "Invalid email format. Please provide a valid email."

        return True, None


class PasswordValidator(BaseValidator):
    """
    Validates password constraints (length, non-empty).
    """

    def __init__(self, min_length: int = 6):
        self.min_length = min_length

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        if not value or not isinstance(value, str):
            return False, "Password is required."

        if len(value) < self.min_length:
            return False, f"Password must be at least {self.min_length} characters long."

        return True, None


class NameValidator(BaseValidator):
    """
    Validates full name field.
    """

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        if not value or not isinstance(value, str) or not value.strip():
            return False, "Name is required."

        name = value.strip()
        if len(name) < 2:
            return False, "Name must be at least 2 characters long."

        return True, None


class RegistrationValidator(BaseValidator):
    """
    Validates user registration payload (name, email, password).
    """

    def __init__(self):
        self.name_validator = NameValidator()
        self.email_validator = EmailValidator()
        self.password_validator = PasswordValidator()

    def validate(self, data: Any) -> Tuple[bool, Optional[str]]:
        if not isinstance(data, dict):
            return False, "Invalid request payload."

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        is_valid_name, err_name = self.name_validator.validate(name)
        if not is_valid_name:
            return False, err_name

        is_valid_email, err_email = self.email_validator.validate(email)
        if not is_valid_email:
            return False, err_email

        is_valid_pass, err_pass = self.password_validator.validate(password)
        if not is_valid_pass:
            return False, err_pass

        return True, None


class LoginValidator(BaseValidator):
    """
    Validates login credentials payload.
    """

    def validate(self, data: Any) -> Tuple[bool, Optional[str]]:
        if not isinstance(data, dict):
            return False, "Invalid request payload."

        email = data.get("email")
        password = data.get("password")

        if not email or not isinstance(email, str) or not email.strip():
            return False, "Email is required."

        if not password or not isinstance(password, str):
            return False, "Password is required."

        return True, None


class BookingValidator(BaseValidator):
    """
    Validates appointment booking payload.
    """

    def validate(self, data: Any) -> Tuple[bool, Optional[str]]:
        if not isinstance(data, dict):
            return False, "Invalid request payload."

        slot_id = data.get("slot_id")
        if slot_id is None:
            return False, "Slot ID is required."

        try:
            int(slot_id)
        except (ValueError, TypeError):
            return False, "Slot ID must be a valid integer."

        purpose = data.get("purpose")
        if purpose is not None and isinstance(purpose, str) and len(purpose.strip()) > 255:
            return False, "Purpose exceeds maximum allowed length of 255 characters."

        return True, None


class ValidationService:
    """
    Service Layer / Facade providing high-level validation routines.
    """

    _email_validator = EmailValidator()
    _password_validator = PasswordValidator()
    _name_validator = NameValidator()
    _registration_validator = RegistrationValidator()
    _login_validator = LoginValidator()
    _booking_validator = BookingValidator()

    @classmethod
    def validate_email(cls, email: str) -> Tuple[bool, Optional[str]]:
        return cls._email_validator.validate(email)

    @classmethod
    def validate_password(cls, password: str, min_length: int = 6) -> Tuple[bool, Optional[str]]:
        return PasswordValidator(min_length=min_length).validate(password)

    @classmethod
    def validate_name(cls, name: str) -> Tuple[bool, Optional[str]]:
        return cls._name_validator.validate(name)

    @classmethod
    def validate_registration(cls, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        return cls._registration_validator.validate(data)

    @classmethod
    def validate_login(cls, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        return cls._login_validator.validate(data)

    @classmethod
    def validate_booking(cls, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        return cls._booking_validator.validate(data)
