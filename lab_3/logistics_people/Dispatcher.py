from datetime import date

from exceptions.DriverNotAvailableException import DriverNotAvailableException
from exceptions.OrderNotFoundException import OrderNotFoundException
from exceptions.VehicleNotAvailableException import VehicleNotAvailableException
from logistics_people.Employee import Employee


class Dispatcher(Employee):
    """Assigns orders to drivers."""

    def __init__(self, name: str, salary: float, hire_date: date, region: str, radio_id: str):
        super().__init__(name, salary, hire_date)
        if not region:
            raise ValueError("Region must not be empty")
        if not radio_id:
            raise ValueError("Radio id must not be empty")
        self._region = region
        self._assigned_orders = []
        self._radio_id = radio_id

    @property
    def region(self):
        return self._region

    @property
    def assigned_orders(self):
        return list(self._assigned_orders)

    @property
    def radio_id(self):
        return self._radio_id

    def find_free_driver(self, drivers):
        """Return the first driver that can take an order."""
        if drivers is None:
            raise ValueError("Drivers list must not be None")
        for driver in drivers:
            try:
                if driver.can_take_order():
                    return driver
            except DriverNotAvailableException:
                continue
        raise DriverNotAvailableException(reason="no free driver")

    def assign_order(self, order, driver):
        """Assign an order to a driver and their vehicle.

        Raises:
            DriverNotAvailableException: If the driver cannot take work.
            VehicleNotAvailableException: If there is no idle vehicle.
        """
        if order is None or driver is None:
            raise ValueError("Order and driver must not be None")
        driver.can_take_order()
        vehicle = driver.assigned_vehicle
        if vehicle is None:
            raise VehicleNotAvailableException(status="no vehicle assigned")
        if vehicle.status != "idle":
            raise VehicleNotAvailableException(plate=vehicle.plate, status=vehicle.status)
        order.assign_driver(driver)
        order.assign_vehicle(vehicle)
        self._assigned_orders.append(order)
        return True

    def reassign(self, order, driver):
        """Move an already assigned order to another driver."""
        if order not in self._assigned_orders:
            raise OrderNotFoundException(number=getattr(order, "number", None))
        self._assigned_orders.remove(order)
        return self.assign_order(order, driver)

    def close_shift(self):
        """Clear assigned orders at the end of the shift."""
        self._assigned_orders.clear()
        return True
