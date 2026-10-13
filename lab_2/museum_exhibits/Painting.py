from museum_exhibits.Exhibit import Exhibit


class Painting(Exhibit):
    """A painting exhibit.

    Extends Exhibit with painting-specific attributes: technique,
    canvas dimensions, frame, and varnish state. Paintings do not
    change their own condition — that happens only through a
    Restoration process.
    """

    RESTORATION_COST_PER_SQM = 500.0

    def __init__(self, title: str, author: str, technique: str,
                 width: float, height: float, condition: str = "good"):
        """Initialize a painting.

        Args:
            title: The painting title. Must not be empty.
            author: The painter. Must not be empty.
            technique: Painting technique, e.g. "oil", "watercolor", "tempera".
                Must not be empty.
            width: Canvas width in meters. Must be positive.
            height: Canvas height in meters. Must be positive.
            condition: One of Exhibit.CONDITION_* constants.

        Raises:
            ValueError: If technique is empty, width or height is not
                positive, or inherited validation fails.
        """
        super().__init__(title, author, condition)

        if not technique:
            raise ValueError("Technique must not be empty")
        if width <= 0:
            raise ValueError(f"Width must be positive, got {width}")
        if height <= 0:
            raise ValueError(f"Height must be positive, got {height}")

        self._technique = technique
        self._width = width
        self._height = height
        self._frame = None
        self._has_varnish = False


    @property
    def technique(self):
        return self._technique

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def frame(self):
        return self._frame

    @property
    def has_varnish(self):
        return self._has_varnish


    def area(self) -> float:
        """Return the canvas area in square meters."""
        return self._width * self._height


    def set_frame(self, frame: str):
        """Attach a frame to the painting.

        Args:
            frame: The frame description. Must not be empty.

        Raises:
            ValueError: If frame is empty.
        """
        if not frame:
            raise ValueError("Frame must not be empty")
        self._frame = frame
        return True


    def apply_varnish(self):
        """Apply varnish to the painting.

        Idempotent: applying varnish to an already varnished painting
        is not an error.
        """
        self._has_varnish = True
        return True



    def estimate_restoration_cost(self) -> float:
        """Estimate the cost of restoring this painting.

        The cost scales with canvas area.

        Returns:
            Estimated cost in conventional units.
        """
        return Painting.RESTORATION_COST_PER_SQM * self.area()