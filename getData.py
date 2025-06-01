from .scraper import scraper
from .parser import parser

BASE_URL = 'https://warthunder.com/en/community/claninfo/'

async def getData(squad):
    url = BASE_URL + squad
    content = await scraper(url)
    if content:
        return parser(content)
    return None, 0

