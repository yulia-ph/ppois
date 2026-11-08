from exceptions.InsufficientFundsException import InsufficientFundsException
from exceptions.OrderNotFoundException import OrderNotFoundException


class TransportCompany:
    """Root aggregate of the logistics company."""

    def __init__(self, name: str, license_number: str, headquarters):
        """Initialize a company.

        Raises:
            ValueError: If name or license_number is empty, or headquarters is None.
        """
        if not name:
            raise ValueError("Company name must not be empty")
        if not license_number:
            raise ValueError("License number must not be empty")
        if headquarters is None:
            raise ValueError("Headquarters must not be None")
        self._name = name
        self._license_number = license_number
        self._headquarters = headquarters
        self._vehicles = []
        self._warehouses = []
        self._employees = []
        self._clients = []
        self._orders = []
        self._budget = 0.0

    @property
    def name(self):
        return self._name

    @property
    def license_number(self):
        return self._license_number

    @property
    def headquarters(self):
        return self._headquarters

    @property
    def vehicles(self):
        return list(self._vehicles)

    @property
    def warehouses(self):
        return list(self._warehouses)

    @property
    def employees(self):
        return list(self._employees)

    @property
    def clients(self):
        return list(self._clients)

    @property
    def orders(self):
        return list(self._orders)

    @property
    def budget(self):
        return self._budget

    def add_vehicle(self, vehicle):
        """Add a vehicle to the fleet."""
        if vehicle is None:
            raise ValueError("Vehicle must not be None")
        if vehicle in self._vehicles:
            raise ValueError("Vehicle is already in the fleet")
        self._vehicles.append(vehicle)
        return True

    def remove_vehicle(self, vehicle):
        """Remove a vehicle from the fleet."""
        if vehicle not in self._vehicles:
            raise ValueError("Vehicle is not in the fleet")
        self._vehicles.remove(vehicle)
        return True

    def add_warehouse(self, warehouse):
        """Add a warehouse."""
        if warehouse is None:
            raise ValueError("Warehouse must not be None")
        if warehouse in self._warehouses:
            raise ValueError("Warehouse is already registered")
        self._warehouses.append(warehouse)
        return True

    def add_employee(self, employee):
        """Hire an employee into the company."""
        if employee is None:
            raise ValueError("Employee must not be None")
        if employee in self._employees:
            raise ValueError("Employee already works here")
        self._employees.append(employee)
        return True

    def register_client(self, client):
        """Register a client."""
        if client is None:
            raise ValueError("Client must not be None")
        if client in self._clients:
            raise ValueError("Client is already registered")
        self._clients.append(client)
        return True

    def register_order(self, order):
        """Keep a shipment order on the company books."""
        if order is None:
            raise ValueError("Order must not be None")
        if order in self._orders:
            raise ValueError("Order is already registered")
        self._orders.append(order)
        return True

    def find_vehicle(self, plate: str):
        """Find a vehicle by plate.

        Raises:
            ValueError: If plate is empty or no vehicle matches.
        """
        if not plate:
            raise ValueError("Plate must not be empty")
        for vehicle in self._vehicles:
            if vehicle.plate == plate:
                return vehicle
        raise ValueError(f"Vehicle '{plate}' not found")

    def find_order(self, number: str):
        """Find a shipment order by number.

        Raises:
            OrderNotFoundException: If no order matches.
        """
        if not number:
            raise ValueError("Order number must not be empty")
        for order in self._orders:
            if order.number == number:
                return order
        raise OrderNotFoundException(number=number)

    def set_budget(self, budget: float):
        """Set the company budget."""
        if budget < 0:
            raise ValueError(f"Budget must be non-negative, got {budget}")
        self._budget = budget
        return True

    def increase_budget(self, amount: float):
        """Add money to the budget."""
        if amount <= 0:
            raise ValueError(f"Increase amount must be positive, got {amount}")
        self._budget += amount
        return True

    def spend_budget(self, amount: float):
        """Spend money from the budget.

        Raises:
            InsufficientFundsException: If the budget cannot cover the amount.
        """
        if amount <= 0:
            raise ValueError(f"Spend amount must be positive, got {amount}")
        if amount > self._budget:
            raise InsufficientFundsException(required=amount, available=self._budget)
        self._budget -= amount
        return True
