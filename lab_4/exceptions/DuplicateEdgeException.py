from exceptions.Lab4Exception import Lab4Exception


class DuplicateEdgeException(Lab4Exception):
    """Raised when adding an edge that is already present."""

    def __init__(self, start=None, end=None):
        super().__init__(
            message=f"Edge {start!r}--{end!r} is already in the graph",
            error_code="DUPLICATE_EDGE",
        )
        self._start = start
        self._end = end
