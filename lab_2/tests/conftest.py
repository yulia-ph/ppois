"""Shared pytest fixtures for the museum test suite."""
from datetime import date, timedelta

import pytest

from museum_core.Building import Building
from museum_core.Hall import Hall
from museum_core.Room import Room, RoomPurpose
from museum_exhibits.Catalog import Catalog
from museum_exhibits.Exhibit import Exhibit


@pytest.fixture
def main_building():
    """A main-type building with three floors."""
    return Building("Main Building", "1 Main St", Building.TYPE_MAIN, 3)


@pytest.fixture
def storage_building():
    """A storage-type building."""
    return Building("Storage", "2 Storage St", Building.TYPE_STORAGE, 1)


@pytest.fixture
def admin_building():
    """An admin-type building."""
    return Building("Admin", "3 Admin St", Building.TYPE_ADMIN, 2)


@pytest.fixture
def sample_hall():
    """A simple hall instance."""
    return Hall(1, 100.0)


@pytest.fixture
def sample_room():
    """A simple room instance."""
    return Room(101, RoomPurpose.OFFICE)

from museum_core.ClimateZone import ClimateZone


@pytest.fixture
def climate_zone():
    """A standard climate zone with norm 20°C / 50%."""
    return ClimateZone(norm_temperature=20.0, norm_humidity=50.0)


class FakeShowcase:
    """Minimal showcase stub for Hall tests."""
    _counter = 0

    def __init__(self, inventory_number=None, exhibit=None):
        FakeShowcase._counter += 1
        self.inventory_number = inventory_number or f"SC-{FakeShowcase._counter:03d}"
        self.exhibit = exhibit


@pytest.fixture
def fake_showcase():
    """A minimal showcase stub."""
    return FakeShowcase()


@pytest.fixture
def fake_showcase_with_exhibit():
    """A showcase stub with a fake exhibit attached."""
    return FakeShowcase(exhibit=object())


from museum_core.Museum import Museum


class FakeNamed:
    """Fake object with a name attribute."""
    def __init__(self, name):
        self.name = name


class FakeTitled:
    """Fake object with a title attribute."""
    def __init__(self, title):
        self.title = title


class FakeAccessRecord:
    """Fake AccessControl record."""
    def __init__(self, is_granted, zone, time):
        self.is_granted = is_granted
        self.zone = zone
        self.time = time


@pytest.fixture
def museum():
    """An empty museum instance."""
    return Museum("Hermitage", "Palace Sq. 2", "hermitage.ru")


@pytest.fixture
def fake_building():
    return FakeNamed("Main Building")


@pytest.fixture
def fake_employee():
    return FakeNamed("Ivanov")


@pytest.fixture
def fake_fund():
    return FakeNamed("Painting Fund")


@pytest.fixture
def fake_exhibition():
    return FakeTitled("Impressionists")


@pytest.fixture
def fake_ticket_type():
    return FakeNamed("Adult")


class FakeClimateZone:
    """Minimal climate-zone stub with a controllable norm flag."""

    def __init__(self, within_norm=True):
        self._within_norm = within_norm

    def is_within_norm(self):
        return self._within_norm


@pytest.fixture
def fake_climate_zone_ok():
    """A fake climate zone that is always within norm."""
    return FakeClimateZone(within_norm=True)


@pytest.fixture
def fake_climate_zone_bad():
    """A fake climate zone that is out of norm."""
    return FakeClimateZone(within_norm=False)


@pytest.fixture
def sensor_temperature(climate_zone):
    """A temperature sensor attached to the standard climate zone."""
    from museum_core.Sensor import Sensor, SensorType
    return Sensor("T-01", SensorType.TEMPERATURE, climate_zone)


@pytest.fixture
def sensor_humidity(climate_zone):
    """A humidity sensor attached to the standard climate zone."""
    from museum_core.Sensor import Sensor, SensorType
    return Sensor("H-01", SensorType.HUMIDITY, climate_zone)


@pytest.fixture
def sensor_motion(climate_zone):
    """A motion sensor attached to the standard climate zone."""
    from museum_core.Sensor import Sensor, SensorType
    return Sensor("M-01", SensorType.MOTION, climate_zone)


class FakeEmployee:
    """Minimal employee stub with a position attribute."""
    def __init__(self, name="Ivanov", position="Curator"):
        self.name = name
        self.position = position


class FakeVisitor:
    """Fake object with no position — used to test access denial."""
    def __init__(self, name="Anna"):
        self.name = name


class FakeExhibit(Exhibit):
    """Minimal exhibit stub with title and condition."""
    def __init__(self, title="Mona Lisa", condition="good"):
        super().__init__(title, "Unknown", condition)


@pytest.fixture
def fake_employee_with_position():
    """An employee stub with a `position` attribute."""
    return FakeEmployee()


@pytest.fixture
def fake_visitor():
    return FakeVisitor()


@pytest.fixture
def fake_exhibit():
    return FakeExhibit(title="Mona Lisa", condition="good")


@pytest.fixture
def fake_exhibit_damaged():
    return FakeExhibit(title="Broken Vase", condition="damaged")


@pytest.fixture
def fake_exhibit_critical():
    return FakeExhibit(title="Ruined Fresco", condition="critical")


@pytest.fixture
def showcase():
    from museum_core.Showcase import Showcase
    return Showcase("SC-001", "horizontal")


@pytest.fixture
def showcase_open(showcase, fake_employee_with_position):
    showcase.open_showcase(fake_employee_with_position)
    return showcase


@pytest.fixture
def showcase_with_exhibit(showcase, fake_exhibit):
    showcase.place_exhibit(fake_exhibit)
    return showcase


class FakeExhibitForStorage:
    """Minimal exhibit stub with only inventory_number."""
    def __init__(self, inventory_number):
        self.inventory_number = inventory_number


@pytest.fixture
def storage():
    """A storage with capacity 3."""
    from museum_core.Storage import Storage
    return Storage("Main Storage", 3)


@pytest.fixture
def storage_full():
    """A storage already filled to capacity."""
    from museum_core.Storage import Storage
    s = Storage("Tiny", 2)
    s.place_exhibit(FakeExhibitForStorage("EX-001")) # type: ignore[arg-type]
    s.place_exhibit(FakeExhibitForStorage("EX-002")) # type: ignore[arg-type]
    return s


@pytest.fixture
def fake_exhibit_storage_a():
    return FakeExhibitForStorage("EX-100")


@pytest.fixture
def fake_exhibit_storage_b():
    return FakeExhibitForStorage("EX-200")



class FakeExhibitForCatalog:
    """Minimal exhibit stub for Catalog tests."""

    def __init__(self, inventory_number, title="Untitled", author="Unknown",
                 condition="good", collection=None, insurance_value=0.0):
        self.inventory_number = inventory_number
        self.title = title
        self.author = author
        self.condition = condition
        self.collection = collection
        self.insurance_value = insurance_value


@pytest.fixture
def catalog():
    return Catalog()


@pytest.fixture
def sample_exhibits():
    """Three exhibits used across Catalog tests."""
    return [
        FakeExhibitForCatalog("EX-001", "Mona Lisa", "Leonardo",
                              "excellent", insurance_value=1000.0),
        FakeExhibitForCatalog("EX-002", "Sunflowers", "Van Gogh",
                              "good", insurance_value=500.0),
        FakeExhibitForCatalog("EX-003", "Starry Night", "Van Gogh",
                              "damaged", insurance_value=800.0),
    ]


@pytest.fixture
def catalog_with_exhibits(sample_exhibits):
    """A catalog preloaded with three exhibits."""
    c = Catalog()
    for ex in sample_exhibits:
        c.add(ex)
    return c


class FakeExhibitForCollection:
    """Minimal exhibit stub for Collection tests.

    Implements the interface expected by Collection:
        - inventory_number, title, author, condition, insurance_value
        - attach_to_collection(collection) -> bool
        - remove_from_collection()
        - is_available_for_exhibition() -> bool
    """

    def __init__(self, inventory_number, title="Untitled", author="Unknown",
                 condition="good", insurance_value=0.0,
                 available=True):
        self.inventory_number = inventory_number
        self.title = title
        self.author = author
        self.condition = condition
        self.insurance_value = insurance_value
        self._available = available
        self._collection = None

    def attach_to_collection(self, collection):
        if collection is None:
            return False
        if self._collection is not None:
            return False
        self._collection = collection
        return True

    def remove_from_collection(self):
        self._collection = None
        return True

    def is_available_for_exhibition(self):
        return self._available


@pytest.fixture
def collection():
    """An empty collection."""
    from museum_exhibits.Collection import Collection
    return Collection("Dutch Golden Age", "17th-century Dutch painting")


@pytest.fixture
def collection_exhibits():
    """Three exhibits for Collection tests."""
    return [
        FakeExhibitForCollection("EX-001", "Night Watch", "Rembrandt",
                                 "excellent", insurance_value=5000.0),
        FakeExhibitForCollection("EX-002", "Girl with a Pearl Earring", "Vermeer",
                                 "good", insurance_value=3000.0),
        FakeExhibitForCollection("EX-003", "The Anatomy Lesson", "Rembrandt",
                                 "damaged", insurance_value=1000.0,
                                 available=False),
    ]


@pytest.fixture
def collection_with_exhibits(collection_exhibits):
    """A collection preloaded with three exhibits."""
    from museum_exhibits.Collection import Collection
    c = Collection("Dutch Golden Age", "17th-century Dutch painting")
    for ex in collection_exhibits:
        c.add_exhibit(ex)
    return c


class FakeExhibitForDigitalCopy:
    """Minimal exhibit stub with only inventory_number."""
    def __init__(self, inventory_number="EX-001"):
        self.inventory_number = inventory_number


@pytest.fixture
def fake_source():
    return FakeExhibitForDigitalCopy("EX-001")


@pytest.fixture
def digital_copy(fake_source):
    from museum_exhibits.DigitalCopy import DigitalCopy
    return DigitalCopy(fake_source, "jpg", 1024, "300dpi")


@pytest.fixture
def digital_copy_created(digital_copy):
    digital_copy.create()
    return digital_copy


@pytest.fixture
def document():
    from museum_exhibits.Document import Document
    return Document("Codex Sinaiticus", "Unknown", "manuscript",
                    pages=346, language="grc")


@pytest.fixture
def document_acidic():
    from museum_exhibits.Document import Document
    d = Document("Old Letter", "Someone", "letter", pages=2, language="en")
    d.set_acidity_level(4.0)
    return d


@pytest.fixture
def document_critical():
    from museum_exhibits.Document import Document
    return Document("Ruined Papyrus", "Unknown", "manuscript",
                    pages=1, language="grc",
                    condition="critical")


@pytest.fixture
def exhibit():
    """A plain Exhibit in good condition."""
    from museum_exhibits.Exhibit import Exhibit
    return Exhibit("Mona Lisa", "Leonardo da Vinci")


@pytest.fixture
def exhibit_damaged():
    from museum_exhibits.Exhibit import Exhibit
    return Exhibit("Broken Vase", "Unknown", condition="damaged")


@pytest.fixture
def exhibit_critical():
    from museum_exhibits.Exhibit import Exhibit
    return Exhibit("Ruined Fresco", "Unknown", condition="critical")


@pytest.fixture
def fake_location_a():
    """Fake location stub (Storage or Showcase)."""
    return object()


@pytest.fixture
def fake_location_b():
    return object()


@pytest.fixture
def fake_collection_a():
    """Fake collection stub."""
    return object()


@pytest.fixture
def fake_collection_b():
    return object()


@pytest.fixture
def fake_policy():
    """Fake insurance policy stub."""
    return object()



@pytest.fixture
def fund_painting():
    """A painting-only fund."""
    from museum_exhibits.Fund import Fund
    return Fund("Painting Fund", Fund.TYPE_PAINTING)


@pytest.fixture
def fund_mixed():
    """A mixed fund that accepts any exhibit type."""
    from museum_exhibits.Fund import Fund
    return Fund("Mixed Fund", Fund.TYPE_MIXED)


@pytest.fixture
def fund_with_collection():
    """A painting fund with one empty collection."""
    from museum_exhibits.Collection import Collection
    from museum_exhibits.Fund import Fund
    f = Fund("Painting Fund", Fund.TYPE_PAINTING)
    c = Collection("Dutch Golden Age", "17th-century Dutch painting")
    f.add_collection(c)
    return f

@pytest.fixture
def painting():
    """A painting in excellent condition."""
    from museum_exhibits.Painting import Painting
    return Painting("Night Watch", "Rembrandt", "oil", width=3.6, height=4.4,
                    condition="excellent")


@pytest.fixture
def painting_damaged():
    """A damaged painting."""
    from museum_exhibits.Painting import Painting
    return Painting("Broken Canvas", "Unknown", "oil", width=1.0, height=1.0,
                    condition="damaged")


@pytest.fixture
def sculpture():
    """A sculpture in good condition."""
    from museum_exhibits.Sculpture import Sculpture
    return Sculpture("David", "Michelangelo", "marble", height=5.17, weight=5660.0)


@pytest.fixture
def employee():
    """A plain Employee hired in 2020."""
    from museum_people.Employee import Employee
    return Employee("Ivanov", 50000.0, date(2020, 1, 1))


@pytest.fixture
def employee_on_vacation():
    """An employee currently on vacation."""
    from museum_people.Employee import Employee
    e = Employee("Petrov", 60000.0, date(2019, 5, 15))
    e.take_vacation(date(2024, 6, 1), 14)
    return e


class FakeTicketTypeForVisitor:
    """Minimal ticket type for Visitor tests.

    Only exposes what Visitor.buy_ticket needs: cost, name, and
    is_eligible(visitor).
    """

    def __init__(self, name="Adult", cost=500.0, eligible=True):
        self._name = name
        self._cost = cost
        self._eligible = eligible

    @property
    def name(self):
        return self._name

    @property
    def cost(self):
        return self._cost

    def is_eligible(self, visitor):
        return self._eligible


@pytest.fixture
def visitor():
    """A plain visitor."""
    from museum_people.Visitor import Visitor
    return Visitor("Anna", 25)


@pytest.fixture
def fake_visitor_ticket_type():
    """An eligible ticket type for Visitor.buy_ticket."""
    return FakeTicketTypeForVisitor(name="Adult", cost=500.0, eligible=True)


@pytest.fixture
def fake_visitor_ticket_type_ineligible():
    """An ineligible ticket type."""
    return FakeTicketTypeForVisitor(name="Child", cost=200.0, eligible=False)


@pytest.fixture
def visitor_with_ticket(fake_visitor_ticket_type):
    """A visitor holding a valid ticket for today."""
    from museum_people.Visitor import Visitor
    v = Visitor("Boris", 30)
    v.buy_ticket(fake_visitor_ticket_type, date.today()) # type: ignore[arg-type]
    return v


class FakeMembership:
    def __init__(self, active=True, discount=0.10):
        self._active = active
        self._discount = discount

    def is_active(self):
        return self._active

    def check_discount(self):
        return self._discount if self._active else 0.0


class FakeCard:
    def __init__(self, balance=1000.0):
        self._balance = balance


@pytest.fixture
def fake_membership():
    return FakeMembership(active=True, discount=0.2)


@pytest.fixture
def fake_card():
    return FakeCard(balance=1000.0)


class FakeLoan:
    """Minimal loan stub for Administrator tests."""
    def __init__(self, overdue=False):
        self._overdue = overdue
        self._approved = False

    def is_overdue(self):
        return self._overdue

    def approve_loan(self):
        self._approved = True
        return True

    @property
    def is_approved(self):
        return self._approved


class FakeInvoice:
    """Minimal invoice stub for Administrator tests."""
    def __init__(self, amount, already_paid=False):
        self._amount = amount
        self._paid = already_paid

    @property
    def amount(self):
        return self._amount

    def pay(self, payment):
        if self._paid:
            return False
        payment.process()
        self._paid = True
        return True

    @property
    def is_paid(self):
        return self._paid


class FakePayment:
    """Minimal payment stub for Cashier and Administrator tests.

    When `succeed=False`, `process()` raises PaymentFailedException
    to simulate a real payment failure.
    """

    def __init__(self, amount, succeed=True):
        self._amount = amount
        self._succeed = succeed
        self._processed = False

    @property
    def amount(self):
        return self._amount

    def process(self):
        if not self._succeed:
            from exceptions.PaymentFailedException import PaymentFailedException
            raise PaymentFailedException(
                amount=self._amount,
                reason="Simulated payment failure",
            )
        self._processed = True
        return True

    @property
    def is_processed(self):
        return self._processed

class FakeMuseumForAdmin:
    """Minimal museum stub for Administrator tests."""
    def __init__(self, budget=0.0):
        self._employees = []
        self._budget = budget

    @property
    def employees(self):
        return list(self._employees)

    @property
    def budget(self):
        return self._budget

    def add_employee(self, employee):
        if employee in self._employees:
            raise ValueError("Employee already in museum")
        self._employees.append(employee)
        return True

    def remove_employee(self, employee):
        if employee not in self._employees:
            raise ValueError("Employee not in museum")
        self._employees.remove(employee)
        return True

    def spend_budget(self, amount):
        from exceptions.InsufficientFundsException import InsufficientFundsException
        if amount > self._budget:
            raise InsufficientFundsException(required=amount, available=self._budget)
        self._budget -= amount
        return True

    def increase_budget(self, amount):
        self._budget += amount
        return True


@pytest.fixture
def administrator():
    from museum_people.Administrator import Administrator
    return Administrator("Sidorov", 80000.0, date(2020, 1, 1), "management")


@pytest.fixture
def fake_loan():
    return FakeLoan(overdue=False)


@pytest.fixture
def fake_loan_overdue():
    return FakeLoan(overdue=True)


@pytest.fixture
def fake_invoice():
    return FakeInvoice(amount=1000.0)


@pytest.fixture
def fake_invoice_paid():
    return FakeInvoice(amount=1000.0, already_paid=True)


@pytest.fixture
def fake_payment_ok():
    return FakePayment(amount=1000.0, succeed=True)


@pytest.fixture
def fake_payment_fail():
    return FakePayment(amount=1000.0, succeed=False)


@pytest.fixture
def fake_museum():
    return FakeMuseumForAdmin(budget=100000.0)


@pytest.fixture
def cashier():
    from museum_people.Cashier import Cashier
    return Cashier("Petrova", 50000.0, date(2020, 1, 1), "day")


@pytest.fixture
def cashier_visitor():
    from museum_people.Visitor import Visitor
    return Visitor("Anna", 25)


class FakeExcursion:
    """Minimal excursion stub for Guide tests."""
    def __init__(self, can_start=True, can_finish=True):
        self._can_start = can_start
        self._can_finish = can_finish
        self._started = False
        self._finished = False

    def start(self):
        if not self._can_start:
            return False
        self._started = True
        return True

    def finish(self):
        if not self._can_finish:
            return False
        self._finished = True
        return True

    @property
    def is_started(self):
        return self._started

    @property
    def is_finished(self):
        return self._finished


@pytest.fixture
def guide():
    from museum_people.Guide import Guide
    return Guide("Smirnova", 45000.0, date(2019, 1, 1),
                 languages=["ru", "en"], experience_years=5)


@pytest.fixture
def fake_excursion():
    return FakeExcursion()


@pytest.fixture
def fake_excursion_cannot_start():
    return FakeExcursion(can_start=False)


@pytest.fixture
def fake_excursion_cannot_finish():
    return FakeExcursion(can_finish=False)


@pytest.fixture
def curator():
    from museum_people.Curator import Curator
    return Curator("Sokolova", 70000.0, date(2015, 1, 1), "painting")


@pytest.fixture
def fake_loan_pending():
    """A pending loan that approves cleanly."""
    return FakeLoan(overdue=False)


@pytest.fixture
def fake_loan_that_fails():
    """A loan whose approve_loan returns False."""
    class FailingLoan:
        borrower = "Other Museum"
        def is_overdue(self):
            return False
        def approve_loan(self):
            return False
    return FailingLoan()


@pytest.fixture
def restorer():
    from museum_people.Restorer import Restorer
    return Restorer("Ivanov", 60000.0, date(2018, 1, 1),
                    specialization="painting", certificate="cert-123")


@pytest.fixture
def restoration_module_stub(monkeypatch):
    """Inject a fake museum_documents.Restoration into sys.modules.

    Returns a class so tests can assert on instances.
    """
    import sys
    import types

    module = types.ModuleType("museum_documents.Restoration")

    class FakeRestoration:
        def __init__(self, exhibit, restorer):
            self.exhibit = exhibit
            self.restorer = restorer
            self._started = False
            self._completed = False

        def start_restoration(self):
            self._started = True
            return True

        def complete_restoration(self):
            self._completed = True
            return True

        def write_report(self):
            if not self._completed:
                return None
            return f"report-for-{self.exhibit.inventory_number}"

        @property
        def is_started(self):
            return self._started

        @property
        def is_completed(self):
            return self._completed

    module.Restoration = FakeRestoration
    parent = types.ModuleType("museum_documents")
    monkeypatch.setitem(sys.modules, "museum_documents", parent)
    monkeypatch.setitem(sys.modules, "museum_documents.Restoration", module)
    return FakeRestoration


@pytest.fixture
def guard():
    from museum_people.SecurityGuard import SecurityGuard
    return SecurityGuard("Sidorov", 40000.0, date(2020, 1, 1),
                         shift="night", zone="hall-1")


@pytest.fixture
def access_control_stub(monkeypatch):
    """Inject a fake museum_security.AccessControl into sys.modules."""
    import sys
    import types

    module = types.ModuleType("museum_security.AccessControl")

    class FakeAccessControl:
        _counter = 0

        def __init__(self, person, zone):
            FakeAccessControl._counter += 1
            self._id = FakeAccessControl._counter
            self._person = person
            self._zone = zone
            self._is_granted = False
            self._time = date.today()

        @property
        def person(self):
            return self._person

        @property
        def zone(self):
            return self._zone

        @property
        def is_granted(self):
            return self._is_granted

        @property
        def time(self):
            return self._time

        def check_access(self):
            # Simple rule: granted only if person has a `ticket`
            # attribute that is truthy.
            self._is_granted = getattr(self._person, "ticket", None) is not None
            return self._is_granted

    module.AccessControl = FakeAccessControl
    parent = types.ModuleType("museum_security")
    monkeypatch.setitem(sys.modules, "museum_security", parent)
    monkeypatch.setitem(sys.modules, "museum_security.AccessControl", module)
    return FakeAccessControl


@pytest.fixture
def incident_stub(monkeypatch):
    """Inject a fake museum_security.Incident into sys.modules."""
    import sys
    import types

    module = types.ModuleType("museum_security.Incident")

    class FakeIncident:
        _counter = 0

        def __init__(self, type_, place, severity):
            FakeIncident._counter += 1
            self._id = f"INC-{FakeIncident._counter:04d}"
            self._type = type_
            self._place = place
            self._severity = severity
            self._guard = None
            self._is_closed = False
            self._can_close = False

        @property
        def id(self):
            return self._id

        @property
        def type(self):
            return self._type

        @property
        def place(self):
            return self._place

        @property
        def severity(self):
            return self._severity

        @property
        def guard(self):
            return self._guard

        @property
        def is_closed(self):
            return self._is_closed

        def assign_guard(self, guard):
            self._guard = guard
            self._can_close = True
            return True

        def close_incident(self):
            if not self._can_close or self._is_closed:
                return False
            self._is_closed = True
            return True

    module.Incident = FakeIncident
    parent = types.ModuleType("museum_security")
    monkeypatch.setitem(sys.modules, "museum_security", parent)
    monkeypatch.setitem(sys.modules, "museum_security.Incident", module)
    return FakeIncident


@pytest.fixture
def adult_ticket_type():
    from museum_sales.TicketType import TicketType
    return TicketType("Adult", cost=500.0, min_age=18)


@pytest.fixture
def child_ticket_type():
    from museum_sales.TicketType import TicketType
    return TicketType("Child", cost=200.0, max_age=17)


@pytest.fixture
def student_ticket_type():
    from museum_sales.TicketType import TicketType
    return TicketType("Student", cost=250.0, min_age=16, max_age=25)


@pytest.fixture
def ticket(adult_ticket_type):
    """A valid ticket for today, adult type."""
    from museum_sales.Ticket import Ticket
    return Ticket(adult_ticket_type, date.today())


@pytest.fixture
def ticket_yesterday(adult_ticket_type):
    from museum_sales.Ticket import Ticket
    return Ticket(adult_ticket_type, date.today() - timedelta(days=1))


@pytest.fixture
def ticket_used(ticket):
    ticket.mark_used()
    return ticket


@pytest.fixture
def ticket_refunded(ticket):
    ticket.refund()
    return ticket

@pytest.fixture
def magnet():
    from museum_sales.ShopItem import ShopItem
    return ShopItem("Museum Magnet", price=200.0, stock=50)


@pytest.fixture
def book():
    from museum_sales.ShopItem import ShopItem
    return ShopItem("Exhibition Catalog", price=500.0, stock=10)


@pytest.fixture
def sold_out_item():
    from museum_sales.ShopItem import ShopItem
    return ShopItem("Rare Postcard", price=1000.0, stock=0)


@pytest.fixture
def payment_cash():
    from museum_sales.Payment import Payment
    return Payment(amount=500.0, method=Payment.METHOD_CASH)


@pytest.fixture
def payment_card():
    from museum_sales.Payment import Payment
    return Payment(amount=500.0, method=Payment.METHOD_CARD)


@pytest.fixture
def payment_paid(payment_card):
    payment_card.process()
    return payment_card


@pytest.fixture
def payment_refunded(payment_paid):
    payment_paid.refund()
    return payment_paid


@pytest.fixture
def order(visitor):
    from museum_sales.Order import Order
    return Order(visitor)


@pytest.fixture
def order_with_items(visitor, magnet, book):
    from museum_sales.Order import Order
    o = Order(visitor)
    o.add_item(magnet, 1)
    o.add_item(book, 2)
    return o


@pytest.fixture
def paid_order(order_with_items, visitor):
    from museum_sales.Payment import Payment
    total = order_with_items.calculate_total()
    payment = Payment(total, Payment.METHOD_CARD)
    order_with_items.checkout(payment)
    return order_with_items


@pytest.fixture
def order_with_membership(visitor, magnet):
    """Order with a visitor having 20% membership discount."""
    from museum_sales.Order import Order
    visitor.get_membership(FakeMembership(active=True, discount=0.2))
    o = Order(visitor)
    o.add_item(magnet, 1)
    return o


@pytest.fixture
def booking(visitor):
    from museum_sales.Booking import Booking
    return Booking(visitor, date.today())


@pytest.fixture
def booking_with_tickets(visitor, adult_ticket_type):
    from museum_sales.Booking import Booking
    from museum_sales.Ticket import Ticket
    b = Booking(visitor, date.today())
    b.add_ticket(Ticket(adult_ticket_type, date.today()))
    b.add_ticket(Ticket(adult_ticket_type, date.today()))
    return b


@pytest.fixture
def confirmed_booking(booking_with_tickets):
    booking_with_tickets.confirm()
    return booking_with_tickets


@pytest.fixture
def paid_booking(confirmed_booking):
    from museum_sales.Payment import Payment
    total = confirmed_booking.calculate_total()
    payment = Payment(total, Payment.METHOD_CARD)
    confirmed_booking.pay(payment)
    return confirmed_booking


@pytest.fixture
def membership_basic(visitor):
    from museum_sales.Membership import Membership
    return Membership(visitor, "basic", date.today() + timedelta(days=365))


@pytest.fixture
def membership_silver(visitor):
    from museum_sales.Membership import Membership
    return Membership(visitor, "silver", date.today() + timedelta(days=365))


@pytest.fixture
def membership_gold(visitor):
    from museum_sales.Membership import Membership
    return Membership(visitor, "gold", date.today() + timedelta(days=365))


@pytest.fixture
def membership_expired(visitor):
    from museum_sales.Membership import Membership
    return Membership(visitor, "gold", date.today() - timedelta(days=1))


@pytest.fixture
def card(visitor):
    from museum_sales.MuseumCard import MuseumCard
    return MuseumCard(visitor, balance=1000.0)


@pytest.fixture
def empty_card(visitor):
    from museum_sales.MuseumCard import MuseumCard
    return MuseumCard(visitor, balance=0.0)


@pytest.fixture
def blocked_card(card):
    card.block()
    return card

@pytest.fixture
def access_attempt(visitor_with_ticket):
    from museum_security.AccessControl import AccessControl
    return AccessControl(visitor_with_ticket, AccessControl.ZONE_PUBLIC)


@pytest.fixture
def access_attempt_no_ticket(visitor):
    from museum_security.AccessControl import AccessControl
    return AccessControl(visitor, AccessControl.ZONE_PUBLIC)


@pytest.fixture
def employee_curator():
    from museum_people.Curator import Curator
    return Curator("Sokolova", 70000.0, date(2015, 1, 1), "painting")


@pytest.fixture
def employee_restorer():
    from museum_people.Restorer import Restorer
    return Restorer("Ivanov", 60000.0, date(2018, 1, 1), "painting", "cert-1")


@pytest.fixture
def employee_cashier():
    from museum_people.Cashier import Cashier
    return Cashier("Petrova", 50000.0, date(2020, 1, 1), "day")


@pytest.fixture
def employee_administrator():
    from museum_people.Administrator import Administrator
    return Administrator("Sidorov", 80000.0, date(2020, 1, 1), "management")


@pytest.fixture
def incident():
    from museum_security.Incident import Incident
    return Incident("theft", "Hall 1", "high")


@pytest.fixture
def incident_with_guard(incident, guard):
    incident.assign_guard(guard)
    return incident


@pytest.fixture
def incident_with_evidence(incident_with_guard):
    incident_with_guard.add_evidence("Camera captured the suspect at 22:15")
    return incident_with_guard


@pytest.fixture
def closed_incident(incident_with_evidence):
    incident_with_evidence.close_incident()
    return incident_with_evidence


@pytest.fixture
def audio_guide(exhibit):
    from museum_events.AudioGuide import AudioGuide
    return AudioGuide("en", duration=30, target=exhibit)


@pytest.fixture
def lecture_event():
    from museum_events.Event import Event
    return Event("Impressionism Today", Event.TYPE_LECTURE,
                 date(2025, 6, 1), "Hall A", capacity=50)


@pytest.fixture
def workshop_event():
    from museum_events.Event import Event
    return Event("Painting Workshop", Event.TYPE_WORKSHOP,
                 date(2025, 6, 2), "Studio 1", capacity=15)


@pytest.fixture
def concert_event():
    from museum_events.Event import Event
    return Event("Evening Concert", Event.TYPE_CONCERT,
                 date(2025, 6, 3), "Main Hall", capacity=200)


@pytest.fixture
def schedule():
    from museum_events.Schedule import Schedule
    return Schedule()


@pytest.fixture
def schedule_with_events(lecture_event, workshop_event):
    from museum_events.Schedule import Schedule
    s = Schedule()
    s.add_event(lecture_event)
    s.add_event(workshop_event)
    return s


@pytest.fixture
def exhibition(curator):
    from museum_exhibitions.Exhibition import Exhibition
    return Exhibition("Impressionists", date(2025, 1, 1), date(2025, 12, 31),
                      curator)


@pytest.fixture
def exhibition_open(exhibition):
    exhibition.open()
    return exhibition


@pytest.fixture
def temporary_exhibition(curator):
    from museum_exhibitions.TemporaryExhibition import TemporaryExhibition
    return TemporaryExhibition("Van Gogh in Paris",
                               date(2025, 1, 1), date(2025, 6, 30),
                               curator, theme="post-impressionism")


@pytest.fixture
def permanent_exhibition(curator):
    from museum_exhibitions.PermanentExhibition import PermanentExhibition
    return PermanentExhibition("Ancient Egypt",
                               date(2020, 1, 1), curator,
                               description="Permanent Egyptian collection")


@pytest.fixture
def fake_excursion_guide():
    """Guide to fixture already exists as `guide`, but here is a reminder."""
    from museum_people.Guide import Guide
    return Guide("Smirnov", 45000.0, date(2019, 1, 1),
                 languages=["ru", "en"], experience_years=5)


@pytest.fixture
def excursion(fake_excursion_guide, sample_hall):
    from datetime import datetime

    from museum_exhibitions.Excursion import Excursion
    return Excursion([sample_hall], fake_excursion_guide,
                     datetime(2025, 6, 1, 10, 0), duration_minutes=60)


@pytest.fixture
def excursion_with_visitors(excursion, visitor):
    excursion.add_visitor(visitor)
    return excursion


@pytest.fixture
def fake_loan_for_exhibition():
    """A loan stub for TemporaryExhibition tests."""
    class ExhibitionLoan:
        def __init__(self, returned=False, overdue=False):
            self._returned = returned
            self._overdue = overdue
        def return_exhibit(self):
            if self._returned:
                return False
            self._returned = True
            return True
        def is_overdue(self):
            return self._overdue
    return ExhibitionLoan()


@pytest.fixture
def contract():
    from museum_documents.Contract import Contract
    return Contract(["Hermitage", "Louvre"], "Loan agreement", 100000.0)


@pytest.fixture
def signed_contract(contract):
    contract.sign()
    return contract


@pytest.fixture
def insurance_policy(exhibit):
    from datetime import date, timedelta

    from museum_documents.InsurancePolicy import InsurancePolicy
    return InsurancePolicy(
        exhibit, "Ingosstrakh", 5000.0,
        valid_until=date.today() + timedelta(days=365),
        policy_number="POL-001",
    )


@pytest.fixture
def acquisition():
    from museum_documents.Acquisition import Acquisition
    from museum_exhibits.Painting import Painting
    p = Painting("Starry Night", "Van Gogh", "oil", 1.0, 1.0)
    return Acquisition(Acquisition.SOURCE_PURCHASE, p, price=1000000.0)


@pytest.fixture
def inventory(employee):
    from museum_documents.Inventory import Inventory
    return Inventory(employee)


@pytest.fixture
def report_module_stub(monkeypatch):
    """Inject a fake museum_documents.Report into sys.modules."""
    import sys
    import types

    module = types.ModuleType("museum_documents.Report")

    class FakeReport:
        TYPE_ANNUAL = "annual"
        TYPE_FINANCIAL = "financial"
        TYPE_ATTENDANCE = "attendance"
        TYPE_RESTORATION = "restoration"
        TYPE_INVENTORY = "inventory"

        _counter = 0

        def __init__(self, period, type_):
            FakeReport._counter += 1
            self.id = f"REP-{FakeReport._counter:04d}"
            self.period = period
            self.type = type_
            self.data = {}

        def generate(self, data):
            self.data.update(data)
            return True

    module.Report = FakeReport
    parent = types.ModuleType("museum_documents")
    monkeypatch.setitem(sys.modules, "museum_documents", parent)
    monkeypatch.setitem(sys.modules, "museum_documents.Report", module)
    return FakeReport


@pytest.fixture
def loan(exhibit):
    """A pending loan for a good-condition exhibit."""
    from museum_documents.Loan import Loan
    return Loan(
        exhibit, "Louvre",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=30),
    )


@pytest.fixture
def approved_loan(loan):
    loan.approve_loan()
    return loan


@pytest.fixture
def overdue_loan(exhibit):
    """An approved loan whose end date is in the past."""
    from museum_documents.Loan import Loan
    l = Loan(
        exhibit, "Louvre",
        start_date=date(2020, 1, 1),
        end_date=date(2020, 6, 1),
    )
    l.approve_loan()
    return l


@pytest.fixture
def restoration(exhibit_damaged, restorer):
    from museum_documents.Restoration import Restoration
    return Restoration(exhibit_damaged, restorer)


@pytest.fixture
def invoice():
    from museum_documents.Invoice import Invoice
    return Invoice(amount=1000.0, payer="Hermitage")


@pytest.fixture
def paid_invoice(invoice):
    from museum_sales.Payment import Payment
    invoice.pay(Payment(1000.0, Payment.METHOD_CARD))
    return invoice


@pytest.fixture
def report():
    from museum_documents.Report import Report
    return Report(period="2025", type_="annual")


@pytest.fixture
def move_act(painting):
    """StorageMoveAct with a painting in 'Storage A' and 'Storage B' as target."""
    from museum_core.Storage import Storage
    from museum_documents.StorageMoveAct import StorageMoveAct
    from museum_people.Employee import Employee
    storage_a = Storage("Storage A", capacity=10)
    storage_b = Storage("Storage B", capacity=10)
    storage_a.place_exhibit(painting)
    employee = Employee("Ivanov", 50000.0, date(2020, 1, 1))
    return StorageMoveAct(painting, storage_a, storage_b, employee)