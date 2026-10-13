from enum import Enum

from museum_core.ClimateZone import ClimateZone


class RoomPurpose(Enum):
    """The intended use of a service room inside a museum building."""

    CASHIER = "cashier"
    RESTORATION = "restoration"
    SECURITY = "security"
    OFFICE = "office"
    STORAGE = "storage"
    OTHER = "other"


class Room:
    """A service room inside a museum building.

    Rooms are non-exhibition spaces such as cashier desks, restoration
    workshops, security rooms, and offices. A room can optionally have
    its own climate zone. Certain purposes (restoration, storage)
    require climate control while others do not.
    """

    CLIMATE_CONTROLLED_PURPOSES = (RoomPurpose.RESTORATION, RoomPurpose.STORAGE)

    def __init__(self, number: int, purpose: RoomPurpose):
        """Initialize a room.

        Args:
            number: The room number, unique within a building.
            purpose: The room purpose. Must be a RoomPurpose value.

        Raises:
            TypeError: If purpose is not a RoomPurpose instance.
        """
        if not isinstance(purpose, RoomPurpose):
            raise TypeError(
                f"purpose must be a RoomPurpose, got {type(purpose).__name__}"
            )
        self._number = number
        self._purpose = purpose
        self._climate_zone = None

    @property
    def number(self):
        return self._number

    @property
    def purpose(self):
        return self._purpose

    @property
    def climate_zone(self):
        return self._climate_zone

    @property
    def has_climate_control(self):
        return self._climate_zone is not None

    def assign_purpose(self, purpose: RoomPurpose):
        """Change the room's purpose.

        Args:
            purpose: The new purpose. Must be a RoomPurpose value.

        Raises:
            TypeError: If purpose is not a RoomPurpose instance.
        """
        if not isinstance(purpose, RoomPurpose):
            raise TypeError(
                f"purpose must be a RoomPurpose, got {type(purpose).__name__}"
            )
        self._purpose = purpose
        return True

    def set_climate_zone(self, zone: ClimateZone):
        """Attach a climate zone to this room.

        Args:
            zone: The climate zone to attach. Must not be None.

        Raises:
            ValueError: If zone is None.
        """
        if zone is None:
            raise ValueError("Climate zone must not be None")
        self._climate_zone = zone
        return True

    def remove_climate_zone(self):
        """Detach the climate zone from this room.

        Idempotent: calling on a room without a climate zone is not an error.
        """
        self._climate_zone = None
        return True

    def check_climate(self) -> bool:
        """Return True if the room's climate is within norm.

        If the room has no climate zone, returns True (nothing to check).
        """
        if self._climate_zone is None:
            return True
        return self._climate_zone.is_within_norm()

    def needs_climate_control(self) -> bool:
        """Return True if the room's purpose requires climate control."""
        return self._purpose in Room.CLIMATE_CONTROLLED_PURPOSES