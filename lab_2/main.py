from datetime import date, datetime, timedelta

from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
from exceptions.InvalidTicketException import InvalidTicketException
from exceptions.LoanOverdueException import LoanOverdueException
from exceptions.PaymentFailedException import PaymentFailedException
from exceptions.RestorationException import RestorationException
from museum_core.Building import Building
from museum_core.ClimateZone import ClimateZone
from museum_core.Hall import Hall
from museum_core.Museum import Museum
from museum_core.Sensor import Sensor, SensorType
from museum_core.Storage import Storage
from museum_documents.Acquisition import Acquisition
from museum_documents.Inventory import Inventory
from museum_documents.Loan import Loan
from museum_exhibitions.Excursion import Excursion
from museum_exhibits.Collection import Collection
from museum_exhibits.Exhibit import Exhibit
from museum_exhibits.Fund import Fund
from museum_exhibits.Painting import Painting
from museum_people.Administrator import Administrator
from museum_people.Cashier import Cashier
from museum_people.Curator import Curator
from museum_people.Employee import Employee
from museum_people.Guide import Guide
from museum_people.Restorer import Restorer
from museum_people.SecurityGuard import SecurityGuard
from museum_people.Visitor import Visitor
from museum_sales.Membership import Membership
from museum_sales.Order import Order
from museum_sales.Payment import Payment
from museum_sales.ShopItem import ShopItem
from museum_sales.Ticket import Ticket
from museum_sales.TicketType import TicketType
from museum_security.AccessControl import AccessControl


def setup_museum() -> Museum:
    museum = Museum("Hermitage", "Palace Square 2", "hermitage.ru")
    museum.set_budget(10_000_000)

    museum.add_ticket_type(TicketType("Adult", 500, min_age=18))
    museum.add_ticket_type(TicketType("Child", 200, max_age=17))
    museum.add_ticket_type(TicketType("Student", 250, min_age=16, max_age=25))

    main_building = Building("Main Building", "Palace Square 2",
                             Building.TYPE_MAIN, 3)
    hall1 = Hall(1, 200.0)
    hall2 = Hall(2, 150.0)
    main_building.add_hall(hall1)
    main_building.add_hall(hall2)
    museum.add_building(main_building)

    storage = Storage("Main Storage", 100)
    storage.set_climate_zone(ClimateZone(20.0, 50.0))

    fund = Fund("Painting Fund", Fund.TYPE_PAINTING)
    collection = Collection("Western European Painting", "painting")
    fund.add_collection(collection)
    museum.add_fund(fund)

    return museum


def scenario_1_sell_and_enter(museum: Museum):
    print("\n[Scenario 1] Ticket sale and visitor entry")

    visitor = Visitor("Anna", 25)
    cashier = Cashier("Petrova", 50_000, date(2020, 1, 1), "day")
    guard = SecurityGuard("Sidorov", 40_000, date(2020, 1, 1),
                          "day", AccessControl.ZONE_PUBLIC)

    try:
        adult = museum.find_ticket_type("Adult")
    except ValueError as exc:
        print(f"  ✗ {exc}")
        return

    try:
        ticket = cashier.sell_ticket(adult, visitor, date.today())
    except InvalidTicketException as exc:
        print(f"  ✗ Ticket not sold: {exc}")
        return

    print(f"  ✓ Sold ticket {ticket.number} for {ticket.cost} RUB")

    if not guard.check_access(visitor, AccessControl.ZONE_PUBLIC):
        print("  ✗ Access denied")
        return

    try:
        visitor.enter_museum()
        ticket.mark_used()
        print(f"  ✓ {visitor.name} entered the museum")
    except (InvalidTicketException, InvalidExhibitStateException) as exc:
        print(f"  ✗ Cannot enter: {exc}")


def scenario_2_excursion(museum: Museum):
    print("\n[Scenario 2] Guided excursion")

    guide = Guide("Smirnova", 45_000, date(2019, 1, 1),
                  languages=["ru", "en"], experience_years=5)
    hall = museum.buildings[0].halls[0]

    excursion = Excursion(
        route_points=[hall],
        guide=guide,
        start_time=datetime.now(),
        duration_minutes=60,
    )

    for name, age in [("Boris", 30), ("Kate", 28), ("Dmitry", 35)]:
        excursion.add_visitor(Visitor(name, age))

    try:
        excursion.start()
    except InvalidExhibitStateException as exc:
        print(f"  ✗ Cannot start excursion: {exc}")
        return

    print(f"  ✓ Guide: {guide.name}")
    print(f"    Route points: {excursion.count_points()}")
    print(f"    Visitors: {excursion.count_visitors()}")

    try:
        guide.finish_tour(excursion)
        print(f"  ✓ Excursion finished: {excursion.is_finished}")
    except (ValueError, InvalidExhibitStateException) as exc:
        print(f"  ✗ Cannot finish: {exc}")


def scenario_3_restoration(museum: Museum):
    print("\n[Scenario 3] Exhibit restoration")

    restorer = Restorer("Ivanov", 60_000, date(2018, 1, 1),
                        specialization="painting", certificate="cert-123")
    painting = Painting("Sunflowers", "Van Gogh", "oil", 0.9, 0.7,
                        condition=Exhibit.CONDITION_DAMAGED)

    print(f"  Condition before: {painting.condition}")

    try:
        restoration = restorer.restore_exhibit(painting)
    except RestorationException as exc:
        print(f"  ✗ Cannot start restoration: {exc}")
        return

    try:
        restoration.complete_restoration()
        report = restoration.write_report()
    except InvalidExhibitStateException as exc:
        print(f"  ✗ Restoration failed: {exc}")
        return

    print(f"  Condition after: {painting.condition}")
    print(f"  Cost: {restoration.cost} RUB")
    print(f"  Duration: {restoration.calculate_duration()} days")
    if report is not None:
        print(f"  Report: {report.id}")


def scenario_4_loan(museum: Museum):
    print("\n[Scenario 4] Loan of an exhibit")

    admin = Administrator("Petrov", 80_000, date(2015, 1, 1), "administration")

    painting = Painting("The Night Watch", "Rembrandt", "oil", 3.6, 4.4)

    loan = Loan(
        exhibit=painting,
        borrower="Prado Museum",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=30),
    )

    try:
        admin.approve_loan(loan)
    except (LoanOverdueException, InvalidExhibitStateException) as exc:
        print(f"  ✗ Loan not approved: {exc}")
        return

    print(f"  ✓ '{painting.title}' loaned to {loan.borrower}")
    print(f"    Status: {loan.status}")

    try:
        loan.return_exhibit()
        loan.register_return("excellent")
    except (ValueError, InvalidExhibitStateException) as exc:
        print(f"  ✗ Return failed: {exc}")
        return

    print(f"  ✓ Return registered: {loan.status}, "
          f"condition: {loan.return_condition}")


def scenario_5_inventory(museum: Museum):
    print("\n[Scenario 5] Storage inventory")

    storage = Storage("Temporary Storage", 50)
    p1 = Painting("A", "Author X", "oil", 1.0, 1.0)
    p2 = Painting("B", "Author Y", "oil", 1.0, 1.0)
    p3 = Painting("C", "Author Z", "oil", 1.0, 1.0)

    storage.place_exhibit(p1)
    storage.place_exhibit(p2)
    storage.place_exhibit(p3)

    employee = Employee("Sidorov", 50_000, date(2020, 1, 1))
    inventory = Inventory(employee)

    inventory.scan_exhibit(p1)
    inventory.scan_exhibit(p2)

    inventory.reconcile(catalog_exhibits=[p1, p2, p3])

    print(f"  Scanned: {inventory.count_scanned()}")
    print(f"  Mismatches: {len(inventory.mismatches)}")
    print(f"  Clean: {inventory.is_clean()}")


def scenario_6_acquisition(museum: Museum):
    print("\n[Scenario 6] New exhibit acquisition")

    fund = Fund("Painting Fund", Fund.TYPE_PAINTING)
    collection = Collection("Italian Renaissance", "painting")
    fund.add_collection(collection)

    painting = Painting("Mona Lisa", "Leonardo", "oil", 0.77, 0.53)

    acq = Acquisition(
        source=Acquisition.SOURCE_PURCHASE,
        exhibit=painting,
        price=1_000_000,
    )

    try:
        acq.approve_acquisition()
        acq.register_exhibit()
        fund.accept_item(painting)
    except (InvalidExhibitStateException, ValueError) as exc:
        print(f"  ✗ Acquisition failed: {exc}")
        return

    print(f"  Acquired: {painting.title}")
    print(f"  Registration date: {painting.acquired_date}")
    print(f"  In collection: {collection.count_exhibits()} exhibit(s)")
    print(f"  Inventory number: {painting.inventory_number}")


def scenario_7_incident(museum: Museum):
    print("\n[Scenario 7] Incident in the hall")

    guard = SecurityGuard("Sidorov", 40_000, date(2020, 1, 1),
                          "night", "Hall 1")

    incident = guard.report_incident(
        type_="vandalism",
        place="Hall 1",
        severity="high",
    )

    try:
        incident.add_evidence("Showcase #3 broken, glass on the floor")
        incident.add_evidence("Camera recorded a visitor at 22:15")
    except (ValueError, InvalidExhibitStateException) as exc:
        print(f"  ✗ Cannot add evidence: {exc}")
        return

    if incident.investigate():
        try:
            incident.close_incident()
        except InvalidExhibitStateException as exc:
            print(f"  ✗ Cannot close: {exc}")
            return

    print(f"  Incident {incident.id}: {incident.type}")
    print(f"  Assigned guard: {incident.guard.name if incident.guard else '—'}")
    print(f"  Closed: {incident.is_closed}")
    print(f"  Open incidents for guard: {len(guard.get_open_incidents())}")


def scenario_8_shop(museum: Museum):
    print("\n[Scenario 8] Purchase in the museum shop")

    visitor = Visitor("Anna", 25)
    membership = Membership(visitor, "silver",
                            date.today() + timedelta(days=365))
    visitor.get_membership(membership)

    magnet = ShopItem("Hermitage Magnet", 200, 50)
    book = ShopItem("Exhibition Catalog", 500, 10)

    order = Order(visitor)
    order.add_item(magnet, 1)
    order.add_item(book, 1)

    total = order.calculate_total()
    print(f"  Items: {len(order.items)}")
    print("  Silver membership discount: 20%")
    print(f"  Total: {total} RUB")

    payment = Payment(total, Payment.METHOD_CARD)
    try:
        order.checkout(payment)
    except (ValueError, InvalidExhibitStateException, PaymentFailedException) as exc:
        print(f"  ✗ Checkout failed: {exc}")
        return

    print(f"  ✓ Order paid, status: {order.status}")
    print(f"  Magnet stock left: {magnet.stock}")


def scenario_9_climate(museum: Museum):
    print("\n[Scenario 9] Climate monitoring")

    zone = ClimateZone(norm_temperature=20.0, norm_humidity=50.0)
    sensor_temp = Sensor("S1", SensorType.TEMPERATURE, zone)
    sensor_humid = Sensor("S2", SensorType.HUMIDITY, zone)
    zone.add_sensor(sensor_temp)
    zone.add_sensor(sensor_humid)

    print(f"  Norm: T={zone.norm_temperature}°C, H={zone.norm_humidity}%")
    print(f"  Current: T={zone.temperature}°C, H={zone.humidity}%")
    print(f"  Within norm: {zone.is_within_norm()}")

    zone.adjust(30.0, 50.0)
    print(f"\n  After adjust: T={zone.temperature}°C")
    print(f"  Within norm: {zone.is_within_norm()}")

    if sensor_temp.send_alert():
        print(f"  ⚠ Alert! Sensor {sensor_temp.id} reports deviation")


def scenario_10_exhibition(museum: Museum):
    print("\n[Scenario 10] Curator creates an exhibition")

    curator = Curator("Sokolova", 70_000, date(2015, 1, 1), "painting")

    collection = Collection("Impressionists", "painting")
    p1 = Painting("Water Lilies", "Monet", "oil", 1.0, 0.8)
    p2 = Painting("The Dance", "Matisse", "oil", 2.0, 1.5)
    p3 = Painting("Starry Night", "Van Gogh", "oil", 0.9, 0.7)
    collection.add_exhibit(p1)
    collection.add_exhibit(p2)
    collection.add_exhibit(p3)

    try:
        exhibition = curator.create_exhibition(
            title="Impressionists",
            start=date.today(),
            end=date.today() + timedelta(days=30),
        )
    except ValueError as exc:
        print(f"  ✗ Cannot create exhibition: {exc}")
        return

    selected = curator.select_exhibits(collection, count=2)
    for p in selected:
        try:
            exhibition.add_exhibit(p)
        except (ValueError, InvalidExhibitStateException) as exc:
            print(f"  ⚠ Skipped '{p.title}': {exc}")

    exhibition.open()

    print(f"  Exhibition: '{exhibition.title}'")
    print(f"  Curator: {curator.name}")
    print(f"  Exhibits: {exhibition.count_exhibits()}")
    print(f"  Open: {exhibition.is_open}")
    print(f"  Duration: {exhibition.duration_days()} days")

    visitor = Visitor("Igor", 30)
    try:
        adult = museum.find_ticket_type("Adult")
    except ValueError as exc:
        print(f"  ✗ {exc}")
        return

    ticket = Ticket(adult, date.today(), exhibition=exhibition)
    visitor.receive_ticket(ticket)
    exhibition.add_ticket(ticket)

    print(f"  Tickets sold: {exhibition.calculate_tickets_sold()}")
    print(f"  Revenue: {exhibition.calculate_revenue()} RUB")


SCENARIOS = {
    1: ("Ticket sale and visitor entry", scenario_1_sell_and_enter),
    2: ("Guided excursion", scenario_2_excursion),
    3: ("Exhibit restoration", scenario_3_restoration),
    4: ("Exhibit loan", scenario_4_loan),
    5: ("Storage inventory", scenario_5_inventory),
    6: ("Exhibit acquisition", scenario_6_acquisition),
    7: ("Incident in the hall", scenario_7_incident),
    8: ("Museum shop purchase", scenario_8_shop),
    9: ("Climate monitoring", scenario_9_climate),
    10: ("Create an exhibition", scenario_10_exhibition),
}


def show_menu():
    print("\n" + "=" * 50)
    print("  MUSEUM — SCENARIO DEMONSTRATION")
    print("=" * 50)
    for n, (title, _) in SCENARIOS.items():
        print(f"  {n:>2}. {title}")
    print("   0. Exit")
    print("=" * 50)


def main():
    """Museum demonstration.

    This script is a demo, not production code. Sample data (names,
    salaries, prices, dates) is intentionally hardcoded here so that the
    scenarios are readable at a glance. Domain logic does not depend on
    these literals — they are inputs for the demo, not configuration.

    """
    museum = setup_museum()
    print(f"✓ Museum '{museum.name}' initialized")
    print(f"  Budget: {museum.budget} RUB")
    print(f"  Ticket types: {len(museum.ticket_types)}")

    while True:
        show_menu()
        choice = input("Your choice: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        try:
            n = int(choice)
        except ValueError:
            print("⚠ Please enter a number")
            continue

        if n not in SCENARIOS:
            print("⚠ No such scenario")
            continue

        _, func = SCENARIOS[n]
        try:
            func(museum)
        except Exception as exc:
            print(f"⚠ Unexpected error: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()