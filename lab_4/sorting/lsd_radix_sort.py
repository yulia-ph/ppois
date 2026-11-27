RADIX = 10


def _digits_of(number: int) -> int:
    if number == 0:
        return 1
    digits = 0
    while number > 0:
        number //= RADIX
        digits += 1
    return digits


def _max_digits(numbers) -> int:
    longest = 1
    for number in numbers:
        length = _digits_of(number)
        longest = max(longest, length)
    return longest


def _counting_pass(items, keys, digit_index: int):
    """Stable pass by one decimal digit (0 = least significant)."""
    buckets = [[] for _ in range(RADIX)]
    divisor = RADIX ** digit_index
    for item, key in zip(items, keys, strict=True):
        digit = (key // divisor) % RADIX
        buckets[digit].append((item, key))
    ordered = []
    for bucket in buckets:
        ordered.extend(bucket)
    return [pair[0] for pair in ordered], [pair[1] for pair in ordered]


def lsd_radix_sort(sequence, key=None):
    """Sort a mutable sequence of integers in place with LSD radix sort.

    Negative numbers are supported by sorting the offset from the minimum.
    ``key`` must return an ``int`` for each item (for custom objects).
    """
    if not sequence:
        return sequence
    raw_keys = [item if key is None else key(item) for item in sequence]
    for raw in raw_keys:
        if type(raw) is not int:
            raise TypeError("LSD radix sort requires integer keys")
    offset = min(raw_keys)
    keys = [raw - offset for raw in raw_keys]
    items = list(sequence)
    passes = _max_digits(keys)
    for digit_index in range(passes):
        items, keys = _counting_pass(items, keys, digit_index)
    for index, item in enumerate(items):
        sequence[index] = item
    return sequence
