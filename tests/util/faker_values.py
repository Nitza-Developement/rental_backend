from typing import Callable, TypeVar

T = TypeVar("T")


def get_different_from(
    old_value: T,
    random_metod: Callable[[], T],
) -> T:
    new_value = random_metod()
    while new_value == old_value:
        new_value = random_metod()
    return new_value
