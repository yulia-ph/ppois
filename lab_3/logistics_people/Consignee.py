class Consignee:
    """The party that receives a delivery."""

    def __init__(self, name: str, address, phone: str, preferred_window: str = "09:00-18:00"):
        if not name:
            raise ValueError("Consignee name must not be empty")
        if address is None:
            raise ValueError("Address must not be None")
        if not phone:
            raise ValueError("Phone must not be empty")
        self._name = name
        self._address = address
        self._phone = phone
        self._preferred_window = preferred_window

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def phone(self):
        return self._phone

    @property
    def preferred_window(self):
        return self._preferred_window

    def confirm_delivery(self, delivery):
        """Confirm a delivery by signing it."""
        if delivery is None:
            raise ValueError("Delivery must not be None")
        return delivery.confirm(signature=self._name)

    def refuse(self, delivery, reason: str):
        """Refuse a delivery."""
        if delivery is None:
            raise ValueError("Delivery must not be None")
        if not reason:
            raise ValueError("Reason must not be empty")
        return delivery.refuse(reason)

    def reschedule(self, window: str):
        """Change the preferred delivery window."""
        if not window:
            raise ValueError("Window must not be empty")
        self._preferred_window = window
        return True
