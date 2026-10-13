from exceptions.MuseumException import MuseumException


class InventoryMismatchException(MuseumException):

    def __init__(self, missing_count: int = 0, extra_count: int = 0):
        message = "Inventory discrepancy"
        if missing_count or extra_count:
            message = f"Inventory: missing {missing_count}, extra {extra_count}"
        super().__init__(message, error_code="INVENTORY_MISMATCH")
        self._missing_count = missing_count
        self._extra_count = extra_count

    @property
    def missing_count(self):
        return self._missing_count

    @property
    def extra_count(self):
        return self._extra_count