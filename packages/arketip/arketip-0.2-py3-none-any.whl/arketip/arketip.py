from collections.abc import Callable, Iterable, Mapping
from typing import Any, TypeGuard, TypeVar, get_args, get_origin, is_typeddict

from .cached import cached

T = TypeVar("T")


def autocast(data: Any, t: type[T]) -> T:
    if autoguard(t)(data):
        return data
    else:
        raise TypeError(f"{data} is not of type {t}")


@cached(lambda x: hash(x))
def autoguard(t: type[T]) -> Callable[[Any], TypeGuard[T]]:
    origin = get_origin(t)

    if is_typeddict(t):
        keys = t.__annotations__.keys()
        kg = autoguard(dict[str, Any])
        vgs = {k: autoguard(v) for k, v in t.__annotations__.items()}

        def inner(data: Any) -> TypeGuard[T]:
            return kg(data) and set(data.keys()) == set(keys) and all(vgs[x](data[x]) for x in keys)

    elif origin and issubclass(origin, Mapping):
        gt = origin
        gg = autoguard(gt)
        kg, vg = (autoguard(x) for x in get_args(t))

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and all(kg(x) for x in data.keys()) and all(vg(x) for x in data.values())

    elif origin is tuple:
        vgs2 = [autoguard(x) for x in get_args(t)]

        def inner(data: Any) -> TypeGuard[T]:
            return isinstance(data, tuple) and len(data) == len(vgs2) and all(vg(x) for vg, x in zip(vgs2, data))

    elif origin and issubclass(origin, Iterable):
        gt = origin
        gg = autoguard(gt)
        vt = get_args(t)[0]
        vg = autoguard(vt)

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and all(vg(x) for x in data)

    elif origin is type:
        vt = get_args(t)[0]

        def inner(data: Any) -> TypeGuard[T]:
            return isinstance(data, type) and data == vt

    elif t is Any:

        def inner(data: Any) -> TypeGuard[T]:
            return True

    else:

        def inner(data: Any) -> TypeGuard[T]:
            return isinstance(data, t)

    return inner
