import logging
from . import get_all_clans
import functions  # ✅ importa l'intero modulo per accedere a cache condivisa

async def search_for_clan(short_name, second_iter=False):
    if functions.cache is None:  # ✅ accedi alla cache condivisa
        functions.cache = await get_all_clans.get_all_clans()  # ✅ aggiorna la cache

    for page in functions.cache:
        if page:
            for clan in page:
                if clan["short_name"] == short_name.lower():
                    logging.info(f"{short_name} trovato in cache")
                    return clan

    if not second_iter:
        logging.warning(f"{short_name} non trovato. Riprovo aggiornando la cache.")
        functions.cache = await get_all_clans.get_all_clans()
        return await search_for_clan(short_name, second_iter=True)

    logging.error(f"{short_name} non trovato dopo due tentativi.")
    return None