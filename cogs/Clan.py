from discord.ext import commands
import discord
from functions.search_for_clan import search_for_clan
from functions.fetch_squadron_info import fetch_squadron_info

class Clan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="clan", description="Mostra informazioni su una squadriglia di War Thunder")
    @discord.app_commands.describe(
        squadron="Il tag della squadriglia (es: WTI)",
        type="Tipo di informazione: members, points o logs"
    )
    async def clan(self, interaction: discord.Interaction,
                   squadron: str,
                   type: str = ""):
        await interaction.response.defer(ephemeral=False)

        clan_data = await search_for_clan(squadron)
        if not clan_data:
            await interaction.followup.send("❌ Squadriglia non trovata.", ephemeral=True)
            return

        squadron_name = clan_data.get("long_name")
        embed_info = await fetch_squadron_info(squadron_name, type)

        # Ricrea embed nello stile di top20
        embed = discord.Embed(
            title=f"📋 Informazioni Squadriglia: {clan_data.get('long_name')} [{clan_data.get('short_name').upper()}]",
            description=f"Tag ufficiale: `{clan_data.get('tag') or 'N/A'}`",
            color=discord.Color.gold()
        )

        # Esempio struttura a colonne come /top20
        embed.add_field(name="🔢 Posizione", value=str(clan_data.get('position', 'N/A')), inline=True)
        embed.add_field(name="👥 Membri", value=str(clan_data.get('members', 'N/A')), inline=True)
        embed.add_field(name="⚔️ Battaglie", value=str(clan_data.get('battles', 'N/A')), inline=True)

        embed.add_field(name="🏆 Vittorie", value=str(clan_data.get('wins', 'N/A')), inline=True)
        embed.add_field(name="✈️ Uccisioni Aeree", value=str(clan_data.get('a_kills', 'N/A')), inline=True)
        embed.add_field(name="🚜 Uccisioni Terra", value=str(clan_data.get('g_kills', 'N/A')), inline=True)

        embed.add_field(name="💀 Morti", value=str(clan_data.get('deaths', 'N/A')), inline=True)
        embed.add_field(name="⏳ Tempo di gioco", value=str(clan_data.get('playtime', 'N/A')), inline=True)
        embed.add_field(name="⭐ Clan Rating", value=str(clan_data.get('clanrating', 'N/A')), inline=True)

        # Se fetch_squadron_info restituisce un embed o dati extra puoi aggiungerli qui
        if embed_info:
            for field in embed_info.fields:
                embed.add_field(name=field.name, value=field.value, inline=field.inline)

        embed.set_footer(text="📊 Dati da warthunder.com")
        embed.timestamp = discord.utils.utcnow()

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Clan(bot))