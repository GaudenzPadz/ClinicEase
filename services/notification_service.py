from abc import ABC, abstractmethod
from email.message import EmailMessage
import os
import smtplib
import ssl


# Abstraction: Base notification service contract
class BaseNotificationService(ABC):
    @abstractmethod
    def send_notification(self, recipient: str, subject: str, body: str) -> bool:
        pass


# Concrete notification implementations
class ConsoleNotificationService(BaseNotificationService):
    def send_notification(self, recipient: str, subject: str, body: str) -> bool:
        print("[CONSOLE NOTIFICATION]")
        print(f"Recipient: {recipient}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        return True


class EmailNotificationService(BaseNotificationService):
    def send_notification(self, recipient: str, subject: str, body: str) -> bool:
        host = os.getenv("CLINICEASE_SMTP_HOST")
        sender = os.getenv("CLINICEASE_SMTP_SENDER")
        if not host or not sender:
            raise RuntimeError(
                "SMTP email requires CLINICEASE_SMTP_HOST and CLINICEASE_SMTP_SENDER."
            )

        message = EmailMessage()
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        port = int(os.getenv("CLINICEASE_SMTP_PORT", "587"))
        username = os.getenv("CLINICEASE_SMTP_USERNAME")
        password = os.getenv("CLINICEASE_SMTP_PASSWORD")
        with smtplib.SMTP(host, port, timeout=20) as server:
            server.starttls(context=ssl.create_default_context())
            if username:
                server.login(username, password or "")
            refused_recipients = server.send_message(message)
            if refused_recipients:
                raise smtplib.SMTPRecipientsRefused(refused_recipients)
        return True


# Factory Pattern: Instantiates notification service based on mode
class NotificationServiceFactory:
    @staticmethod
    def create_service(mode: str = "console") -> BaseNotificationService:
        mode_clean = (mode or "console").strip().lower()

        if mode_clean == "console":
            return ConsoleNotificationService()
        elif mode_clean == "email":
            return EmailNotificationService()
        else:
            raise ValueError(f"Unknown notification mode: '{mode}'. Expected 'console' or 'email'.")
