import asyncio
from aiogram import Dispatcher, Bot
from config import BOT_TOKEN
from handlers.start import register_start
from utils.session import on_startup, on_shutdown
from handlers.alert_handler import register_alert_handler
from tasks import monitor_alerts
from handlers.get_prices import register_price
from handlers.delete_alert import register_delete
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot)

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    client_session = await on_startup()
    asyncio.create_task(monitor_alerts(bot, client_session))
    await register_delete(dp)
    await register_start(dp)
    await register_price(dp, client_session)

    await register_alert_handler(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await client_session.on_shutdown()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass