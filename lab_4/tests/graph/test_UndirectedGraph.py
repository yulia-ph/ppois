from typing import get_args, get_origin

import pytest

from exceptions.DuplicateEdgeException import DuplicateEdgeException
from exceptions.DuplicateVertexException import DuplicateVertexException
from exceptions.EdgeNotFoundException import EdgeNotFoundException
from exceptions.InvalidIteratorException import InvalidIteratorException
from exceptions.VertexNotFoundException import VertexNotFoundException
from graph.UndirectedGraph import UndirectedGraph


def test_generic_vertex_type():
    graph = UndirectedGraph[str]()
    graph.add_vertex("Minsk")
    assert graph.has_vertex("Minsk")
    assert get_origin(UndirectedGraph[str]) is UndirectedGraph
    assert get_args(UndirectedGraph[str]) == (str,)


def test_empty_clear_copy(triangle):
    empty = UndirectedGraph()
    assert empty.empty()
    assert empty.is_empty()
    assert empty.vertex_count() == 0
    assert empty.edge_count() == 0
    triangle.clear()
    assert triangle.empty()
    other = UndirectedGraph()
    other.add_vertex("X")
    empty.assign_from(other)
    assert empty.has_vertex("X")
    with pytest.raises(ValueError):
        empty.assign_from(None)


def test_add_and_lookup(triangle):
    assert triangle.has_vertex("A")
    assert triangle.has_edge("A", "B")
    assert triangle.has_edge("B", "A")
    assert not triangle.has_edge("A", "A")
    assert triangle.vertex_count() == 3
    assert triangle.edge_count() == 3
    assert triangle.vertex_degree("A") == 2
    assert triangle.edge_degree("A", "B") == 2


def test_duplicates_and_missing():
    graph = UndirectedGraph()
    graph.add_vertex("A")
    with pytest.raises(DuplicateVertexException):
        graph.add_vertex("A")
    with pytest.raises(VertexNotFoundException):
        graph.add_edge("A", "B")
    graph.add_vertex("B")
    graph.add_edge("A", "B")
    with pytest.raises(DuplicateEdgeException):
        graph.add_edge("B", "A")
    with pytest.raises(VertexNotFoundException):
        graph.remove_vertex("Z")
    with pytest.raises(EdgeNotFoundException):
        graph.remove_edge("A", "A")
    with pytest.raises(EdgeNotFoundException):
        graph.edge_degree("A", "A")
    assert not graph.has_edge("A", "Z")
    graph.remove_edge("A", "B")
    assert not graph.has_edge("A", "B")


def test_remove_middle_vertex_rewrites_later_edges():
    graph = UndirectedGraph()
    for name in ("A", "B", "C", "D"):
        graph.add_vertex(name)
    graph.add_edge("A", "B")
    graph.add_edge("C", "D")
    graph.remove_vertex("B")
    assert graph.has_edge("C", "D")
    assert not graph.has_vertex("B")


def test_remove_vertex_drops_edges(triangle):
    triangle.remove_vertex("B")
    assert not triangle.has_vertex("B")
    assert not triangle.has_edge("A", "B")
    assert triangle.has_edge("C", "A")
    assert triangle.vertex_count() == 2
    assert triangle.edge_count() == 1


def test_loop_edge_degree():
    graph = UndirectedGraph()
    graph.add_vertex("A")
    graph.add_edge("A", "A")
    assert graph.edge_degree("A", "A") == 1
    assert graph.vertex_degree("A") == 2


def test_copy_and_compare(triangle):
    clone = triangle.copy()
    same = triangle.copy()
    assert clone == triangle
    assert (same != triangle) is False
    clone.add_vertex("D")
    assert clone != triangle
    assert triangle < clone
    assert clone > triangle
    assert triangle <= clone
    assert clone >= triangle
    assert same <= triangle
    assert same >= triangle
    text = str(triangle)
    assert "A" in text
    assert "A--B" in text or "B--A" in text


def test_compare_not_implemented(triangle):
    assert triangle.__eq__("x") is NotImplemented
    assert triangle.__ne__("x") is NotImplemented
    assert triangle.__lt__("x") is NotImplemented
    assert triangle.__le__("x") is NotImplemented
    assert triangle.__gt__("x") is NotImplemented
    assert triangle.__ge__("x") is NotImplemented


def test_remove_by_iterator(triangle):
    vertex_it = triangle.vertices()
    vertex_it.next()
    triangle.remove_vertex_at(vertex_it)
    assert not triangle.has_vertex("A")
    edge_it = triangle.edges()
    edge_it.next()
    triangle.remove_edge_at(edge_it)
    assert triangle.edge_count() == 0
    const_it = triangle.const_vertices()
    const_it.next()
    with pytest.raises(InvalidIteratorException):
        triangle.remove_vertex_at(const_it)
