from typing import Any, Callable, Coroutine, Sequence, TypeVar, cast

FuncType = TypeVar("FuncType", bound=Callable[..., object])
AsyncFuncType = TypeVar("AsyncFuncType", bound=Callable[..., Coroutine[Any, Any, object]])
AnyType = TypeVar("AnyType")
IfsType = TypeVar("IfsType", int, float, str)

Null = cast(Any, None)
Function = Callable[..., Any]
Some = set[AnyType] | Sequence[AnyType]
