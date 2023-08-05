from typing import Any, Iterable


# noinspection PyShadowingBuiltins
def sum(iterable: Iterable, /, start: Any = None) -> Any:
    for index, i in enumerate(iterable):
        start = i if index == 0 else start + i

    return start
