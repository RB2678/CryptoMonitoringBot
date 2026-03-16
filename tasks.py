import asyncio
import logging
from db import async_session
from sqlalchemy import select
from models.Alert import Alert
from sqlalchemy.orm import joinedload
from utils.get_prices import get_prices_multiple

async def monitor_alerts(bot, session):
    while True:
        try:
            async with async_session() as db_session:
                stmt = select(Alert).where(Alert.is_active == True).options(joinedload(Alert.user))
                result = await db_session.execute(stmt)
                alerts = result.scalars().all()

                if not alerts:
                    await asyncio.sleep(60)
                    continue

                unique_coins = list(set(a.coin for a in alerts))
                prices = await get_prices_multiple(session, unique_coins)

                for alert in alerts:
                    current_price = prices.get(alert.coin)

                    if current_price and current_price >= alert.target_price:
                        await bot.send_message(
                            alert.user.telegram_id,
                            f"🔔 СРАБОТАЛО!\n{alert.coin.upper()} превысил цену ${alert.target_price}!\n"
                            f"Текущая цена: {current_price}"
                        )
                        alert.is_active = False

                await db_session.commit()
        except Exception as e:
            logging.error(f"Ошибка в фоновой задаче: {e}")

        await asyncio.sleep(60)