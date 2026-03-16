from aiogram import types
from aiogram.filters import Command
from sqlalchemy import select
from db import async_session
from models.User import User


async def register_start(dp):
    @dp.message(Command('start'))
    async def start_command(message: types.Message):
        async with async_session() as db_session:
            result = await db_session.execute(select(User).where(User.telegram_id == message.from_user.id))
            user = result.scalar_one_or_none()

            if not user:
                new_user = User(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                )

                db_session.add(new_user)
                await db_session.commit()

                text = "Вы зарегистрированы! Теперь я смогу отслеживать нужные вам криптовалюты."
            else:
                text = f"С возвращением, {message.from_user.full_name}!"

        await message.answer(text)