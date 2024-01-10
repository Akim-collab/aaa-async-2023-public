async def magic_func() -> int:
    return 42


async def fix_this_code() -> int:
    result = await magic_func()
    return result
