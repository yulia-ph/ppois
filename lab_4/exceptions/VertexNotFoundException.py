from exceptions.Lab4Exception import Lab4Exception


class VertexNotFoundException(Lab4Exception):
    """Raised when a vertex is not in the graph."""

    def __init__(self, vertex=None):
        super().__init__(
            message=f"Vertex {vertex!r} is not in the graph",
            error_code="VERTEX_NOT_FOUND",
        )
        self._vertex = vertex
