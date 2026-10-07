from exceptions.MuseumException import MuseumException


class AccessDeniedException(MuseumException):

    def __init__(self, person_name: str = None, zone: str = None):
        message = "Access is denied"
        if person_name and zone:
            message = f"Access is denied: {person_name} cannot enter zone {zone}"
        super().__init__(message, error_code="ACCESS_DENIED")
        self._person_name = person_name
        self._zone = zone

    @property
    def person_name(self):
        return self._person_name

    @property
    def zone(self):
        return self._zone