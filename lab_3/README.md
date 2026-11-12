# Transport & Logistics — OOP Project

A domain model and demonstration program for a **freight logistics
company**: vehicles, cargo, drivers, warehouses, routes, shipments,
invoices, and incidents.

The project is written in pure Python 3, uses no external
dependencies at runtime, and is fully covered by pytest tests.

---

## Inheritance

| Base | Subclasses |
|------|------------|
| `Vehicle` | `Truck`, `Van`, `Tanker` |
| `Cargo` | `FragileCargo`, `PerishableCargo`, `HazardousCargo` |
| `Employee` | `Driver`, `Dispatcher`, `WarehouseWorker`, `Mechanic` |
| `LogisticsException` | all domain exceptions below |

---

## Classes by package

### 1 `logistics_core` — company and places

| Class              | Fields                                                                  | Key methods                                                              |
|--------------------|-------------------------------------------------------------------------|--------------------------------------------------------------------------|
| `TransportCompany` | name, license_number, headquarters, vehicles, warehouses, employees, clients, budget | add/remove_vehicle, add_warehouse, add_employee, register_client, find_vehicle, spend_budget, increase_budget |
| `Address`          | street, city, region, country, postal_code, coordinates                 | is_same_city, format, is_complete, in_country, distance_to               |
| `GPSPosition`      | latitude, longitude, timestamp, accuracy                                | distance_to, is_valid, update, move_towards                              |
| `Terminal`         | name, address, docks, is_open, working_hours                            | open_terminal, close_terminal, add_dock, assign_dock, count_free_docks   |
| `Dock`             | number, length_m, current_vehicle, is_occupied, terminal                | occupy, release, can_accept, is_free                                     |
| `Checkpoint`       | name, address, is_border, required_documents, is_open                   | inspect, allow_passage, deny_passage, require_document                   |

### 2 `logistics_fleet` — vehicles and upkeep

| Class                | Fields                                                         | Key methods                                          |
|----------------------|----------------------------------------------------------------|------------------------------------------------------|
| `Vehicle`            | plate, vin, capacity_kg, volume_m3, status, driver, gps, fuel_level, odometer | assign_driver, start_trip, finish_trip, refuel, can_load, locate |
| `Truck`              | axles, has_sleeper, attached_trailer                           | hitch_trailer, unhitch, axle_load, can_take_trailer  |
| `Van`                | door_count, has_liftgate                                       | open_doors, close_doors, use_liftgate                |
| `Tanker`             | tank_volume, chemical_class, is_cleaned                        | load_liquid, unload_liquid, clean_tank, is_compatible |
| `Trailer`            | plate, capacity_kg, trailer_type, attached_to                  | attach, detach, is_attached, remaining_capacity      |
| `MaintenanceRecord`  | vehicle, mechanic, date, description, cost, status             | start_work, complete, add_part, estimate_downtime    |
| `VehicleInsurance`   | vehicle, company, amount, valid_until, policy_number           | is_active, renew, claim, cancel                      |
| `FuelLog`            | vehicle, liters, cost, station, date, odometer                 | record, consumption_per_100km, is_anomaly            |

### 3 `logistics_cargo` — what is moved

| Class              | Fields                                                        | Key methods                                        |
|--------------------|---------------------------------------------------------------|----------------------------------------------------|
| `Cargo`            | tracking_id, weight, volume, status, declared_value, origin, destination | pack, unpack, mark_damaged, can_fit, update_status |
| `FragileCargo`     | packing_class, this_side_up, min_insurance                    | require_label, check_orientation, estimate_packing |
| `PerishableCargo`  | temp_min, temp_max, expires_at                                | is_expired, check_temperature, extend_shelf_life   |
| `HazardousCargo`   | un_number, hazard_class, requires_escort                      | needs_permit, compatible_with, require_escort      |
| `Package`          | tracking_number, contents, size, is_sealed                    | seal, unseal, scan, is_oversize                    |
| `Pallet`           | code, packages, max_weight, is_wrapped                        | add_package, wrap, unwrap, total_weight            |
| `Container`        | iso_code, pallets, seal_number, is_sealed, max_payload        | load_pallet, unload_pallet, seal, inspect          |

### 4 `logistics_people` — staff and counterparties

| Class              | Fields                                                      | Key methods                                              |
|--------------------|-------------------------------------------------------------|----------------------------------------------------------|
| `Employee`         | name, salary, hire_date, on_leave, vacations                | work, take_leave, raise_salary, calculate_monthly_salary |
| `Driver`           | license, assigned_vehicle, hours_driven, is_available, rest_until | start_shift, end_shift, assign_vehicle, log_hours, can_take_order |
| `DrivingLicense`   | number, categories, issued_on, expires_at, is_suspended     | covers_category, is_expired, renew, suspend              |
| `Dispatcher`       | region, assigned_orders, radio_id                           | assign_order, reassign, find_free_driver, close_shift    |
| `WarehouseWorker`  | warehouse, forklift_certified, current_zone                 | pick_item, put_away, operate_forklift, count_items       |
| `Mechanic`         | specialization, certificate, jobs                           | inspect_vehicle, repair, write_report, estimate_cost     |
| `Client`           | name, tax_id, credit_limit, balance, contracts              | place_order, pay_invoice, check_credit, add_contract     |
| `Consignee`        | name, address, phone, preferred_window                      | confirm_delivery, refuse, reschedule                     |

### 5 `logistics_orders` — shipments and money

| Class            | Fields                                                                  | Key methods                                      |
|------------------|-------------------------------------------------------------------------|--------------------------------------------------|
| `ShipmentOrder`  | number, client, cargo, route, status, vehicle, driver, price, created_at | confirm, assign_vehicle, assign_driver, dispatch, deliver, cancel |
| `Delivery`       | order, completed_at, signature, is_partial, notes                       | confirm, mark_partial, refuse, attach_note       |
| `Pickup`         | order, warehouse, window_start, window_end, status                      | schedule, complete, reschedule, fail             |
| `Payment`        | amount, method, status                                                  | process, refund, verify                          |
| `Invoice`        | number, amount, payer, status, issued_date, paid_date, payment          | issue, pay, cancel, change_amount                |
| `Tariff`         | name, per_kg, per_km, min_charge, is_active                             | calculate_price, is_applicable, apply_surcharge, deactivate |

`Invoice` is a bill the **client** pays the company. `Payment.process`
runs once; a second call on an already-processed payment fails.
`Client.pay_invoice` spends client credit / company budget in one place.

### 6 `logistics_routes` — movement and tracking

| Class             | Fields                                              | Key methods                                           |
|-------------------|-----------------------------------------------------|-------------------------------------------------------|
| `Route`           | origin, destination, waypoints, distance_km, estimated_hours | add_waypoint, remove_waypoint, duration, crosses_border, total_distance |
| `Waypoint`        | address, sequence, window_start, window_end, stop_type, is_visited | arrive, depart, is_missed, reschedule        |
| `Trip`            | vehicle, driver, route, started_at, finished_at, status | start, finish, pause, resume, add_delay           |
| `TrackingEvent`   | trip, position, timestamp, event_type               | record, is_delay, describe                            |
| `TrackingSystem`  | trips, last_positions                               | register_trip, update_position, find_vehicle, eta     |

### 7 `logistics_warehouse` — storage

| Class             | Fields                                                       | Key methods                                      |
|-------------------|--------------------------------------------------------------|--------------------------------------------------|
| `Warehouse`       | name, address, capacity_m3, zones, used_volume               | receive, ship, find_cargo, remaining_capacity, run_inventory |
| `StorageZone`     | name, warehouse, zone_type, temperature, racks, is_locked    | lock, unlock, add_rack, check_temperature        |
| `Rack`            | code, zone, slots, max_weight, occupied                      | place, remove, remaining_weight, is_full         |
| `InventoryCount`  | warehouse, responsible, scanned, mismatches, is_reconciled, date | scan, diff, reconcile, is_clean, generate_report |
| `StockMove`       | cargo, from_zone, to_zone, worker, is_confirmed              | confirm, cancel, register                        |
| `LoadingTask`     | dock, order, worker, status, started_at                      | start, finish, assign_worker, is_overdue         |

`Warehouse.run_inventory` reuses `InventoryCount.diff` so storage and
inventory share one missing/extra comparison.

### 8 `logistics_documents`

| Class            | Fields                                                     | Key methods                                   |
|------------------|------------------------------------------------------------|-----------------------------------------------|
| `Contract`       | parties, terms, amount, is_signed, signed_date, valid_until | add_party, sign, terminate, is_active, change_amount |
| `Waybill`        | number, order, shipper, consignee, cargo_desc, is_signed   | issue, sign_by_driver, sign_by_consignee, cancel |
| `CargoManifest`  | shipment, items, issuer, is_verified, issued_date          | add_item, remove_item, verify, total_weight   |
| `Report`         | id, period, type, data, author, created_date               | set_author, generate, add_section, export, to_string |
| `Incident`       | id, type, place, severity, date, vehicle, driver           | add_evidence, close, is_open, link_order      |
| `Claim`          | order, reason, amount, status, evidence                    | file, approve, reject, add_evidence           |

---

## Associations (selected)

An association is any case where class A references class B as a
field or accepts it as a method parameter. Below is a representative
list (out of ~70 total).

### Containment (A holds a reference to B)

| From               | To                 | Description                                      |
|--------------------|--------------------|--------------------------------------------------|
| `TransportCompany` | `Vehicle`          | company owns the fleet                           |
| `TransportCompany` | `Warehouse`        | company operates warehouses                      |
| `TransportCompany` | `Employee`         | company employs staff                            |
| `TransportCompany` | `Client`           | company serves clients                           |
| `TransportCompany` | `Address`          | headquarters address                             |
| `Address`          | `GPSPosition`      | address has coordinates                          |
| `Terminal`         | `Address`          | terminal has an address                          |
| `Terminal`         | `Dock`             | terminal contains docks                          |
| `Dock`             | `Vehicle`          | dock may hold one vehicle                        |
| `Checkpoint`       | `Address`          | checkpoint has an address                        |
| `Vehicle`          | `Driver`           | vehicle has an assigned driver                   |
| `Vehicle`          | `GPSPosition`      | vehicle has a current position                   |
| `Truck`            | `Trailer`          | truck may hitch a trailer                        |
| `Trailer`          | `Vehicle`          | trailer knows what it is attached to             |
| `MaintenanceRecord`| `Vehicle`          | record is about a vehicle                        |
| `MaintenanceRecord`| `Mechanic`         | mechanic performs the work                       |
| `VehicleInsurance` | `Vehicle`          | policy covers a vehicle                          |
| `FuelLog`          | `Vehicle`          | log belongs to a vehicle                         |
| `Cargo`            | `Address`          | origin and destination                           |
| `Package`          | `Cargo`            | package wraps cargo contents                     |
| `Pallet`           | `Package`          | pallet holds packages                            |
| `Container`        | `Pallet`           | container holds pallets                          |
| `Driver`           | `DrivingLicense`   | driver holds a license                           |
| `Driver`           | `Vehicle`          | driver may be assigned a vehicle                 |
| `Dispatcher`       | `ShipmentOrder`    | dispatcher tracks assigned orders                |
| `WarehouseWorker`  | `Warehouse`        | worker belongs to a warehouse                    |
| `WarehouseWorker`  | `StorageZone`      | worker has a current zone                        |
| `Mechanic`         | `MaintenanceRecord`| mechanic keeps a job list                        |
| `Client`           | `Contract`         | client has contracts                             |
| `Consignee`        | `Address`          | consignee has a delivery address                 |
| `ShipmentOrder`    | `Client`           | order belongs to a client                        |
| `ShipmentOrder`    | `Cargo`            | order moves cargo                                |
| `ShipmentOrder`    | `Route`            | order follows a route                            |
| `ShipmentOrder`    | `Vehicle`          | order is assigned a vehicle                      |
| `ShipmentOrder`    | `Driver`           | order is assigned a driver                       |
| `Delivery`         | `ShipmentOrder`    | delivery closes an order                         |
| `Pickup`           | `ShipmentOrder`    | pickup starts an order                           |
| `Pickup`           | `Warehouse`        | pickup happens at a warehouse                    |
| `Invoice`          | `Payment`          | invoice is paid via a payment                    |
| `Route`            | `Address`          | origin and destination                           |
| `Route`            | `Waypoint`         | route contains stops                             |
| `Waypoint`         | `Address`          | stop has an address                              |
| `Trip`             | `Vehicle`          | trip uses a vehicle                              |
| `Trip`             | `Driver`           | trip is driven by a driver                       |
| `Trip`             | `Route`            | trip follows a route                             |
| `TrackingEvent`    | `Trip`             | event belongs to a trip                          |
| `TrackingEvent`    | `GPSPosition`      | event has a position                             |
| `TrackingSystem`   | `Trip`             | system tracks trips                              |
| `Warehouse`        | `Address`          | warehouse has an address                         |
| `Warehouse`        | `StorageZone`      | warehouse contains zones                         |
| `StorageZone`      | `Rack`             | zone contains racks                              |
| `InventoryCount`   | `Warehouse`        | count is for a warehouse                         |
| `StockMove`        | `Cargo`            | move relocates cargo                             |
| `StockMove`        | `StorageZone`      | from/to zones                                    |
| `LoadingTask`      | `Dock`             | loading uses a dock                              |
| `LoadingTask`      | `ShipmentOrder`    | loading is for an order                          |
| `Waybill`          | `ShipmentOrder`    | waybill documents an order                       |
| `Waybill`          | `Consignee`        | consignee signs the waybill                      |
| `CargoManifest`    | `ShipmentOrder`    | manifest lists order cargo                       |
| `Incident`         | `Vehicle`          | incident involves a vehicle                      |
| `Incident`         | `Driver`           | incident involves a driver                       |
| `Claim`            | `ShipmentOrder`    | claim is about an order                          |

### Use as parameter (A's method takes B)

| From               | Parameter                         | Method                          |
|--------------------|-----------------------------------|---------------------------------|
| `TransportCompany` | `Vehicle`, `Warehouse`, `Employee`, `Client` | add_* / register_client |
| `Dispatcher`       | `ShipmentOrder`, `Driver`         | `assign_order`, `reassign`      |
| `Driver`           | `Vehicle`                         | `assign_vehicle`                |
| `Vehicle`          | `Cargo`                           | `can_load`                      |
| `Truck`            | `Trailer`                         | `hitch_trailer`                 |
| `Warehouse`        | `Cargo`                           | `receive`, `ship`               |
| `Client`           | `Invoice`, `Payment`              | `pay_invoice`                   |
| `Invoice`          | `Payment`                         | `pay`                           |
| `Tariff`           | `Cargo`, `Route`                  | `calculate_price`               |
| `TrackingSystem`   | `Trip`, `GPSPosition`             | `register_trip`, `update_position` |
| `Checkpoint`       | `Trip`, `HazardousCargo`          | `inspect`, `allow_passage`      |
| `Consignee`        | `Delivery`                        | `confirm_delivery`, `refuse`    |

---

## Exceptions

All exceptions inherit from `LogisticsException`. Every exception is
used at least once in domain logic — none are reserved stubs.

| Exception                            | Thrown by                                                                 |
|--------------------------------------|---------------------------------------------------------------------------|
| `LogisticsException`                 | base class for all logistics errors                                       |
| `VehicleNotAvailableException`       | `Vehicle.start_trip`, `Dispatcher.assign_order`                           |
| `VehicleOverloadException`           | `Vehicle.can_load`, `Truck.hitch_trailer`, `Container.load_pallet`        |
| `DriverNotAvailableException`        | `Driver.can_take_order`, `Dispatcher.assign_order`                        |
| `InvalidLicenseException`            | `Driver.assign_vehicle`, `DrivingLicense.covers_category`                 |
| `CargoOverweightException`           | `Pallet.add_package`, `Cargo.can_fit`                                     |
| `InvalidCargoStateException`         | `Cargo.update_status`, `ShipmentOrder.*`, `Trip.*`, `Delivery.*`, `Pickup.*`, `Invoice.*`, `Payment.*`, `Waybill.*`, `Contract.*` |
| `WarehouseCapacityExceededException` | `Warehouse.receive`                                                       |
| `RouteConflictException`             | `TrackingSystem.register_trip`, `Trip.start`                              |
| `PaymentFailedException`             | `Payment.process`, `Client.pay_invoice`, `Invoice.pay`                    |
| `InsufficientFundsException`         | `TransportCompany.spend_budget`, `Client.pay_invoice`                     |
| `OrderNotFoundException`             | `TransportCompany` lookup, `Dispatcher.reassign`                          |
| `HazardousRestrictionException`      | `HazardousCargo.compatible_with`, `Dock.can_accept`, `Checkpoint.inspect` |
| `DeliveryRefusedException`           | `Consignee.refuse`, `Delivery.refuse`                                     |

---

## Scenarios (see `main.py`)

You'll get an interactive menu with 10 scenarios. Each scenario in
`main.py` demonstrates a real-world workflow that crosses several
packages:

1. **Place a shipment** — `Client`, `Tariff`, `Cargo`, `ShipmentOrder`, `Route`.
2. **Assign driver and truck** — `Dispatcher`, `Driver`, `DrivingLicense`, `Truck`.
3. **Load at the warehouse** — `Warehouse`, `Dock`, `LoadingTask`, `Pallet`, `WarehouseWorker`.
4. **Start a trip and track GPS** — `Trip`, `TrackingSystem`, `GPSPosition`, `Route`.
5. **Deliver and sign the waybill** — `Delivery`, `Consignee`, `Waybill`.
6. **Perishable cargo in a cold zone** — `PerishableCargo`, `StorageZone`, `Warehouse`.
7. **Hazardous cargo at a checkpoint** — `HazardousCargo`, `Checkpoint`, `Tanker`.
8. **Vehicle maintenance** — `Mechanic`, `MaintenanceRecord`, `Truck`.
9. **Invoice and payment** — `Invoice`, `Payment`, `Client`, `TransportCompany`.
10. **Warehouse inventory** — `InventoryCount`, `Warehouse`, `WarehouseWorker`.

---

## Target statistics

| Metric       | Target | Required |
|--------------|--------|----------|
| Classes      | 52     | ≥ 50     |
| Fields       | ~250   | ≥ 150    |
| Behaviors    | ~210   | ≥ 100    |
| Associations | ~70    | ≥ 30     |
| Exceptions   | 13 + base | ≥ 12  |
