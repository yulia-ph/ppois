import pytest

from logistics_core.Dock import Dock
from logistics_core.Terminal import Terminal


class TestTerminal:
    def test_terminal_flow(self, address, truck):
        terminal = Terminal("North", address)
        dock = Dock(1, 20.0, terminal)
        terminal.add_dock(dock)
        with pytest.raises(ValueError):
            terminal.assign_dock(truck)
        terminal.open_terminal()
        assigned = terminal.assign_dock(truck)
        assert assigned is dock
        assert terminal.count_free_docks() == 0
        terminal.close_terminal()
        assert not terminal.is_open

    def test_terminal_validation(self, address, truck):
        with pytest.raises(ValueError):
            Terminal("", address)
        with pytest.raises(ValueError):
            Terminal("T", None)
        t = Terminal("T", address)
        t.open_terminal()
        with pytest.raises(ValueError):
            t.add_dock(None)
        d = Dock(1, 20)
        t.add_dock(d)
        with pytest.raises(ValueError):
            t.add_dock(d)
        d.occupy(truck)
        with pytest.raises(ValueError):
            t.assign_dock(truck)
