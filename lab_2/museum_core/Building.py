from exceptions.AccessDeniedException import AccessDeniedException
from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
from museum_core.Hall import Hall
from museum_core.Room import Room


class Building:
    """A museum building such as the main hall, storage, or administration.

    Buildings contain halls (for exhibitions) and rooms (for staff and
    service purposes). The type of building defines which operations
    are allowed — for example, visitors cannot enter a storage building.
    """

    TYPE_MAIN = "main"
    TYPE_STORAGE = "storage"
    TYPE_ADMIN = "admin"

    SLOTS_PER_FLOOR = 10

    def __init__(self, name: str, address: str, building_type: str, floors: int):
        """Initialize a building.

        Args:
            name: The name of the building.
            address: The postal address.
            building_type: One of TYPE_MAIN, TYPE_STORAGE, TYPE_ADMIN.
            floors: The number of floors.
        """
        self._name = name
        self._address = address
        self._type = building_type
        self._floors = floors
        self._halls = []
        self._rooms = []
        self._is_open = False

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def type(self):
        return self._type

    @property
    def floors(self):
        return self._floors

    @property
    def halls(self):
        return list(self._halls)

    @property
    def rooms(self):
        return list(self._rooms)

    @property
    def is_open(self):
        return self._is_open

    def add_hall(self, hall: Hall):
        """Add a hall to this building.

        Args:
            hall: The hall to add.

        Raises:
            ValueError: If the hall is already attached to this building.
        """
        if hall in self._halls:
            raise ValueError(f"Hall '{hall.number}' is already in building '{self._name}'")
        self._halls.append(hall)
        return True

    def add_room(self, room: Room):
        """Add a room to this building.

        Args:
            room: The room to add.

        Raises:
            ValueError: If the room is already attached to this building.
        """
        if room in self._rooms:
            raise ValueError(f"Room '{room.number}' is already in building '{self._name}'")
        self._rooms.append(room)
        return True

    def remove_hall(self, hall: Hall):
        """Remove a hall from this building.

        Args:
            hall: The hall to remove.

        Raises:
            ValueError: If the hall is not part of this building.
        """
        if hall not in self._halls:
            raise ValueError(f"Hall '{hall.number}' is not in building '{self._name}'")
        self._halls.remove(hall)
        return True

    def remove_room(self, room: Room):
        """Remove a room from this building.

        Args:
            room: The room to remove.

        Raises:
            ValueError: If the room is not part of this building.
        """
        if room not in self._rooms:
            raise ValueError(f"Room '{room.number}' is not in building '{self._name}'")
        self._rooms.remove(room)
        return True

    def open_for_visitors(self):
        """Open the building for public access.

        Only TYPE_MAIN buildings may be open to visitors. Storage and
        administration buildings are restricted areas.

        Raises:
            AccessDeniedException: If the building type is storage or admin.

        Returns:
            True if the building was opened.
        """
        if self._type == Building.TYPE_STORAGE:
            raise AccessDeniedException(self._name, "public")
        if self._type == Building.TYPE_ADMIN:
            raise AccessDeniedException(self._name, "public")
        self._is_open = True
        return True

    def close_for_visitors(self):
        """Close the building for public access."""
        self._is_open = False
        return True

    def evacuate(self):
        """Evacuate all visitors from the building.

        Raises:
            InvalidExhibitStateException: If the building is already closed.
        """
        if not self._is_open:
            raise InvalidExhibitStateException(
                exhibit_title=self._name,
                state="closed",
                reason="Cannot evacuate a closed building",
            )
        self._is_open = False
        return True

    def count_free_space(self) -> int:
        """Return the number of free slots in the building.

        Each floor can hold up to 10 halls or rooms. The result may be
        negative if the building is overcrowded.

        Returns:
            The number of free slots.
        """
        total_slots = self._floors * Building.SLOTS_PER_FLOOR
        return total_slots - len(self._halls) - len(self._rooms)

    def is_full(self) -> bool:
        """Return True if the building has no free space left."""
        return self.count_free_space() <= 0