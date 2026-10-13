from datetime import date

from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Inventory:
    """A reconciliation of physical exhibits against the catalog.

    An inventory records which exhibits were physically scanned
    (found) and reconciles them against a reference catalog. It can
    only be reconciled once; after that, mismatches are fixed.

    A clean inventory has no mismatches: every catalog exhibit was
    scanned, and no scanned exhibit is missing from the catalog.
    """

    def __init__(self, responsible):
        """Initialize an inventory.

        Args:
            responsible: The employee responsible. Must not be None.

        Raises:
            ValueError: If responsible is None.
        """
        if responsible is None:
            raise ValueError("Responsible employee must not be None")
        self._date = date.today()
        self._responsible = responsible
        self._scanned = []
        self._reconciled = False
        self._mismatches = []


    @property
    def date(self):
        return self._date

    @property
    def responsible(self):
        return self._responsible

    @property
    def scanned(self):
        return list(self._scanned)

    @property
    def is_reconciled(self):
        return self._reconciled

    @property
    def mismatches(self):
        return list(self._mismatches)


    def scan_exhibit(self, exhibit):
        """Record a physically found exhibit.

        Args:
            exhibit: The exhibit. Must not be None and must not already
                be scanned.

        Raises:
            ValueError: If exhibit is None or already scanned.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        if exhibit in self._scanned:
            raise ValueError(
                f"Exhibit '{exhibit.inventory_number}' has already been scanned"
            )
        self._scanned.append(exhibit)
        return True

    def count_scanned(self) -> int:
        """Return the number of scanned exhibits."""
        return len(self._scanned)


    def reconcile(self, catalog_exhibits: list):
        """Reconcile scanned exhibits against a catalog.

        Args:
            catalog_exhibits: The reference list of exhibits that
                should be present.

        Raises:
            ValueError: If catalog_exhibits is None.
            InvalidExhibitStateException: If already reconciled.
        """
        if catalog_exhibits is None:
            raise ValueError("Catalog list must not be None")
        if self._reconciled:
            raise InvalidExhibitStateException(
                exhibit_title=str(self._date),
                state="reconciled",
                reason="Inventory has already been reconciled",
            )

        missing = [ex for ex in catalog_exhibits if ex not in self._scanned]
        extra = [ex for ex in self._scanned if ex not in catalog_exhibits]
        self._mismatches = missing + extra
        self._reconciled = True
        return True

    def is_clean(self) -> bool:
        """Return True if there are no mismatches after reconciliation.

        Returns False if reconciliation has not yet happened.
        """
        if not self._reconciled:
            return False
        return len(self._mismatches) == 0

    def generate_report(self):
        """Generate a Report instance summarizing this inventory."""
        from museum_documents.Report import Report
        report = Report(period=str(self._date), type_="inventory")
        report.generate({
            "responsible": self._responsible.name if self._responsible else None,
            "scanned": len(self._scanned),
            "mismatches": len(self._mismatches),
            "is_clean": self.is_clean(),
        })
        return report