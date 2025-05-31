import discord
from discord.ext import commands
from discord import app_commands

from functions import get_top_20  # importa la funzione da functions

class Top20(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="top20", description="Mostra le prime 20 squadriglie War Thunder")
    async def top20(self, interaction: discord.Interaction):
        await interaction.response.defer()  # opzionale: mostra "pensando..."

        try:
            clans = await get_top_20.get_top_20()
            if not clans:
                await interaction.followup.send("❌ Errore nel recupero dei dati.")
                return

            description = ""
            for clan in clans:
                description += f"**{clan['position'] + 1}**. [{clan['short_name'].upper()}] {clan['long_name']} – Rating: **{clan['clanrating']}**\n"

            embed = discord.Embed(
                title="🏆 Top 20 Clan War Thunder",
                description=description,
                color=discord.Color.gold()
            )
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send("❌ Errore durante l'esecuzione del comando.")
            print(f"[top20] Errore: {e}")

async def setup(bot):
    await bot.add_cog(Top20(bot))
