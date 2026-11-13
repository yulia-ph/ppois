import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_cargo.Container import Container
from logistics_cargo.Package import Package
from logistics_cargo.Pallet import Pallet


class TestPackage:
    def test_package_pallet_container(self, cargo):
        pkg = Package(cargo, 0.5)
        pkg.seal()
        assert pkg.scan().startswith("PKG-")
        assert not pkg.is_oversize()
        pkg.unseal()
        pallet = Pallet("P1", 500)
        pkg2 = Package(cargo, 2.0)
        assert pkg2.is_oversize()
        pallet.add_package(pkg)
        pallet.wrap()
        pallet.unwrap()
        pallet.wrap()
        container = Container("ISO-1", 1000)
        container.load_pallet(pallet)
        container.seal("S-1")
        assert container.inspect()
        container._is_sealed = False
        container.unload_pallet(pallet)

    def test_package_errors(self, cargo):
        with pytest.raises(ValueError):
            Package(None, 1)
        with pytest.raises(ValueError):
            Package(cargo, 0)
        p = Package(cargo, 1)
        with pytest.raises(InvalidCargoStateException):
            p.unseal()
        p.seal()
        with pytest.raises(InvalidCargoStateException):
            p.seal()
