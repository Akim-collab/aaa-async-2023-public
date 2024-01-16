from asyncio import Task, ensure_future
from typing import Callable, Coroutine, Any


async def await_my_func(f: Callable[..., Coroutine] | Task | Coroutine) -> Any:
    if isinstance(f, Callable):
        f = f()

    if isinstance(f, Task):
        return await f

    if isinstance(f, Coroutine):
        task = ensure_future(f)
        return await task

    raise ValueError('Invalid argument')
