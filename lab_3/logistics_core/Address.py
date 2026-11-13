from logistics_core.GPSPosition import GPSPosition


class Address:
    """A postal address with optional GPS coordinates."""

    def __init__(
        self,
        street: str,
        city: str,
        region: str,
        country: str,
        postal_code: str,
        coordinates: GPSPosition = None,
    ):
        """Initialize an address.

        Raises:
            ValueError: If city or country is empty.
        """
        if not city:
            raise ValueError("City must not be empty")
        if not country:
            raise ValueError("Country must not be empty")
        self._street = street or ""
        self._city = city
        self._region = region or ""
        self._country = country
        self._postal_code = postal_code or ""
        self._coordinates = coordinates

    @property
    def street(self):
        return self._street

    @property
    def city(self):
        return self._city

    @property
    def region(self):
        return self._region

    @property
    def country(self):
        return self._country

    @property
    def postal_code(self):
        return self._postal_code

    @property
    def coordinates(self):
        return self._coordinates

    def is_complete(self) -> bool:
        """Return True if street, city, country and postal code are set."""
        return bool(self._street and self._city and self._country and self._postal_code)

    def is_same_city(self, other) -> bool:
        """Return True if both addresses are in the same city and country."""
        if other is None:
            raise ValueError("Other address must not be None")
        return (
            self._city.lower() == other.city.lower()
            and self._country.lower() == other.country.lower()
        )

    def in_country(self, country: str) -> bool:
        """Return True if this address is in `country`."""
        if not country:
            raise ValueError("Country must not be empty")
        return self._country.lower() == country.lower()

    def format(self) -> str:
        """Return a one-line formatted address."""
        parts = [self._street, self._postal_code, self._city, self._region, self._country]
        return ", ".join(p for p in parts if p)

    def distance_to(self, other) -> float:
        """Distance in kilometres via GPS, or 0 if either has no coordinates."""
        if other is None:
            raise ValueError("Other address must not be None")
        if self._coordinates is None or other.coordinates is None:
            return 0.0
        return self._coordinates.distance_to(other.coordinates)
