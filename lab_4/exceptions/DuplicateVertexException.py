from exceptions.Lab4Exception import Lab4Exception


class DuplicateVertexException(Lab4Exception):
    """Raised when adding a vertex that is already present."""

    def __init__(self, vertex=None):
        super().__init__(
            message=f"Vertex {vertex!r} is already in the graph",
            error_code="DUPLICATE_VERTEX",
        )
        self._vertex = vertex
