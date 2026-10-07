from exceptions.MuseumException import MuseumException


class StorageCapacityExceededException(MuseumException):

    def __init__(self, storage_name: str = None, capacity: int = None):
        message = "The storage is full"
        if storage_name:
            message = f"Storage «{storage_name}» is full"
            if capacity is not None:
                message += f" (capacity: {capacity})"
        super().__init__(message, error_code="STORAGE_FULL")
        self._storage_name = storage_name
        self._capacity = capacity

    @property
    def storage_name(self):
        return self._storage_name

    @property
    def capacity(self):
        return self._capacity