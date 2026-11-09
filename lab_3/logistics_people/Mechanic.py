from datetime import date

from logistics_people.Employee import Employee


class Mechanic(Employee):
    """A mechanic who inspects and repairs vehicles."""

    HOURLY_RATE = 40.0

    def __init__(self, name: str, salary: float, hire_date: date, specialization: str, certificate: str):
        super().__init__(name, salary, hire_date)
        if not specialization:
            raise ValueError("Specialization must not be empty")
        if not certificate:
            raise ValueError("Certificate must not be empty")
        self._specialization = specialization
        self._certificate = certificate
        self._jobs = []

    @property
    def specialization(self):
        return self._specialization

    @property
    def certificate(self):
        return self._certificate

    @property
    def jobs(self):
        return list(self._jobs)

    def inspect_vehicle(self, vehicle) -> bool:
        """Return True if the vehicle looks roadworthy (has fuel)."""
        if vehicle is None:
            raise ValueError("Vehicle must not be None")
        return vehicle.fuel_level > 0

    def repair(self, record):
        """Start a maintenance record and keep it on the job list."""
        if record is None:
            raise ValueError("Record must not be None")
        record.start_work()
        self._jobs.append(record)
        return True

    def write_report(self, record):
        """Build a short report for a completed job."""
        if record is None:
            raise ValueError("Record must not be None")
        from logistics_documents.Report import Report
        report = Report(period=str(record.date), type_=Report.TYPE_MAINTENANCE)
        report.set_author(self.name)
        report.generate({
            "vehicle": record.vehicle.plate,
            "cost": record.cost,
            "status": record.status,
        })
        return report

    def estimate_cost(self, hours: float) -> float:
        """Estimate labour cost."""
        if hours <= 0:
            raise ValueError(f"Hours must be positive, got {hours}")
        return hours * Mechanic.HOURLY_RATE
