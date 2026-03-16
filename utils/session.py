import aiohttp
import logging
from db import init_db

http_session: aiohttp.ClientSession = None

async def on_startup():
    logging.info("Бот запущен")

    await init_db()

    global http_session

    http_session = aiohttp.ClientSession()
    return http_session

async def on_shutdown():
    logging.info("Завершение работы")

    global http_session
    if http_session:
        await http_session.close()