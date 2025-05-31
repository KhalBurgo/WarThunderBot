from discord.ext import commands
import discord
import aiohttp
from config import GUILD
from datetime import datetime
import os

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="player",
        description="Mostra i profili War Thunder e ThunderSkill del giocatore"
    )
    @discord.app_commands.describe(nomeplayer="Il nickname del giocatore su War Thunder")
    @discord.app_commands.guilds(GUILD)
    async def player(self, interaction: discord.Interaction, nomeplayer: str):
        await interaction.response.defer()

        wt_url = f"https://warthunder.com/en/community/userinfo?nick={nomeplayer}"
        ts_url = f"https://thunderskill.com/en/stat/{nomeplayer}"

        # Verifica se il profilo War Thunder esiste
        async with aiohttp.ClientSession() as session:
            async with session.get(wt_url) as response:
                html = await response.text()
                if "Page not found on server." in html:
                    await interaction.followup.send(f"❌ Giocatore **{nomeplayer}** non trovato.")
                    return

        embed = discord.Embed(
            title=f"Profilo di {nomeplayer}",
            description=(
                f"🌐 [Profilo War Thunder]({wt_url})\n\n"
                f"📊 [Profilo ThunderSkill]({ts_url})"
            ),
            color=discord.Color.blue()
        )

        # Avatar statico
        static_avatar_url = "attachment://default.jpg"  # percorso nel messaggio Discord
        embed.set_thumbnail(url=static_avatar_url)

        # Footer con data e ora
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        embed.set_footer(text=f"Richiesta il {now}")

        # Invio con file allegato
        file = discord.File("avatar/default.jpg", filename="default.jpg")
        await interaction.followup.send(embed=embed, file=file)

async def setup(bot):
    await bot.add_cog(Player(bot))