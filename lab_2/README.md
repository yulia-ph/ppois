# Museum — OOP Project

A domain model and demonstration program for a **museum**:
exhibits, exhibitions, tickets, staff, storage, climate control,
loans, restoration, inventory, and security.

The project is written in pure Python 3, uses no external
dependencies at runtime, and is fully covered by pytest tests.

---

##  Classes by package

### 1 `museum_core` — physical world

| Class         | Fields                                                                                 | Key methods                                                        |
|---------------|----------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| `Museum`      | name, address, website, buildings, employees, exhibitions, funds, ticket_types, budget | find_ticket_type, add/remove_*, spend_budget, count_visitors_today |
| `Building`    | name, address, type, floors, halls, rooms, is_open                                     | add_hall, add_room, open_for_visitors, evacuate, count_free_space  |
| `Hall`        | number, area, showcases, current_exhibition                                            | add_showcase, set_exhibition, calculate_capacity, count_exhibits   |
| `Room`        | number, purpose, climate_zone                                                          | assign_purpose, set_climate_zone, check_climate                    |
| `Storage`     | name, capacity, exhibits, climate_zone                                                 | place_exhibit, remove_exhibit, find_exhibit, run_inventory         |
| `Showcase`    | inventory_number, type, exhibit, is_locked                                             | open_showcase, close_showcase, place_exhibit, needs_restoration    |
| `ClimateZone` | temperature, humidity, norm_temperature, norm_humidity, tolerances, sensors            | monitor, adjust, is_within_norm, set_tolerances                    |
| `Sensor`      | id, type, zone, value, is_calibrated                                                   | read_value, send_alert, calibrate, reset                           |

### 2 `museum_exhibits` — exhibit accounting

| Class         | Fields                                                                            | Key methods                                                                |
|---------------|-----------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| `Exhibit`     | inventory_number, title, author, condition, collection, insurance_value, location | move_to, attach_to_collection, update_condition, evaluate_insurance        |
| `Painting`    | technique, width, height, frame, has_varnish                                      | area, set_frame, apply_varnish, estimate_restoration_cost                  |
| `Sculpture`   | material, height, weight, needs_reinforcement, base_condition                     | reinforce_base, mark_for_reinforcement, calculate_weight_load              |
| `Document`    | doc_type, pages, language, is_digitized, acidity_level, digital_copy              | digitize, check_acidity, is_fragile                                        |
| `Collection`  | name, theme, curator, exhibits                                                    | add_exhibit, find_exhibit, calculate_total_value, available_for_exhibition |
| `Fund`        | name, type, collections, written_off                                              | add_collection, accept_item, write_off_item, generate_report               |
| `Catalog`     | items, index                                                                      | add, remove, find_by_number, search, filter_by_*                           |
| `DigitalCopy` | source, format, size, resolution, path, is_published                              | create, store, publish_to_website, convert                                 |

### 3 `museum_people` — visitors and staff

| Class           | Fields                                                        | Key methods                                                         |
|-----------------|---------------------------------------------------------------|---------------------------------------------------------------------|
| `Employee`      | name, salary, hire_date, on_vacation, vacations               | work, take_vacation, raise_salary, calculate_monthly_salary         |
| `Visitor`       | name, age, ticket, membership, card, is_inside, visit_history | buy_ticket, enter_museum, leave_museum, is_regular                  |
| `Curator`       | specialization, collections, exhibitions                      | curate_collection, create_exhibition, select_exhibits, approve_loan |
| `Restorer`      | specialization, certificate, tasks                            | restore_exhibit, make_restoration_report, estimate_cost             |
| `Guide`         | languages, experience_years, tours                            | speak_language, conduct_tour, finish_tour, answer_question          |
| `Cashier`       | shift, cash_in_register, sold_tickets                         | sell_ticket, accept_payment, close_shift, refund_ticket             |
| `Administrator` | department, invoices, hired_employees                         | approve_loan, pay_invoice, hire_employee, fire_employee             |
| `SecurityGuard` | shift, zone, journal, incidents                               | patrol, check_access, report_incident, close_incident               |

### 4 `museum_sales` — ticketing and shop

| Class         | Fields                                                          | Key methods                                                     |
|---------------|-----------------------------------------------------------------|-----------------------------------------------------------------|
| `Ticket`      | number, type, date, exhibition, base_cost, discount, is_used    | validate, mark_used, refund, apply_discount, covers_exhibition  |
| `TicketType`  | name, cost, min_age, max_age                                    | is_eligible, calculate_price                                    |
| `Membership`  | visitor, level, valid_until                                     | is_active, check_discount, renew, upgrade_level                 |
| `MuseumCard`  | visitor, balance, is_blocked                                    | top_up, pay, block, unblock                                     |
| `Payment`     | amount, method, status                                          | process, refund, verify                                         |
| `ShopItem`    | name, price, stock                                              | is_available, sell, replenish, change_price                     |
| `Order`       | buyer, items, status, payment                                   | add_item, remove_item, calculate_total, checkout, cancel        |
| `Booking`     | visitor, date, tickets, payments, status                        | add_ticket, confirm, pay, cancel                                |

### 5 `museum_security`

| Class           | Fields                                           | Key methods                                              |
|-----------------|--------------------------------------------------|----------------------------------------------------------|
| `AccessControl` | person, zone, time, is_granted, reason           | check_access, require_access, log_entry                  |
| `Incident`      | id, type, place, severity, date, guard, evidence | assign_guard, add_evidence, link_exhibit, close_incident |

### 6 `museum_events`

| Class        | Fields                                                      | Key methods                                                        |
|--------------|-------------------------------------------------------------|--------------------------------------------------------------------|
| `Event`      | title, type, date, venue, capacity, registered              | register, unregister, cancel, free_seats, is_same_venue_and_date   |
| `Schedule`   | events                                                      | add_event, get_events_for_day, get_events_in_range, find_conflicts |
| `AudioGuide` | language, duration, target, is_playing, available_languages | play, pause, stop, change_language, set_target                     |

### 7 `museum_exhibitions`

| Class                 | Fields                                                      | Key methods                                               |
|-----------------------|-------------------------------------------------------------|-----------------------------------------------------------|
| `Exhibition`          | id, title, start_date, end_date, curator, exhibits, tickets | add_exhibit, open, close, extend_dates, calculate_revenue |
| `TemporaryExhibition` | theme, loans                                                | add_loan, return_loans, check_loans_overdue               |
| `PermanentExhibition` | description, last_update, rotation_period_days              | update_description, set_rotation_period, rotate_exhibits  |
| `Excursion`           | id, route_points, guide, visitors, is_started, is_finished  | add_route_point, add_visitor, start, finish, change_guide |

### 8 `museum_documents`

| Class             | Fields                                                          | Key methods                                                     |
|-------------------|-----------------------------------------------------------------|-----------------------------------------------------------------|
| `Loan`            | exhibit, borrower, start_date, end_date, status, return_*       | approve_loan, return_exhibit, extend_loan, mark_overdue         |
| `Restoration`     | exhibit, restorer, start_date, end_date, status, cost, report   | start_restoration, complete_restoration, write_report           |
| `Inventory`       | date, responsible, scanned, is_reconciled, mismatches           | scan_exhibit, diff, reconcile, is_clean, generate_report        |
| `Acquisition`     | source, date, exhibit, price, is_approved, invoice              | approve_acquisition, register_exhibit, is_free                  |
| `InsurancePolicy` | exhibit, company, amount, valid_until, policy_number            | insure_exhibit, is_active, renew, claim_insurance, cancel       |
| `StorageMoveAct`  | exhibit, from_storage, to_storage, responsible, is_confirmed    | create, confirm, register_movement, cancel                      |
| `Invoice`         | number, amount, payer, status, issued_date, paid_date, payment  | issue, pay, cancel, change_amount (museum is the payer)         |
| `Contract`        | parties, terms, amount, is_signed, signed_date, permit_number   | add_party, sign, terminate, issue_permit, change_amount         |
| `Report`          | id, period, type, data, created_date, author                    | set_author, generate, add_section, export, to_string            |

---

##  Associations (selected)

An association is any case where class A references class B as a
field or accepts it as a method parameter. Below is a representative
list (out of ~80 total).

### Containment (A holds a reference to B)

| From                  | To                    | Description                                   |
|-----------------------|-----------------------|-----------------------------------------------|
| `Museum`              | `Building`            | museum owns its buildings                     |
| `Museum`              | `Employee`            | museum employs staff                          |
| `Museum`              | `Exhibition`          | museum hosts exhibitions                      |
| `Museum`              | `Fund`                | museum keeps funds                            |
| `Museum`              | `TicketType`          | museum defines ticket tariffs                 |
| `Building`            | `Hall`                | building contains halls                       |
| `Building`            | `Room`                | building contains service rooms               |
| `Hall`                | `Showcase`            | hall contains showcases                       |
| `Hall`                | `Exhibition`          | hall currently hosts one exhibition           |
| `Room`                | `ClimateZone`         | room has its own climate zone                 |
| `Storage`             | `Exhibit`             | storage holds exhibits                        |
| `Storage`             | `ClimateZone`         | storage has a climate zone                    |
| `Showcase`            | `Exhibit`             | showcase holds exactly one exhibit            |
| `ClimateZone`         | `Sensor`              | climate zone has sensors                      |
| `Sensor`              | `ClimateZone`         | sensor is attached to a zone (back-reference) |
| `Collection`          | `Exhibit`             | collection contains exhibits                  |
| `Collection`          | `Curator`             | collection has a curator                      |
| `Fund`                | `Collection`          | fund groups collections                       |
| `Catalog`             | `Exhibit`             | catalog indexes exhibits                      |
| `DigitalCopy`         | `Exhibit`             | digital copy references its source            |
| `Exhibit`             | `Collection`          | exhibit knows its collection (back-reference) |
| `Exhibit`             | `InsurancePolicy`     | exhibit has a policy                          |
| `Visitor`             | `Ticket`              | visitor holds a ticket                        |
| `Visitor`             | `Membership`          | visitor may have a membership                 |
| `Visitor`             | `MuseumCard`          | visitor may have a card                       |
| `Curator`             | `Collection`          | curator curates collections                   |
| `Curator`             | `Exhibition`          | curator creates exhibitions                   |
| `Restorer`            | `Restoration`         | restorer performs restorations                |
| `Cashier`             | `Ticket`              | cashier sells tickets                         |
| `Administrator`       | `Invoice`             | admin pays supplier invoices from museum budget |
| `Storage`             | `Inventory`           | `run_inventory` reuses `Inventory.diff`       |
| `SecurityGuard`       | `AccessControl`       | guard logs access attempts                    |
| `SecurityGuard`       | `Incident`            | guard reports incidents                       |
| `Order`               | `ShopItem`            | order contains items (with quantities)        |
| `Order`               | `Payment`             | order uses a payment                          |
| `Booking`             | `Ticket`              | booking contains tickets                      |
| `Booking`             | `Payment`             | booking uses a payment                        |
| `Event`               | `Visitor`             | event tracks registered visitors              |
| `Schedule`            | `Event`               | schedule contains events                      |
| `Exhibition`          | `Exhibit`             | exhibition contains exhibits                  |
| `Exhibition`          | `Ticket`              | exhibition tracks sold tickets                |
| `TemporaryExhibition` | `Loan`                | temporary exhibition contains loans           |
| `Excursion`           | `Hall`                | excursion route is a list of halls            |
| `Excursion`           | `Guide`               | excursion is led by a guide                   |
| `Excursion`           | `Visitor`             | excursion has visitors                        |
| `Loan`                | `Exhibit`             | loan is about a specific exhibit              |
| `Restoration`         | `Exhibit`, `Restorer` | restoration links an exhibit and a restorer   |
| `InsurancePolicy`     | `Exhibit`             | policy is for an exhibit                      |
| `StorageMoveAct`      | `Storage`, `Exhibit`  | move act links two storages and an exhibit    |
| `Invoice`             | `Payment`             | invoice is paid via a payment                 |

### Use as parameter (A's method takes B)

| From            | Parameter                              | Method                            |
|-----------------|----------------------------------------|-----------------------------------|
| `TicketType`    | `Visitor`                              | `is_eligible(visitor)`            |
| `TicketType`    | `Visitor`                              | `calculate_price(visitor)`        |
| `Collection`    | `Exhibit`                              | `add_exhibit(exhibit)`            |
| `Fund`          | `Exhibit`                              | `accept_item(exhibit)`            |
| `Building`      | `Hall`, `Room`                         | `add_hall`, `add_room`            |
| `Curator`       | `Loan`                                 | `approve_loan(loan)`              |
| `Administrator` | `Loan`, `Invoice`, `Payment`, `Museum` | `approve_loan`, `pay_invoice`     |
| `Order`         | `Payment`                              | `checkout(payment)`               |
| `Booking`       | `Payment`                              | `pay(payment)`                    |
| `Storage`       | `Exhibit`                              | `place_exhibit`, `remove_exhibit` |

---

##  Exceptions

All exceptions inherit from `MuseumException`. Every exception is
used at least once in domain logic.

| Exception                          | Thrown by                                                                                                                                                                                                                                                                                                                                                |
|------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `MuseumException`                  | base class for all museum errors                                                                                                                                                                                                                                                                                                                         |
| `InvalidTicketException`           | `Ticket.validate`, `Ticket.mark_used`, `Ticket.refund`, `TicketType.calculate_price`, `Visitor.buy_ticket`, `Cashier.sell_ticket`                                                                                                                                                                                                                        |
| `ExhibitNotFoundException`         | `Catalog.find_by_number`, `Collection.find_exhibit`                                                                                                                                                                                                                                                                                                      |
| `RestorationException`             | `Restorer.restore_exhibit`, `Restorer.make_restoration_report`                                                                                                                                                                                                                                                                                           |
| `LoanAlreadyActiveException`       | (reserved for future)                                                                                                                                                                                                                                                                                                                                    |
| `LoanOverdueException`             | `Administrator.approve_loan`, `Curator.approve_loan`                                                                                                                                                                                                                                                                                                     |
| `InsufficientFundsException`       | `Museum.spend_budget`, `MuseumCard.pay`, `Administrator.pay_invoice`                                                                                                                                                                                                                                                                                     |
| `StorageCapacityExceededException` | `Storage.place_exhibit`                                                                                                                                                                                                                                                                                                                                  |
| `AccessDeniedException`            | `Building.open_for_visitors`, `Showcase.open_showcase`, `AccessControl.require_access`                                                                                                                                                                                                                                                                   |
| `ClimateControlException`          | (reserved for future)                                                                                                                                                                                                                                                                                                                                    |
| `InventoryMismatchException`       | (reserved for future)                                                                                                                                                                                                                                                                                                                                    |
| `PaymentFailedException`           | `Cashier.accept_payment`, `Administrator.pay_invoice`, `Order.checkout`, `Booking.pay` (propagated from `Payment.process`)                                                                                                                                                                                                                               |
| `BookingConflictException`         | `Hall.set_exhibition`                                                                                                                                                                                                                                                                                                                                    |
| `InvalidExhibitStateException`     | `Exhibit.attach_to_collection`, `Showcase.open/place/remove`, `Collection.add_exhibit`, `Employee.take_vacation`, `Visitor.enter_museum`, `Loan.*`, `Restoration.*`, `Invoice.*`, `Order.checkout`, `Booking.*`, `Event.*`, `Exhibition.*`, `Excursion.*`, `Incident.*`, `Acquisition.*`, `InsurancePolicy.*`, `Contract.*`, `Payment.*`, `MuseumCard.*` |

---

## Scenarios (see `main.py`)

You'll get an interactive menu with 10 scenarios. Each scenario in `main.py` demonstrates a real-world workflow that
crosses several packages:

1. **Ticket sale and visitor entry** — `Visitor`, `Cashier`, `TicketType`, `Ticket`, `SecurityGuard`, `AccessControl`.
2. **Guided excursion** — `Guide`, `Excursion`, `Hall`, `Visitor`.
3. **Exhibit restoration** — `Restorer`, `Restoration`, `Painting`, `Report`.
4. **Exhibit loan** — `Administrator`, `Loan`, `Painting`, `Contract`.
5. **Storage inventory** — `Storage`, `Inventory`, `Employee`, `Painting`.
6. **New acquisition** — `Acquisition`, `Painting`, `Fund`, `Collection`.
7. **Incident in the hall** — `SecurityGuard`, `Incident`.
8. **Museum shop purchase** — `Visitor`, `Membership`, `Order`, `ShopItem`, `Payment`.
9. **Climate monitoring** — `ClimateZone`, `Sensor`, `SensorType`.
10. **Create an exhibition** — `Curator`, `Collection`, `Exhibition`, `Ticket`.
