from datetime import date, timedelta

from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Employee:
    """Base class for all museum employees.

    An employee has a name, salary, hire date, and vacation state.
    Subclasses (Curator, Restorer, Cashier, etc.) inherit these and
    add role-specific attributes and behaviors.

    The `position` property is derived from the concrete subclass name
    and is used by the access-control layer to authorize entry into
    restricted zones.
    """

    def __init__(self, name: str, salary: float, hire_date: date):
        """Initialize an employee.

        Args:
            name: The employee's full name. Must not be empty.
            salary: Monthly salary. Must be non-negative.
            hire_date: The date of hire. Must not be None.

        Raises:
            ValueError: If name is empty, salary is negative, or
                hire_date is None.
        """
        if not name:
            raise ValueError("Employee name must not be empty")
        if salary < 0:
            raise ValueError(f"Salary must be non-negative, got {salary}")
        if hire_date is None:
            raise ValueError("Hire date must not be None")

        self._name = name
        self._salary = salary
        self._hire_date = hire_date
        self._on_vacation = False
        self._vacations = []


    @property
    def name(self):
        return self._name

    @property
    def position(self):
        """Return the concrete class name as the role identifier.

        Examples: "Employee", "Curator", "Restorer".
        """
        return self.__class__.__name__

    @property
    def salary(self):
        return self._salary

    @property
    def hire_date(self):
        return self._hire_date

    @property
    def on_vacation(self):
        return self._on_vacation

    @property
    def vacations(self):
        return list(self._vacations)


    def work(self) -> bool:
        """Return True if the employee can work today (not on vacation)."""
        return not self._on_vacation

    def raise_salary(self, new_salary: float):
        """Increase the employee's salary.

        Args:
            new_salary: The new monthly salary. Must be positive and
                not less than the current salary.

        Raises:
            ValueError: If new_salary is not positive or is lower than
                the current salary.
        """
        if new_salary <= 0:
            raise ValueError(f"New salary must be positive, got {new_salary}")
        if new_salary < self._salary:
            raise ValueError(
                f"New salary {new_salary} is lower than current {self._salary}"
            )
        self._salary = new_salary
        return True

    def take_vacation(self, start: date, days: int):
        """Send the employee on vacation.

        Args:
            start: Vacation start date. Must not be None.
            days: Duration in days. Must be positive.

        Raises:
            ValueError: If start is None or days is not positive.
            InvalidExhibitStateException: If the employee is already
                on vacation.
        """
        if start is None:
            raise ValueError("Vacation start date must not be None")
        if days <= 0:
            raise ValueError(f"Vacation duration must be positive, got {days}")
        if self._on_vacation:
            raise InvalidExhibitStateException(
                exhibit_title=self._name,
                state="on_vacation",
                reason="Employee is already on vacation",
            )
        end = start + timedelta(days=days)
        self._vacations.append((start, end))
        self._on_vacation = True
        return True

    def return_from_vacation(self):
        """Return the employee from vacation.

        Idempotent: calling when the employee is not on vacation is
        not an error.
        """
        self._on_vacation = False
        return True