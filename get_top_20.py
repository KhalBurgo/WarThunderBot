from .fetch_clan_leaderboard import fetch_clan_leaderboard

async def get_top_20():
    return await fetch_clan_leaderboard()
