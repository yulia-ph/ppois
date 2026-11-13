from datetime import date

import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_people.Employee import Employee


class TestEmployee:
    def test_work_leave_salary(self, employee):
        assert employee.work()
        assert employee.position == "Employee"
        employee.take_leave(date.today(), 5)
        assert employee.on_leave
        assert employee.calculate_monthly_salary() == 20_000
        employee._on_leave = False
        employee.raise_salary(45_000)
        with pytest.raises(InvalidCargoStateException):
            employee.take_leave(date.today(), 1)
            employee.take_leave(date.today(), 1)

    def test_employee_errors(self):
        with pytest.raises(ValueError):
            Employee("", 1, date.today())
        with pytest.raises(ValueError):
            Employee("n", -1, date.today())
        with pytest.raises(ValueError):
            Employee("n", 1, None)
        e = Employee("n", 10, date.today())
        with pytest.raises(ValueError):
            e.raise_salary(0)
        with pytest.raises(ValueError):
            e.raise_salary(5)
        with pytest.raises(ValueError):
            e.take_leave(None, 1)
        with pytest.raises(ValueError):
            e.take_leave(date.today(), 0)
        assert e.vacations == []
