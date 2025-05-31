import aiohttp
import json
import logging
from .parse_clan_data import parse_clan_data

async def fetch_clan_leaderboard(page=1):
    url = f"https://warthunder.com/en/community/getclansleaderboard/dif/_hist/page/{page}/sort/dr_era5"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    try:
                        data = json.loads(text)
                        return parse_clan_data(data)
                    except json.JSONDecodeError as e:
                        logging.error(f"Errore parsing JSON: {e}")
                        return []
                else:
                    logging.warning(f"Errore HTTP pagina {page}: {response.status}")
                    return []
        except Exception as e:
            logging.error(f"Errore durante la richiesta pagina {page}: {e}")
            return []
