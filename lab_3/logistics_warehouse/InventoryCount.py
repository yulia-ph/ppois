from datetime import date

from exceptions.InvalidCargoStateException import InvalidCargoStateException


class InventoryCount:
    """A physical count of warehouse cargo against a catalog."""

    def __init__(self, warehouse, responsible):
        if warehouse is None:
            raise ValueError("Warehouse must not be None")
        if responsible is None:
            raise ValueError("Responsible employee must not be None")
        self._warehouse = warehouse
        self._responsible = responsible
        self._scanned = []
        self._mismatches = []
        self._is_reconciled = False
        self._date = date.today()

    @property
    def warehouse(self):
        return self._warehouse

    @property
    def responsible(self):
        return self._responsible

    @property
    def scanned(self):
        return list(self._scanned)

    @property
    def mismatches(self):
        return list(self._mismatches)

    @property
    def is_reconciled(self):
        return self._is_reconciled

    @property
    def date(self):
        return self._date

    @staticmethod
    def diff(found: list, catalog: list):
        """Return (missing, extra) relative to a catalog."""
        missing = [ex for ex in catalog if ex not in found]
        extra = [ex for ex in found if ex not in catalog]
        return missing, extra

    def scan(self, cargo):
        """Record a physically found cargo item."""
        if cargo is None:
            raise ValueError("Cargo must not be None")
        if cargo in self._scanned:
            raise ValueError("Cargo has already been scanned")
        self._scanned.append(cargo)
        return True

    def reconcile(self, catalog):
        """Compare scanned items against a catalog."""
        if catalog is None:
            raise ValueError("Catalog must not be None")
        if self._is_reconciled:
            raise InvalidCargoStateException(
                title=str(self._date),
                state="reconciled",
                reason="Inventory has already been reconciled",
            )
        missing, extra = InventoryCount.diff(self._scanned, catalog)
        self._mismatches = missing + extra
        self._is_reconciled = True
        return True

    def is_clean(self) -> bool:
        """True if reconciled with no mismatches."""
        if not self._is_reconciled:
            return False
        return len(self._mismatches) == 0

    def generate_report(self):
        """Build an inventory report."""
        from logistics_documents.Report import Report
        report = Report(period=str(self._date), type_=Report.TYPE_INVENTORY)
        report.generate({
            "responsible": self._responsible.name,
            "scanned": len(self._scanned),
            "mismatches": len(self._mismatches),
            "is_clean": self.is_clean(),
        })
        return report
