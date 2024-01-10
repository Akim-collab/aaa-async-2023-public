import abc
import asyncio


class AbstractModel:
    @abc.abstractmethod
    def compute(self):
        ...


class Handler:
    def __init__(self, model: AbstractModel):
        self._model = model

    async def handle_request(self) -> None:
        await asyncio.to_thread(self._model.compute)
