import asyncio
from dataclasses import dataclass
from typing import Awaitable


@dataclass
class Ticket:
    number: int
    key: str


async def coroutines_execution_order(coros: list[Awaitable[Ticket]]) -> str:
    results = await asyncio.gather(*coros)

    sorted_results = sorted(results, key=lambda ticket: ticket.number)

    result_str = ''.join(ticket.key for ticket in sorted_results)

    return result_str
