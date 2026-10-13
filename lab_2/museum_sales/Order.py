from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Order:
    """A merchandise order placed by a museum visitor.

    An order collects items (ShopItem, quantity) pairs and tracks its
    status: pending, paid, or canceled. On checkout the order:

        1. Validates that all items are still available.
        2. Processes the payment.
        3. Deducts the items from stock.

    If step 3 fails after payment succeeded, the payment is refunded.
    Cancelling a paid order refunds the payment and returns items to
    stock.
    """

    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_CANCELLED = "cancelled"

    def __init__(self, buyer):
        """Initialize an order.

        Args:
            buyer: The visitor placing the order. Must not be None.
                Should expose `.membership` (may be None).

        Raises:
            ValueError: If buyer is None.
        """
        if buyer is None:
            raise ValueError("Buyer must not be None")
        self._buyer = buyer
        self._items = []
        self._status = Order.STATUS_PENDING
        self._payment = None


    @property
    def buyer(self):
        return self._buyer

    @property
    def items(self):
        return list(self._items)

    @property
    def status(self):
        return self._status

    @property
    def payment(self):
        return self._payment

    @property
    def is_paid(self):
        return self._status == Order.STATUS_PAID

    @property
    def is_cancelled(self):
        return self._status == Order.STATUS_CANCELLED


    def add_item(self, item, qty: int = 1):
        """Add an item (and quantity) to the order.

        If the item is already in the order, its quantity is increased.

        Args:
            item: The ShopItem to add. Must not be None.
            qty: Quantity to add. Must be positive.

        Raises:
            ValueError: If item is None or qty is not positive.
            InvalidExhibitStateException: If the item does not have
                enough stock for the requested quantity.
        """
        if item is None:
            raise ValueError("Item must not be None")
        if qty <= 0:
            raise ValueError(f"Quantity must be positive, got {qty}")
        if not item.is_available(qty):
            raise InvalidExhibitStateException(
                exhibit_title=item.name,
                state="out_of_stock",
                reason=f"Not enough stock: requested {qty}, available {item.stock}",
            )

        for i, (existing, existing_qty) in enumerate(self._items):
            if existing is item:
                self._items[i] = (existing, existing_qty + qty)
                return True
        self._items.append((item, qty))
        return True

    def remove_item(self, item):
        """Remove an item (all its quantity) from the order.

        Args:
            item: The ShopItem to remove. Must not be None.

        Raises:
            ValueError: If item is None or not in the order.
        """
        if item is None:
            raise ValueError("Item must not be None")
        for i, (existing, _) in enumerate(self._items):
            if existing is item:
                self._items.pop(i)
                return True
        raise ValueError(f"Item '{item.name}' is not in the order")


    def calculate_total(self) -> float:
        """Return the order total, after membership discount if any.

        The discount is applied via the buyer's membership (if any and
        active).
        """
        total = sum(item.price * qty for item, qty in self._items)
        membership = getattr(self._buyer, "membership", None)
        if membership is not None and membership.is_active():
            total *= (1 - membership.check_discount())
        return total

    def checkout(self, payment):
        """Pay for the order and deduct items from stock.

        Args:
            payment: The payment to use. Must expose `.amount` and
                `.process()`.

        Returns:
            True on success.

        Raises:
            InvalidExhibitStateException: If the order is not pending, or
                an item ran out of stock between add_item and checkout.
            ValueError: If the order is empty or the payment amount does
                not match the order total.
            PaymentFailedException: Propagated from payment.process().
        """
        self._ensure_pending()
        self._ensure_has_items()
        self._ensure_payment_matches(payment)
        self._ensure_items_available()

        payment.process()
        self._deduct_items(payment)

        self._payment = payment
        self._status = Order.STATUS_PAID
        return True

    def _ensure_pending(self):
        if self._status != Order.STATUS_PENDING:
            raise InvalidExhibitStateException(
                exhibit_title=f"Order for {self._buyer.name}",
                state=self._status,
                reason="Cannot checkout an order that is not pending",
            )

    def _ensure_has_items(self):
        if not self._items:
            raise ValueError("Cannot checkout an empty order")

    def _ensure_payment_matches(self, payment):
        total = self.calculate_total()
        if payment.amount != total:
            raise ValueError(
                f"Payment amount {payment.amount} does not match "
                f"order total {total}"
            )

    def _ensure_items_available(self):
        for item, qty in self._items:
            if not item.is_available(qty):
                raise InvalidExhibitStateException(
                    exhibit_title=item.name,
                    state="out_of_stock",
                    reason=f"Stock changed: need {qty}, available {item.stock}",
                )

    def _deduct_items(self, payment):
        try:
            for item, qty in self._items:
                item.sell(qty)
        except InvalidExhibitStateException:
            payment.refund()
            raise

    def cancel(self):
        """Cancel the order.

        If the order was paid, the payment is refunded and items are
        returned to stock.

        Idempotent: cancelling an already cancelled order is not an
        error.
        """
        if self._status == Order.STATUS_CANCELLED:
            return True
        if self._status == Order.STATUS_PAID:
            if self._payment is not None:
                self._payment.refund()
            for item, qty in self._items:
                item.replenish(qty)
        self._status = Order.STATUS_CANCELLED
        return True