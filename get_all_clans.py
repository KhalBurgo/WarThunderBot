import asyncio
from .fetch_clan_leaderboard import fetch_clan_leaderboard

async def get_all_clans():
    max_pages = 1000
    tasks = [fetch_clan_leaderboard(page) for page in range(1, max_pages + 1)]
    results = await asyncio.gather(*tasks)
    return results
