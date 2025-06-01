import aiohttp
from bs4 import BeautifulSoup

async def scraper(url: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=60) as response:
                content = BeautifulSoup(await response.text(), "lxml")
                return content
    except (aiohttp.ClientError, Exception) as e:
        print(f"Error raised in 'scraper' function: {e}")
        return None
