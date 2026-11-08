import math
from datetime import datetime


class GPSPosition:
    """A geographic point with optional accuracy."""

    def __init__(self, latitude: float, longitude: float, accuracy: float = 10.0):
        """Initialize a GPS position.

        Args:
            latitude: Degrees, must be in [-90, 90].
            longitude: Degrees, must be in [-180, 180].
            accuracy: Metres. Must be non-negative.

        Raises:
            ValueError: If coordinates or accuracy are out of range.
        """
        if not -90 <= latitude <= 90:
            raise ValueError(f"Latitude must be in [-90, 90], got {latitude}")
        if not -180 <= longitude <= 180:
            raise ValueError(f"Longitude must be in [-180, 180], got {longitude}")
        if accuracy < 0:
            raise ValueError(f"Accuracy must be non-negative, got {accuracy}")
        self._latitude = latitude
        self._longitude = longitude
        self._timestamp = datetime.now()
        self._accuracy = accuracy

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def accuracy(self):
        return self._accuracy

    def is_valid(self) -> bool:
        """Return True if coordinates are inside the valid ranges."""
        return -90 <= self._latitude <= 90 and -180 <= self._longitude <= 180

    def update(self, latitude: float, longitude: float, accuracy: float = None):
        """Move the point to a new coordinate.

        Raises:
            ValueError: If the new coordinates are out of range.
        """
        if not -90 <= latitude <= 90:
            raise ValueError(f"Latitude must be in [-90, 90], got {latitude}")
        if not -180 <= longitude <= 180:
            raise ValueError(f"Longitude must be in [-180, 180], got {longitude}")
        self._latitude = latitude
        self._longitude = longitude
        self._timestamp = datetime.now()
        if accuracy is not None:
            if accuracy < 0:
                raise ValueError(f"Accuracy must be non-negative, got {accuracy}")
            self._accuracy = accuracy
        return True

    def distance_to(self, other) -> float:
        """Approximate distance in kilometres using a flat projection."""
        if other is None:
            raise ValueError("Other position must not be None")
        dy = (self._latitude - other.latitude) * 111.0
        dx = (self._longitude - other.longitude) * 111.0 * math.cos(
            math.radians(self._latitude)
        )
        return math.hypot(dx, dy)

    def move_towards(self, other, fraction: float):
        """Move this point a fraction of the way toward `other`.

        Args:
            other: Target GPSPosition.
            fraction: 0..1 inclusive.

        Raises:
            ValueError: If other is None or fraction is out of range.
        """
        if other is None:
            raise ValueError("Other position must not be None")
        if not 0 <= fraction <= 1:
            raise ValueError(f"Fraction must be in [0, 1], got {fraction}")
        lat = self._latitude + (other.latitude - self._latitude) * fraction
        lon = self._longitude + (other.longitude - self._longitude) * fraction
        return self.update(lat, lon)
