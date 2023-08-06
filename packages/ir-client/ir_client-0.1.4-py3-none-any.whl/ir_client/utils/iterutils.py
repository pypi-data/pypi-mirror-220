#TODO extract to separate repo

from typing import TypeVar

import itertools

T = TypeVar("T")

#TODO test
def pairwise(iterable: list[T]) -> tuple[T, T]:
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)
