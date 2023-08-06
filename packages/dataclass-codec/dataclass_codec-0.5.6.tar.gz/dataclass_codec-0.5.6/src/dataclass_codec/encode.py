import base64
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any, Callable, Dict, Type, Tuple, List

from uuid import UUID

from dataclass_codec.types_predicates import (
    is_dataclass_predicate,
    is_enum_predicate,
)


TYPEMATCHPREDICATE = Callable[[Type[Any]], bool]

ENCODEIT = Callable[[Any], Any]
TYPEENCODER = Callable[[Any, ENCODEIT], Any]


def raw_encode(
    obj: Any,
    encoders: Dict[Type[Any], TYPEENCODER],
    encoders_by_predicate: List[Tuple[TYPEMATCHPREDICATE, TYPEENCODER]],
) -> Any:
    obj_type = type(obj)

    def encode_it(obj: Any) -> Any:
        return raw_encode(obj, encoders, encoders_by_predicate)

    if obj_type in encoders:
        return encoders[obj_type](obj, encode_it)

    for predicate, encoder in encoders_by_predicate:
        if predicate(obj_type):
            return encoder(obj, encode_it)

    raise TypeError(f"Cannot encode {obj_type}")


def primitive_hook(_type: Type[Any]) -> TYPEENCODER:
    def encode_primitive(obj: Any, _encode_it: ENCODEIT) -> Any:
        return obj

    return encode_primitive


def list_hook(obj: Any, encode_it: ENCODEIT) -> Any:
    return [encode_it(i) for i in obj]


def dict_hook(obj: Any, encode_it: ENCODEIT) -> Any:
    return {k: encode_it(v) for k, v in obj.items()}


def bytes_to_base64(obj: Any, _encode_it: ENCODEIT) -> Any:
    assert isinstance(obj, bytes)

    return base64.b64encode(obj).decode("ascii")


def datetime_to_iso(obj: Any, _encode_it: ENCODEIT) -> Any:
    assert isinstance(obj, (datetime, date, time))
    return obj.isoformat()


def dataclass_to_primitive_dict(obj: Any, encode_it: ENCODEIT) -> Any:
    assert is_dataclass_predicate(type(obj))
    return {
        k: encode_it(
            getattr(obj, k),
        )
        for k in obj.__dataclass_fields__.keys()
        if not k.startswith("_")
    }


def enum_to_primitive(obj: Any, _encode_it: ENCODEIT) -> Any:
    assert isinstance(obj, Enum)
    return obj.value


def decimal_to_str(obj: Any, _encode_it: ENCODEIT) -> Any:
    assert isinstance(obj, Decimal)
    return str(obj)


def uuid_to_str(obj: Any, _encode_it: ENCODEIT) -> Any:
    assert isinstance(obj, UUID), f"Expected UUID, got {type(obj)}"
    return str(obj)


def encode(obj: Any) -> Any:
    return raw_encode(
        obj,
        {
            **{t: primitive_hook(t) for t in [bool, int, float, str]},
            type(None): lambda obj, _: None,
            list: list_hook,
            tuple: list_hook,
            dict: dict_hook,
            bytes: bytes_to_base64,
            datetime: datetime_to_iso,
            date: datetime_to_iso,
            time: datetime_to_iso,
            Decimal: decimal_to_str,
            UUID: uuid_to_str,
        },
        [
            (is_dataclass_predicate, dataclass_to_primitive_dict),
            (is_enum_predicate, enum_to_primitive),
        ],
    )
