from aiogram import types
from aiogram.filters import Command
from utils.get_prices import get_prices_multiple

async def register_price(dp, session):
    @dp.message(Command('btc', 'eth', 'sol', 'dot'))
    async def cmd_crypto_price(message: types.Message):
        coin_id = message.text.replace("/", "").lower()

        prices = await get_prices_multiple(session, [coin_id])
        price = prices.get(coin_id)

        if price:
            await message.answer(f"Текущая цена {coin_id.upper()}: ${price}")
        else:
            await message.answer("Не удалось получить цену. Попробуйте позже.")