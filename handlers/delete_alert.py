from sqlalchemy import select
from aiogram import F, types, Dispatcher
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from models.User import User
from models.Alert import Alert
from db import async_session

async def register_delete(dp: Dispatcher):
    @dp.message(Command("my_alerts"))
    async def cmd_my_alerts(message: types.Message):
        async with async_session() as session:

            stmt = select(Alert).join(User).where(
                User.telegram_id == message.from_user.id,
                Alert.is_active == True
            )
            res = await session.execute(stmt)
            alerts = res.scalars().all()

            if not alerts:
                await message.answer("У вас нет активных уведомлений.")
                return

            builder = InlineKeyboardBuilder()
            for alert in alerts:

                builder.row(types.InlineKeyboardButton(
                    text=f"❌ Удалить {alert.coin.upper()} (${alert.target_price})",
                    callback_data=f"del_{alert.id}"
                ))

            await message.answer("Ваши активные уведомления:", reply_markup=builder.as_markup())


    @dp.callback_query(F.data.startswith("del_"))
    async def delete_alert_handler(callback: types.CallbackQuery):
        alert_id = int(callback.data.split("_")[1])

        async with async_session() as session:
            alert = await session.get(Alert, alert_id)
            if alert:
                await session.delete(alert)
                await session.commit()
                await callback.answer("Уведомление удалено!")
                await callback.message.edit_text("Уведомление успешно удалено.")
            else:
                await callback.answer("Ошибка: уведомление не найдено.")