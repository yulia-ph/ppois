from datetime import date

from exceptions.InsufficientFundsException import InsufficientFundsException
from museum_core.Building import Building
from museum_exhibitions.Exhibition import Exhibition
from museum_exhibits.Fund import Fund
from museum_people.Employee import Employee
from museum_sales.TicketType import TicketType


class Museum:
    """Top-level model of a museum as an organization.

    A museum owns buildings, employs staff, hosts exhibitions, keeps
    funds, and issues tickets. It also manages an annual budget.

    The museum acts as the root aggregate of the domain: it holds
    references to most other entities and provides lookup methods
    for them.
    """

    def __init__(self, name: str, address: str, website: str):
        """Initialize a museum.

        Args:
            name: The museum name.
            address: The postal address.
            website: The public website URL.

        Raises:
            ValueError: If any of the required strings is empty.
        """
        if not name:
            raise ValueError("Museum name must not be empty")
        if not address:
            raise ValueError("Museum address must not be empty")
        if not website:
            raise ValueError("Museum website must not be empty")

        self._name = name
        self._address = address
        self._website = website
        self._buildings = []
        self._employees = []
        self._exhibitions = []
        self._funds = []
        self._ticket_types = []
        self._budget = 0.0

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def website(self):
        return self._website

    @property
    def buildings(self):
        return list(self._buildings)

    @property
    def employees(self):
        return list(self._employees)

    @property
    def exhibitions(self):
        return list(self._exhibitions)

    @property
    def funds(self):
        return list(self._funds)

    @property
    def ticket_types(self):
        return list(self._ticket_types)

    @property
    def budget(self):
        return self._budget

    def add_building(self, building: Building):
        """Register a building with the museum.

        Args:
            building: The building to register.

        Raises:
            ValueError: If the building is already registered.
        """
        if building in self._buildings:
            raise ValueError(f"Building '{building.name}' is already registered")
        self._buildings.append(building)
        return True

    def add_employee(self, employee: Employee):
        """Register an employee with the museum.

        Args:
            employee: The employee to register.

        Raises:
            ValueError: If the employee is already registered.
        """
        if employee in self._employees:
            raise ValueError(f"Employee '{employee.name}' is already registered")
        self._employees.append(employee)
        return True

    def add_exhibition(self, exhibition: Exhibition):
        """Register an exhibition with the museum.

        Args:
            exhibition: The exhibition to register.

        Raises:
            ValueError: If the exhibition is already registered.
        """
        if exhibition in self._exhibitions:
            raise ValueError(f"Exhibition '{exhibition.title}' is already registered")
        self._exhibitions.append(exhibition)
        return True

    def add_fund(self, fund: Fund):
        """Register a fund with the museum.

        Args:
            fund: The fund to register.

        Raises:
            ValueError: If the fund is already registered.
        """
        if fund in self._funds:
            raise ValueError(f"Fund '{fund.name}' is already registered")
        self._funds.append(fund)
        return True

    def add_ticket_type(self, ticket_type: TicketType):
        """Register a ticket type with the museum.

        Args:
            ticket_type: The ticket type to register.

        Raises:
            ValueError: If the ticket type is already registered.
        """
        if ticket_type in self._ticket_types:
            raise ValueError(f"Ticket type '{ticket_type.name}' is already registered")
        self._ticket_types.append(ticket_type)
        return True


    def remove_building(self, building: Building):
        """Unregister a building from the museum.

        Args:
            building: The building to remove.

        Raises:
            ValueError: If the building is not registered.
        """
        if building not in self._buildings:
            raise ValueError(f"Building '{building.name}' is not registered")
        self._buildings.remove(building)
        return True

    def remove_employee(self, employee: Employee):
        """Unregister an employee from the museum.

        Args:
            employee: The employee to remove.

        Raises:
            ValueError: If the employee is not registered.
        """
        if employee not in self._employees:
            raise ValueError(f"Employee '{employee.name}' is not registered")
        self._employees.remove(employee)
        return True

    def remove_exhibition(self, exhibition: Exhibition):
        """Unregister an exhibition from the museum.

        Args:
            exhibition: The exhibition to remove.

        Raises:
            ValueError: If the exhibition is not registered.
        """
        if exhibition not in self._exhibitions:
            raise ValueError(f"Exhibition '{exhibition.title}' is not registered")
        self._exhibitions.remove(exhibition)
        return True

    def remove_fund(self, fund: Fund):
        """Unregister a fund from the museum.

        Args:
            fund: The fund to remove.

        Raises:
            ValueError: If the fund is not registered.
        """
        if fund not in self._funds:
            raise ValueError(f"Fund '{fund.name}' is not registered")
        self._funds.remove(fund)
        return True

    def remove_ticket_type(self, ticket_type: TicketType):
        """Unregister a ticket type from the museum.

        Args:
            ticket_type: The ticket type to remove.

        Raises:
            ValueError: If the ticket type is not registered.
        """
        if ticket_type not in self._ticket_types:
            raise ValueError(f"Ticket type '{ticket_type.name}' is not registered")
        self._ticket_types.remove(ticket_type)
        return True


    def find_ticket_type(self, name: str) -> TicketType:
        """Find a ticket type by name.

        Args:
            name: The ticket type name.

        Returns:
            The matching TicketType.

        Raises:
            ValueError: If no ticket type with the given name exists.
        """
        for tt in self._ticket_types:
            if tt.name == name:
                return tt
        raise ValueError(f"Ticket type '{name}' not found")

    def find_employee(self, name: str) -> Employee:
        """Find an employee by name.

        Args:
            name: The employee name.

        Returns:
            The matching Employee.

        Raises:
            ValueError: If no employee with the given name exists.
        """
        for e in self._employees:
            if e.name == name:
                return e
        raise ValueError(f"Employee '{name}' not found")

    def find_building(self, name: str) -> Building:
        """Find a building by name.

        Args:
            name: The building name.

        Returns:
            The matching Building.

        Raises:
            ValueError: If no building with the given name exists.
        """
        for b in self._buildings:
            if b.name == name:
                return b
        raise ValueError(f"Building '{name}' not found")

    def set_budget(self, budget: float):
        """Set the annual budget to a specific value.

        Args:
            budget: The new budget amount. Must be non-negative.

        Raises:
            ValueError: If budget is negative.
        """
        if budget < 0:
            raise ValueError(f"Budget must be non-negative, got {budget}")
        self._budget = budget
        return True

    def increase_budget(self, amount: float):
        """Increase the budget by the given amount.

        Args:
            amount: The amount to add. Must be positive.

        Raises:
            ValueError: If amount is not positive.
        """
        if amount <= 0:
            raise ValueError(f"Increase amount must be positive, got {amount}")
        self._budget += amount
        return True

    def spend_budget(self, amount: float):
        """Spend the given amount from the budget.

        Args:
            amount: The amount to spend. Must be positive.

        Raises:
            ValueError: If amount is not positive.
            InsufficientFundsException: If amount exceeds the current budget.
        """
        if amount <= 0:
            raise ValueError(f"Spend amount must be positive, got {amount}")
        if amount > self._budget:
            raise InsufficientFundsException(required=amount, available=self._budget)
        self._budget -= amount
        return True

    def count_visitors_today(self, access_records) -> int:
        """Count today's public-zone visits from access records.

        Only records that were granted, occurred today, and target the
        public zone are counted.

        Args:
            access_records: An iterable of AccessControl-like objects.
                Each must expose `.is_granted`, `.zone`, and `.time`.

        Returns:
            The number of visitors admitted to the public zone today.
        """
        today = date.today()
        count = 0
        for record in access_records:
            if not record.is_granted:
                continue
            if record.zone != "public":
                continue
            if record.time.date() != today:
                continue
            count += 1
        return count