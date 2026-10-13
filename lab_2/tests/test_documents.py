"""Tests for the museum_documents package.

Covers: Contract, InsurancePolicy, Acquisition, Inventory, Invoice,
Loan, Report, Restoration, StorageMoveAct. Sections are added as each
class is implemented.
"""
from datetime import date, timedelta

import pytest

from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class TestContractInit:
    def test_init_stores_fields(self, contract):
        assert contract.terms == "Loan agreement"
        assert contract.amount == 100000.0
        assert "Hermitage" in contract.parties
        assert "Louvre" in contract.parties

    def test_init_not_signed(self, contract):
        assert contract.is_signed is False
        assert contract.signed_date is None

    def test_init_no_permit(self, contract):
        assert contract.permit_number is None

    def test_init_empty_parties_allowed(self):
        from museum_documents.Contract import Contract
        c = Contract([], "Terms", 100.0)
        assert c.parties == []

    def test_init_empty_terms_raises(self):
        from museum_documents.Contract import Contract
        with pytest.raises(ValueError):
            Contract(["A"], "", 100.0)

    def test_init_negative_amount_raises(self):
        from museum_documents.Contract import Contract
        with pytest.raises(ValueError):
            Contract(["A"], "Terms", -1.0)


class TestContractAddParty:
    def test_add_success(self, contract):
        result = contract.add_party("Prado")
        assert result is True
        assert "Prado" in contract.parties

    def test_add_empty_raises(self, contract):
        with pytest.raises(ValueError):
            contract.add_party("")

    def test_add_duplicate_raises(self, contract):
        with pytest.raises(ValueError):
            contract.add_party("Hermitage")

    def test_add_to_signed_raises(self, signed_contract):
        with pytest.raises(InvalidExhibitStateException):
            signed_contract.add_party("New Party")


class TestContractSign:
    def test_sign_success(self, contract):
        result = contract.sign()
        assert result is True
        assert contract.is_signed is True
        assert contract.signed_date == date.today()

    def test_sign_no_parties_raises(self):
        from museum_documents.Contract import Contract
        c = Contract([], "Terms", 100.0)
        with pytest.raises(InvalidExhibitStateException):
            c.sign()

    def test_sign_twice_raises(self, signed_contract):
        with pytest.raises(InvalidExhibitStateException):
            signed_contract.sign()


class TestContractTerminate:
    def test_terminate_success(self, signed_contract):
        result = signed_contract.terminate()
        assert result is True
        assert signed_contract.is_signed is False

    def test_terminate_unsigned_raises(self, contract):
        with pytest.raises(InvalidExhibitStateException):
            contract.terminate()


class TestContractPermit:
    def test_issue_success(self, signed_contract):
        result = signed_contract.issue_permit("PERMIT-001")
        assert result is True
        assert signed_contract.permit_number == "PERMIT-001"

    def test_issue_empty_number_raises(self, signed_contract):
        with pytest.raises(ValueError):
            signed_contract.issue_permit("")

    def test_issue_unsigned_raises(self, contract):
        with pytest.raises(InvalidExhibitStateException):
            contract.issue_permit("PERMIT-001")

    def test_revoke_success(self, signed_contract):
        signed_contract.issue_permit("PERMIT-001")
        assert signed_contract.revoke_permit() is True
        assert signed_contract.permit_number is None

    def test_revoke_idempotent(self, signed_contract):
        assert signed_contract.revoke_permit() is True
        assert signed_contract.permit_number is None


class TestContractChangeAmount:
    def test_change_success(self, contract):
        result = contract.change_amount(200000.0)
        assert result is True
        assert contract.amount == 200000.0


    def test_change_negative_raises(self, contract):
        with pytest.raises(ValueError):
            contract.change_amount(-1.0)

    def test_change_signed_raises(self, signed_contract):
        with pytest.raises(InvalidExhibitStateException):
            signed_contract.change_amount(200000.0)


class TestInsurancePolicyInit:
    def test_init_stores_fields(self, insurance_policy, exhibit):
        assert insurance_policy.exhibit is exhibit
        assert insurance_policy.company == "Ingosstrakh"
        assert insurance_policy.amount == 5000.0
        assert insurance_policy.policy_number == "POL-001"

    def test_init_not_cancelled(self, insurance_policy):
        assert insurance_policy.is_cancelled is False

    def test_init_none_exhibit_raises(self):
        from museum_documents.InsurancePolicy import InsurancePolicy
        with pytest.raises(ValueError):
            InsurancePolicy(None, "Co", 1000.0, date.today(), "P1")

    def test_init_empty_company_raises(self, exhibit):
        from museum_documents.InsurancePolicy import InsurancePolicy
        with pytest.raises(ValueError):
            InsurancePolicy(exhibit, "", 1000.0, date.today(), "P1")

    def test_init_negative_amount_raises(self, exhibit):
        from museum_documents.InsurancePolicy import InsurancePolicy
        with pytest.raises(ValueError):
            InsurancePolicy(exhibit, "Co", -1.0, date.today(), "P1")

    def test_init_none_date_raises(self, exhibit):
        from museum_documents.InsurancePolicy import InsurancePolicy
        with pytest.raises(ValueError):
            InsurancePolicy(exhibit, "Co", 1000.0, None, "P1")

    def test_init_empty_number_raises(self, exhibit):
        from museum_documents.InsurancePolicy import InsurancePolicy
        with pytest.raises(ValueError):
            InsurancePolicy(exhibit, "Co", 1000.0, date.today(), "")


class TestInsurancePolicyInsureExhibit:
    def test_insure_success(self, insurance_policy, exhibit):
        result = insurance_policy.insure_exhibit()
        assert result is True
        assert exhibit.insurance_value == 5000.0
        assert exhibit.insurance_policy is insurance_policy

    def test_insure_cancelled_raises(self, insurance_policy):
        insurance_policy.cancel()
        with pytest.raises(InvalidExhibitStateException):
            insurance_policy.insure_exhibit()


class TestInsurancePolicyIsActive:
    def test_active_future(self, insurance_policy):
        assert insurance_policy.is_active() is True

    def test_active_today(self, exhibit):
        from museum_documents.InsurancePolicy import InsurancePolicy
        p = InsurancePolicy(exhibit, "Co", 1000.0, date.today(), "P1")
        assert p.is_active() is True

    def test_inactive_past(self, exhibit):
        from museum_documents.InsurancePolicy import InsurancePolicy
        p = InsurancePolicy(exhibit, "Co", 1000.0,
                            date.today() - timedelta(days=1), "P1")
        assert p.is_active() is False

    def test_inactive_cancelled(self, insurance_policy):
        insurance_policy.cancel()
        assert insurance_policy.is_active() is False


class TestInsurancePolicyRenew:
    def test_renew_active(self, insurance_policy):
        old = insurance_policy.valid_until
        insurance_policy.renew(6)
        assert insurance_policy.valid_until == old + timedelta(days=180)

    def test_renew_expired_from_today(self, exhibit):
        from museum_documents.InsurancePolicy import InsurancePolicy
        p = InsurancePolicy(exhibit, "Co", 1000.0,
                            date.today() - timedelta(days=10), "P1")
        p.renew(1)
        assert p.valid_until == date.today() + timedelta(days=30)

    def test_renew_zero_raises(self, insurance_policy):
        with pytest.raises(ValueError):
            insurance_policy.renew(0)

    def test_renew_negative_raises(self, insurance_policy):
        with pytest.raises(ValueError):
            insurance_policy.renew(-1)

    def test_renew_cancelled_raises(self, insurance_policy):
        insurance_policy.cancel()
        with pytest.raises(InvalidExhibitStateException):
            insurance_policy.renew(6)


class TestInsurancePolicyClaim:
    def test_claim_active(self, insurance_policy):
        assert insurance_policy.claim_insurance() is True

    def test_claim_expired_raises(self, exhibit):
        from museum_documents.InsurancePolicy import InsurancePolicy
        p = InsurancePolicy(exhibit, "Co", 1000.0,
                            date.today() - timedelta(days=1), "P1")
        with pytest.raises(InvalidExhibitStateException):
            p.claim_insurance()

    def test_claim_cancelled_raises(self, insurance_policy):
        insurance_policy.cancel()
        with pytest.raises(InvalidExhibitStateException):
            insurance_policy.claim_insurance()


class TestInsurancePolicyCancel:
    def test_cancel_success(self, insurance_policy):
        assert insurance_policy.cancel() is True
        assert insurance_policy.is_cancelled is True

    def test_cancel_idempotent(self, insurance_policy):
        insurance_policy.cancel()
        assert insurance_policy.cancel() is True


class TestAcquisitionInit:
    def test_init_stores_fields(self, acquisition):
        assert acquisition.source == "purchase"
        assert acquisition.price == 1000000.0

    def test_init_not_approved(self, acquisition):
        assert acquisition.is_approved is False

    def test_init_no_invoice(self, acquisition):
        assert acquisition.invoice is None

    def test_init_all_valid_sources(self, painting):
        from museum_documents.Acquisition import Acquisition
        for s in ("purchase", "gift", "find"):
            a = Acquisition(s, painting)
            assert a.source == s

    def test_init_invalid_source_raises(self, painting):
        from museum_documents.Acquisition import Acquisition
        with pytest.raises(ValueError):
            Acquisition("stolen", painting)

    def test_init_none_exhibit_raises(self):
        from museum_documents.Acquisition import Acquisition
        with pytest.raises(ValueError):
            Acquisition(Acquisition.SOURCE_GIFT, None)

    def test_init_negative_price_raises(self, painting):
        from museum_documents.Acquisition import Acquisition
        with pytest.raises(ValueError):
            Acquisition(Acquisition.SOURCE_PURCHASE, painting, price=-1.0)


class TestAcquisitionApprove:
    def test_approve_success(self, acquisition):
        assert acquisition.approve_acquisition() is True
        assert acquisition.is_approved is True

    def test_approve_twice_raises(self, acquisition):
        acquisition.approve_acquisition()
        with pytest.raises(InvalidExhibitStateException):
            acquisition.approve_acquisition()


class TestAcquisitionRegister:
    def test_register_success(self, acquisition):
        acquisition.approve_acquisition()
        assert acquisition.register_exhibit() is True
        assert acquisition.exhibit.acquired_date == acquisition.date

    def test_register_unapproved_raises(self, acquisition):
        with pytest.raises(InvalidExhibitStateException):
            acquisition.register_exhibit()


class TestAcquisitionCost:

    def test_set_price_success(self, acquisition):
        assert acquisition.set_price(2000000.0) is True
        assert acquisition.price == 2000000.0


    def test_set_price_negative_raises(self, acquisition):
        with pytest.raises(ValueError):
            acquisition.set_price(-1.0)

    def test_set_price_after_approved_raises(self, acquisition):
        acquisition.approve_acquisition()
        with pytest.raises(InvalidExhibitStateException):
            acquisition.set_price(999.0)


class TestAcquisitionAttachInvoice:
    def test_attach_success(self, acquisition):
        invoice = object()
        assert acquisition.attach_invoice(invoice) is True
        assert acquisition.invoice is invoice

    def test_attach_none_raises(self, acquisition):
        with pytest.raises(ValueError):
            acquisition.attach_invoice(None)


class TestInventoryInit:
    def test_init_stores_responsible(self, inventory, employee):
        assert inventory.responsible is employee

    def test_init_empty_scanned(self, inventory):
        assert inventory.scanned == []
        assert inventory.count_scanned() == 0

    def test_init_not_reconciled(self, inventory):
        assert inventory.is_reconciled is False

    def test_init_no_mismatches(self, inventory):
        assert inventory.mismatches == []

    def test_init_none_responsible_raises(self):
        from museum_documents.Inventory import Inventory
        with pytest.raises(ValueError):
            Inventory(None)


class TestInventoryScanExhibit:
    def test_scan_success(self, inventory, painting):
        assert inventory.scan_exhibit(painting) is True
        assert painting in inventory.scanned

    def test_scan_none_raises(self, inventory):
        with pytest.raises(ValueError):
            inventory.scan_exhibit(None)

    def test_scan_duplicate_raises(self, inventory, painting):
        inventory.scan_exhibit(painting)
        with pytest.raises(ValueError):
            inventory.scan_exhibit(painting)


class TestInventoryReconcile:
    def test_reconcile_clean(self, inventory, painting):
        inventory.scan_exhibit(painting)
        result = inventory.reconcile([painting])
        assert result is True
        assert inventory.is_reconciled is True
        assert inventory.is_clean() is True

    def test_reconcile_missing_exhibit(self, inventory, painting):
        # did not scan painting, but it's in catalog
        inventory.reconcile([painting])
        assert inventory.is_clean() is False
        assert painting in inventory.mismatches

    def test_reconcile_extra_exhibit(self, inventory, painting):
        inventory.scan_exhibit(painting)
        # catalog is empty
        inventory.reconcile([])
        assert inventory.is_clean() is False
        assert painting in inventory.mismatches

    def test_reconcile_twice_raises(self, inventory):
        inventory.reconcile([])
        with pytest.raises(InvalidExhibitStateException):
            inventory.reconcile([])

    def test_reconcile_none_raises(self, inventory):
        with pytest.raises(ValueError):
            inventory.reconcile(None)


class TestInventoryIsClean:
    def test_not_clean_before_reconcile(self, inventory):
        assert inventory.is_clean() is False

    def test_clean_after_matching(self, inventory, painting):
        inventory.scan_exhibit(painting)
        inventory.reconcile([painting])
        assert inventory.is_clean() is True


class TestInventoryGenerateReport:
    def test_generate_report(self, inventory, painting, report_module_stub):
        inventory.scan_exhibit(painting)
        inventory.reconcile([painting])
        report = inventory.generate_report()
        assert report is not None
        assert report.type == "inventory"
        assert report.data["scanned"] == 1
        assert report.data["is_clean"] is True


class TestLoanInit:
    def test_init_stores_fields(self, loan, exhibit):
        assert loan.exhibit is exhibit
        assert loan.borrower == "Louvre"
        assert loan.start_date == date.today()
        assert loan.end_date == date.today() + timedelta(days=30)

    def test_init_status_pending(self, loan):
        assert loan.status == "pending"
        assert loan.is_active is False
        assert loan.is_returned is False

    def test_init_no_return_info(self, loan):
        assert loan.return_condition is None
        assert loan.returned_date is None

    def test_init_none_exhibit_raises(self):
        from museum_documents.Loan import Loan
        with pytest.raises(ValueError):
            Loan(None, "X", date.today(), date.today() + timedelta(days=30))

    def test_init_empty_borrower_raises(self, exhibit):
        from museum_documents.Loan import Loan
        with pytest.raises(ValueError):
            Loan(exhibit, "", date.today(), date.today() + timedelta(days=30))

    def test_init_none_start_raises(self, exhibit):
        from museum_documents.Loan import Loan
        with pytest.raises(ValueError):
            Loan(exhibit, "X", None, date.today() + timedelta(days=30))

    def test_init_none_end_raises(self, exhibit):
        from museum_documents.Loan import Loan
        with pytest.raises(ValueError):
            Loan(exhibit, "X", date.today(), None)

    def test_init_end_before_start_raises(self, exhibit):
        from museum_documents.Loan import Loan
        with pytest.raises(ValueError):
            Loan(exhibit, "X", date.today(), date.today() - timedelta(days=1))


class TestLoanApprove:
    def test_approve_success(self, loan):
        assert loan.approve_loan() is True
        assert loan.status == "approved"
        assert loan.is_active is True

    def test_approve_twice_raises(self, approved_loan):
        with pytest.raises(InvalidExhibitStateException):
            approved_loan.approve_loan()

    def test_approve_critical_exhibit_raises(self, exhibit_critical):
        from museum_documents.Loan import Loan
        l = Loan(exhibit_critical, "X", date.today(),
                 date.today() + timedelta(days=30))
        with pytest.raises(InvalidExhibitStateException):
            l.approve_loan()


class TestLoanReturn:
    def test_return_success(self, approved_loan):
        assert approved_loan.return_exhibit() is True
        assert approved_loan.status == "returned"
        assert approved_loan.is_returned is True
        assert approved_loan.returned_date == date.today()

    def test_return_pending_raises(self, loan):
        with pytest.raises(InvalidExhibitStateException):
            loan.return_exhibit()

    def test_return_twice_raises(self, approved_loan):
        approved_loan.return_exhibit()
        with pytest.raises(InvalidExhibitStateException):
            approved_loan.return_exhibit()


class TestLoanRegisterReturn:
    def test_register_success(self, approved_loan):
        approved_loan.return_exhibit()
        assert approved_loan.register_return("excellent") is True
        assert approved_loan.return_condition == "excellent"

    def test_register_empty_raises(self, approved_loan):
        approved_loan.return_exhibit()
        with pytest.raises(ValueError):
            approved_loan.register_return("")

    def test_register_before_return_raises(self, approved_loan):
        with pytest.raises(InvalidExhibitStateException):
            approved_loan.register_return("excellent")


class TestLoanExtend:
    def test_extend_success(self, approved_loan):
        new_end = approved_loan.end_date + timedelta(days=30)
        assert approved_loan.extend_loan(new_end) is True
        assert approved_loan.end_date == new_end

    def test_extend_none_raises(self, approved_loan):
        with pytest.raises(ValueError):
            approved_loan.extend_loan(None)

    def test_extend_same_or_earlier_raises(self, approved_loan):
        with pytest.raises(ValueError):
            approved_loan.extend_loan(approved_loan.end_date)
        with pytest.raises(ValueError):
            approved_loan.extend_loan(approved_loan.end_date - timedelta(days=1))

    def test_extend_returned_raises(self, approved_loan):
        approved_loan.return_exhibit()
        with pytest.raises(InvalidExhibitStateException):
            approved_loan.extend_loan(approved_loan.end_date + timedelta(days=30))


class TestLoanOverdue:
    def test_is_overdue_false_pending(self, loan):
        assert loan.is_overdue() is False

    def test_is_overdue_false_approved_future(self, approved_loan):
        assert approved_loan.is_overdue() is False

    def test_is_overdue_true(self, overdue_loan):
        assert overdue_loan.is_overdue() is True

    def test_is_overdue_false_returned(self, approved_loan):
        approved_loan.return_exhibit()
        assert approved_loan.is_overdue() is False


class TestRestorationInit:
    def test_init_stores_fields(self, restoration, exhibit_damaged, restorer):
        assert restoration.exhibit is exhibit_damaged
        assert restoration.restorer is restorer

    def test_init_status_pending(self, restoration):
        assert restoration.status == "pending"
        assert restoration.is_completed is False
        assert restoration.is_in_progress is False

    def test_init_no_dates(self, restoration):
        assert restoration.start_date is None
        assert restoration.end_date is None

    def test_init_cost_zero(self, restoration):
        assert restoration.cost == 0.0

    def test_init_none_exhibit_raises(self, restorer):
        from museum_documents.Restoration import Restoration
        with pytest.raises(ValueError):
            Restoration(None, restorer)

    def test_init_none_restorer_raises(self, exhibit_damaged):
        from museum_documents.Restoration import Restoration
        with pytest.raises(ValueError):
            Restoration(exhibit_damaged, None)


class TestRestorationStart:
    def test_start_success(self, restoration):
        assert restoration.start_restoration() is True
        assert restoration.is_in_progress is True
        assert restoration.start_date == date.today()
        assert restoration.cost > 0

    def test_start_healthy_exhibit_raises(self, restorer, exhibit):
        from museum_documents.Restoration import Restoration
        r = Restoration(exhibit, restorer)
        with pytest.raises(InvalidExhibitStateException):
            r.start_restoration()

    def test_start_twice_raises(self, restoration):
        restoration.start_restoration()
        with pytest.raises(InvalidExhibitStateException):
            restoration.start_restoration()


class TestRestorationComplete:
    def test_complete_success(self, restoration, exhibit_damaged):
        restoration.start_restoration()
        assert restoration.complete_restoration() is True
        assert restoration.is_completed is True
        assert restoration.end_date == date.today()

    def test_complete_changes_exhibit_condition(self, restoration, exhibit_damaged):
        restoration.start_restoration()
        restoration.complete_restoration()
        assert exhibit_damaged.condition == "good"

    def test_complete_without_start_raises(self, restoration):
        with pytest.raises(InvalidExhibitStateException):
            restoration.complete_restoration()


class TestRestorationReport:
    def test_write_report_success(self, restoration, report_module_stub):
        restoration.start_restoration()
        restoration.complete_restoration()
        report = restoration.write_report()
        assert report is not None
        assert report.type == "restoration"
        assert restoration.report is report

    def test_write_report_incomplete_raises(self, restoration):
        with pytest.raises(InvalidExhibitStateException):
            restoration.write_report()


class TestRestorationDuration:
    def test_duration_zero_when_incomplete(self, restoration):
        assert restoration.calculate_duration() == 0

    def test_duration_same_day(self, restoration):
        restoration.start_restoration()
        restoration.complete_restoration()
        assert restoration.calculate_duration() == 0


class TestRestorationSetCost:
    def test_set_cost_success(self, restoration):
        assert restoration.set_cost(500.0) is True
        assert restoration.cost == 500.0

    def test_set_cost_zero_allowed(self, restoration):
        restoration.set_cost(0.0)
        assert restoration.cost == 0.0

    def test_set_cost_negative_raises(self, restoration):
        with pytest.raises(ValueError):
            restoration.set_cost(-1.0)

    def test_set_cost_after_start_raises(self, restoration):
        restoration.start_restoration()
        with pytest.raises(InvalidExhibitStateException):
            restoration.set_cost(500.0)


class TestInvoiceInit:
    def test_init_stores_fields(self, invoice):
        assert invoice.amount == 1000.0
        assert invoice.payer == "Hermitage"
        assert invoice.number.startswith("INV-")

    def test_init_status_issued(self, invoice):
        assert invoice.status == "issued"
        assert invoice.is_paid is False
        assert invoice.is_cancelled is False

    def test_init_issued_date_today(self, invoice):
        assert invoice.issued_date == date.today()

    def test_init_no_paid_date(self, invoice):
        assert invoice.paid_date is None
        assert invoice.payment is None

    def test_init_ids_unique(self):
        from museum_documents.Invoice import Invoice
        i1 = Invoice(100.0, "A")
        i2 = Invoice(200.0, "B")
        assert i1.number != i2.number

    def test_init_zero_amount_raises(self):
        from museum_documents.Invoice import Invoice
        with pytest.raises(ValueError):
            Invoice(0.0, "A")

    def test_init_negative_amount_raises(self):
        from museum_documents.Invoice import Invoice
        with pytest.raises(ValueError):
            Invoice(-100.0, "A")

    def test_init_empty_payer_raises(self):
        from museum_documents.Invoice import Invoice
        with pytest.raises(ValueError):
            Invoice(100.0, "")


class TestInvoicePay:
    def test_pay_success(self, invoice):
        from museum_sales.Payment import Payment
        payment = Payment(1000.0, Payment.METHOD_CARD)
        assert invoice.pay(payment) is True
        assert invoice.is_paid is True
        assert invoice.paid_date == date.today()
        assert invoice.payment is payment

    def test_pay_none_raises(self, invoice):
        with pytest.raises(ValueError):
            invoice.pay(None)

    def test_pay_amount_mismatch_raises(self, invoice):
        from museum_sales.Payment import Payment
        with pytest.raises(ValueError):
            invoice.pay(Payment(500.0, Payment.METHOD_CARD))

    def test_pay_twice_raises(self, paid_invoice):
        from museum_sales.Payment import Payment
        with pytest.raises(InvalidExhibitStateException):
            paid_invoice.pay(Payment(1000.0, Payment.METHOD_CARD))

    def test_pay_cancelled_raises(self, invoice):
        from museum_sales.Payment import Payment
        invoice.cancel()
        with pytest.raises(InvalidExhibitStateException):
            invoice.pay(Payment(1000.0, Payment.METHOD_CARD))


class TestInvoiceCancel:
    def test_cancel_success(self, invoice):
        assert invoice.cancel() is True
        assert invoice.is_cancelled is True

    def test_cancel_twice_raises(self, invoice):
        invoice.cancel()
        with pytest.raises(InvalidExhibitStateException):
            invoice.cancel()

    def test_cancel_paid_raises(self, paid_invoice):
        with pytest.raises(InvalidExhibitStateException):
            paid_invoice.cancel()


class TestInvoiceChangeAmount:
    def test_change_success(self, invoice):
        assert invoice.change_amount(2000.0) is True
        assert invoice.amount == 2000.0

    def test_change_zero_raises(self, invoice):
        with pytest.raises(ValueError):
            invoice.change_amount(0.0)

    def test_change_negative_raises(self, invoice):
        with pytest.raises(ValueError):
            invoice.change_amount(-100.0)

    def test_change_paid_raises(self, paid_invoice):
        with pytest.raises(InvalidExhibitStateException):
            paid_invoice.change_amount(2000.0)


class TestReportInit:
    def test_init_stores_fields(self, report):
        assert report.period == "2025"
        assert report.type == "annual"
        assert report.id.startswith("REP-")

    def test_init_data_empty(self, report):
        assert report.data == {}
        assert report.is_empty() is True

    def test_init_no_author(self, report):
        assert report.author is None

    def test_init_empty_period_raises(self):
        from museum_documents.Report import Report
        with pytest.raises(ValueError):
            Report("", "annual")

    def test_init_invalid_type_raises(self):
        from museum_documents.Report import Report
        with pytest.raises(ValueError):
            Report("2025", "gossip")


class TestReportAuthor:
    def test_set_author_success(self, report, employee):
        assert report.set_author(employee) is True
        assert report.author is employee

    def test_set_author_none_raises(self, report):
        with pytest.raises(ValueError):
            report.set_author(None)


class TestReportGenerate:
    def test_generate_success(self, report):
        assert report.generate({"total": 100}) is True
        assert report.data["total"] == 100

    def test_generate_updates_existing(self, report):
        report.generate({"a": 1})
        report.generate({"b": 2})
        assert report.data == {"a": 1, "b": 2}

    def test_generate_overwrites(self, report):
        report.generate({"a": 1})
        report.generate({"a": 2})
        assert report.data["a"] == 2

    def test_generate_non_dict_raises(self, report):
        with pytest.raises(TypeError):
            report.generate([("a", 1)])

    def test_generate_none_raises(self, report):
        with pytest.raises(TypeError):
            report.generate(None)


class TestReportAddSection:
    def test_add_success(self, report):
        assert report.add_section("count", 5) is True
        assert report.data["count"] == 5

    def test_add_empty_key_raises(self, report):
        with pytest.raises(ValueError):
            report.add_section("", 5)


class TestReportExport:
    def test_export_pdf(self, report):
        report.generate({"a": 1})
        text = report.export("pdf")
        assert "[pdf]" in text
        assert report.id in text


    def test_export_invalid_raises(self, report):
        with pytest.raises(ValueError):
            report.export("docx")


class TestReportToString:
    def test_to_string_contains_info(self, report):
        text = report.to_string()
        assert report.id in text
        assert "annual" in text


class TestStorageMoveActInit:
    def test_init_stores_fields(self, move_act, painting):
        assert move_act.exhibit is painting
        assert move_act.from_storage.name == "Storage A"
        assert move_act.to_storage.name == "Storage B"

    def test_init_not_confirmed(self, move_act):
        assert move_act.is_confirmed is False

    def test_init_none_exhibit_raises(self):
        from museum_core.Storage import Storage
        from museum_documents.StorageMoveAct import StorageMoveAct
        from museum_people.Employee import Employee
        s1 = Storage("A", 10)
        s2 = Storage("B", 10)
        e = Employee("I", 50000.0, date(2020, 1, 1))
        with pytest.raises(ValueError):
            StorageMoveAct(None, s1, s2, e)

    def test_init_none_storages_raises(self, painting):
        from museum_core.Storage import Storage
        from museum_documents.StorageMoveAct import StorageMoveAct
        from museum_people.Employee import Employee
        s = Storage("A", 10)
        e = Employee("I", 50000.0, date(2020, 1, 1))
        with pytest.raises(ValueError):
            StorageMoveAct(painting, None, s, e)
        with pytest.raises(ValueError):
            StorageMoveAct(painting, s, None, e)

    def test_init_same_storages_raises(self, painting):
        from museum_core.Storage import Storage
        from museum_documents.StorageMoveAct import StorageMoveAct
        from museum_people.Employee import Employee
        s = Storage("A", 10)
        e = Employee("I", 50000.0, date(2020, 1, 1))
        with pytest.raises(ValueError):
            StorageMoveAct(painting, s, s, e)

    def test_init_none_responsible_raises(self, painting):
        from museum_core.Storage import Storage
        from museum_documents.StorageMoveAct import StorageMoveAct
        s1 = Storage("A", 10)
        s2 = Storage("B", 10)
        with pytest.raises(ValueError):
            StorageMoveAct(painting, s1, s2, None)


class TestStorageMoveActCreate:
    def test_create_success(self, move_act):
        assert move_act.create() is True

    def test_create_exhibit_not_in_source_raises(self, painting):
        from museum_core.Storage import Storage
        from museum_documents.StorageMoveAct import StorageMoveAct
        from museum_people.Employee import Employee
        s1 = Storage("A", 10)
        s2 = Storage("B", 10)
        e = Employee("I", 50000.0, date(2020, 1, 1))
        # painting NOT placed in s1
        act = StorageMoveAct(painting, s1, s2, e)
        with pytest.raises(InvalidExhibitStateException):
            act.create()


class TestStorageMoveActConfirm:
    def test_confirm_success(self, move_act):
        assert move_act.confirm() is True
        assert move_act.is_confirmed is True

    def test_confirm_idempotent(self, move_act):
        move_act.confirm()
        assert move_act.confirm() is True

    def test_confirm_when_exhibit_missing_raises(self, painting):
        from museum_core.Storage import Storage
        from museum_documents.StorageMoveAct import StorageMoveAct
        from museum_people.Employee import Employee
        s1 = Storage("A", 10)
        s2 = Storage("B", 10)
        e = Employee("I", 50000.0, date(2020, 1, 1))
        act = StorageMoveAct(painting, s1, s2, e)
        with pytest.raises(InvalidExhibitStateException):
            act.confirm()


class TestStorageMoveActRegister:
    def test_register_success(self, move_act, painting):
        move_act.confirm()
        assert move_act.register_movement() is True
        assert not move_act.from_storage.has_exhibit(painting)
        assert move_act.to_storage.has_exhibit(painting)

    def test_register_updates_exhibit_location(self, move_act, painting):
        move_act.confirm()
        move_act.register_movement()
        assert painting.location is move_act.to_storage

    def test_register_without_confirm_raises(self, move_act):
        with pytest.raises(InvalidExhibitStateException):
            move_act.register_movement()


class TestStorageMoveActCancel:
    def test_cancel_success(self, move_act):
        move_act.cancel()
        assert move_act.is_confirmed is False

    def test_cancel_idempotent(self, move_act):
        assert move_act.cancel() is True
        assert move_act.is_confirmed is False