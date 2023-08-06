import base64
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import MISSING, Field, dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from operator import indexOf
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    ForwardRef,
    Generator,
    Generic,
    List,
    Literal,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    get_args,
)
from uuid import UUID

from dataclass_codec.types_predicates import (
    is_dataclass_predicate,
    is_enum_predicate,
    is_generic_dataclass_predicate,
)

if TYPE_CHECKING:
    pass


ANYTYPE = Union[Type[Any], Any]


TYPEMATCHPREDICATE = Callable[[ANYTYPE], bool]
DECODEIT = Callable[[Any, ANYTYPE], Any]
TYPEDECODER = Callable[[Any, ANYTYPE, DECODEIT], Any]


T = TypeVar("T")


FORWARD_REF_SCOPES_BY_DATACLASS_TYPE: Dict[Type[Any], Dict[str, Any]] = {}


def register_forward_refs_for_dataclass_type(
    dataclass_type: Type[Any], **forward_refs: Any
) -> None:
    FORWARD_REF_SCOPES_BY_DATACLASS_TYPE[dataclass_type] = forward_refs


forward_ref_map_cxt_var = ContextVar[Dict[str, Any]](
    "forward_ref_map_cxt_var", default={}
)


def forward_ref_map() -> Dict[str, Any]:
    return forward_ref_map_cxt_var.get()


@contextmanager
def forward_ref_map_scope(
    forward_ref_map: Dict[str, Any],
) -> Generator[None, Any, None]:
    token = forward_ref_map_cxt_var.set(forward_ref_map)
    try:
        yield
    finally:
        forward_ref_map_cxt_var.reset(token)


@dataclass
class DecodeContext:
    strict: bool = False
    primitive_cast_values: bool = True
    dataclass_unset_as_none: bool = True
    collect_errors: bool = False
    forward_refs: Optional[Dict[str, Any]] = None


decode_context_cxt_var = ContextVar(
    "decode_context_cxt_var", default=DecodeContext()
)


def decode_context() -> DecodeContext:
    return decode_context_cxt_var.get()


@contextmanager
def decode_context_scope(
    decode_context: DecodeContext,
) -> Generator[None, Any, None]:
    token = decode_context_cxt_var.set(decode_context)
    try:
        yield
    finally:
        decode_context_cxt_var.reset(token)


error_list_cxt_var = ContextVar[List[Tuple[str, Exception]]](
    "error_list_cxt_var", default=[]
)


def error_list() -> List[Tuple[str, Exception]]:
    return error_list_cxt_var.get()


@contextmanager
def error_list_scope(
    error_list: Optional[List[Tuple[str, Exception]]] = None,
) -> Generator[List[Tuple[str, Exception]], Any, None]:
    if error_list is None:
        error_list = []
    token = error_list_cxt_var.set(error_list)
    try:
        yield error_list
    finally:
        error_list_cxt_var.reset(token)


current_path_cxt_var = ContextVar("current_path_cxt_var", default="$")


def current_path() -> str:
    return current_path_cxt_var.get()


@contextmanager
def current_path_scope(path: str) -> Generator[None, Any, None]:
    token = current_path_cxt_var.set(path)
    try:
        yield

    except Exception as e:
        error_list().append((current_path(), e))
        if not decode_context().collect_errors:
            raise
    finally:
        current_path_cxt_var.reset(token)


TYPES_PATH = Tuple[Type[Any], ...]

types_path_cxt_var = ContextVar[TYPES_PATH]("types_path_cxt_var", default=())


@contextmanager
def types_path_scope(
    types_path: TYPES_PATH,
) -> Generator[None, Any, None]:
    token = types_path_cxt_var.set(types_path)
    try:
        yield
    finally:
        types_path_cxt_var.reset(token)


def current_types_path() -> TYPES_PATH:
    return types_path_cxt_var.get()


def discover_typevar(_type: TypeVar) -> Any:
    if len(current_types_path()) == 0:
        raise TypeError(f"Cannot decode {_type}")

    typevar_context = [*current_types_path()][::-1]

    types_path: Tuple[Type[Any], ...] = ()
    index = -1
    for t in typevar_context:
        base_t = t
        types_path = types_path + (base_t,)
        while hasattr(base_t, "__origin__") or hasattr(
            base_t, "__orig_bases__"
        ):
            if hasattr(base_t, "__origin__"):
                if hasattr(base_t.__origin__, "__orig_bases__"):
                    if hasattr(
                        base_t.__origin__.__orig_bases__[0], "__origin__"
                    ):
                        if (
                            base_t.__origin__.__orig_bases__[0].__origin__
                            is Generic
                        ):
                            index = indexOf(
                                base_t.__origin__.__orig_bases__[0].__args__,
                                _type,
                            )
                            if index != -1:
                                break

                base_t = base_t.__origin__
            else:
                base_t = base_t.__orig_bases__[0]

    if index == -1:
        raise TypeError(f"Typevar {_type} not found in {types_path}")
    corresponding_type = base_t.__args__[index]
    return corresponding_type


def is_forward_ref_predicate(_type: ANYTYPE) -> bool:
    return isinstance(_type, ForwardRef)
    # return hasattr(_type, "__forward_arg__")


def forward_ref_decoder(obj: Any, _type: ANYTYPE, decode_it: DECODEIT) -> Any:
    assert isinstance(_type, ForwardRef), "{} is not a forward ref".format(
        _type.__name__
    )

    current_map = forward_ref_map()

    if _type.__forward_arg__ in current_map:
        real_type = current_map[_type.__forward_arg__]
        return decode_it(obj, real_type)

    raise TypeError(f"Could not resolve forward ref {_type}")


def is_string_forward_ref_predicate(_type: ANYTYPE) -> bool:
    return isinstance(_type, str)


def string_forward_ref_decoder(
    obj: Any, _type: ANYTYPE, decode_it: DECODEIT
) -> Any:
    assert isinstance(_type, str), "{} is not a string forward ref".format(
        _type.__name__
    )

    return decode_it(obj, ForwardRef(_type))


def raw_decode(
    obj: Any,
    obj_type: Type[T],
    decoders: Dict[ANYTYPE, TYPEDECODER],
    decoders_by_predicate: List[Tuple[TYPEMATCHPREDICATE, TYPEDECODER]],
) -> T:
    def decode_it(obj: Any, _type: ANYTYPE) -> Any:
        if isinstance(_type, TypeVar):
            newtype = discover_typevar(_type)
        else:
            newtype = _type

        return raw_decode(obj, newtype, decoders, decoders_by_predicate)

    if isinstance(obj_type, TypeVar):
        obj_type.__bound__

    if obj_type in decoders:
        return cast(T, decoders[obj_type](obj, obj_type, decode_it))

    for predicate, decoder in decoders_by_predicate:
        if predicate(obj_type):
            with types_path_scope(current_types_path() + (obj_type,)):
                return cast(T, decoder(obj, obj_type, decode_it))

    raise TypeError(f"Cannot decode {obj_type}")


def primitive_hook(_type: ANYTYPE) -> TYPEDECODER:
    def decode_primitive(
        obj: Any, _type: ANYTYPE, _decode_it: DECODEIT
    ) -> Any:
        ctx = decode_context()

        def type_can_cast(_type: ANYTYPE) -> bool:
            return _type in (
                str,
                int,
                float,
                Decimal,
                bool,
                date,
                datetime,
                time,
            )

        if ctx.primitive_cast_values and type_can_cast(_type):
            return _type(obj)

        if ctx.strict and _type(obj) != obj:
            raise TypeError(f"Cannot decode {obj} ({type(obj)}) as {_type}")

        return obj

    return decode_primitive


def list_hook(obj: Any, _type: ANYTYPE, decode_it: DECODEIT) -> Any:
    return [decode_it(i, _type) for i in obj]


def dict_hook(obj: Any, _type: ANYTYPE, decode_it: DECODEIT) -> Any:
    assert isinstance(obj, dict), "{} is {} not dict".format(
        current_path(), type(obj)
    )

    def make_value(k: str) -> Any:
        with current_path_scope(current_path() + "." + k):
            return decode_it(obj[k], _type)

    return {k: make_value(v) for k, v in obj.items()}


def base64_to_bytes(obj: Any, _type: ANYTYPE, _decode_it: DECODEIT) -> Any:
    assert isinstance(obj, str), "{} is {} not str".format(
        current_path(), type(obj)
    )
    return base64.b64decode(obj)


def iso_datetime_to_datetime(
    obj: Any, _type: ANYTYPE, _decode_it: DECODEIT
) -> Any:
    assert isinstance(obj, str), "{} is {} not str".format(
        current_path(), type(obj)
    )
    return datetime.fromisoformat(obj)


def iso_date_to_date(obj: Any, _type: ANYTYPE, _decode_it: DECODEIT) -> Any:
    assert isinstance(obj, str), "{} is {} not str".format(
        current_path(), type(obj)
    )
    return datetime.fromisoformat(obj).date()


def iso_time_to_time(obj: Any, _type: ANYTYPE, _decode_it: DECODEIT) -> Any:
    assert isinstance(obj, str), "{} is {} not str".format(
        current_path(), type(obj)
    )
    return time.fromisoformat(obj)


def dataclass_from_primitive_dict(
    obj: Any, _type: ANYTYPE, decode_it: DECODEIT
) -> Any:
    cxt = decode_context()
    assert is_dataclass_predicate(_type), "{} is not a dataclass".format(
        _type.__name__
    )

    assert isinstance(obj, dict), "{} is {} not dict".format(
        current_path(), type(obj)
    )

    def make_value(k: str) -> Any:
        with current_path_scope(current_path() + "." + k):
            field: "Field[Any]" = _type.__dataclass_fields__[k]
            if k not in obj:
                if callable(field.default_factory):
                    return field.default_factory()
                elif field.default is not MISSING:
                    return field.default
                elif cxt.dataclass_unset_as_none:
                    return None
                else:
                    raise ValueError(f"Missing key {k}")

            return decode_it(obj[k], _type.__dataclass_fields__[k].type)

    with forward_ref_map_scope(
        {
            **(decode_context().forward_refs or {}),
            **forward_ref_map(),
            **FORWARD_REF_SCOPES_BY_DATACLASS_TYPE.get(_type, {}),
        }
    ):
        return _type(
            **{k: make_value(k) for k in _type.__dataclass_fields__.keys()}
        )


def generic_dataclass_from_primitive_dict(
    obj: Any, _type: ANYTYPE, decode_it: DECODEIT
) -> Any:
    cxt = decode_context()
    assert is_generic_dataclass_predicate(
        _type
    ), "{} is not a dataclass".format(_type.__name__)

    assert isinstance(obj, dict), "{} is {} not dict".format(
        current_path(), type(obj)
    )

    def make_value(k: str, t: Type[Any]) -> Any:
        with current_path_scope(current_path() + "." + k):
            if k not in obj:
                if cxt.dataclass_unset_as_none:
                    return None
                else:
                    raise ValueError(f"Missing key {k}")

            if isinstance(t, TypeVar):
                generic_args: Tuple[Any, ...] = get_args(
                    _type.__origin__.__orig_bases__[0]
                )
                index = indexOf(generic_args, t)
                if index == -1:
                    raise TypeError(f"Typevar {t} not found in {generic_args}")
                t = _type.__args__[index]
            return decode_it(obj[k], t)

    with forward_ref_map_scope(
        {
            **(decode_context().forward_refs or {}),
            **forward_ref_map(),
            **FORWARD_REF_SCOPES_BY_DATACLASS_TYPE.get(_type, {}),
        }
    ):
        return _type(
            **{
                k: make_value(k, t.type)
                for k, t in _type.__origin__.__dataclass_fields__.items()
            }
        )


def decimal_from_str(obj: Any, _type: ANYTYPE, _decode_it: DECODEIT) -> Any:
    assert isinstance(
        obj, (str, int, float)
    ), "{} is {} not str, int or float".format(current_path(), type(obj))
    return Decimal(obj)


def uuid_from_str(obj: Any, _type: ANYTYPE, _decode_it: DECODEIT) -> Any:
    assert isinstance(obj, str), "{} is {} not str".format(
        current_path(), type(obj)
    )
    return UUID(obj)


def is_generic_list_predicate(_type: ANYTYPE) -> bool:
    return hasattr(_type, "__origin__") and _type.__origin__ is list


def generic_list_decoder(obj: Any, _type: ANYTYPE, decode_it: DECODEIT) -> Any:
    assert is_generic_list_predicate(_type), "{} is not a list".format(
        _type.__name__
    )

    assert isinstance(obj, list), "{} is {} not list".format(
        current_path(), type(obj)
    )

    def make_value(i: int) -> Any:
        with current_path_scope(current_path() + f"[{i}]"):
            return decode_it(obj[i], _type.__args__[0])

    return [make_value(i) for i in range(len(obj))]


def is_generic_tuple_predicate(_type: ANYTYPE) -> bool:
    return hasattr(_type, "__origin__") and _type.__origin__ is tuple


def generic_tuple_decoder(
    obj: Any, _type: ANYTYPE, decode_it: DECODEIT
) -> Any:
    assert is_generic_tuple_predicate(_type), "{} is not a tuple".format(
        _type.__name__
    )

    assert isinstance(obj, tuple), "{} is {} not tuple".format(
        current_path(), type(obj)
    )

    def make_value(i: int) -> Any:
        with current_path_scope(current_path() + f"[{i}]"):
            return decode_it(obj[i], _type.__args__[0])

    return tuple([make_value(i) for i in range(len(obj))])


def is_generic_dict_predicate(_type: ANYTYPE) -> bool:
    return hasattr(_type, "__origin__") and _type.__origin__ is dict


def generic_dict_decoder(obj: Any, _type: ANYTYPE, decode_it: DECODEIT) -> Any:
    assert is_generic_dict_predicate(_type), "{} is not a dict".format(
        _type.__name__
    )
    assert isinstance(obj, dict), "{} is {} not dict".format(
        current_path(), type(obj)
    )

    def make_value(k: str) -> Any:
        with current_path_scope(current_path() + "." + k):
            return decode_it(obj[k], _type.__args__[1])

    return {k: make_value(k) for k in obj.keys()}


def is_union_predicate(_type: ANYTYPE) -> bool:
    return hasattr(_type, "__origin__") and _type.__origin__ is Union


def generic_union_decoder(
    obj: Any, _type: ANYTYPE, decode_it: DECODEIT
) -> Any:
    assert is_union_predicate(_type), "{} is not a union".format(
        _type.__name__
    )

    obj_type = type(obj)
    allowed_types = _type.__args__

    if obj_type in allowed_types:
        return decode_it(obj, obj_type)

    raise TypeError(f"Cannot decode {obj_type} as {allowed_types}")


def enum_decoder(obj: Any, _type: ANYTYPE, decode_it: DECODEIT) -> Any:
    assert issubclass(_type, Enum), "{} is not an enum".format(_type.__name__)
    assert isinstance(obj, str), "{} is {} not str".format(
        current_path(), type(obj)
    )

    return _type[obj]


def inherits_some_class_predicate(_type: ANYTYPE) -> bool:
    return hasattr(_type, "__bases__") and len(_type.__bases__) > 0


def generic_inheritance_decoder(
    obj: Any, _type: ANYTYPE, decode_it: DECODEIT
) -> Any:
    assert inherits_some_class_predicate(_type), "{} is not a class".format(
        _type.__name__
    )

    parent_types = _type.__bases__
    first_parent_type = parent_types[0]

    return _type(decode_it(obj, first_parent_type))


def is_new_type_predicate(_type: ANYTYPE) -> bool:
    return hasattr(_type, "__supertype__")


def generic_new_type_decoder(
    obj: Any, _type: ANYTYPE, decode_it: DECODEIT
) -> Any:
    assert is_new_type_predicate(_type), "{} is not a new type".format(
        _type.__name__
    )

    type(obj)
    supertype = _type.__supertype__

    return _type(decode_it(obj, supertype))


def is_any_type_predicate(_type: ANYTYPE) -> bool:
    return _type is Any


def any_type_decoder(obj: Any, _type: ANYTYPE, decode_it: DECODEIT) -> Any:
    return obj


def is_literal_predicate(_type: ANYTYPE) -> bool:
    return hasattr(_type, "__origin__") and _type.__origin__ is Literal


def generic_literal_decoder(
    obj: Any, _type: ANYTYPE, decode_it: DECODEIT
) -> Any:
    assert is_literal_predicate(_type), "{} is not a literal".format(
        _type.__name__
    )

    obj_type = type(obj)
    allowed_types = _type.__args__

    if obj in allowed_types:
        return decode_it(obj, obj_type)

    raise ValueError(
        f"Cannot decode {obj_type} as some of literal [{allowed_types}]"
    )


DEFAULT_DECODERS: Dict[ANYTYPE, TYPEDECODER] = {
    **{
        t: primitive_hook(t)
        for t in (
            int,
            float,
            str,
            bool,
            type(None),
        )
    },
    list: list_hook,
    dict: dict_hook,
    bytes: base64_to_bytes,
    datetime: iso_datetime_to_datetime,
    date: iso_date_to_date,
    time: iso_time_to_time,
    Decimal: decimal_from_str,
    UUID: uuid_from_str,
}

DEFAULT_DECODERS_BY_PREDICATE: List[Tuple[TYPEMATCHPREDICATE, TYPEDECODER]] = [
    (is_any_type_predicate, any_type_decoder),
    (is_dataclass_predicate, dataclass_from_primitive_dict),
    (is_generic_dataclass_predicate, generic_dataclass_from_primitive_dict),
    (is_generic_list_predicate, generic_list_decoder),
    (is_generic_dict_predicate, generic_dict_decoder),
    (is_union_predicate, generic_union_decoder),
    (is_generic_tuple_predicate, generic_tuple_decoder),
    (is_literal_predicate, generic_literal_decoder),
    (is_forward_ref_predicate, forward_ref_decoder),
    (is_string_forward_ref_predicate, string_forward_ref_decoder),
    # This must be before is_enum_predicate
    (is_new_type_predicate, generic_new_type_decoder),
    (is_enum_predicate, enum_decoder),
    # This must be last
    (inherits_some_class_predicate, generic_inheritance_decoder),
]


TYPEVAR_MAP = Dict[TypeVar, Type[Any]]

typevar_context_cxt_var = ContextVar[TYPEVAR_MAP](
    "typevar_context_cxt_var", default={}
)


@contextmanager
def typevar_context_scope(
    typevar_context: TYPEVAR_MAP,
) -> Generator[None, Any, None]:
    token = typevar_context_cxt_var.set(typevar_context)
    try:
        yield
    finally:
        typevar_context_cxt_var.reset(token)


def get_root_generic_type(_type: Type[Any]) -> Optional[Type[Any]]:
    if hasattr(_type, "__origin__"):
        if _type.__origin__ is Generic:
            return _type
        return get_root_generic_type(_type.__origin__)
    elif hasattr(_type, "__orig_bases__"):
        if len(_type.__orig_bases__) == 0:
            return _type
        if len(_type.__orig_bases__) > 1:
            raise TypeError(f"Cannot decode {type(_type)} with multiple bases")
        if _type.__orig_bases__[0] is Generic:
            return _type

        return get_root_generic_type(_type.__orig_bases__[0])
    else:
        return None


def decode(obj: Any, _type: Type[T]) -> T:
    if _type is None:
        _type = type(obj)

    with current_path_scope("$"):
        return raw_decode(
            obj, _type, DEFAULT_DECODERS, DEFAULT_DECODERS_BY_PREDICATE
        )
