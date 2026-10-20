from abc import ABC, abstractmethod


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
        print(f"[EMAIL NOTIFICATION -> {recipient}]")
        print(f"Subject: {subject}")
        print(f"Message: {body}")
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
