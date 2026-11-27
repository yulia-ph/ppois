from collections.abc import Iterable
from typing import Generic, TypeVar

from exceptions.InvalidIteratorException import InvalidIteratorException

T = TypeVar("T")


class BidirectionalIterator(Generic[T]):  # noqa: UP046
    """A two-way cursor over a snapshot of items of type ``T``.

    ``next()`` walks the iterator's forward direction. ``prev()`` walks back.
    A reverse iterator starts at the last item and moves toward the first.
    Const iterators may be read but must not be used to erase from a graph.
    """

    def __init__(self, items: Iterable[T], *, reverse: bool = False, const: bool = False):
        self._items = list(items)
        self._reverse = reverse
        self._const = const
        self._size = len(self._items)
        self._pos = self._size if reverse else -1

    @property
    def is_const(self) -> bool:
        return self._const

    @property
    def is_reverse(self) -> bool:
        return self._reverse

    def get(self) -> T:
        """Return the current element."""
        if not 0 <= self._pos < self._size:
            raise InvalidIteratorException("Iterator is not on an element")
        return self._items[self._pos]

    def has_next(self) -> bool:
        """True if ``next()`` would return an element."""
        if self._reverse:
            return self._pos > 0
        return self._pos + 1 < self._size

    def has_prev(self) -> bool:
        """True if ``prev()`` would return an element."""
        if self._reverse:
            return self._pos + 1 < self._size
        return self._pos > 0

    def next(self) -> T:
        """Move one step forward along this iterator and return the element."""
        if self._reverse:
            nxt = self._pos - 1
            if nxt < 0:
                self._pos = -1
                raise StopIteration
            self._pos = nxt
        else:
            nxt = self._pos + 1
            if nxt >= self._size:
                self._pos = self._size
                raise StopIteration
            self._pos = nxt
        return self.get()

    def prev(self) -> T:
        """Move one step backward along this iterator and return the element."""
        if self._reverse:
            nxt = self._pos + 1
            if nxt >= self._size:
                self._pos = self._size
                raise StopIteration
            self._pos = nxt
        else:
            nxt = self._pos - 1
            if nxt < 0:
                self._pos = -1
                raise StopIteration
            self._pos = nxt
        return self.get()

    def __iter__(self):
        return self

    def __next__(self) -> T:
        return self.next()
