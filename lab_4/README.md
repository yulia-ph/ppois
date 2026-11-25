# Sorting and Graphs — Lab 4

Variant **7**: Shell sort, LSD radix sort, and an **undirected graph**
stored as ordered lists of vertices and edges.

The project is written in pure Python 3, uses no external
dependencies at runtime, and is covered by pytest tests.

---

## Sorting

| Function         | What it sorts                                      |
|------------------|----------------------------------------------------|
| `shell_sort`     | Any mutable sequence; optional `key` and `reverse` |
| `lsd_radix_sort` | Integers, or objects via an integer `key`          |

`Parcel` is a small user type (destination, weight) used to show that
Shell sort works on custom objects and radix sort can use `key=weight`.

## Graph

`UndirectedGraph[T]` is generic over the vertex type (`Generic[T]`).
It keeps vertices in insertion order and edges in a sorted list of
index pairs. The representation is private.

| Method | Meaning |
|--------|---------|
| `empty` / `clear` / `copy` / `assign_from` | container basics |
| `has_vertex` / `has_edge` | membership |
| `vertex_count` / `edge_count` | sizes |
| `vertex_degree` / `edge_degree` | degrees (a loop has edge degree 1) |
| `add_vertex` / `add_edge` | insert |
| `remove_vertex` / `remove_edge` | delete by value |
| `remove_vertex_at` / `remove_edge_at` | delete by iterator |
| `vertices` / `edges` / `incident_edges` / `adjacent_vertices` | iterators |
| `reverse_*` / `const_*` | reverse and read-only variants |

Iterators are bidirectional (`next` / `prev`). `__str__` is built by
walking those iterators.

## Exceptions

| Exception | When |
|-----------|------|
| `Lab4Exception` | base class |
| `VertexNotFoundException` | missing vertex |
| `EdgeNotFoundException` | missing edge |
| `DuplicateVertexException` | vertex already present |
| `DuplicateEdgeException` | edge already present |
| `InvalidIteratorException` | iterator not on an element, or const erase |

## Scenarios (see `main.py`)

1. Shell sort numbers
2. Shell sort parcels
3. LSD radix sort integers
4. LSD radix sort parcels by weight
5. Build a graph
6. Walk graph iterators
7. Erase a vertex by iterator
8. Copy and compare graphs
