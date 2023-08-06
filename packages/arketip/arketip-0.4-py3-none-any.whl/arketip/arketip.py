from collections.abc import Callable, Iterable, Mapping, MutableMapping, MutableSequence, MutableSet, Sequence, Set
from typing import Any, TypeGuard, TypeVar, get_args, get_origin, is_typeddict

from .cached import cached

T = TypeVar("T")


def cast_to_type(data: Any, t: type[T], strict: bool = False) -> T:
    if is_type(data, t, strict):
        return data
    else:
        raise TypeError(f"{data} is not of type {t}")


def is_type(data: Any, t: type[T], strict: bool = False) -> TypeGuard[T]:
    return _guard(t, False, strict)(data)


def is_mutable_collection(t: type[T]) -> bool:
    if issubclass(t, Mapping):
        return issubclass(t, MutableMapping)
    elif issubclass(t, Sequence):
        return issubclass(t, MutableSequence)
    elif issubclass(t, Set):
        return issubclass(t, MutableSet)
    else:
        return False


def _arg_hash(t: type[T], invariant: bool, strict: bool) -> int:
    return hash((t, invariant, strict))


@cached(_arg_hash)
def _guard(t: type[T], invariant: bool, strict: bool) -> Callable[[Any], TypeGuard[T]]:
    origin = get_origin(t)

    if is_typeddict(t):
        gg = _guard(dict, invariant, strict)
        invariant = is_mutable_collection(dict)
        kg = _guard(str, False, strict)
        keys = t.__annotations__.keys()
        vgs = {k: _guard(v, False, strict) for k, v in t.__annotations__.items()}

        def inner(data: Any) -> TypeGuard[T]:
            return (
                gg(data)
                and set(data.keys()) == set(keys)
                and all(kg(x) for x in keys)
                and all(vgs[x](data[x]) for x in keys)
            )

    elif origin is tuple:
        gg = _guard(origin, invariant, strict)
        vgs2 = [_guard(x, invariant, strict) for x in get_args(t)]

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and len(data) == len(vgs2) and all(vg(x) for vg, x in zip(vgs2, data))

    elif origin and issubclass(origin, Mapping):
        gg = _guard(origin, invariant, strict)
        invariant = is_mutable_collection(origin)
        kg, vg = (_guard(x, invariant, strict) for x in get_args(t))

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and all(kg(x) for x in data.keys()) and all(vg(x) for x in data.values())

    elif origin and issubclass(origin, Iterable):
        gg = _guard(origin, invariant, strict)
        invariant = is_mutable_collection(origin)
        vt = get_args(t)[0]
        vg = _guard(vt, invariant, strict)

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and all(vg(x) for x in data)

    elif origin is type:
        gg = _guard(origin, invariant, strict)
        vt = get_args(t)[0]

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and data is vt

    elif t is Any:

        def inner(data: Any) -> TypeGuard[T]:
            return not (strict and invariant)

    else:

        def inner(data: Any) -> TypeGuard[T]:
            return type(data) is t if (strict and invariant) else isinstance(data, t)

    return inner
