from discord.ext import commands
import discord
from Leaderboard import search_for_clan
from Data_Extractor import fetch_squadron_info
from config import GUILD  # ← Importa GUILD dal config

class Quick-Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# --- Finta funzione che simula la ricerca del clan ---
async def search_for_clan(sq_short_name: str):
    # Simula il risultato dell'API
    return {
        "long_name": f"Squadron {sq_short_name.upper()}",
    }

# --- Comando /quick-log ---
@bot.tree.command(name="quick-log", description="Registra un allarme per Logs o Points in questo canale")
@app_commands.describe(sq_name="Il tag breve della squadriglia", type="Logs o Points")
async def quick_log(interaction: discord.Interaction, sq_name: str, type: str = "Logs"):
    await interaction.response.defer(ephemeral=True)

    type = type.title()
    if type not in ("Logs", "Points"):
        await interaction.followup.send("Il tipo deve essere 'Logs' o 'Points'", ephemeral=True)
        return

    guild_id = interaction.guild_id
    channel_id = interaction.channel_id

    prefs = preference.load_preferences(guild_id)

    clan_data = await search_for_clan(sq_name.lower())
    if not clan_data:
        await interaction.followup.send("Squadriglia non trovata.", ephemeral=True)
        return

    long_name = clan_data["long_name"]

    prefs.setdefault(long_name, {})[type] = f"<#{channel_id}>"
    preference.save_preferences(guild_id, prefs)

    await interaction.followup.send(f"{type} per **{sq_name}** impostato su questo canale!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Clan(bot))