from exceptions.LogisticsException import LogisticsException


class WarehouseCapacityExceededException(LogisticsException):

    def __init__(self, warehouse_name: str = None, capacity: float = None):
        message = "The warehouse is full"
        if warehouse_name:
            message = f"Warehouse «{warehouse_name}» is full"
            if capacity is not None:
                message += f" (capacity: {capacity})"
        super().__init__(message, error_code="WAREHOUSE_FULL")
        self._warehouse_name = warehouse_name
        self._capacity = capacity

    @property
    def warehouse_name(self):
        return self._warehouse_name

    @property
    def capacity(self):
        return self._capacity
