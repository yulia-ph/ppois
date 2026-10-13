from datetime import date

from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Acquisition:
    """The acquisition of a new exhibit by the museum.

    An acquisition records how an exhibit entered the museum: by
    purchase, gift, or find. It goes through an approval step before
    the exhibit is registered (given an acquisition date). An
    acquisition can optionally be linked to an invoice.
    """

    SOURCE_PURCHASE = "purchase"
    SOURCE_GIFT = "gift"
    SOURCE_FIND = "find"

    VALID_SOURCES = (SOURCE_PURCHASE, SOURCE_GIFT, SOURCE_FIND)

    def __init__(self, source: str, exhibit, price: float = 0.0):
        """Initialize an acquisition.

        Args:
            source: One of VALID_SOURCES.
            exhibit: The acquired exhibit. Must not be None.
            price: Acquisition price. Must be non-negative.

        Raises:
            ValueError: If source is invalid, exhibit is None, or price
                is negative.
        """
        if source not in Acquisition.VALID_SOURCES:
            raise ValueError(
                f"Invalid source '{source}'. "
                f"Must be one of {Acquisition.VALID_SOURCES}"
            )
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        if price < 0:
            raise ValueError(f"Price must be non-negative, got {price}")

        self._source = source
        self._date = date.today()
        self._exhibit = exhibit
        self._price = price
        self._approved = False
        self._invoice = None


    @property
    def source(self):
        return self._source

    @property
    def date(self):
        return self._date

    @property
    def exhibit(self):
        return self._exhibit

    @property
    def price(self):
        return self._price

    @property
    def is_approved(self):
        return self._approved

    @property
    def invoice(self):
        return self._invoice


    def approve_acquisition(self):
        """Approve the acquisition.

        Raises:
            InvalidExhibitStateException: If the acquisition is already
                approved.
        """
        if self._approved:
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.inventory_number,
                state="approved",
                reason="Acquisition is already approved",
            )
        self._approved = True
        return True

    def register_exhibit(self):
        """Register the exhibit: set its acquisition date.

        Raises:
            InvalidExhibitStateException: If the acquisition has not
                been approved yet.
        """
        if not self._approved:
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.inventory_number,
                state="not_approved",
                reason="Cannot register an unapproved acquisition",
            )
        return self._exhibit.set_acquired_date(self._date)


    def set_price(self, value: float):
        """Change the acquisition price.

        Args:
            value: New price. Must be non-negative.

        Raises:
            ValueError: If value is negative.
            InvalidExhibitStateException: If the acquisition is already
                approved.
        """
        if value < 0:
            raise ValueError(f"Price must be non-negative, got {value}")
        if self._approved:
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.inventory_number,
                state="approved",
                reason="Cannot change the price of an approved acquisition",
            )
        self._price = value
        return True

    def attach_invoice(self, invoice):
        """Attach an invoice to the acquisition.

        Args:
            invoice: The invoice. Must not be None.

        Raises:
            ValueError: If invoice is None.
        """
        if invoice is None:
            raise ValueError("Invoice must not be None")
        self._invoice = invoice
        return True