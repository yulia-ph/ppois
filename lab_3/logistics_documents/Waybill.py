from exceptions.InvalidCargoStateException import InvalidCargoStateException


class Waybill:
    """Transport document signed by driver and consignee."""

    _counter = 0

    def __init__(self, order, shipper: str, consignee, cargo_desc: str):
        if order is None or consignee is None:
            raise ValueError("Order and consignee must not be None")
        if not shipper:
            raise ValueError("Shipper must not be empty")
        if not cargo_desc:
            raise ValueError("Cargo description must not be empty")
        Waybill._counter += 1
        self._number = f"WB-{Waybill._counter:05d}"
        self._order = order
        self._shipper = shipper
        self._consignee = consignee
        self._cargo_desc = cargo_desc
        self._is_signed = False
        self._driver_signed = False
        self._consignee_signed = False
        self._issued = False

    @property
    def number(self):
        return self._number

    @property
    def order(self):
        return self._order

    @property
    def shipper(self):
        return self._shipper

    @property
    def consignee(self):
        return self._consignee

    @property
    def cargo_desc(self):
        return self._cargo_desc

    @property
    def is_signed(self):
        return self._is_signed

    def issue(self):
        """Issue the waybill."""
        if self._issued:
            raise InvalidCargoStateException(
                title=self._number,
                state="issued",
                reason="Waybill is already issued",
            )
        self._issued = True
        return True

    def sign_by_driver(self):
        """Driver signature."""
        if not self._issued:
            raise InvalidCargoStateException(
                title=self._number,
                state="draft",
                reason="Issue the waybill first",
            )
        self._driver_signed = True
        self._refresh_signed()
        return True

    def sign_by_consignee(self):
        """Consignee signature."""
        if not self._issued:
            raise InvalidCargoStateException(
                title=self._number,
                state="draft",
                reason="Issue the waybill first",
            )
        self._consignee_signed = True
        self._refresh_signed()
        return True

    def _refresh_signed(self):
        self._is_signed = self._driver_signed and self._consignee_signed

    def cancel(self):
        """Cancel an unsigned waybill."""
        if self._is_signed:
            raise InvalidCargoStateException(
                title=self._number,
                state="signed",
                reason="Cannot cancel a fully signed waybill",
            )
        self._issued = False
        return True
