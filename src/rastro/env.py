import os
from typing import Callable, TypeVar, overload

T = TypeVar("T")


@overload
def get_env(
    key: str,
    *,
    default: str,
) -> str: ...


@overload
def get_env(
    key: str,
    *,
    default: None = None,
) -> str | None: ...


def get_env(
    key: str,
    *,
    default: str | None = None,
) -> str | None:
    value = os.environ.get(key)

    if value is None:
        return default

    return value


def cast_env(value: str, *, parser: Callable[[str], T]) -> T:
    return parser(value)


def parse_csv(value: str | list[str]) -> list[str]:
    if isinstance(value, str):
        return [item.strip() for item in value.split(",")]

    return value


def parse_booleanish(raw_value: str | bool) -> bool:
    if type(raw_value) is bool:
        return raw_value

    value = raw_value.lower()

    if value == "true" or value == "1":
        return True

    if value == "false" or value == "0":
        return False

    raise TypeError(f"Could not parse {raw_value} as booleanish value.")
