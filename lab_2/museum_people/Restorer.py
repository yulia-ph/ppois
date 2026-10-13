from exceptions.RestorationException import RestorationException
from museum_people.Employee import Employee


class Restorer(Employee):
    """A museum restorer.

    Restorers work on damaged exhibits, creating Restoration processes
    and producing reports. Each restorer has a specialization and a
    certificate.

    A restorer can only start a restoration on an exhibit that
    actually needs one (damaged or critical condition). Attempting to
    restore a healthy exhibit is an error.
    """

    BASE_RESTORATION_COST = 1000.0
    CONDITION_COST_MULTIPLIERS = {
        "excellent": 0.5,
        "good": 1.0,
        "damaged": 2.0,
        "critical": 5.0,
    }
    FALLBACK_COST_MULTIPLIER = 1.0

    def __init__(self, name: str, salary: float, hire_date,
                 specialization: str, certificate: str):
        """Initialize a restorer.

        Args:
            name: Employee name. Must not be empty.
            salary: Monthly salary. Must be non-negative.
            hire_date: Date of hire. Must not be None.
            specialization: Area of expertise. Must not be empty.
            certificate: Certificate identifier. Must not be empty.

        Raises:
            ValueError: If inherited validation fails, or
                specialization or certificate is empty.
        """
        super().__init__(name, salary, hire_date)
        if not specialization:
            raise ValueError("Specialization must not be empty")
        if not certificate:
            raise ValueError("Certificate must not be empty")
        self._specialization = specialization
        self._certificate = certificate
        self._tasks = []


    @property
    def specialization(self):
        return self._specialization

    @property
    def certificate(self):
        return self._certificate

    @property
    def tasks(self):
        return list(self._tasks)


    def restore_exhibit(self, exhibit):
        """Start a restoration process for an exhibit.

        Args:
            exhibit: The exhibit to restore. Must not be None, and must
                need restoration (condition is damaged or critical).

        Returns:
            The started Restoration instance.

        Raises:
            ValueError: If exhibit is None.
            RestorationException: If the exhibit does not need
                restoration, or if the restoration could not be started.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        if not exhibit.needs_restoration():
            raise RestorationException(
                f"Exhibit '{exhibit.inventory_number}' does not need restoration "
                f"(condition: {exhibit.condition})"
            )

        from museum_documents.Restoration import Restoration
        restoration = Restoration(exhibit, self)
        if not restoration.start_restoration():
            raise RestorationException(
                f"Could not start restoration for '{exhibit.inventory_number}'"
            )
        self._tasks.append(restoration)
        return restoration

    def make_restoration_report(self, restoration):
        """Generate a report for a completed restoration.

        Args:
            restoration: The restoration to report on. Must not be None
                and must be completed.

        Returns:
            The generated Report.

        Raises:
            ValueError: If restoration is None.
            RestorationException: If the report could not be generated.
        """
        if restoration is None:
            raise ValueError("Restoration must not be None")
        report = restoration.write_report()
        if report is None:
            raise RestorationException(
                "Cannot generate a report for an incomplete restoration"
            )
        return report


    def estimate_cost(self, exhibit) -> float:
        """Estimate the cost of restoring an exhibit.

        Cost is based on the exhibit's condition:
            excellent -> 0.5x base
            good      -> 1.0x base
            damaged   -> 2.0x base
            critical  -> 5.0x base

        Args:
            exhibit: The exhibit to estimate for. Must not be None.

        Raises:
            ValueError: If exhibit is None.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        multiplier = Restorer.CONDITION_COST_MULTIPLIERS.get(
            exhibit.condition, Restorer.FALLBACK_COST_MULTIPLIER
        )
        return Restorer.BASE_RESTORATION_COST * multiplier
