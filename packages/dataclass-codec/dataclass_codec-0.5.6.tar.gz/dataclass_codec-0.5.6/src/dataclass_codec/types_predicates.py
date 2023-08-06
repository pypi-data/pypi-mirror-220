from enum import Enum
from typing import Any, Type


def is_generic_dataclass_predicate(_type: Type[Any]) -> bool:
    return hasattr(_type, "__origin__") and is_dataclass_predicate(
        _type.__origin__
    )


def is_dataclass_predicate(_type: Type[Any]) -> bool:
    return hasattr(_type, "__dataclass_fields__")


def is_enum_predicate(_type: Type[Any]) -> bool:
    return type(_type) is type(Enum) and issubclass(_type, Enum)
