import calendar
from abc import ABC, abstractmethod
from datetime import date, datetime, time, timedelta
from typing import Iterable, List, Union

from database import get_connection


TimeValue = Union[str, time, timedelta]


class SlotGenerationStrategy(ABC):
    """Strategy contract for splitting clinic hours into appointment times."""

    @abstractmethod
    def generate_slots(
        self,
        start_time: TimeValue,
        end_time: TimeValue,
        duration_minutes: int = 30,
    ) -> Iterable[time]:
        raise NotImplementedError


class Standard30MinStrategy(SlotGenerationStrategy):
    """Generate adjacent 30-minute appointment starts that fit clinic hours."""

    def generate_slots(
        self,
        start_time: TimeValue,
        end_time: TimeValue,
        duration_minutes: int = 30,
    ) -> List[time]:
        if duration_minutes != 30:
            raise ValueError("Standard30MinStrategy requires a 30-minute duration.")

        start = _as_time(start_time)
        end = _as_time(end_time)
        if start >= end:
            raise ValueError("Clinic closing time must be later than opening time.")

        current = datetime.combine(date.min, start)
        closing = datetime.combine(date.min, end)
        duration = timedelta(minutes=duration_minutes)
        slots = []
        while current + duration <= closing:
            slots.append(current.time())
            current += duration
        return slots


class SlotGeneratorFactory:
    """Factory for selecting the clinic's slot-generation strategy."""

    @staticmethod
    def create(strategy_name: str = "standard_30_min") -> SlotGenerationStrategy:
        if strategy_name == "standard_30_min":
            return Standard30MinStrategy()
        raise ValueError(f"Unknown slot-generation strategy: {strategy_name!r}.")


def _as_time(value: TimeValue) -> time:
    if isinstance(value, time):
        return value.replace(tzinfo=None)
    if isinstance(value, timedelta):
        seconds = int(value.total_seconds()) % (24 * 60 * 60)
        return (datetime.min + timedelta(seconds=seconds)).time()
    if isinstance(value, str):
        for format_string in ("%H:%M:%S", "%H:%M", "%I:%M %p"):
            try:
                return datetime.strptime(value, format_string).time()
            except ValueError:
                continue
    raise ValueError(f"Invalid clinic schedule time: {value!r}.")


class CalendarSlotService:
    """Create missing appointment slots from the recurring clinic calendar."""

    def __init__(
        self,
        connection_factory=None,
        strategy: SlotGenerationStrategy = None,
        strategy_name: str = "standard_30_min",
        today_provider=None,
    ):
        self.connection_factory = connection_factory or get_connection
        # Strategy selection stays behind the factory; callers can inject a strategy in tests.
        self.strategy = strategy or SlotGeneratorFactory.create(strategy_name)
        self.today_provider = today_provider or date.today

    def generate_slots_for_month(self, year: int, month: int) -> int:
        if isinstance(year, bool) or not isinstance(year, int):
            raise ValueError("Year must be an integer.")
        if isinstance(month, bool) or not isinstance(month, int) or not 1 <= month <= 12:
            raise ValueError("Month must be an integer from 1 to 12.")
        if not 2000 <= year <= 9999:
            raise ValueError("Year must be between 2000 and 9999.")

        last_day = calendar.monthrange(year, month)[1]
        month_start = date(year, month, 1)
        month_end = date(year, month, last_day)
        today = self.today_provider()
        if month_end < today:
            raise ValueError("Appointment slots cannot be generated for a past month.")
        first_generation_day = max(month_start, today)

        conn = self.connection_factory()
        if not conn:
            raise RuntimeError("Database connection failed while generating slots.")

        cursor = None
        try:
            conn.autocommit = False
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT weekday, open_time, close_time, slot_duration_minutes
                FROM clinic_schedule
                WHERE is_active = 1
                ORDER BY weekday, open_time
                """
            )
            schedule_rows = cursor.fetchall()
            if not schedule_rows:
                raise ValueError(
                    "Clinic hours are not configured. Add an active weekly schedule first."
                )

            cursor.execute(
                """
                SELECT blocked_date
                FROM blocked_dates
                WHERE blocked_date BETWEEN %s AND %s
                """,
                (month_start, month_end),
            )
            blocked_dates = {
                row["blocked_date"] for row in cursor.fetchall()
            }

            schedules_by_weekday = {}
            for schedule in schedule_rows:
                weekday = schedule["weekday"]
                if not isinstance(weekday, int) or not 0 <= weekday <= 6:
                    raise ValueError(f"Invalid clinic schedule weekday: {weekday!r}.")
                schedules_by_weekday.setdefault(weekday, []).append(schedule)

            inserted_count = 0
            current_date = first_generation_day
            while current_date <= month_end:
                if (
                    current_date not in blocked_dates
                    and current_date.weekday() in schedules_by_weekday
                ):
                    for schedule in schedules_by_weekday[current_date.weekday()]:
                        duration = schedule["slot_duration_minutes"]
                        if duration != 30:
                            raise ValueError(
                                "The standard slot strategy supports 30-minute schedules only."
                            )
                        for slot_time in self.strategy.generate_slots(
                            schedule["open_time"],
                            schedule["close_time"],
                            duration,
                        ):
                            cursor.execute(
                                """
                                INSERT IGNORE INTO appointment_slots
                                    (slot_date, time, status)
                                VALUES (%s, %s, 'Available')
                                """,
                                (current_date, slot_time.strftime("%I:%M %p")),
                            )
                            inserted_count += max(cursor.rowcount, 0)
                current_date += timedelta(days=1)

            conn.commit()
            return inserted_count
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()
