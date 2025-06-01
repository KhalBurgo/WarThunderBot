import discord
from discord.ext import commands
from discord import app_commands
from functions.preferences import load_preferences

class ShowCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="show", description="Mostra le preferenze configurate per questo server.")
    async def show(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        prefs = load_preferences(guild_id)

        if not prefs:
            await interaction.response.send_message(
                "ℹ️ Nessuna preferenza trovata per questo server.", ephemeral=True
            )
            return

        embed = discord.Embed(
            title="⚙️ Preferenze del server",
            description=f"Configurazione per **{interaction.guild.name}**",
            color=discord.Color.blue()
        )

        pretty_names = {
            "clan_name": "🏷️ Squadriglia",
            "clan_tag": "📌 TAG",
            "language": "🌐 Lingua",
            "log_channel": "Report Channel"
        }

        for key, value in prefs.items():
            name = pretty_names.get(key, key)
            embed.add_field(name=name, value=str(value) if value else "❌ Non impostato", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ShowCommands(bot))
