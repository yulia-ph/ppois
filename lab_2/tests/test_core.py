"""Tests for the museum_core package.

Covers: Museum, Building, Hall, Room, Storage, Showcase, ClimateZone, Sensor.
Sections are added as each class is implemented.
"""
import pytest

from exceptions.AccessDeniedException import AccessDeniedException
from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
from museum_core.Sensor import SensorType
from tests.conftest import *


class TestBuildingInit:
    """Tests for Building.__init__ and basic properties."""

    def test_init_stores_basic_fields(self, main_building):
        assert main_building.name == "Main Building"
        assert main_building.address == "1 Main St"
        assert main_building.type == Building.TYPE_MAIN
        assert main_building.floors == 3

    def test_init_halls_and_rooms_are_empty(self, main_building):
        assert main_building.halls == []
        assert main_building.rooms == []


class TestBuildingAddHall:
    def test_add_hall_success(self, main_building, sample_hall):
        result = main_building.add_hall(sample_hall)
        assert result is True
        assert sample_hall in main_building.halls

    def test_add_hall_duplicate_raises(self, main_building, sample_hall):
        main_building.add_hall(sample_hall)
        with pytest.raises(ValueError):
            main_building.add_hall(sample_hall)


class TestBuildingAddRoom:
    def test_add_room_success(self, main_building, sample_room):
        result = main_building.add_room(sample_room)
        assert result is True
        assert sample_room in main_building.rooms

    def test_add_room_duplicate_raises(self, main_building, sample_room):
        main_building.add_room(sample_room)
        with pytest.raises(ValueError):
            main_building.add_room(sample_room)


class TestBuildingRemoveHall:
    def test_remove_hall_success(self, main_building, sample_hall):
        main_building.add_hall(sample_hall)
        result = main_building.remove_hall(sample_hall)
        assert result is True
        assert sample_hall not in main_building.halls

    def test_remove_hall_not_present_raises(self, main_building, sample_hall):
        with pytest.raises(ValueError):
            main_building.remove_hall(sample_hall)


class TestBuildingRemoveRoom:
    def test_remove_room_success(self, main_building, sample_room):
        main_building.add_room(sample_room)
        result = main_building.remove_room(sample_room)
        assert result is True
        assert sample_room not in main_building.rooms

    def test_remove_room_not_present_raises(self, main_building, sample_room):
        with pytest.raises(ValueError):
            main_building.remove_room(sample_room)


class TestBuildingOpenForVisitors:
    def test_main_building_opens(self, main_building):
        result = main_building.open_for_visitors()
        assert result is True
        assert main_building.is_open is True

    def test_storage_building_raises(self, storage_building):
        with pytest.raises(AccessDeniedException):
            storage_building.open_for_visitors()
        assert storage_building.is_open is False

    def test_admin_building_raises(self, admin_building):
        with pytest.raises(AccessDeniedException):
            admin_building.open_for_visitors()
        assert admin_building.is_open is False


class TestBuildingCloseForVisitors:
    def test_close_opened_building(self, main_building):
        main_building.open_for_visitors()
        result = main_building.close_for_visitors()
        assert result is True
        assert main_building.is_open is False

    def test_close_already_closed_building(self, main_building):
        """Closing an already closed building is not an error."""
        result = main_building.close_for_visitors()
        assert result is True
        assert main_building.is_open is False


class TestBuildingEvacuate:
    def test_evacuate_opened_building(self, main_building):
        main_building.open_for_visitors()
        result = main_building.evacuate()
        assert result is True
        assert main_building.is_open is False

    def test_evacuate_closed_building_raises(self, main_building):
        with pytest.raises(InvalidExhibitStateException):
            main_building.evacuate()


class TestBuildingFreeSpace:
    def test_free_space_empty_building(self, main_building):
        # 3 floors * 10 = 30 slots
        assert main_building.count_free_space() == 30

    def test_free_space_after_adding_hall(self, main_building, sample_hall):
        main_building.add_hall(sample_hall)
        assert main_building.count_free_space() == 29

    def test_is_full_true_when_capacity_reached(self):
        from museum_core.Hall import Hall
        small = Building("Tiny", "addr", Building.TYPE_MAIN, 1)
        for i in range(10):
            small.add_hall(Hall(i, 50.0))
        assert small.is_full() is True


class TestClimateZoneInit:
    def test_init_stores_norm_values(self, climate_zone):
        assert climate_zone.norm_temperature == 20.0
        assert climate_zone.norm_humidity == 50.0

    def test_init_current_equals_norm(self, climate_zone):
        assert climate_zone.temperature == 20.0
        assert climate_zone.humidity == 50.0

    def test_init_default_tolerances(self, climate_zone):
        assert climate_zone.temp_tolerance == 2.0
        assert climate_zone.humid_tolerance == 5.0

    def test_init_sensors_empty(self, climate_zone):
        assert climate_zone.sensors == []

    def test_init_humidity_out_of_range_raises(self):
        from museum_core.ClimateZone import ClimateZone
        with pytest.raises(ValueError):
            ClimateZone(norm_temperature=20.0, norm_humidity=200.0)


class TestClimateZoneSensors:
    def test_add_sensor_success(self, climate_zone):
        class FakeSensor:
            id = "S1"
        s = FakeSensor()
        assert climate_zone.add_sensor(s) is True
        assert s in climate_zone.sensors

    def test_add_sensor_duplicate_raises(self, climate_zone):
        class FakeSensor:
            id = "S1"
        s = FakeSensor()
        climate_zone.add_sensor(s)
        with pytest.raises(ValueError):
            climate_zone.add_sensor(s)

    def test_remove_sensor_success(self, climate_zone):
        class FakeSensor:
            id = "S1"
        s = FakeSensor()
        climate_zone.add_sensor(s)
        assert climate_zone.remove_sensor(s) is True
        assert s not in climate_zone.sensors

    def test_remove_sensor_not_present_raises(self, climate_zone):
        class FakeSensor:
            id = "S1"
        s = FakeSensor()
        with pytest.raises(ValueError):
            climate_zone.remove_sensor(s)


class TestClimateZoneMonitor:
    def test_monitor_returns_tuple(self, climate_zone):
        assert climate_zone.monitor() == (20.0, 50.0)

    def test_monitor_reflects_adjustment(self, climate_zone):
        climate_zone.adjust(22.0, 55.0)
        assert climate_zone.monitor() == (22.0, 55.0)


class TestClimateZoneAdjust:
    def test_adjust_valid_values(self, climate_zone):
        assert climate_zone.adjust(22.0, 55.0) is True
        assert climate_zone.temperature == 22.0
        assert climate_zone.humidity == 55.0


    def test_adjust_temperature_too_low_raises(self, climate_zone):
        with pytest.raises(ValueError):
            climate_zone.adjust(-100.0, 50.0)

    def test_adjust_humidity_too_high_raises(self, climate_zone):
        with pytest.raises(ValueError):
            climate_zone.adjust(20.0, 200.0)

    def test_adjust_humidity_negative_raises(self, climate_zone):
        with pytest.raises(ValueError):
            climate_zone.adjust(20.0, -1.0)


class TestClimateZoneNorm:
    def test_is_within_norm_when_at_norm(self, climate_zone):
        assert climate_zone.is_within_norm() is True

    def test_is_within_norm_when_at_tolerance_edge(self, climate_zone):
        # tolerance is 2.0 for temp, 5.0 for humidity
        climate_zone.adjust(22.0, 55.0)
        assert climate_zone.is_within_norm() is True

    def test_is_within_norm_when_temperature_exceeds(self, climate_zone):
        climate_zone.adjust(25.0, 50.0)
        assert climate_zone.is_within_norm() is False

    def test_is_within_norm_when_humidity_exceeds(self, climate_zone):
        climate_zone.adjust(20.0, 60.0)
        assert climate_zone.is_within_norm() is False


class TestClimateZoneTolerances:
    def test_set_tolerances_success(self, climate_zone):
        assert climate_zone.set_tolerances(3.0, 7.0) is True
        assert climate_zone.temp_tolerance == 3.0
        assert climate_zone.humid_tolerance == 7.0

    def test_set_tolerances_negative_temperature_raises(self, climate_zone):
        with pytest.raises(ValueError):
            climate_zone.set_tolerances(-1.0, 5.0)

    def test_set_tolerances_negative_humidity_raises(self, climate_zone):
        with pytest.raises(ValueError):
            climate_zone.set_tolerances(2.0, -1.0)


class TestClimateZoneEncapsulation:
    def test_sensors_property_returns_copy(self, climate_zone):
        class FakeSensor:
            id = "S1"
        climate_zone.add_sensor(FakeSensor())
        sensors = climate_zone.sensors
        sensors.append("fake")
        assert len(climate_zone.sensors) == 1


class TestHallInit:
    def test_init_stores_fields(self, sample_hall):
        assert sample_hall.number == 1
        assert sample_hall.area == 100.0

    def test_init_showcases_empty(self, sample_hall):
        assert sample_hall.showcases == []

    def test_init_no_exhibition(self, sample_hall):
        assert sample_hall.current_exhibition is None
        assert sample_hall.is_busy is False

    def test_init_zero_area_raises(self):
        from museum_core.Hall import Hall
        with pytest.raises(ValueError):
            Hall(1, 0.0)

    def test_init_negative_area_raises(self):
        from museum_core.Hall import Hall
        with pytest.raises(ValueError):
            Hall(1, -10.0)


class TestHallShowcases:
    def test_add_showcase_success(self, sample_hall, fake_showcase):
        result = sample_hall.add_showcase(fake_showcase)
        assert result is True
        assert fake_showcase in sample_hall.showcases

    def test_add_showcase_duplicate_raises(self, sample_hall, fake_showcase):
        sample_hall.add_showcase(fake_showcase)
        with pytest.raises(ValueError):
            sample_hall.add_showcase(fake_showcase)

    def test_remove_showcase_success(self, sample_hall, fake_showcase):
        sample_hall.add_showcase(fake_showcase)
        result = sample_hall.remove_showcase(fake_showcase)
        assert result is True
        assert fake_showcase not in sample_hall.showcases

    def test_remove_showcase_not_present_raises(self, sample_hall, fake_showcase):
        with pytest.raises(ValueError):
            sample_hall.remove_showcase(fake_showcase)


class TestHallSetExhibition:
    def test_set_exhibition_success(self, sample_hall):
        class FakeExhibition:
            title = "Impressionists"
        exhibition = FakeExhibition()
        result = sample_hall.set_exhibition(exhibition)
        assert result is True
        assert sample_hall.current_exhibition is exhibition
        assert sample_hall.is_busy is True

    def test_set_exhibition_none_raises(self, sample_hall):
        with pytest.raises(ValueError):
            sample_hall.set_exhibition(None)

    def test_set_exhibition_when_busy_raises(self, sample_hall):
        from exceptions.BookingConflictException import BookingConflictException
        class FakeExhibition:
            title = "Impressionists"
        sample_hall.set_exhibition(FakeExhibition())
        with pytest.raises(BookingConflictException):
            sample_hall.set_exhibition(FakeExhibition())


class TestHallClearExhibition:
    def test_clear_exhibition_success(self, sample_hall):
        class FakeExhibition:
            title = "Impressionists"
        sample_hall.set_exhibition(FakeExhibition())
        result = sample_hall.clear_exhibition()
        assert result is True
        assert sample_hall.current_exhibition is None
        assert sample_hall.is_busy is False

    def test_clear_exhibition_idempotent(self, sample_hall):
        """Clearing an empty hall is not an error."""
        assert sample_hall.clear_exhibition() is True
        assert sample_hall.current_exhibition is None


class TestHallCapacity:
    def test_capacity_at_100_sqm(self, sample_hall):
        # 100 / 2 = 50
        assert sample_hall.calculate_capacity() == 50

    def test_capacity_at_odd_area(self):
        from museum_core.Hall import Hall
        hall = Hall(2, 75.0)
        # 75 / 2 = 37 (int truncation)
        assert hall.calculate_capacity() == 37

    def test_is_full_below_capacity(self, sample_hall):
        assert sample_hall.is_full(10) is False

    def test_is_full_at_capacity(self, sample_hall):
        assert sample_hall.is_full(50) is True

    def test_is_full_above_capacity(self, sample_hall):
        assert sample_hall.is_full(100) is True


class TestHallCountExhibits:
    def test_count_exhibits_no_showcases(self, sample_hall):
        assert sample_hall.count_exhibits() == 0

    def test_count_exhibits_empty_showcases(self, sample_hall, fake_showcase):
        sample_hall.add_showcase(fake_showcase)
        assert sample_hall.count_exhibits() == 0

    def test_count_exhibits_with_exhibits(self, sample_hall, fake_showcase_with_exhibit):
        sample_hall.add_showcase(fake_showcase_with_exhibit)
        assert sample_hall.count_exhibits() == 1

    def test_count_exhibits_mixed(self, sample_hall):
        from tests.conftest import FakeShowcase
        empty = FakeShowcase()
        full = FakeShowcase(exhibit=object())
        sample_hall.add_showcase(empty)
        sample_hall.add_showcase(full)
        assert sample_hall.count_exhibits() == 1


from datetime import datetime, timedelta


class TestMuseumInit:
    def test_init_stores_fields(self, museum):
        assert museum.name == "Hermitage"
        assert museum.address == "Palace Sq. 2"
        assert museum.website == "hermitage.ru"

    def test_init_budget_zero(self, museum):
        assert museum.budget == 0.0

    def test_init_empty_name_raises(self):
        from museum_core.Museum import Museum
        with pytest.raises(ValueError):
            Museum("", "addr", "site")

    def test_init_empty_address_raises(self):
        from museum_core.Museum import Museum
        with pytest.raises(ValueError):
            Museum("name", "", "site")

    def test_init_empty_website_raises(self):
        from museum_core.Museum import Museum
        with pytest.raises(ValueError):
            Museum("name", "addr", "")


class TestMuseumAddEntities:
    def test_add_building_success(self, museum, fake_building):
        assert museum.add_building(fake_building) is True
        assert fake_building in museum.buildings

    def test_add_building_duplicate_raises(self, museum, fake_building):
        museum.add_building(fake_building)
        with pytest.raises(ValueError):
            museum.add_building(fake_building)

    def test_add_employee_success(self, museum, fake_employee):
        assert museum.add_employee(fake_employee) is True
        assert fake_employee in museum.employees

    def test_add_employee_duplicate_raises(self, museum, fake_employee):
        museum.add_employee(fake_employee)
        with pytest.raises(ValueError):
            museum.add_employee(fake_employee)

    def test_add_exhibition_success(self, museum, fake_exhibition):
        assert museum.add_exhibition(fake_exhibition) is True

    def test_add_exhibition_duplicate_raises(self, museum, fake_exhibition):
        museum.add_exhibition(fake_exhibition)
        with pytest.raises(ValueError):
            museum.add_exhibition(fake_exhibition)

    def test_add_fund_success(self, museum, fake_fund):
        assert museum.add_fund(fake_fund) is True

    def test_add_fund_duplicate_raises(self, museum, fake_fund):
        museum.add_fund(fake_fund)
        with pytest.raises(ValueError):
            museum.add_fund(fake_fund)

    def test_add_ticket_type_success(self, museum, fake_ticket_type):
        assert museum.add_ticket_type(fake_ticket_type) is True

    def test_add_ticket_type_duplicate_raises(self, museum, fake_ticket_type):
        museum.add_ticket_type(fake_ticket_type)
        with pytest.raises(ValueError):
            museum.add_ticket_type(fake_ticket_type)


class TestMuseumRemoveEntities:
    def test_remove_building_success(self, museum, fake_building):
        museum.add_building(fake_building)
        assert museum.remove_building(fake_building) is True
        assert fake_building not in museum.buildings

    def test_remove_building_not_present_raises(self, museum, fake_building):
        with pytest.raises(ValueError):
            museum.remove_building(fake_building)

    def test_remove_employee_success(self, museum, fake_employee):
        museum.add_employee(fake_employee)
        assert museum.remove_employee(fake_employee) is True

    def test_remove_employee_not_present_raises(self, museum, fake_employee):
        with pytest.raises(ValueError):
            museum.remove_employee(fake_employee)

    def test_remove_exhibition_success(self, museum, fake_exhibition):
        museum.add_exhibition(fake_exhibition)
        assert museum.remove_exhibition(fake_exhibition) is True

    def test_remove_exhibition_not_present_raises(self, museum, fake_exhibition):
        with pytest.raises(ValueError):
            museum.remove_exhibition(fake_exhibition)

    def test_remove_fund_success(self, museum, fake_fund):
        museum.add_fund(fake_fund)
        assert museum.remove_fund(fake_fund) is True

    def test_remove_fund_not_present_raises(self, museum, fake_fund):
        with pytest.raises(ValueError):
            museum.remove_fund(fake_fund)

    def test_remove_ticket_type_success(self, museum, fake_ticket_type):
        museum.add_ticket_type(fake_ticket_type)
        assert museum.remove_ticket_type(fake_ticket_type) is True

    def test_remove_ticket_type_not_present_raises(self, museum, fake_ticket_type):
        with pytest.raises(ValueError):
            museum.remove_ticket_type(fake_ticket_type)


class TestMuseumFind:
    def test_find_ticket_type_found(self, museum, fake_ticket_type):
        museum.add_ticket_type(fake_ticket_type)
        found = museum.find_ticket_type("Adult")
        assert found is fake_ticket_type

    def test_find_ticket_type_not_found_raises(self, museum):
        with pytest.raises(ValueError):
            museum.find_ticket_type("VIP")

    def test_find_employee_found(self, museum, fake_employee):
        museum.add_employee(fake_employee)
        found = museum.find_employee("Ivanov")
        assert found is fake_employee

    def test_find_employee_not_found_raises(self, museum):
        with pytest.raises(ValueError):
            museum.find_employee("Petrov")

    def test_find_building_found(self, museum, fake_building):
        museum.add_building(fake_building)
        found = museum.find_building("Main Building")
        assert found is fake_building

    def test_find_building_not_found_raises(self, museum):
        with pytest.raises(ValueError):
            museum.find_building("Storage")


class TestMuseumBudget:
    def test_set_budget_success(self, museum):
        assert museum.set_budget(1000.0) is True
        assert museum.budget == 1000.0

    def test_set_budget_negative_raises(self, museum):
        with pytest.raises(ValueError):
            museum.set_budget(-1.0)

    def test_increase_budget_success(self, museum):
        museum.set_budget(1000.0)
        assert museum.increase_budget(500.0) is True
        assert museum.budget == 1500.0

    def test_increase_budget_zero_raises(self, museum):
        with pytest.raises(ValueError):
            museum.increase_budget(0.0)

    def test_increase_budget_negative_raises(self, museum):
        with pytest.raises(ValueError):
            museum.increase_budget(-100.0)

    def test_spend_budget_success(self, museum):
        museum.set_budget(1000.0)
        assert museum.spend_budget(300.0) is True
        assert museum.budget == 700.0

    def test_spend_budget_zero_raises(self, museum):
        museum.set_budget(1000.0)
        with pytest.raises(ValueError):
            museum.spend_budget(0.0)

    def test_spend_budget_insufficient_raises(self, museum):
        from exceptions.InsufficientFundsException import InsufficientFundsException
        museum.set_budget(100.0)
        with pytest.raises(InsufficientFundsException):
            museum.spend_budget(500.0)


class TestMuseumVisitorsToday:
    def test_count_visitors_empty_records(self, museum):
        assert museum.count_visitors_today([]) == 0

    def test_count_visitors_only_public_zone(self, museum):
        from tests.conftest import FakeAccessRecord
        now = datetime.now()
        records = [
            FakeAccessRecord(True, "public", now),
            FakeAccessRecord(True, "storage", now),
            FakeAccessRecord(True, "admin", now),
        ]
        assert museum.count_visitors_today(records) == 1

    def test_count_visitors_only_granted(self, museum):
        from tests.conftest import FakeAccessRecord
        now = datetime.now()
        records = [
            FakeAccessRecord(True, "public", now),
            FakeAccessRecord(False, "public", now),
            FakeAccessRecord(False, "public", now),
        ]
        assert museum.count_visitors_today(records) == 1

    def test_count_visitors_only_today(self, museum):
        from tests.conftest import FakeAccessRecord
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        records = [
            FakeAccessRecord(True, "public", now),
            FakeAccessRecord(True, "public", yesterday),
        ]
        assert museum.count_visitors_today(records) == 1

    def test_count_visitors_all_conditions(self, museum):
        from tests.conftest import FakeAccessRecord
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        records = [
            FakeAccessRecord(True, "public", now),         # ✓
            FakeAccessRecord(True, "public", now),         # ✓
            FakeAccessRecord(False, "public", now),        # ✗ not granted
            FakeAccessRecord(True, "storage", now),        # ✗ wrong zone
            FakeAccessRecord(True, "public", yesterday),   # ✗ wrong day
        ]
        assert museum.count_visitors_today(records) == 2


class TestMuseumEncapsulation:
    def test_buildings_property_returns_copy(self, museum, fake_building):
        museum.add_building(fake_building)
        buildings = museum.buildings
        buildings.append("fake")
        assert len(museum.buildings) == 1

    def test_employees_property_returns_copy(self, museum, fake_employee):
        museum.add_employee(fake_employee)
        employees = museum.employees
        employees.append("fake")
        assert len(museum.employees) == 1

    def test_exhibitions_property_returns_copy(self, museum, fake_exhibition):
        museum.add_exhibition(fake_exhibition)
        exhibitions = museum.exhibitions
        exhibitions.append("fake")
        assert len(museum.exhibitions) == 1

    def test_funds_property_returns_copy(self, museum, fake_fund):
        museum.add_fund(fake_fund)
        funds = museum.funds
        funds.append("fake")
        assert len(museum.funds) == 1

    def test_ticket_types_property_returns_copy(self, museum, fake_ticket_type):
        museum.add_ticket_type(fake_ticket_type)
        types_ = museum.ticket_types
        types_.append("fake")
        assert len(museum.ticket_types) == 1


class TestRoomInit:
    def test_init_stores_fields(self, sample_room):
        assert sample_room.number == 101
        assert sample_room.purpose == RoomPurpose.OFFICE

    def test_init_climate_zone_none(self, sample_room):
        assert sample_room.climate_zone is None
        assert sample_room.has_climate_control is False

    def test_init_invalid_purpose_type_raises(self):
        from museum_core.Room import Room
        with pytest.raises(TypeError):
            Room(1, "cashier")

    def test_init_none_purpose_raises(self):
        from museum_core.Room import Room
        with pytest.raises(TypeError):
            Room(1, None)


class TestRoomAssignPurpose:
    def test_assign_purpose_success(self, sample_room):
        result = sample_room.assign_purpose(RoomPurpose.RESTORATION)
        assert result is True
        assert sample_room.purpose == RoomPurpose.RESTORATION

    def test_assign_purpose_invalid_type_raises(self, sample_room):
        with pytest.raises(TypeError):
            sample_room.assign_purpose("restoration")

    def test_assign_purpose_none_raises(self, sample_room):
        with pytest.raises(TypeError):
            sample_room.assign_purpose(None)


class TestRoomClimateZone:
    def test_set_climate_zone_success(self, sample_room, fake_climate_zone_ok):
        result = sample_room.set_climate_zone(fake_climate_zone_ok)
        assert result is True
        assert sample_room.climate_zone is fake_climate_zone_ok
        assert sample_room.has_climate_control is True

    def test_set_climate_zone_none_raises(self, sample_room):
        with pytest.raises(ValueError):
            sample_room.set_climate_zone(None)

    def test_remove_climate_zone_success(self, sample_room, fake_climate_zone_ok):
        sample_room.set_climate_zone(fake_climate_zone_ok)
        result = sample_room.remove_climate_zone()
        assert result is True
        assert sample_room.climate_zone is None
        assert sample_room.has_climate_control is False

    def test_remove_climate_zone_idempotent(self, sample_room):
        """Removing when nothing is attached is not an error."""
        assert sample_room.remove_climate_zone() is True
        assert sample_room.climate_zone is None


class TestRoomCheckClimate:
    def test_check_climate_no_zone_returns_true(self, sample_room):
        assert sample_room.check_climate() is True

    def test_check_climate_zone_ok_returns_true(self, sample_room, fake_climate_zone_ok):
        sample_room.set_climate_zone(fake_climate_zone_ok)
        assert sample_room.check_climate() is True

    def test_check_climate_zone_bad_returns_false(self, sample_room, fake_climate_zone_bad):
        sample_room.set_climate_zone(fake_climate_zone_bad)
        assert sample_room.check_climate() is False


class TestRoomNeedsClimateControl:
    def test_office_does_not_need(self, sample_room):
        assert sample_room.needs_climate_control() is False

    def test_restoration_needs(self, sample_room):
        sample_room.assign_purpose(RoomPurpose.RESTORATION)
        assert sample_room.needs_climate_control() is True

    def test_storage_needs(self, sample_room):
        sample_room.assign_purpose(RoomPurpose.STORAGE)
        assert sample_room.needs_climate_control() is True

    def test_cashier_does_not_need(self, sample_room):
        sample_room.assign_purpose(RoomPurpose.CASHIER)
        assert sample_room.needs_climate_control() is False

    def test_security_does_not_need(self, sample_room):
        sample_room.assign_purpose(RoomPurpose.SECURITY)
        assert sample_room.needs_climate_control() is False


class TestSensorInit:
    def test_init_stores_fields(self, sensor_temperature, climate_zone):
        assert sensor_temperature.id == "T-01"
        assert sensor_temperature.type == SensorType.TEMPERATURE
        assert sensor_temperature.zone is climate_zone

    def test_init_value_zero(self, sensor_temperature):
        assert sensor_temperature.value == 0.0

    def test_init_not_calibrated(self, sensor_temperature):
        assert sensor_temperature.is_calibrated is False

    def test_init_empty_id_raises(self, climate_zone):
        from museum_core.Sensor import Sensor, SensorType
        with pytest.raises(ValueError):
            Sensor("", SensorType.TEMPERATURE, climate_zone)

    def test_init_invalid_type_raises(self, climate_zone):
        from museum_core.Sensor import Sensor
        with pytest.raises(TypeError):
            Sensor("X", "temperature", climate_zone)

    def test_init_none_zone_raises(self):
        from museum_core.Sensor import Sensor, SensorType
        with pytest.raises(ValueError):
            Sensor("X", SensorType.TEMPERATURE, None)


class TestSensorReadValue:
    def test_temperature_reads_zone_temperature(self, sensor_temperature, climate_zone):
        value = sensor_temperature.read_value()
        assert value == climate_zone.temperature

    def test_temperature_reflects_zone_change(self, sensor_temperature, climate_zone):
        climate_zone.adjust(25.0, 55.0)
        assert sensor_temperature.read_value() == 25.0

    def test_humidity_reads_zone_humidity(self, sensor_humidity, climate_zone):
        value = sensor_humidity.read_value()
        assert value == climate_zone.humidity

    def test_humidity_reflects_zone_change(self, sensor_humidity, climate_zone):
        climate_zone.adjust(25.0, 60.0)
        assert sensor_humidity.read_value() == 60.0

    def test_motion_always_reads_zero(self, sensor_motion):
        assert sensor_motion.read_value() == 0.0

    def test_motion_ignores_zone_changes(self, sensor_motion, climate_zone):
        climate_zone.adjust(30.0, 80.0)
        assert sensor_motion.read_value() == 0.0


class TestSensorSendAlert:
    def test_temperature_no_alert_when_in_norm(self, sensor_temperature):
        # zone is at norm 20/50, tolerance 2/5
        assert sensor_temperature.send_alert() is False

    def test_temperature_alert_when_out_of_norm(self, sensor_temperature, climate_zone):
        climate_zone.adjust(30.0, 50.0)  # deviation 10°C > tolerance 2°C
        assert sensor_temperature.send_alert() is True

    def test_humidity_alert_when_out_of_norm(self, sensor_humidity, climate_zone):
        climate_zone.adjust(20.0, 70.0)  # deviation 20% > tolerance 5%
        assert sensor_humidity.send_alert() is True

    def test_humidity_no_alert_when_in_norm(self, sensor_humidity):
        assert sensor_humidity.send_alert() is False

    def test_motion_never_alerts(self, sensor_motion, climate_zone):
        climate_zone.adjust(40.0, 90.0)
        assert sensor_motion.send_alert() is False


class TestSensorCalibrate:
    def test_calibrate_success(self, sensor_temperature):
        result = sensor_temperature.calibrate(25.0)
        assert result is True
        assert sensor_temperature.value == 25.0
        assert sensor_temperature.is_calibrated is True

    def test_calibrate_at_min_boundary(self, sensor_temperature):
        assert sensor_temperature.calibrate(-100.0) is True
        assert sensor_temperature.value == -100.0

    def test_calibrate_at_max_boundary(self, sensor_temperature):
        assert sensor_temperature.calibrate(100.0) is True
        assert sensor_temperature.value == 100.0

    def test_calibrate_below_min_raises(self, sensor_temperature):
        with pytest.raises(ValueError):
            sensor_temperature.calibrate(-200.0)

    def test_calibrate_above_max_raises(self, sensor_temperature):
        with pytest.raises(ValueError):
            sensor_temperature.calibrate(200.0)


class TestSensorReset:
    def test_reset_clears_value(self, sensor_temperature):
        sensor_temperature.calibrate(25.0)
        assert sensor_temperature.reset() is True
        assert sensor_temperature.value == 0.0

    def test_reset_clears_calibration_flag(self, sensor_temperature):
        sensor_temperature.calibrate(25.0)
        sensor_temperature.reset()
        assert sensor_temperature.is_calibrated is False

    def test_reset_idempotent(self, sensor_temperature):
        assert sensor_temperature.reset() is True
        assert sensor_temperature.reset() is True
        assert sensor_temperature.value == 0.0


class TestShowcaseInit:
    def test_init_stores_fields(self, showcase):
        assert showcase.inventory_number == "SC-001"
        assert showcase.type == "horizontal"

    def test_init_is_locked(self, showcase):
        assert showcase.is_locked is True

    def test_init_is_empty(self, showcase):
        assert showcase.is_empty is True
        assert showcase.exhibit is None

    def test_init_empty_inventory_raises(self):
        from museum_core.Showcase import Showcase
        with pytest.raises(ValueError):
            Showcase("", "horizontal")

    def test_init_non_string_type_raises(self):
        from museum_core.Showcase import Showcase
        with pytest.raises(TypeError):
            Showcase("SC-001", 123)


class TestShowcaseOpen:
    def test_open_success(self, showcase, fake_employee_with_position):
        result = showcase.open_showcase(fake_employee_with_position)
        assert result is True
        assert showcase.is_locked is False

    def test_open_already_open_raises(self, showcase_open, fake_employee_with_position):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            showcase_open.open_showcase(fake_employee_with_position)

    def test_open_without_position_raises(self, showcase, fake_visitor):
        from exceptions.AccessDeniedException import AccessDeniedException
        with pytest.raises(AccessDeniedException):
            showcase.open_showcase(fake_visitor)

    def test_open_failed_keeps_locked(self, showcase, fake_visitor):
        from exceptions.AccessDeniedException import AccessDeniedException
        with pytest.raises(AccessDeniedException):
            showcase.open_showcase(fake_visitor)
        assert showcase.is_locked is True



class TestShowcasePlaceExhibit:
    def test_place_success(self, showcase, fake_exhibit):
        result = showcase.place_exhibit(fake_exhibit)
        assert result is True
        assert showcase.exhibit is fake_exhibit
        assert showcase.is_empty is False

    def test_place_none_raises(self, showcase):
        with pytest.raises(ValueError):
            showcase.place_exhibit(None)

    def test_place_when_occupied_raises(self, showcase_with_exhibit, fake_exhibit):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            showcase_with_exhibit.place_exhibit(fake_exhibit)


class TestShowcaseRemoveExhibit:
    def test_remove_returns_exhibit(self, showcase_with_exhibit, fake_exhibit):
        removed = showcase_with_exhibit.remove_exhibit()
        assert removed is fake_exhibit
        assert showcase_with_exhibit.is_empty is True

    def test_remove_from_empty_raises(self, showcase):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            showcase.remove_exhibit()


class TestShowcaseHumidity:
    def test_check_humidity_returns_zero(self, showcase):
        assert showcase.check_humidity() == 0.0


class TestShowcaseNeedsRestoration:
    def test_empty_showcase_returns_false(self, showcase):
        assert showcase.needs_restoration() is False

    def test_good_exhibit_returns_false(self, showcase, fake_exhibit):
        showcase.place_exhibit(fake_exhibit)
        assert showcase.needs_restoration() is False

    def test_damaged_exhibit_returns_true(self, showcase, fake_exhibit_damaged):
        showcase.place_exhibit(fake_exhibit_damaged)
        assert showcase.needs_restoration() is True

    def test_critical_exhibit_returns_true(self, showcase, fake_exhibit_critical):
        showcase.place_exhibit(fake_exhibit_critical)
        assert showcase.needs_restoration() is True


class TestStorageInit:
    def test_init_stores_fields(self, storage):
        assert storage.name == "Main Storage"
        assert storage.capacity == 3

    def test_init_exhibits_empty(self, storage):
        assert storage.exhibits == []

    def test_init_climate_zone_none(self, storage):
        assert storage.climate_zone is None

    def test_init_free_space_equals_capacity(self, storage):
        assert storage.free_space == 3
        assert storage.is_full is False

    def test_init_empty_name_raises(self):
        from museum_core.Storage import Storage
        with pytest.raises(ValueError):
            Storage("", 10)

    def test_init_zero_capacity_raises(self):
        from museum_core.Storage import Storage
        with pytest.raises(ValueError):
            Storage("X", 0)

    def test_init_negative_capacity_raises(self):
        from museum_core.Storage import Storage
        with pytest.raises(ValueError):
            Storage("X", -5)


class TestStoragePlaceExhibit:
    def test_place_success(self, storage, fake_exhibit_storage_a):
        result = storage.place_exhibit(fake_exhibit_storage_a)
        assert result is True
        assert fake_exhibit_storage_a in storage.exhibits

    def test_place_reduces_free_space(self, storage, fake_exhibit_storage_a):
        storage.place_exhibit(fake_exhibit_storage_a)
        assert storage.free_space == 2

    def test_place_none_raises(self, storage):
        with pytest.raises(ValueError):
            storage.place_exhibit(None)

    def test_place_duplicate_raises(self, storage, fake_exhibit_storage_a):
        storage.place_exhibit(fake_exhibit_storage_a)
        with pytest.raises(ValueError):
            storage.place_exhibit(fake_exhibit_storage_a)

    def test_place_when_full_raises(self, storage_full):
        from exceptions.StorageCapacityExceededException import StorageCapacityExceededException
        extra = FakeExhibitForStorage("EX-003")
        with pytest.raises(StorageCapacityExceededException):
            storage_full.place_exhibit(extra)


class TestStorageRemoveExhibit:
    def test_remove_success(self, storage, fake_exhibit_storage_a):
        storage.place_exhibit(fake_exhibit_storage_a)
        result = storage.remove_exhibit(fake_exhibit_storage_a)
        assert result is True
        assert fake_exhibit_storage_a not in storage.exhibits

    def test_remove_increases_free_space(self, storage, fake_exhibit_storage_a):
        storage.place_exhibit(fake_exhibit_storage_a)
        storage.remove_exhibit(fake_exhibit_storage_a)
        assert storage.free_space == 3

    def test_remove_not_present_raises(self, storage, fake_exhibit_storage_a):
        with pytest.raises(ValueError):
            storage.remove_exhibit(fake_exhibit_storage_a)


class TestStorageHasExhibit:
    def test_has_exhibit_true(self, storage, fake_exhibit_storage_a):
        storage.place_exhibit(fake_exhibit_storage_a)
        assert storage.has_exhibit(fake_exhibit_storage_a) is True

    def test_has_exhibit_false(self, storage, fake_exhibit_storage_a):
        assert storage.has_exhibit(fake_exhibit_storage_a) is False


class TestStorageFindExhibit:
    def test_find_exhibit_found(self, storage, fake_exhibit_storage_a):
        storage.place_exhibit(fake_exhibit_storage_a)
        found = storage.find_exhibit("EX-100")
        assert found is fake_exhibit_storage_a

    def test_find_exhibit_not_found_raises(self, storage):
        with pytest.raises(ValueError):
            storage.find_exhibit("EX-999")

    def test_find_exhibit_in_empty_storage_raises(self, storage):
        with pytest.raises(ValueError):
            storage.find_exhibit("EX-001")


class TestStorageIsFull:
    def test_not_full_when_empty(self, storage):
        assert storage.is_full is False

    def test_not_full_when_partially_filled(self, storage, fake_exhibit_storage_a):
        storage.place_exhibit(fake_exhibit_storage_a)
        assert storage.is_full is False

    def test_full_when_at_capacity(self, storage_full):
        assert storage_full.is_full is True


class TestStorageClimateZone:
    def test_set_climate_zone_success(self, storage, fake_climate_zone_ok):
        result = storage.set_climate_zone(fake_climate_zone_ok)
        assert result is True
        assert storage.climate_zone is fake_climate_zone_ok

    def test_set_climate_zone_none_raises(self, storage):
        with pytest.raises(ValueError):
            storage.set_climate_zone(None)

    def test_check_climate_no_zone_returns_true(self, storage):
        assert storage.check_climate() is True

    def test_check_climate_zone_ok_returns_true(self, storage, fake_climate_zone_ok):
        storage.set_climate_zone(fake_climate_zone_ok)
        assert storage.check_climate() is True

    def test_check_climate_zone_bad_returns_false(self, storage, fake_climate_zone_bad):
        storage.set_climate_zone(fake_climate_zone_bad)
        assert storage.check_climate() is False


class TestStorageRunInventory:
    def test_inventory_clean_when_matching(self, storage, fake_exhibit_storage_a, fake_exhibit_storage_b):
        storage.place_exhibit(fake_exhibit_storage_a)
        storage.place_exhibit(fake_exhibit_storage_b)
        catalog = [fake_exhibit_storage_a, fake_exhibit_storage_b]
        result = storage.run_inventory(catalog)
        assert result["is_clean"] is True
        assert result["missing"] == []
        assert result["extra"] == []

    def test_inventory_missing_exhibit(self, storage, fake_exhibit_storage_a, fake_exhibit_storage_b):
        storage.place_exhibit(fake_exhibit_storage_a)
        catalog = [fake_exhibit_storage_a, fake_exhibit_storage_b]
        result = storage.run_inventory(catalog)
        assert result["is_clean"] is False
        assert fake_exhibit_storage_b in result["missing"]
        assert result["extra"] == []

    def test_inventory_extra_exhibit(self, storage, fake_exhibit_storage_a, fake_exhibit_storage_b):
        storage.place_exhibit(fake_exhibit_storage_a)
        storage.place_exhibit(fake_exhibit_storage_b)
        catalog = [fake_exhibit_storage_a]
        result = storage.run_inventory(catalog)
        assert result["is_clean"] is False
        assert result["missing"] == []
        assert fake_exhibit_storage_b in result["extra"]

    def test_inventory_empty_catalog(self, storage, fake_exhibit_storage_a):
        storage.place_exhibit(fake_exhibit_storage_a)
        result = storage.run_inventory([])
        assert result["is_clean"] is False
        assert fake_exhibit_storage_a in result["extra"]

    def test_inventory_empty_storage(self, storage, fake_exhibit_storage_a):
        result = storage.run_inventory([fake_exhibit_storage_a])
        assert result["is_clean"] is False
        assert fake_exhibit_storage_a in result["missing"]

    def test_inventory_both_empty(self, storage):
        result = storage.run_inventory([])
        assert result["is_clean"] is True


class TestStorageEncapsulation:
    def test_exhibits_property_returns_copy(self, storage, fake_exhibit_storage_a):
        storage.place_exhibit(fake_exhibit_storage_a)
        exhibits = storage.exhibits
        exhibits.append("fake")
        assert len(storage.exhibits) == 1