from datetime import date, timedelta

import pytest

from exceptions.InvalidLicenseException import InvalidLicenseException
from logistics_people.DrivingLicense import DrivingLicense


class TestDrivingLicense:
    def test_license(self, license_c):
        assert license_c.covers_category("C")
        assert not license_c.is_expired()
        license_c.renew(10)
        license_c.suspend()
        with pytest.raises(InvalidLicenseException):
            license_c.covers_category("C")

    def test_license_errors(self):
        with pytest.raises(ValueError):
            DrivingLicense("", ["B"], date.today(), date.today() + timedelta(days=1))
        with pytest.raises(ValueError):
            DrivingLicense("n", [], date.today(), date.today() + timedelta(days=1))
        with pytest.raises(ValueError):
            DrivingLicense("n", ["B"], None, date.today())
        with pytest.raises(ValueError):
            DrivingLicense("n", ["B"], date.today(), date.today())
        lic = DrivingLicense("n", ["B"], date(2020, 1, 1), date.today() + timedelta(days=1))
        with pytest.raises(ValueError):
            lic.covers_category("")
        with pytest.raises(InvalidLicenseException):
            lic.covers_category("C")
        old = DrivingLicense("o", ["B"], date(2000, 1, 1), date(2001, 1, 1))
        with pytest.raises(InvalidLicenseException):
            old.covers_category("B")
        with pytest.raises(ValueError):
            lic.renew(0)
        lic.suspend()
        with pytest.raises(InvalidLicenseException):
            lic.renew(1)
