import asyncio
from functools import wraps
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
from pyrogram.types import Message
from config import *

executor = ThreadPoolExecutor(max_workers=cpu_count() * 5)

def async_wrap(func_):
    @wraps(func_)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
                executor, lambda: func_(*args, **kwargs)
            )
    return wrapper

def sudo_wrap(func_):
    @wraps(func_)
    async def wrapper_f(client, message: Message):
        if not (message or message.from_user):
            return
        if (message.from_user.is_self or (SUDO_USERS and SUDO_USERS == "all")):
            return await func_(client, message)
        elif SUDO_USERS and message.from_user.id in SUDO_USERS:
            return await func_(client, message)
    return wrapper_f


def monkeypatch(obj):
    def wrapper(sub):
        for (func_name, func_) in sub.__dict__.items():
            if func_name[:2] != "__":
                setattr(obj, func_name, func_)
        return sub
    return wrapper