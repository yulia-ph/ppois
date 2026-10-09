from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
from exceptions.LoanOverdueException import LoanOverdueException
from museum_people.Employee import Employee


class Administrator(Employee):
    """A museum administrator.

    Handles cross-cutting management tasks: approving loans, paying
    invoices, hiring and firing staff, and scheduling. Works with
    other domain objects through duck typing (no direct imports of
    Loan, Invoice, Payment, Museum) to avoid circular dependencies.
    """

    def __init__(self, name: str, salary: float, hire_date, department: str):
        """Initialize an administrator.

        Args:
            name: Employee name. Must not be empty.
            salary: Monthly salary. Must be non-negative.
            hire_date: Date of hire. Must not be None.
            department: The department name. Must not be empty.

        Raises:
            ValueError: If any inherited validation fails, or
                department is empty.
        """
        super().__init__(name, salary, hire_date)
        if not department:
            raise ValueError("Department must not be empty")
        self._department = department
        self._invoices = []
        self._hired_employees = []


    @property
    def department(self):
        return self._department

    @property
    def invoices(self):
        return list(self._invoices)

    @property
    def hired_employees(self):
        return list(self._hired_employees)


    def approve_loan(self, loan):
        """Approve a loan request (final approval).

        Args:
            loan: The loan to approve. Must not be None.

        Returns:
            The result of `loan.approve_loan()`.

        Raises:
            ValueError: If loan is None.
            LoanOverdueException: If the loan is already overdue.
        """
        if loan is None:
            raise ValueError("Loan must not be None")
        if loan.is_overdue():
            raise LoanOverdueException()
        return loan.approve_loan()

    def pay_invoice(self, invoice, payment):
        """Pay an invoice.

        Raises:
            ValueError: If invoice or payment is None, or amount mismatch.
            InvalidExhibitStateException: If the invoice was already paid
                or if the payment is not pending.
        """
        if invoice is None:
            raise ValueError("Invoice must not be None")
        if payment is None:
            raise ValueError("Payment must not be None")
        if payment.amount != invoice.amount:
            raise ValueError(
                f"Payment amount {payment.amount} does not match "
                f"invoice amount {invoice.amount}"
            )
        payment.process()
        if not invoice.pay(payment):
            raise InvalidExhibitStateException(
                exhibit_title=f"INV {invoice.amount}",
                state="already_paid",
                reason="Invoice has already been paid",
            )
        self._invoices.append(invoice)
        return True

    def hire_employee(self, museum, employee):
        """Hire an employee into the museum.

        Args:
            museum: The museum to add the employee to. Must not be None.
            employee: The employee to add. Must not be None.

        Returns:
            True on success.

        Raises:
            ValueError: If museum or employee is None, or the employee
                is already in the museum.
        """
        if museum is None:
            raise ValueError("Museum must not be None")
        if employee is None:
            raise ValueError("Employee must not be None")
        if employee in museum.employees:
            raise ValueError(
                f"Employee '{employee.name}' is already registered in the museum"
            )
        museum.add_employee(employee)
        self._hired_employees.append(employee)
        return True

    def fire_employee(self, museum, employee):
        """Fire an employee from the museum.

        Args:
            museum: The museum to remove the employee from. Must not be None.
            employee: The employee to remove. Must not be None.

        Returns:
            True on success.

        Raises:
            ValueError: If museum or employee is None, or the employee
                is not in the museum.
        """
        if museum is None:
            raise ValueError("Museum must not be None")
        if employee is None:
            raise ValueError("Employee must not be None")
        if employee not in museum.employees:
            raise ValueError(
                f"Employee '{employee.name}' is not registered in the museum"
            )
        museum.remove_employee(employee)
        return True