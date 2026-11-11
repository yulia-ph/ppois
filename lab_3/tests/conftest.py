"""Shared fixtures for lab_3 tests."""
from datetime import date, datetime, timedelta

import pytest

from logistics_cargo.Cargo import Cargo
from logistics_core.Address import Address
from logistics_core.GPSPosition import GPSPosition
from logistics_core.TransportCompany import TransportCompany
from logistics_fleet.Truck import Truck
from logistics_people.Driver import Driver
from logistics_people.DrivingLicense import DrivingLicense
from logistics_people.Employee import Employee
from logistics_routes.Route import Route
from logistics_warehouse.Warehouse import Warehouse


@pytest.fixture
def gps():
    return GPSPosition(53.9, 27.56)


@pytest.fixture
def address(gps):
    return Address("Lenina 1", "Minsk", "Minsk", "Belarus", "220000", gps)


@pytest.fixture
def address_warsaw():
    return Address("Marszalkowska 1", "Warsaw", "Mazovia", "Poland", "00-001",
                   GPSPosition(52.23, 21.01))


@pytest.fixture
def company(address):
    c = TransportCompany("BelLogistic", "LIC-001", address)
    c.set_budget(100_000)
    return c


@pytest.fixture
def warehouse(address):
    return Warehouse("Central WH", address, 1000.0)


@pytest.fixture
def cargo(address, address_warsaw):
    return Cargo(100.0, 2.0, address, address_warsaw, declared_value=500.0)


@pytest.fixture
def route(address, address_warsaw):
    return Route(address, address_warsaw, 550.0, 8.0)


@pytest.fixture
def license_c():
    return DrivingLicense(
        "DL-1",
        ["B", "C"],
        date(2020, 1, 1),
        date.today() + timedelta(days=365),
    )


@pytest.fixture
def driver(license_c):
    return Driver("Ivanov", 50_000, date(2020, 1, 1), license_c)


@pytest.fixture
def truck():
    return Truck("AA-1234", "VIN0001", 10_000, 40.0, axles=3, has_sleeper=True)


@pytest.fixture
def employee():
    return Employee("Petrov", 40_000, date(2021, 5, 1))


@pytest.fixture
def now_window():
    start = datetime.now()
    return start, start + timedelta(hours=4)
