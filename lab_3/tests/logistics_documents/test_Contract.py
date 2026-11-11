from datetime import date, timedelta

import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_documents.Contract import Contract


class TestContract:
    def test_contract(self):
        c = Contract([], "haulage", 1000, date.today() + timedelta(days=30))
        c.add_party("Acme")
        c.change_amount(1200)
        c.sign()
        assert c.is_active()
        c.terminate()
        with pytest.raises(ValueError):
            Contract([], "", 1, date.today())
        with pytest.raises(ValueError):
            Contract([], "t", -1, date.today())
        with pytest.raises(ValueError):
            Contract([], "t", 1, None)
        c2 = Contract(["A"], "t", 1, date.today() + timedelta(days=1))
        with pytest.raises(ValueError):
            c2.add_party("")
        c2.add_party("B")
        with pytest.raises(ValueError):
            c2.add_party("B")
        with pytest.raises(ValueError):
            c2.change_amount(-1)
        c2.sign()
        with pytest.raises(InvalidCargoStateException):
            c2.add_party("C")
        with pytest.raises(InvalidCargoStateException):
            c2.sign()
        with pytest.raises(InvalidCargoStateException):
            c2.change_amount(2)
        empty = Contract([], "t", 1, date.today() + timedelta(days=1))
        with pytest.raises(ValueError):
            empty.sign()
        with pytest.raises(InvalidCargoStateException):
            empty.terminate()
