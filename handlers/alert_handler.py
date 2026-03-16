from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import Command, CommandObject
from sqlalchemy import select
from models.Alert import Alert
from db import async_session
from models.User import User
from config import COIN_MAP

async def register_alert_handler(dp: Dispatcher):
    @dp.message(Command('alert'))
    async def cmd_alert(message: types.Message, command: CommandObject):
        try:
            args = (command.args or "").split(' ')
            coin = args[0].lower()
            target_price = float(args[1])

        except (IndexError, ValueError):
            await message.answer("Неверный формат: введите команду в формате: "
                                 "/alert <монета> <цена>. "
                                 "Пример: /alert btc 60000")
            return

        if coin not in COIN_MAP:
            supported = ", ".join(COIN_MAP.keys())
            await message.answer(f"Монета не поддерживается. Доступные: {supported}")
            return

        async with async_session() as db_session:
            res = await db_session.execute(select(User).where(User.telegram_id == message.from_user.id))
            user = res.scalar_one_or_none()

            if not user:
                await message.answer("Отправьте команду /start для регистрации")
                return

            new_alert = Alert(
                user_id=user.id,
                coin=coin,
                target_price=target_price
            )

            db_session.add(new_alert)
            await db_session.commit()

        await message.answer(f"Принято! Когда цена {coin.upper()} достигнет "
                             f"${target_price}, я пришлю уведомление.")