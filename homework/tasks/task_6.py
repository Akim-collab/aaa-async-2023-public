import abc
import asyncio
from typing import Coroutine, Set


class AbstractLongTaskCreator(abc.ABC):
    @abc.abstractmethod
    def create_long_task(self) -> Coroutine:
        ...


class BackgroundCoroutinesWatcher:
    def __init__(self):
        self._running_tasks: Set[asyncio.Task] = set()

    def schedule_soon(self, coro: Coroutine) -> None:
        task = asyncio.create_task(coro)
        self._running_tasks.add(task)
        task.add_done_callback(lambda t: self._remove_from_running_task(t))

    def _remove_from_running_task(self, task: asyncio.Task) -> None:
        self._running_tasks.remove(task)

    async def close(self) -> None:
        for task in self._running_tasks:
            task.cancel()

        await asyncio.gather(*self._running_tasks, return_exceptions=True)


class FastHandlerWithLongBackgroundTask:
    def __init__(self, long_task_creator: AbstractLongTaskCreator, bcw: BackgroundCoroutinesWatcher):
        self._long_task_creator = long_task_creator
        self._bcw = bcw

    async def handle_request(self) -> None:
        coro = self._long_task_creator.create_long_task()
        self._bcw.schedule_soon(coro)

    async def close(self) -> None:
        await self._bcw.close()
