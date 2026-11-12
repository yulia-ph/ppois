from datetime import date, timedelta

from exceptions.HazardousRestrictionException import HazardousRestrictionException
from logistics_cargo.Cargo import Cargo
from logistics_cargo.HazardousCargo import HazardousCargo
from logistics_cargo.Package import Package
from logistics_cargo.Pallet import Pallet
from logistics_cargo.PerishableCargo import PerishableCargo
from logistics_core.Address import Address
from logistics_core.Checkpoint import Checkpoint
from logistics_core.Dock import Dock
from logistics_core.GPSPosition import GPSPosition
from logistics_core.Terminal import Terminal
from logistics_core.TransportCompany import TransportCompany
from logistics_documents.Waybill import Waybill
from logistics_fleet.MaintenanceRecord import MaintenanceRecord
from logistics_fleet.Tanker import Tanker
from logistics_fleet.Truck import Truck
from logistics_orders.Delivery import Delivery
from logistics_orders.Invoice import Invoice
from logistics_orders.Payment import Payment
from logistics_orders.ShipmentOrder import ShipmentOrder
from logistics_orders.Tariff import Tariff
from logistics_people.Client import Client
from logistics_people.Consignee import Consignee
from logistics_people.Dispatcher import Dispatcher
from logistics_people.Driver import Driver
from logistics_people.DrivingLicense import DrivingLicense
from logistics_people.Mechanic import Mechanic
from logistics_people.WarehouseWorker import WarehouseWorker
from logistics_routes.Route import Route
from logistics_routes.TrackingSystem import TrackingSystem
from logistics_routes.Trip import Trip
from logistics_warehouse.InventoryCount import InventoryCount
from logistics_warehouse.LoadingTask import LoadingTask
from logistics_warehouse.StorageZone import StorageZone
from logistics_warehouse.Warehouse import Warehouse


def setup_company() -> TransportCompany:
    hq = Address("Nezavisimosti 10", "Minsk", "Minsk", "Belarus", "220030",
                 GPSPosition(53.9, 27.56))
    company = TransportCompany("BelLogistic", "LIC-2026", hq)
    company.set_budget(1_000_000)
    return company


def _minsk():
    return Address("Lenina 1", "Minsk", "Minsk", "Belarus", "220000",
                   GPSPosition(53.90, 27.56))


def _warsaw():
    return Address("Marszalkowska 1", "Warsaw", "Mazovia", "Poland", "00-001",
                   GPSPosition(52.23, 21.01))


def _license():
    return DrivingLicense("DL-77", ["B", "C"], date(2018, 1, 1),
                          date.today() + timedelta(days=800))


def scenario_1_place_shipment(company: TransportCompany):
    print("\n[Scenario 1] Place a shipment")
    client = Client("Acme Foods", "TAX-100", 50_000)
    client.top_up(20_000)
    company.register_client(client)
    cargo = Cargo(200, 4, _minsk(), _warsaw(), 3000)
    cargo.pack()
    route = Route(_minsk(), _warsaw(), 550, 8)
    tariff = Tariff("standard", 1.5, 2.0, 400)
    price = tariff.calculate_price(cargo, route)
    order = ShipmentOrder(client, cargo, route, price)
    client.place_order(order)
    company.register_order(order)
    print(f"  ✓ Order {order.number} confirmed, price {price:.0f}")


def scenario_2_assign_driver(company: TransportCompany):
    print("\n[Scenario 2] Assign driver and truck")
    truck = Truck("AA-7777", "VIN7777", 12_000, 50, 3, has_sleeper=True)
    company.add_vehicle(truck)
    driver = Driver("Ivanov", 55_000, date(2019, 3, 1), _license())
    company.add_employee(driver)
    truck.assign_driver(driver)
    dispatcher = Dispatcher("Sokolova", 60_000, date(2017, 1, 1), "west", "R-9")
    company.add_employee(dispatcher)
    cargo = Cargo(80, 2, _minsk(), _warsaw())
    cargo.pack()
    order = ShipmentOrder(Client("Beta", "T2", 1000), cargo, Route(_minsk(), _warsaw(), 550, 8), 900)
    order.confirm()
    dispatcher.assign_order(order, driver)
    print(f"  ✓ Driver {driver.name} on truck {truck.plate} for {order.number}")


def scenario_3_load_warehouse(company: TransportCompany):
    print("\n[Scenario 3] Load at the warehouse")
    warehouse = Warehouse("Central", _minsk(), 5000)
    company.add_warehouse(warehouse)
    terminal = Terminal("Minsk Terminal", _minsk())
    dock = Dock(1, 18)
    terminal.add_dock(dock)
    terminal.open_terminal()
    worker = WarehouseWorker("Petrov", 35_000, date(2021, 1, 1), warehouse, True)
    cargo = Cargo(50, 1.5, _minsk(), _warsaw())
    cargo.pack()
    warehouse.receive(cargo)
    pallet = Pallet("PAL-1", 400)
    pallet.add_package(Package(cargo, 0.8))
    pallet.wrap()
    order = ShipmentOrder(Client("Gamma", "T3", 1), cargo, Route(_minsk(), _warsaw(), 100, 2), 200)
    order.confirm()
    task = LoadingTask(dock, order, worker)
    task.start()
    dock.occupy(Truck("LD-1", "VINLD", 8000, 30, 2))
    task.finish()
    print(f"  ✓ Loaded {pallet.code}, dock occupied: {dock.is_occupied}")


def scenario_4_trip_track(company: TransportCompany):
    print("\n[Scenario 4] Start a trip and track GPS")
    truck = Truck("TR-100", "VINTR", 10_000, 40, 3)
    driver = Driver("Kozlov", 50_000, date(2020, 1, 1), _license())
    truck.assign_driver(driver)
    route = Route(_minsk(), _warsaw(), 550, 8)
    trip = Trip(truck, driver, route)
    tracker = TrackingSystem()
    trip.start()
    tracker.register_trip(trip)
    tracker.update_position(trip, GPSPosition(53.0, 25.0))
    print(f"  ✓ Trip {truck.plate} running, ETA {tracker.eta(trip):.1f} h")
    trip.finish()


def scenario_5_deliver(company: TransportCompany):
    print("\n[Scenario 5] Deliver and sign the waybill")
    cargo = Cargo(40, 1, _minsk(), _warsaw())
    cargo.pack()
    truck = Truck("DV-1", "VINDV", 9000, 35, 2)
    driver = Driver("Orlov", 48_000, date(2020, 6, 1), _license())
    truck.assign_driver(driver)
    order = ShipmentOrder(Client("Delta", "T4", 1), cargo, Route(_minsk(), _warsaw(), 550, 8), 700)
    order.confirm()
    order.assign_vehicle(truck)
    order.assign_driver(driver)
    order.dispatch()
    consignee = Consignee("Warsaw Shop", _warsaw(), "+48 111")
    delivery = Delivery(order)
    consignee.confirm_delivery(delivery)
    waybill = Waybill(order, company.name, consignee, "food crates")
    waybill.issue()
    waybill.sign_by_driver()
    waybill.sign_by_consignee()
    print(f"  ✓ Delivered {order.number}, waybill {waybill.number} signed")


def scenario_6_perishable(company: TransportCompany):
    print("\n[Scenario 6] Perishable cargo in a cold zone")
    warehouse = Warehouse("Cold store", _minsk(), 800)
    zone = StorageZone("Chill", warehouse, StorageZone.TYPE_COLD, 3.0)
    warehouse.add_zone(zone)
    cargo = PerishableCargo(30, 2, _minsk(), _warsaw(), 0, 6, date.today() + timedelta(days=5))
    cargo.pack()
    warehouse.receive(cargo)
    ok = zone.check_temperature(3.0)
    print(f"  ✓ Perishable {cargo.tracking_id} stored, temp ok: {ok}")


def scenario_7_hazardous(company: TransportCompany):
    print("\n[Scenario 7] Hazardous cargo at a checkpoint")
    tanker = Tanker("HZ-9", "VINHZ", 8000, 18, 14.0, "3")
    company.add_vehicle(tanker)
    cargo = HazardousCargo(500, 3, _minsk(), _warsaw(), "UN1203", "1", requires_escort=True)
    checkpoint = Checkpoint("Brest border", _minsk(), is_border=True)
    try:
        checkpoint.inspect(cargo)
        print("  ✓ Passed")
    except HazardousRestrictionException as exc:
        print(f"  ✗ Stopped: {exc.message}")


def scenario_8_maintenance(company: TransportCompany):
    print("\n[Scenario 8] Vehicle maintenance")
    truck = Truck("MN-4", "VINMN", 11_000, 45, 3)
    mechanic = Mechanic("Gusev", 42_000, date(2016, 1, 1), "engine", "MECH-12")
    record = MaintenanceRecord(truck, mechanic, "oil and filters", 150)
    mechanic.repair(record)
    record.add_part("oil filter", 25)
    record.complete()
    report = mechanic.write_report(record)
    print(f"  ✓ {truck.plate} serviced, report {report.id}, cost {record.cost}")


def scenario_9_invoice(company: TransportCompany):
    print("\n[Scenario 9] Invoice and payment")
    client = Client("Epsilon", "TAX-9", 20_000)
    client.top_up(5000)
    invoice = Invoice(1200, client.name)
    invoice.issue()
    payment = Payment(1200, Payment.METHOD_TRANSFER)
    client.pay_invoice(invoice, payment, company)
    print(f"  ✓ Invoice {invoice.number} paid, company budget {company.budget:.0f}")


def scenario_10_inventory(company: TransportCompany):
    print("\n[Scenario 10] Warehouse inventory")
    warehouse = Warehouse("South", _minsk(), 2000)
    worker = WarehouseWorker("Novik", 32_000, date(2022, 2, 1), warehouse, True)
    c1 = Cargo(10, 1, _minsk(), _warsaw())
    c2 = Cargo(12, 1, _minsk(), _warsaw())
    warehouse.receive(c1)
    warehouse.receive(c2)
    count = InventoryCount(warehouse, worker)
    count.scan(c1)
    count.scan(c2)
    count.reconcile(warehouse.find_cargo())
    report = count.generate_report()
    print(f"  ✓ Inventory clean: {count.is_clean()}, report {report.id}")


SCENARIOS = {
    1: ("Place a shipment", scenario_1_place_shipment),
    2: ("Assign driver and truck", scenario_2_assign_driver),
    3: ("Load at the warehouse", scenario_3_load_warehouse),
    4: ("Start a trip and track GPS", scenario_4_trip_track),
    5: ("Deliver and sign the waybill", scenario_5_deliver),
    6: ("Perishable cargo in a cold zone", scenario_6_perishable),
    7: ("Hazardous cargo at a checkpoint", scenario_7_hazardous),
    8: ("Vehicle maintenance", scenario_8_maintenance),
    9: ("Invoice and payment", scenario_9_invoice),
    10: ("Warehouse inventory", scenario_10_inventory),
}


def show_menu():
    print("\n" + "=" * 50)
    print("  TRANSPORT & LOGISTICS — SCENARIO DEMONSTRATION")
    print("=" * 50)
    for n, (title, _) in SCENARIOS.items():
        print(f"  {n:>2}. {title}")
    print("   0. Exit")
    print("=" * 50)


def main():
    """Logistics demonstration.

    This script is a demo, not production code. Sample data (names,
    salaries, prices, dates) is intentionally hardcoded here so that the
    scenarios are readable at a glance. Domain logic does not depend on
    these literals — they are inputs for the demo, not configuration.
    """
    company = setup_company()
    print(f"✓ Company '{company.name}' initialized")
    print(f"  Budget: {company.budget} RUB")

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
            func(company)
        except Exception as exc:
            print(f"⚠ Unexpected error: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
