import discord
from discord.ext import commands
from functions.preferences import load_preferences, save_preferences

class SetChannelPoints(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="setchannelpoints", description="Imposta il canale corrente per l'andamento delle squadriglie")
    async def set_channel_points(self, interaction: discord.Interaction):
        current_channel = interaction.channel
        guild_id = interaction.guild.id

        if not isinstance(current_channel, discord.TextChannel):
            await interaction.response.send_message("❌ Questo comando può essere usato solo in un canale testuale.", ephemeral=True)
            return

        prefs = load_preferences(guild_id)
        prefs["log_channel"] = current_channel.id
        save_preferences(guild_id, prefs)

        await interaction.response.send_message(f"✅ Il canale {current_channel.mention} è stato impostato per l'andamento delle squadriglie.")

async def setup(bot):
    await bot.add_cog(SetChannelPoints(bot))
