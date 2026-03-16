import logging
from config import COIN_MAP, REVERSE_MAP

async def get_prices_multiple(session, coins: list):
    gecko_ids = [COIN_MAP.get(c.lower(), c.lower()) for c in coins]

    ids_query = ",".join(gecko_ids)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_query}&vs_currencies=usd"

    async with session.get(url) as response:
        if response.status != 200:
            logging.error(f"Ошибка API: {response.status}")
            return {}

        data = await response.json()
        result = {}
        for gecko_id, price_data in data.items():
            short_name = REVERSE_MAP.get(gecko_id, gecko_id)
            result[short_name] = price_data["usd"]

        return result