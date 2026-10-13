from exceptions.MuseumException import MuseumException


class ExhibitNotFoundException(MuseumException):

    def __init__(self, inventory_number: str = None):
        message = "The exhibit was not found"
        if inventory_number:
            message = f"The exhibit with the inventory number {inventory_number} was not found"
        super().__init__(message, error_code="EXHIBIT_NOT_FOUND")
        self._inventory_number = inventory_number

    @property
    def inventory_number(self):
        return self._inventory_number