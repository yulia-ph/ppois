from graph.UndirectedGraph import UndirectedGraph
from sorting.lsd_radix_sort import lsd_radix_sort
from sorting.Parcel import Parcel
from sorting.shell_sort import shell_sort


def scenario_shell_numbers():
    data = [5, 1, 4, 2, 8, 0]
    print(f"  before: {data}")
    shell_sort(data)
    print(f"  after:  {data}")


def scenario_shell_parcels():
    parcels = [Parcel("Warsaw", 12), Parcel("Minsk", 4), Parcel("Grodno", 9)]
    print(f"  before: {parcels}")
    shell_sort(parcels)
    print(f"  after:  {parcels}")


def scenario_radix_ints():
    data = [170, 45, 75, 90, 802, 24, 2, 66, -3]
    print(f"  before: {data}")
    lsd_radix_sort(data)
    print(f"  after:  {data}")


def scenario_radix_parcels():
    parcels = [Parcel("Warsaw", 12), Parcel("Minsk", 4), Parcel("Grodno", 9)]
    print(f"  before: {parcels}")
    lsd_radix_sort(parcels, key=lambda parcel: parcel.weight)
    print(f"  after:  {parcels}")


def _demo_graph():
    graph = UndirectedGraph[str]()
    graph.add_vertex("Minsk")
    graph.add_vertex("Grodno")
    graph.add_vertex("Brest")
    graph.add_edge("Minsk", "Grodno")
    graph.add_edge("Grodno", "Brest")
    return graph


def scenario_graph_build():
    graph = _demo_graph()
    print(f"  {graph}")
    print(f"  vertices={graph.vertex_count()} edges={graph.edge_count()}")
    print(f"  degree(Grodno)={graph.vertex_degree('Grodno')}")
    print(f"  edge_degree(Minsk--Grodno)={graph.edge_degree('Minsk', 'Grodno')}")


def scenario_graph_iterators():
    graph = _demo_graph()
    print(f"  vertices: {list(graph.vertices())}")
    print(f"  reverse:  {list(graph.reverse_vertices())}")
    print(f"  edges:    {list(graph.edges())}")
    print(f"  adjacent(Grodno): {list(graph.adjacent_vertices('Grodno'))}")
    print(f"  incident(Grodno): {list(graph.incident_edges('Grodno'))}")


def scenario_graph_erase():
    graph = _demo_graph()
    it = graph.vertices()
    it.next()
    graph.remove_vertex_at(it)
    print(f"  after erase first vertex: {graph}")
    clone = graph.copy()
    print(f"  copy equal: {clone == graph}")


def scenario_graph_compare():
    left = _demo_graph()
    right = left.copy()
    right.add_vertex("Vitebsk")
    print(f"  left == right: {left == right}")
    print(f"  left < right:  {left < right}")


MENU = """
==================================================
  LAB 4 — SORTING AND UNDIRECTED GRAPH
==================================================
   1. Shell sort numbers
   2. Shell sort parcels
   3. LSD radix sort integers
   4. LSD radix sort parcels by weight
   5. Build a graph
   6. Walk graph iterators
   7. Erase a vertex by iterator
   8. Copy and compare graphs
   0. Exit
==================================================
"""

SCENARIOS = {
    "1": scenario_shell_numbers,
    "2": scenario_shell_parcels,
    "3": scenario_radix_ints,
    "4": scenario_radix_parcels,
    "5": scenario_graph_build,
    "6": scenario_graph_iterators,
    "7": scenario_graph_erase,
    "8": scenario_graph_compare,
}


def main():
    while True:
        print(MENU)
        choice = input("Your choice: ").strip()
        if choice == "0":
            print("Goodbye!")
            return
        action = SCENARIOS.get(choice)
        if action is None:
            print("Unknown choice")
            continue
        try:
            action()
        except Exception as error:
            print(f"  ✗ Stopped: {error}")


if __name__ == "__main__":
    main()
