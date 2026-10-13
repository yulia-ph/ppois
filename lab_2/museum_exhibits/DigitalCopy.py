from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class DigitalCopy:
    """A digital copy of a physical exhibit.

    Represents a digitized version of an exhibit (image, scan,
    document, etc.) stored on disk. A copy has a lifecycle:
    it must be created before it can be stored, converted, or
    published to the museum's website.
    """

    DEFAULT_FORMAT = "jpg"

    def __init__(self, source, format_: str, size: int, resolution: str):
        """Initialize a digital copy.

        Args:
            source: The physical exhibit this copy represents.
                Must not be None.
            format_: File format (e.g. "jpg", "pdf", "tiff").
                Must not be empty.
            size: File size in bytes. Must be non-negative.
            resolution: Resolution string (e.g. "300dpi", "1920x1080").
                Must not be empty.

        Raises:
            ValueError: If source is None, format_ or resolution is
                empty, or size is negative.
        """
        if source is None:
            raise ValueError("Source exhibit must not be None")
        if not format_:
            raise ValueError("Format must not be empty")
        if not resolution:
            raise ValueError("Resolution must not be empty")
        if size < 0:
            raise ValueError(f"Size must be non-negative, got {size}")

        self._source = source
        self._format = format_
        self._size = size
        self._resolution = resolution
        self._path = None
        self._is_published = False
        self._created = False


    @property
    def source(self):
        return self._source

    @property
    def format(self):
        return self._format

    @property
    def size(self):
        return self._size

    @property
    def resolution(self):
        return self._resolution

    @property
    def path(self):
        return self._path

    @property
    def is_published(self):
        return self._is_published

    @property
    def is_created(self):
        return self._created


    def create(self):
        """Create the digital copy from its source.

        Idempotent: calling on an already created copy is not an error.
        The path is derived from the source's inventory number and the
        current format.
        """
        if not self._created:
            self._path = f"/digital/{self._source.inventory_number}.{self._format}"
            self._created = True
        return True

    def store(self, path: str = None):
        """Store the copy at the given path (or keep the current one).

        Args:
            path: Optional new storage path. If None, the copy is kept
                at its existing path.

        Raises:
            InvalidExhibitStateException: If the copy has not been
                created yet.
        """
        if not self._created:
            raise InvalidExhibitStateException(
                exhibit_title=self._source.inventory_number,
                state="not_created",
                reason="Cannot store a copy that has not been created",
            )
        if path:
            self._path = path
        return True


    def publish_to_website(self):
        """Publish the copy to the museum's website.

        Idempotent: publishing an already published copy is not an error.

        Raises:
            InvalidExhibitStateException: If the copy has not been
                created yet.
        """
        if not self._created:
            raise InvalidExhibitStateException(
                exhibit_title=self._source.inventory_number,
                state="not_created",
                reason="Cannot publish a copy that has not been created",
            )
        self._is_published = True
        return True

    def unpublish(self):
        """Remove the copy from the museum's website.

        Idempotent: unpublishing a copy that is not published is not
        an error.
        """
        self._is_published = False
        return True


    def convert(self, new_format: str):
        """Convert the copy to a different file format.

        Args:
            new_format: Target format. Must not be empty, and must
                differ from the current format.

        Raises:
            InvalidExhibitStateException: If the copy has not been
                created yet.
            ValueError: If new_format is empty or matches the current
                format.
        """
        if not self._created:
            raise InvalidExhibitStateException(
                exhibit_title=self._source.inventory_number,
                state="not_created",
                reason="Cannot convert a copy that has not been created",
            )
        if not new_format:
            raise ValueError("New format must not be empty")
        if new_format == self._format:
            raise ValueError(
                f"Copy is already in format '{new_format}'; nothing to convert"
            )
        self._format = new_format
        self._path = f"/digital/{self._source.inventory_number}.{new_format}"
        return True


    def get_info(self) -> dict:
        """Return a summary dict of the copy's state."""
        return {
            "source": self._source.inventory_number if self._source else None,
            "format": self._format,
            "size": self._size,
            "resolution": self._resolution,
            "path": self._path,
            "published": self._is_published,
        }