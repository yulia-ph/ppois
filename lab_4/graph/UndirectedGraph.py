from typing import Generic, TypeVar

from exceptions.DuplicateEdgeException import DuplicateEdgeException
from exceptions.DuplicateVertexException import DuplicateVertexException
from exceptions.EdgeNotFoundException import EdgeNotFoundException
from exceptions.InvalidIteratorException import InvalidIteratorException
from exceptions.VertexNotFoundException import VertexNotFoundException
from graph.BidirectionalIterator import BidirectionalIterator

T = TypeVar("T")


class UndirectedGraph(Generic[T]):  # noqa: UP046
    """Undirected graph stored as ordered vertex and edge lists.

    ``T`` is the vertex value type. Edges are unique unordered pairs,
    kept sorted by vertex index. The adjacency structure is private.
    """

    def __init__(self):
        self._vertices: list[T] = []
        self._edges: list[tuple[int, int]] = []

    def empty(self) -> bool:
        """Return True if the graph has no vertices."""
        return not self._vertices

    def is_empty(self) -> bool:
        """Alias for empty()."""
        return self.empty()

    def clear(self):
        """Remove all vertices and edges."""
        self._vertices = []
        self._edges = []
        return True

    def copy(self) -> UndirectedGraph[T]:
        """Return a deep-enough copy: new lists, same vertex values."""
        clone: UndirectedGraph[T] = UndirectedGraph()
        clone._vertices = list(self._vertices)
        clone._edges = list(self._edges)
        return clone

    def assign_from(self, other: UndirectedGraph[T]):
        """Replace this graph's state with a copy of ``other``."""
        if other is None:
            raise ValueError("Other graph must not be None")
        self._vertices = list(other._vertices)
        self._edges = list(other._edges)
        return True

    def vertex_count(self) -> int:
        return len(self._vertices)

    def edge_count(self) -> int:
        return len(self._edges)

    def has_vertex(self, vertex: T) -> bool:
        return vertex in self._vertices

    def has_edge(self, start: T, end: T) -> bool:
        """Return True if the undirected edge exists.

        Missing vertices yield False, unlike ``edge_degree`` which raises.
        """
        try:
            pair = self._canonical_pair(start, end)
        except VertexNotFoundException:
            return False
        return pair in self._edges

    def add_vertex(self, vertex: T):
        if vertex in self._vertices:
            raise DuplicateVertexException(vertex)
        self._vertices.append(vertex)
        return True

    def add_edge(self, start: T, end: T):
        """Add an undirected edge. ``A--B`` is the same as ``B--A``. Loops are allowed."""
        pair = self._canonical_pair(start, end)
        if pair in self._edges:
            raise DuplicateEdgeException(start, end)
        self._edges.append(pair)
        self._edges.sort()
        return True

    def remove_vertex(self, vertex: T):
        """Remove a vertex, drop its incident edges, and remap later edge indices."""
        index = self._index_of(vertex)
        self._vertices.pop(index)
        kept = []
        for left, right in self._edges:
            if left == index or right == index:
                continue
            kept.append(self._shift_pair(left, right, index))
        kept.sort()
        self._edges = kept
        return True

    def remove_edge(self, start: T, end: T):
        pair = self._canonical_pair(start, end)
        if pair not in self._edges:
            raise EdgeNotFoundException(start, end)
        self._edges.remove(pair)
        return True

    def vertex_degree(self, vertex: T) -> int:
        """Number of incident edge ends. A loop contributes 2."""
        index = self._index_of(vertex)
        degree = 0
        for left, right in self._edges:
            if left == index and right == index:
                degree += 2
            elif left == index or right == index:
                degree += 1
        return degree

    def edge_degree(self, start: T, end: T) -> int:
        """1 for a loop, 2 for an ordinary undirected edge."""
        pair = self._canonical_pair(start, end)
        if pair not in self._edges:
            raise EdgeNotFoundException(start, end)
        if pair[0] == pair[1]:
            return 1
        return 2

    def vertices(self, *, reverse: bool = False, const: bool = False) -> BidirectionalIterator[T]:
        """Bidirectional iterator over vertices. ``reverse`` and ``const`` match the named wrappers."""
        return BidirectionalIterator(self._vertices, reverse=reverse, const=const)

    def reverse_vertices(self):
        return self.vertices(reverse=True)

    def const_vertices(self):
        return self.vertices(const=True)

    def edges(
        self, *, reverse: bool = False, const: bool = False
    ) -> BidirectionalIterator[tuple[T, T]]:
        """Bidirectional iterator over edges as ``(start, end)`` value pairs."""
        return BidirectionalIterator(self._edge_values(), reverse=reverse, const=const)

    def reverse_edges(self):
        return self.edges(reverse=True)

    def const_edges(self):
        return self.edges(const=True)

    def incident_edges(
        self, vertex: T, *, reverse: bool = False, const: bool = False
    ) -> BidirectionalIterator[tuple[T, T]]:
        """Edges that touch ``vertex``."""
        index = self._index_of(vertex)
        items = []
        for left, right in self._edges:
            if left == index or right == index:
                items.append((self._vertices[left], self._vertices[right]))
        return BidirectionalIterator(items, reverse=reverse, const=const)

    def reverse_incident_edges(self, vertex):
        return self.incident_edges(vertex, reverse=True)

    def const_incident_edges(self, vertex):
        return self.incident_edges(vertex, const=True)

    def adjacent_vertices(
        self, vertex: T, *, reverse: bool = False, const: bool = False
    ) -> BidirectionalIterator[T]:
        """Vertices sharing an edge with ``vertex``."""
        index = self._index_of(vertex)
        items = []
        for left, right in self._edges:
            if left == index:
                items.append(self._vertices[right])
            elif right == index:
                items.append(self._vertices[left])
        return BidirectionalIterator(items, reverse=reverse, const=const)

    def reverse_adjacent_vertices(self, vertex):
        return self.adjacent_vertices(vertex, reverse=True)

    def const_adjacent_vertices(self, vertex):
        return self.adjacent_vertices(vertex, const=True)

    def remove_vertex_at(self, iterator: BidirectionalIterator[T]):
        """Erase the vertex under a non-const iterator."""
        self._require_mutable(iterator)
        return self.remove_vertex(iterator.get())

    def remove_edge_at(self, iterator: BidirectionalIterator[tuple[T, T]]):
        """Erase the edge under a non-const iterator."""
        self._require_mutable(iterator)
        start, end = iterator.get()
        return self.remove_edge(start, end)

    def _index_of(self, vertex: T) -> int:
        for index, value in enumerate(self._vertices):
            if value == vertex:
                return index
        raise VertexNotFoundException(vertex)

    def _canonical_pair(self, start, end):
        left = self._index_of(start)
        right = self._index_of(end)
        if left <= right:
            return (left, right)
        return (right, left)

    def _shift_pair(self, left, right, removed_index):
        if left > removed_index:
            left -= 1
        if right > removed_index:
            right -= 1
        return (left, right)

    def _edge_values(self):
        return [
            (self._vertices[left], self._vertices[right])
            for left, right in self._edges
        ]

    def _require_mutable(self, iterator):
        if getattr(iterator, "is_const", False):
            raise InvalidIteratorException("Cannot mutate the graph through a const iterator")

    def _compare_key(self):
        vertices = tuple(self._vertices)
        edges = tuple(self._edge_values())
        return (len(self._vertices), len(self._edges), vertices, edges)

    def __eq__(self, other):
        if not isinstance(other, UndirectedGraph):
            return NotImplemented
        return self._compare_key() == other._compare_key()

    def __ne__(self, other):
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal

    def __lt__(self, other):
        if not isinstance(other, UndirectedGraph):
            return NotImplemented
        return self._compare_key() < other._compare_key()

    def __le__(self, other):
        if not isinstance(other, UndirectedGraph):
            return NotImplemented
        return self._compare_key() <= other._compare_key()

    def __gt__(self, other):
        if not isinstance(other, UndirectedGraph):
            return NotImplemented
        return self._compare_key() > other._compare_key()

    def __ge__(self, other):
        if not isinstance(other, UndirectedGraph):
            return NotImplemented
        return self._compare_key() >= other._compare_key()

    def __str__(self):
        vertex_text = ", ".join(str(vertex) for vertex in self.vertices())
        edge_text = ", ".join(f"{start}--{end}" for start, end in self.edges())
        return f"UndirectedGraph(vertices=[{vertex_text}], edges=[{edge_text}])"
