from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class ShopItem:
    """A merchandise item sold in the museum shop.

    Tracks the item's name, price, and current stock. Provides
    operations for selling, replenishing, and re-pricing. Stock is
    managed as a non-negative integer.
    """

    def __init__(self, name: str, price: float, stock: int):
        """Initialize a shop item.

        Args:
            name: The item name. Must not be empty.
            price: The unit price. Must be non-negative.
            stock: Initial stock count. Must be non-negative.

        Raises:
            ValueError: If name is empty, or price/stock is negative.
        """
        if not name:
            raise ValueError("Item name must not be empty")
        if price < 0:
            raise ValueError(f"Price must be non-negative, got {price}")
        if stock < 0:
            raise ValueError(f"Stock must be non-negative, got {stock}")

        self._name = name
        self._price = price
        self._stock = stock


    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def stock(self):
        return self._stock


    def is_available(self, qty: int = 1) -> bool:
        """Return True if at least `qty` units are in stock."""
        return self._stock >= qty

    def sell(self, qty: int = 1):
        """Sell the given quantity of the item.

        Args:
            qty: Number of units to sell. Must be positive.

        Raises:
            ValueError: If qty is not positive.
            InvalidExhibitStateException: If there is not enough stock.
        """
        if qty <= 0:
            raise ValueError(f"Quantity must be positive, got {qty}")
        if not self.is_available(qty):
            raise InvalidExhibitStateException(
                exhibit_title=self._name,
                state="out_of_stock",
                reason=f"Only {self._stock} units in stock, requested {qty}",
            )
        self._stock -= qty
        return True

    def replenish(self, qty: int):
        """Add the given quantity to the stock.

        Args:
            qty: Number of units to add. Must be positive.

        Raises:
            ValueError: If qty is not positive.
        """
        if qty <= 0:
            raise ValueError(f"Quantity must be positive, got {qty}")
        self._stock += qty
        return True