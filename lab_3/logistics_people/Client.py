from exceptions.InsufficientFundsException import InsufficientFundsException


class Client:
    """A paying customer of the company."""

    def __init__(self, name: str, tax_id: str, credit_limit: float):
        if not name:
            raise ValueError("Client name must not be empty")
        if not tax_id:
            raise ValueError("Tax id must not be empty")
        if credit_limit < 0:
            raise ValueError(f"Credit limit must be non-negative, got {credit_limit}")
        self._name = name
        self._tax_id = tax_id
        self._credit_limit = credit_limit
        self._balance = 0.0
        self._contracts = []

    @property
    def name(self):
        return self._name

    @property
    def tax_id(self):
        return self._tax_id

    @property
    def credit_limit(self):
        return self._credit_limit

    @property
    def balance(self):
        return self._balance

    @property
    def contracts(self):
        return list(self._contracts)

    def top_up(self, amount: float):
        """Add money the client can spend on invoices."""
        if amount <= 0:
            raise ValueError(f"Amount must be positive, got {amount}")
        self._balance += amount
        return True

    def check_credit(self, amount: float) -> bool:
        """Return True if the amount is within credit limit and balance."""
        if amount <= 0:
            raise ValueError(f"Amount must be positive, got {amount}")
        if amount > self._credit_limit:
            return False
        return amount <= self._balance

    def add_contract(self, contract):
        """Attach a contract."""
        if contract is None:
            raise ValueError("Contract must not be None")
        if contract in self._contracts:
            raise ValueError("Contract is already attached")
        self._contracts.append(contract)
        return True

    def place_order(self, order):
        """Place a shipment order. The client must be set on the order."""
        if order is None:
            raise ValueError("Order must not be None")
        return order.confirm()

    def pay_invoice(self, invoice, payment, company=None):
        """Pay a company invoice from client balance.

        The payment is processed once inside invoice.pay. Company budget
        grows if a company is passed. Balance is rolled back on failure.
        """
        if invoice is None or payment is None:
            raise ValueError("Invoice and payment must not be None")
        if not self.check_credit(invoice.amount):
            raise InsufficientFundsException(
                required=invoice.amount,
                available=min(self._balance, self._credit_limit),
            )
        self._balance -= invoice.amount
        try:
            invoice.pay(payment)
            if company is not None:
                company.increase_budget(invoice.amount)
        except Exception:
            self._balance += invoice.amount
            raise
        return True
