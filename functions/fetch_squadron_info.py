from .getData import getData
from .summary import generate_summary
from .embed_builder import create_embed

async def fetch_squadron_info(squadron_name, embed_type=None):
    squad = squadron_name.replace(" ", "%20")
    players, total_points = await getData(squad)
    if players is not None:
        summary = generate_summary(players, total_points)
        embed = create_embed(players, summary, squadron_name, embed_type)
        return embed
    else:
        return None
