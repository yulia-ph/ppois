def _key_of(item, key):
    if key is None:
        return item
    return key(item)


def _out_of_order(left, right, key, reverse: bool) -> bool:
    left_key = _key_of(left, key)
    right_key = _key_of(right, key)
    if reverse:
        return left_key < right_key
    return left_key > right_key


def shell_sort(sequence, key=None, reverse: bool = False):
    """Sort a mutable sequence in place using Shell sort.

    Works with ``list`` and other sequences that support index assignment.
    ``key`` is the same idea as in ``list.sort``.
    """
    size = len(sequence)
    gap = size // 2
    while gap > 0:
        for index in range(gap, size):
            current = sequence[index]
            shift = index
            while shift >= gap and _out_of_order(
                sequence[shift - gap], current, key, reverse
            ):
                sequence[shift] = sequence[shift - gap]
                shift -= gap
            sequence[shift] = current
        gap //= 2
    return sequence
