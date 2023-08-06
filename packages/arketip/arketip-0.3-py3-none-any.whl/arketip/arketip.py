from collections.abc import Callable, Iterable, Mapping, MutableMapping, MutableSequence, MutableSet
from typing import Any, TypeGuard, TypeVar, get_args, get_origin, is_typeddict

from .cached import cached

T = TypeVar("T")


def cast_to_type(data: Any, t: type[T]) -> T:
    if is_type(data, t):
        return data
    else:
        raise TypeError(f"{data} is not of type {t}")


def is_type(data: Any, t: type[T]) -> TypeGuard[T]:
    return _guard(t, True)(data)


@cached(lambda x, y: hash((x, y)))
def _guard(t: type[T], covariant: bool) -> Callable[[Any], TypeGuard[T]]:
    origin = get_origin(t)

    if is_typeddict(t):
        gg = _guard(dict, covariant)
        kg = _guard(str, False)
        keys = t.__annotations__.keys()
        vgs = {k: _guard(v, False) for k, v in t.__annotations__.items()}

        def inner(data: Any) -> TypeGuard[T]:
            return (
                gg(data)
                and set(data.keys()) == set(keys)
                and all(kg(x) for x in keys)
                and all(vgs[x](data[x]) for x in keys)
            )

    elif origin is tuple:
        gg = _guard(origin, covariant)
        vgs2 = [_guard(x, covariant) for x in get_args(t)]

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and len(data) == len(vgs2) and all(vg(x) for vg, x in zip(vgs2, data))

    elif origin and issubclass(origin, Mapping):
        gg = _guard(origin, covariant)
        invariant = issubclass(origin, MutableMapping)
        kg, vg = (_guard(x, not invariant) for x in get_args(t))

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and all(kg(x) for x in data.keys()) and all(vg(x) for x in data.values())

    elif origin and issubclass(origin, Iterable):
        gg = _guard(origin, covariant)
        invariant = issubclass(origin, MutableSequence) or issubclass(origin, MutableSet)
        vt = get_args(t)[0]
        vg = _guard(vt, not invariant)

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and all(vg(x) for x in data)

    elif origin is type:
        gg = _guard(origin, covariant)
        vt = get_args(t)[0]

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and data is vt

    elif t is Any:

        def inner(data: Any) -> TypeGuard[T]:
            return covariant

    else:

        def inner(data: Any) -> TypeGuard[T]:
            return isinstance(data, t) if covariant else type(data) is t

    return inner
