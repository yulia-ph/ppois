from datetime import date, timedelta

import pytest

from exceptions.InsufficientFundsException import InsufficientFundsException
from exceptions.PaymentFailedException import PaymentFailedException
from logistics_documents.Contract import Contract
from logistics_orders.Invoice import Invoice
from logistics_orders.Payment import Payment
from logistics_orders.ShipmentOrder import ShipmentOrder
from logistics_people.Client import Client


class TestClient:
    def test_client_pay(self, company):
        client = Client("Acme", "TAX", 5000)
        client.top_up(2000)
        inv = Invoice(1000, client.name)
        pay = Payment(1000, Payment.METHOD_CARD)
        client.pay_invoice(inv, pay, company)
        assert inv.is_paid
        assert company.budget == 101_000
        with pytest.raises(InsufficientFundsException):
            client.pay_invoice(Invoice(9000, "Acme"), Payment(9000, Payment.METHOD_CASH), company)
        fail_inv = Invoice(100, "Acme")
        client.top_up(100)
        bad = Payment(100, Payment.METHOD_CARD)
        bad.fail("x") if False else None
        p = Payment(100, Payment.METHOD_CARD)
        p._status = Payment.STATUS_FAILED
        with pytest.raises(PaymentFailedException):
            client.pay_invoice(fail_inv, p, company)
        assert client.balance >= 0

    def test_client_errors(self, cargo, route):
        with pytest.raises(ValueError):
            Client("", "t", 1)
        with pytest.raises(ValueError):
            Client("n", "", 1)
        with pytest.raises(ValueError):
            Client("n", "t", -1)
        c = Client("n", "t", 100)
        with pytest.raises(ValueError):
            c.top_up(0)
        with pytest.raises(ValueError):
            c.check_credit(0)
        assert not c.check_credit(50)
        c.top_up(10)
        assert not c.check_credit(50)
        with pytest.raises(ValueError):
            c.add_contract(None)
        contract = Contract(["n"], "terms", 1, date.today() + timedelta(days=10))
        c.add_contract(contract)
        with pytest.raises(ValueError):
            c.add_contract(contract)
        order = ShipmentOrder(c, cargo, route, 1)
        c.place_order(order)
        with pytest.raises(ValueError):
            c.place_order(None)
        with pytest.raises(ValueError):
            c.pay_invoice(None, Payment(1, Payment.METHOD_CASH))
