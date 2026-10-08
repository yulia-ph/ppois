from museum_exhibits.Exhibit import Exhibit


class Document(Exhibit):
    """A document-type exhibit: manuscript, book, or letter.

    Extends Exhibit with document-specific attributes such as number
    of pages, language, and paper acidity. Documents can be digitized
    into a DigitalCopy, which is stored on the document for later
    retrieval.
    """

    ACIDIC_PH = 5.0
    ALKALINE_PH = 8.0
    MIN_PH = 0.0
    MAX_PH = 14.0

    def __init__(self, title: str, author: str, doc_type: str,
                 pages: int, language: str, condition: str = "good"):
        """Initialize a document.

        Args:
            title: The document title.
            author: The author or creator.
            doc_type: Document type, e.g. "manuscript", "book", "letter".
            pages: Number of pages. Must be non-negative.
            language: Document language code (e.g. "en", "ru").
            condition: One of Exhibit.CONDITION_* constants.

        Raises:
            ValueError: If any string is empty, pages is negative, or
                condition is not a valid Exhibit condition.
        """
        super().__init__(title, author, condition)

        if not doc_type:
            raise ValueError("Document type must not be empty")
        if pages < 0:
            raise ValueError(f"Pages must be non-negative, got {pages}")
        if not language:
            raise ValueError("Language must not be empty")

        self._doc_type = doc_type
        self._pages = pages
        self._language = language
        self._is_digitized = False
        self._acidity_level = 7.0
        self._digital_copy = None

    @property
    def doc_type(self):
        return self._doc_type

    @property
    def pages(self):
        return self._pages

    @property
    def language(self):
        return self._language

    @property
    def is_digitized(self):
        return self._is_digitized

    @property
    def acidity_level(self):
        return self._acidity_level

    @property
    def digital_copy(self):
        return self._digital_copy


    def digitize(self):
        """Create a digital copy of this document.

        Idempotent: if the document is already digitized, returns the
        existing copy. Otherwise creates a new DigitalCopy, stores it
        on the document, and returns it.

        Returns:
            The DigitalCopy instance (existing or newly created).
        """
        if self._is_digitized:
            return self._digital_copy
        from museum_exhibits.DigitalCopy import DigitalCopy
        copy = DigitalCopy(self, "pdf", 0, "300dpi")
        copy.create()
        self._digital_copy = copy
        self._is_digitized = True
        return copy


    def check_acidity(self) -> str:
        """Classify the paper acidity as a string.

        Returns:
            "acidic" if pH is below ACIDIC_PH,
            "alkaline" if pH is above ALKALINE_PH,
            "neutral" otherwise.
        """
        if self._acidity_level < Document.ACIDIC_PH:
            return "acidic"
        if self._acidity_level > Document.ALKALINE_PH:
            return "alkaline"
        return "neutral"

    def set_acidity_level(self, level: float):
        """Set the paper acidity level.

        Args:
            level: pH value. Must be within [MIN_PH, MAX_PH].

        Raises:
            ValueError: If level is outside the pH scale.
        """
        if not (Document.MIN_PH <= level <= Document.MAX_PH):
            raise ValueError(
                f"pH level {level} is out of range "
                f"[{Document.MIN_PH}, {Document.MAX_PH}]"
            )
        self._acidity_level = level
        return True

    def is_fragile(self) -> bool:
        """Return True if the document is fragile.

        A document is fragile if its condition is critical or its
        paper is acidic.
        """
        if self._condition == Exhibit.CONDITION_CRITICAL:
            return True
        return self._acidity_level < Document.ACIDIC_PH