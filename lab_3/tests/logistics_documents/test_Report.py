import pytest

from logistics_documents.Report import Report


class TestReport:
    def test_report(self):
        r = Report("2026-Q4", Report.TYPE_FINANCIAL)
        r.set_author("Ivanov")
        r.generate({"revenue": 10})
        r.add_section("notes", "ok")
        assert "FINANCIAL" in r.export("txt") or "txt" in r.export("txt").lower()
        text = r.to_string()
        assert r.id in text
        with pytest.raises(ValueError):
            Report("", Report.TYPE_ANNUAL)
        with pytest.raises(ValueError):
            Report("p", "nope")
        with pytest.raises(ValueError):
            r.set_author("")
        with pytest.raises(ValueError):
            r.generate(None)
        with pytest.raises(ValueError):
            r.add_section("", 1)
        with pytest.raises(ValueError):
            r.export("doc")
