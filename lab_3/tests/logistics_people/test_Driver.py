from datetime import date

import pytest

from exceptions.DriverNotAvailableException import DriverNotAvailableException
from logistics_people.Driver import Driver


class TestDriver:
    def test_driver_shift(self, driver, truck):
        truck.assign_driver(driver)
        assert driver.assigned_vehicle is truck
        driver.start_shift()
        driver.log_hours(2)
        assert driver.can_take_order()
        driver.log_hours(8)
        with pytest.raises(DriverNotAvailableException):
            driver.can_take_order()
        driver.end_shift()

    def test_driver_errors(self, license_c, truck):
        with pytest.raises(ValueError):
            Driver("n", 1, date.today(), None)
        d = Driver("n", 1, date.today(), license_c)
        d._is_available = False
        with pytest.raises(DriverNotAvailableException):
            d.start_shift()
        d._is_available = True
        d.take_leave(date.today(), 1)
        with pytest.raises(DriverNotAvailableException):
            d.start_shift()
        d._on_leave = False
        with pytest.raises(ValueError):
            d.assign_vehicle(None)
        with pytest.raises(ValueError):
            d.log_hours(0)
