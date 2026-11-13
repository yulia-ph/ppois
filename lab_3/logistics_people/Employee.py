from datetime import date, timedelta

from exceptions.InvalidCargoStateException import InvalidCargoStateException


class Employee:
    """Base class for company staff."""

    def __init__(self, name: str, salary: float, hire_date: date):
        if not name:
            raise ValueError("Employee name must not be empty")
        if salary < 0:
            raise ValueError(f"Salary must be non-negative, got {salary}")
        if hire_date is None:
            raise ValueError("Hire date must not be None")
        self._name = name
        self._salary = salary
        self._hire_date = hire_date
        self._on_leave = False
        self._vacations = []

    @property
    def name(self):
        return self._name

    @property
    def position(self):
        return self.__class__.__name__

    @property
    def salary(self):
        return self._salary

    @property
    def hire_date(self):
        return self._hire_date

    @property
    def on_leave(self):
        return self._on_leave

    @property
    def vacations(self):
        return list(self._vacations)

    def work(self) -> bool:
        """Return True if the employee can work today."""
        return not self._on_leave

    def raise_salary(self, new_salary: float):
        """Increase salary. Must not go down."""
        if new_salary <= 0:
            raise ValueError(f"New salary must be positive, got {new_salary}")
        if new_salary < self._salary:
            raise ValueError(
                f"New salary {new_salary} is lower than current {self._salary}"
            )
        self._salary = new_salary
        return True

    def take_leave(self, start: date, days: int):
        """Send the employee on leave."""
        if start is None:
            raise ValueError("Leave start date must not be None")
        if days <= 0:
            raise ValueError(f"Leave duration must be positive, got {days}")
        if self._on_leave:
            raise InvalidCargoStateException(
                title=self._name,
                state="on_leave",
                reason="Employee is already on leave",
            )
        end = start + timedelta(days=days)
        self._vacations.append((start, end))
        self._on_leave = True
        return True

    def calculate_monthly_salary(self) -> float:
        """Return salary, halved while on leave."""
        if self._on_leave:
            return self._salary / 2
        return self._salary
