from logistics_core.Dock import Dock


class Terminal:
    """A freight terminal with loading docks."""

    def __init__(self, name: str, address, working_hours: str = "08:00-20:00"):
        """Initialize a terminal.

        Raises:
            ValueError: If name is empty or address is None.
        """
        if not name:
            raise ValueError("Terminal name must not be empty")
        if address is None:
            raise ValueError("Address must not be None")
        self._name = name
        self._address = address
        self._docks = []
        self._is_open = False
        self._working_hours = working_hours

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def docks(self):
        return list(self._docks)

    @property
    def is_open(self):
        return self._is_open

    @property
    def working_hours(self):
        return self._working_hours

    def open_terminal(self):
        """Open the terminal for operations."""
        self._is_open = True
        return True

    def close_terminal(self):
        """Close the terminal."""
        self._is_open = False
        return True

    def add_dock(self, dock: Dock):
        """Add a dock.

        Raises:
            ValueError: If dock is None or already present.
        """
        if dock is None:
            raise ValueError("Dock must not be None")
        if dock in self._docks:
            raise ValueError(f"Dock {dock.number} is already at this terminal")
        self._docks.append(dock)
        return True

    def assign_dock(self, vehicle):
        """Occupy the first free dock that can accept the vehicle.

        Raises:
            ValueError: If the terminal is closed or no dock is free.
        """
        if not self._is_open:
            raise ValueError("Terminal is closed")
        for dock in self._docks:
            if dock.can_accept(vehicle):
                dock.occupy(vehicle)
                return dock
        raise ValueError("No free dock can accept this vehicle")

    def count_free_docks(self) -> int:
        """Return the number of unoccupied docks."""
        return sum(1 for d in self._docks if d.is_free())
