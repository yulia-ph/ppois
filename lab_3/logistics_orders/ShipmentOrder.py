from datetime import date

from exceptions.InvalidCargoStateException import InvalidCargoStateException


class ShipmentOrder:
    """A shipment from confirm through dispatch to deliver."""

    STATUS_DRAFT = "draft"
    STATUS_CONFIRMED = "confirmed"
    STATUS_DISPATCHED = "dispatched"
    STATUS_DELIVERED = "delivered"
    STATUS_CANCELLED = "cancelled"

    _counter = 0

    def __init__(self, client, cargo, route, price: float):
        if client is None or cargo is None or route is None:
            raise ValueError("Client, cargo and route must not be None")
        if price < 0:
            raise ValueError(f"Price must be non-negative, got {price}")
        ShipmentOrder._counter += 1
        self._number = f"SO-{ShipmentOrder._counter:05d}"
        self._client = client
        self._cargo = cargo
        self._route = route
        self._status = ShipmentOrder.STATUS_DRAFT
        self._vehicle = None
        self._driver = None
        self._price = price
        self._created_at = date.today()

    @property
    def number(self):
        return self._number

    @property
    def client(self):
        return self._client

    @property
    def cargo(self):
        return self._cargo

    @property
    def route(self):
        return self._route

    @property
    def status(self):
        return self._status

    @property
    def vehicle(self):
        return self._vehicle

    @property
    def driver(self):
        return self._driver

    @property
    def price(self):
        return self._price

    @property
    def created_at(self):
        return self._created_at

    def confirm(self):
        """Confirm a draft order."""
        if self._status != ShipmentOrder.STATUS_DRAFT:
            raise InvalidCargoStateException(
                title=self._number,
                state=self._status,
                reason="Only a draft order can be confirmed",
            )
        self._status = ShipmentOrder.STATUS_CONFIRMED
        return True

    def assign_vehicle(self, vehicle):
        """Assign a vehicle that can load the cargo."""
        if self._status not in (ShipmentOrder.STATUS_CONFIRMED, ShipmentOrder.STATUS_DISPATCHED):
            raise InvalidCargoStateException(
                title=self._number,
                state=self._status,
                reason="Order is not confirmed",
            )
        if vehicle is None:
            raise ValueError("Vehicle must not be None")
        vehicle.can_load(self._cargo)
        self._vehicle = vehicle
        return True

    def assign_driver(self, driver):
        """Assign a driver."""
        if self._status not in (ShipmentOrder.STATUS_CONFIRMED, ShipmentOrder.STATUS_DISPATCHED):
            raise InvalidCargoStateException(
                title=self._number,
                state=self._status,
                reason="Order is not confirmed",
            )
        if driver is None:
            raise ValueError("Driver must not be None")
        driver.can_take_order()
        self._driver = driver
        return True

    def dispatch(self):
        """Send the order on the road."""
        if self._status != ShipmentOrder.STATUS_CONFIRMED:
            raise InvalidCargoStateException(
                title=self._number,
                state=self._status,
                reason="Order is not confirmed",
            )
        if self._vehicle is None or self._driver is None:
            raise InvalidCargoStateException(
                title=self._number,
                state=self._status,
                reason="Vehicle and driver must be assigned",
            )
        self._cargo.update_status("in_transit")
        self._status = ShipmentOrder.STATUS_DISPATCHED
        return True

    def deliver(self):
        """Mark the order delivered."""
        if self._status != ShipmentOrder.STATUS_DISPATCHED:
            raise InvalidCargoStateException(
                title=self._number,
                state=self._status,
                reason="Order is not dispatched",
            )
        self._cargo.update_status("delivered")
        self._status = ShipmentOrder.STATUS_DELIVERED
        return True

    def cancel(self):
        """Cancel a draft or confirmed order."""
        if self._status not in (ShipmentOrder.STATUS_DRAFT, ShipmentOrder.STATUS_CONFIRMED):
            raise InvalidCargoStateException(
                title=self._number,
                state=self._status,
                reason="Cannot cancel an order that is already on the road",
            )
        self._status = ShipmentOrder.STATUS_CANCELLED
        return True
