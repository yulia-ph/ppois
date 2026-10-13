from datetime import date

from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Restoration:
    """A restoration process on a damaged or critical exhibit.

    A restoration moves through states:

        PENDING -> IN_PROGRESS -> COMPLETED

    The exhibit must need restoration (damaged or critical) before
    the process can start. Completing the restoration updates the
    exhibit's condition to "good" — this is the only place where an
    exhibit's condition changes through a restoration.
    """

    STATUS_PENDING = "pending"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"

    def __init__(self, exhibit, restorer):
        """Initialize a restoration process.

        Args:
            exhibit: The exhibit to restore. Must not be None.
            restorer: The restorer. Must not be None.

        Raises:
            ValueError: If exhibit or restorer is None.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        if restorer is None:
            raise ValueError("Restorer must not be None")
        self._exhibit = exhibit
        self._restorer = restorer
        self._start_date = None
        self._end_date = None
        self._status = Restoration.STATUS_PENDING
        self._cost = 0.0
        self._report = None


    @property
    def exhibit(self):
        return self._exhibit

    @property
    def restorer(self):
        return self._restorer

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def status(self):
        return self._status

    @property
    def cost(self):
        return self._cost

    @property
    def report(self):
        return self._report

    @property
    def is_completed(self):
        return self._status == Restoration.STATUS_COMPLETED

    @property
    def is_in_progress(self):
        return self._status == Restoration.STATUS_IN_PROGRESS


    def start_restoration(self):
        """Start the restoration.

        Raises:
            InvalidExhibitStateException: If not pending, or the
                exhibit does not need restoration.
        """
        if self._status != Restoration.STATUS_PENDING:
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.inventory_number,
                state=self._status,
                reason="Cannot start a restoration that is not pending",
            )
        if not self._exhibit.needs_restoration():
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.inventory_number,
                state=self._exhibit.condition,
                reason="Exhibit does not need restoration",
            )
        self._status = Restoration.STATUS_IN_PROGRESS
        self._start_date = date.today()
        self._cost = self._restorer.estimate_cost(self._exhibit)
        return True

    def complete_restoration(self):
        """Complete the restoration and set the exhibit's condition to good.

        Raises:
            InvalidExhibitStateException: If the restoration is not
                in progress.
        """
        if self._status != Restoration.STATUS_IN_PROGRESS:
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.inventory_number,
                state=self._status,
                reason="Cannot complete a restoration that is not in progress",
            )
        self._end_date = date.today()
        self._status = Restoration.STATUS_COMPLETED
        self._exhibit.update_condition("good")
        return True


    def write_report(self):
        """Generate and attach a Report summarizing this restoration.

        Raises:
            InvalidExhibitStateException: If the restoration is not
                completed.
        """
        if self._status != Restoration.STATUS_COMPLETED:
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.inventory_number,
                state=self._status,
                reason="Cannot write a report for an incomplete restoration",
            )
        from museum_documents.Report import Report
        report = Report(
            period=f"{self._start_date} — {self._end_date}",
            type_=Report.TYPE_RESTORATION,
        )
        report.generate({
            "exhibit": self._exhibit.inventory_number,
            "restorer": self._restorer.name,
            "cost": self._cost,
        })
        self._report = report
        return report


    def calculate_duration(self) -> int:
        """Return the restoration duration in days (0 if incomplete)."""
        if self._start_date is None or self._end_date is None:
            return 0
        return (self._end_date - self._start_date).days

    def set_cost(self, value: float):
        """Change the restoration cost.

        Args:
            value: New cost. Must be non-negative.

        Raises:
            ValueError: If value is negative.
            InvalidExhibitStateException: If the restoration is already
                in progress or completed (cost is set automatically on
                start and must not change afterward).
        """
        if value < 0:
            raise ValueError(f"Cost must be non-negative, got {value}")
        if self._status != Restoration.STATUS_PENDING:
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.inventory_number,
                state=self._status,
                reason="Cannot set cost after the restoration has started",
            )
        self._cost = value
        return True