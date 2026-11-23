from exceptions.Lab4Exception import Lab4Exception


class EdgeNotFoundException(Lab4Exception):
    """Raised when an edge is not in the graph."""

    def __init__(self, start=None, end=None):
        super().__init__(
            message=f"Edge {start!r}--{end!r} is not in the graph",
            error_code="EDGE_NOT_FOUND",
        )
        self._start = start
        self._end = end
