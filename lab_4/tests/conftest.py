import pytest

from graph.UndirectedGraph import UndirectedGraph
from sorting.Parcel import Parcel


@pytest.fixture
def parcels():
    return [
        Parcel("Warsaw", 12),
        Parcel("Minsk", 4),
        Parcel("Grodno", 9),
    ]


@pytest.fixture
def triangle():
    graph = UndirectedGraph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "A")
    return graph
