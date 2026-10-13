"""Tests for the museum_security package.

Covers: AccessControl, Incident.
"""
from datetime import date, timedelta

import pytest

from exceptions.AccessDeniedException import AccessDeniedException
from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
from museum_security.AccessControl import AccessControl
from museum_security.Incident import Incident


class TestAccessControlInit:
    def test_init_stores_fields(self, access_attempt, visitor_with_ticket):
        assert access_attempt.person is visitor_with_ticket
        assert access_attempt.zone == "public"

    def test_init_not_granted_yet(self, access_attempt):
        assert access_attempt.is_granted is False
        assert access_attempt.reason is None

    def test_init_records_time(self, access_attempt):
        assert access_attempt.time is not None

    def test_init_all_valid_zones(self, visitor):
        for z in ("public", "storage", "restoration", "admin", "cashier"):
            a = AccessControl(visitor, z)
            assert a.zone == z

    def test_init_none_person_raises(self):
        with pytest.raises(ValueError):
            AccessControl(None, "public")

    def test_init_unknown_zone_raises(self, visitor):
        with pytest.raises(ValueError):
            AccessControl(visitor, "basement")


class TestAccessControlPublicZone:
    def test_public_granted_with_valid_ticket(self, access_attempt):
        assert access_attempt.check_access() is True
        assert access_attempt.is_granted is True

    def test_public_denied_without_ticket(self, access_attempt_no_ticket):
        assert access_attempt_no_ticket.check_access() is False
        assert access_attempt_no_ticket.is_granted is False
        assert "No ticket" in access_attempt_no_ticket.reason

    def test_public_denied_with_invalid_ticket(self, visitor, adult_ticket_type):
        from museum_sales.Ticket import Ticket
        # ticket for yesterday is not valid today
        yesterday = date.today() - timedelta(days=1)
        ticket = Ticket(adult_ticket_type, yesterday)
        visitor.receive_ticket(ticket)
        attempt = AccessControl(visitor, AccessControl.ZONE_PUBLIC)
        assert attempt.check_access() is False
        assert "invalid" in attempt.reason.lower()

    def test_public_denied_with_used_ticket(self, visitor, adult_ticket_type):
        from museum_sales.Ticket import Ticket
        ticket = Ticket(adult_ticket_type, date.today())
        ticket.mark_used()
        visitor.receive_ticket(ticket)
        attempt = AccessControl(visitor, AccessControl.ZONE_PUBLIC)
        assert attempt.check_access() is False

    def test_denied_keeps_denial_reason(self, access_attempt_no_ticket):
        access_attempt_no_ticket.check_access()
        assert access_attempt_no_ticket.reason is not None
        assert access_attempt_no_ticket.reason != ""


class TestAccessControlRestrictedZone:
    def test_storage_allowed_for_curator(self, employee_curator):
        attempt = AccessControl(employee_curator, AccessControl.ZONE_STORAGE)
        assert attempt.check_access() is True

    def test_storage_allowed_for_restorer(self, employee_restorer):
        attempt = AccessControl(employee_restorer, AccessControl.ZONE_STORAGE)
        assert attempt.check_access() is True

    def test_storage_allowed_for_administrator(self, employee_administrator):
        attempt = AccessControl(employee_administrator, AccessControl.ZONE_STORAGE)
        assert attempt.check_access() is True

    def test_storage_denied_for_cashier(self, employee_cashier):
        attempt = AccessControl(employee_cashier, AccessControl.ZONE_STORAGE)
        assert attempt.check_access() is False
        assert "Cashier" in attempt.reason

    def test_restoration_allowed_for_restorer(self, employee_restorer):
        attempt = AccessControl(employee_restorer, AccessControl.ZONE_RESTORATION)
        assert attempt.check_access() is True

    def test_restoration_denied_for_curator(self, employee_curator):
        attempt = AccessControl(employee_curator, AccessControl.ZONE_RESTORATION)
        assert attempt.check_access() is False

    def test_admin_allowed_only_for_administrator(self, employee_administrator):
        attempt = AccessControl(employee_administrator, AccessControl.ZONE_ADMIN)
        assert attempt.check_access() is True

    def test_admin_denied_for_curator(self, employee_curator):
        attempt = AccessControl(employee_curator, AccessControl.ZONE_ADMIN)
        assert attempt.check_access() is False

    def test_cashier_zone_allowed_for_cashier(self, employee_cashier):
        attempt = AccessControl(employee_cashier, AccessControl.ZONE_CASHIER)
        assert attempt.check_access() is True

    def test_restricted_denied_for_non_employee(self, visitor):
        attempt = AccessControl(visitor, AccessControl.ZONE_STORAGE)
        assert attempt.check_access() is False
        assert "Not an employee" in attempt.reason


class TestAccessControlRequireAccess:
    def test_require_access_grants(self, access_attempt):
        assert access_attempt.require_access() is True

    def test_require_access_raises_on_denial(self, access_attempt_no_ticket):
        with pytest.raises(AccessDeniedException):
            access_attempt_no_ticket.require_access()

    def test_require_access_sets_state(self, access_attempt_no_ticket):
        with pytest.raises(AccessDeniedException):
            access_attempt_no_ticket.require_access()
        assert access_attempt_no_ticket.is_granted is False


class TestAccessControlLogging:
    def test_log_entry_granted(self, access_attempt):
        access_attempt.check_access()
        entry = access_attempt.log_entry()
        assert entry["granted"] is True
        assert entry["zone"] == "public"

    def test_log_entry_denied(self, access_attempt_no_ticket):
        access_attempt_no_ticket.check_access()
        entry = access_attempt_no_ticket.log_entry()
        assert entry["granted"] is False
        assert entry["reason"] is not None


class TestIncidentInit:
    def test_init_stores_fields(self, incident):
        assert incident.type == "theft"
        assert incident.place == "Hall 1"
        assert incident.severity == "high"

    def test_init_has_id(self, incident):
        assert incident.id.startswith("INC-")

    def test_init_ids_are_unique(self):
        i1 = Incident("theft", "A")
        i2 = Incident("theft", "B")
        assert i1.id != i2.id

    def test_init_not_closed(self, incident):
        assert incident.is_closed is False

    def test_init_no_guard(self, incident):
        assert incident.guard is None

    def test_init_no_evidence(self, incident):
        assert incident.evidence == []

    def test_init_no_related_exhibits(self, incident):
        assert incident.related_exhibits == []

    def test_init_all_valid_types(self):
        for t in ("theft", "vandalism", "fire", "flood", "medical", "other"):
            i = Incident(t, "A")
            assert i.type == t

    def test_init_all_valid_severities(self):
        for s in ("low", "medium", "high"):
            i = Incident("theft", "A", s)
            assert i.severity == s

    def test_init_default_severity(self):
        i = Incident("theft", "A")
        assert i.severity == "medium"

    def test_init_invalid_type_raises(self):
        with pytest.raises(ValueError):
            Incident("nuclear", "A")

    def test_init_empty_place_raises(self):
        with pytest.raises(ValueError):
            Incident("theft", "")

    def test_init_invalid_severity_raises(self):
        with pytest.raises(ValueError):
            Incident("theft", "A", "catastrophic")


class TestIncidentAssignGuard:
    def test_assign_success(self, incident, guard):
        result = incident.assign_guard(guard)
        assert result is True
        assert incident.guard is guard

    def test_assign_none_raises(self, incident):
        with pytest.raises(ValueError):
            incident.assign_guard(None)

    def test_assign_closed_raises(self, closed_incident):
        from museum_people.SecurityGuard import SecurityGuard
        other = SecurityGuard("X", 40000.0, date(2020, 1, 1), "day", "hall")
        with pytest.raises(InvalidExhibitStateException):
            closed_incident.assign_guard(other)


class TestIncidentAddEvidence:
    def test_add_success(self, incident):
        result = incident.add_evidence("Witness saw suspect")
        assert result is True
        assert "Witness saw suspect" in incident.evidence

    def test_add_empty_raises(self, incident):
        with pytest.raises(ValueError):
            incident.add_evidence("")

    def test_add_closed_raises(self, closed_incident):
        with pytest.raises(InvalidExhibitStateException):
            closed_incident.add_evidence("late evidence")


class TestIncidentLinkExhibit:
    def test_link_success(self, incident, exhibit):
        result = incident.link_exhibit(exhibit)
        assert result is True
        assert exhibit in incident.related_exhibits

    def test_link_same_exhibit_idempotent(self, incident, exhibit):
        incident.link_exhibit(exhibit)
        assert incident.link_exhibit(exhibit) is True
        assert len(incident.related_exhibits) == 1

    def test_link_none_raises(self, incident):
        with pytest.raises(ValueError):
            incident.link_exhibit(None)


class TestIncidentInvestigate:
    def test_investigate_requires_guard(self, incident):
        incident.add_evidence("some evidence")
        assert incident.investigate() is False

    def test_investigate_requires_evidence(self, incident_with_guard):
        assert incident_with_guard.investigate() is False

    def test_investigate_all_present(self, incident_with_evidence):
        assert incident_with_evidence.investigate() is True

    def test_investigate_closed_returns_false(self, closed_incident):
        assert closed_incident.investigate() is False


class TestIncidentCloseIncident:
    def test_close_success(self, incident_with_evidence):
        result = incident_with_evidence.close_incident()
        assert result is True
        assert incident_with_evidence.is_closed is True

    def test_close_no_guard_raises(self, incident):
        incident.add_evidence("some evidence")
        with pytest.raises(InvalidExhibitStateException):
            incident.close_incident()

    def test_close_no_evidence_raises(self, incident_with_guard):
        with pytest.raises(InvalidExhibitStateException):
            incident_with_guard.close_incident()

    def test_close_twice_raises(self, closed_incident):
        with pytest.raises(InvalidExhibitStateException):
            closed_incident.close_incident()


class TestIncidentEncapsulation:
    def test_evidence_returns_copy(self, incident):
        incident.add_evidence("x")
        ev = incident.evidence
        ev.append("fake")
        assert len(incident.evidence) == 1

    def test_related_exhibits_returns_copy(self, incident, exhibit):
        incident.link_exhibit(exhibit)
        rel = incident.related_exhibits
        rel.append("fake")
        assert len(incident.related_exhibits) == 1