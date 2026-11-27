import pytest

from exceptions.InvalidIteratorException import InvalidIteratorException
from graph.BidirectionalIterator import BidirectionalIterator
from graph.UndirectedGraph import UndirectedGraph


def test_forward_and_prev():
    it = BidirectionalIterator(["A", "B", "C"])
    with pytest.raises(InvalidIteratorException):
        it.get()
    assert it.next() == "A"
    assert it.next() == "B"
    assert it.prev() == "A"
    assert it.next() == "B"
    assert it.next() == "C"
    with pytest.raises(StopIteration):
        it.next()
    with pytest.raises(InvalidIteratorException):
        it.get()


def test_reverse_walk():
    it = BidirectionalIterator(["A", "B", "C"], reverse=True)
    assert it.is_reverse
    assert list(it) == ["C", "B", "A"]
    rev = BidirectionalIterator(["A", "B"], reverse=True)
    assert rev.next() == "B"
    assert rev.next() == "A"
    assert rev.prev() == "B"
    with pytest.raises(StopIteration):
        rev.prev()


def test_has_next_prev_and_const():
    it = BidirectionalIterator([1, 2], const=True)
    assert it.is_const
    assert it.has_next()
    assert not it.has_prev()
    it.next()
    assert it.has_next()
    assert not it.has_prev()
    it.next()
    assert not it.has_next()
    assert it.has_prev()
    it.prev()
    assert it.get() == 1
    rev = BidirectionalIterator([1, 2], reverse=True)
    assert rev.has_next()
    assert not rev.has_prev()
    rev.next()
    assert rev.has_next()
    assert not rev.has_prev()
    rev.next()
    assert not rev.has_next()
    assert rev.has_prev()


def test_graph_iterators(triangle):
    assert list(triangle.vertices()) == ["A", "B", "C"]
    assert list(triangle.reverse_vertices()) == ["C", "B", "A"]
    assert list(triangle.const_vertices()) == ["A", "B", "C"]
    edges = list(triangle.edges())
    assert ("A", "B") in edges
    assert list(triangle.reverse_edges()) == list(reversed(edges))
    assert list(triangle.const_edges()) == edges
    incident = list(triangle.incident_edges("B"))
    assert ("A", "B") in incident
    assert ("B", "C") in incident
    assert list(triangle.reverse_incident_edges("B")) == list(reversed(incident))
    assert list(triangle.const_incident_edges("B")) == incident
    neighbors = list(triangle.adjacent_vertices("B"))
    assert set(neighbors) == {"A", "C"}
    assert list(triangle.reverse_adjacent_vertices("B")) == list(reversed(neighbors))
    assert list(triangle.const_adjacent_vertices("B")) == neighbors


def test_prev_at_start_stops():
    it = BidirectionalIterator([1, 2])
    with pytest.raises(StopIteration):
        it.prev()
    rev = BidirectionalIterator([1, 2], reverse=True)
    rev.next()
    rev.next()
    with pytest.raises(StopIteration):
        rev.next()


def test_empty_iterator():
    it = BidirectionalIterator([])
    assert not it.has_next()
    with pytest.raises(StopIteration):
        it.next()
    graph = UndirectedGraph()
    assert list(graph.vertices()) == []
    assert str(graph).startswith("UndirectedGraph")
