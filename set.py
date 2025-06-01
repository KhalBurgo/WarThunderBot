import discord
from discord.ext import commands
from discord import app_commands
from utils.preferences import load_preferences, save_preferences
from functions.search_for_clan import search_for_clan  # FUNZIONE GIUSTA!

class InputTagModal(discord.ui.Modal):
    def __init__(self, guild_id: int):
        super().__init__(title="Imposta Tag Squadriglia")
        self.guild_id = guild_id
        self.input = discord.ui.TextInput(
            label="Inserisci il TAG della squadriglia (es: WTI)",
            required=True,
            max_length=10
        )
        self.add_item(self.input)

    async def on_submit(self, interaction: discord.Interaction):
        tag = self.input.value.strip().upper()

        await interaction.response.defer(ephemeral=True, thinking=True)

        try:
            clan_data = await search_for_clan(tag)
            if not clan_data:
                await interaction.followup.send(f"❌ Nessuna squadriglia trovata con tag `{tag}`.", ephemeral=True)
                return

            prefs = load_preferences(self.guild_id)
            prefs["clan_tag"] = tag
            prefs["clan_name"] = clan_data["long_name"]
            save_preferences(self.guild_id, prefs)

            await interaction.followup.send(
                f"✅ Tag impostato su `{tag}`.\n"
                f"📛 Nome squadriglia: `{clan_data['long_name']}`",
                ephemeral=True
            )

        except Exception as e:
            await interaction.followup.send(f"❌ Errore durante il recupero della squadriglia: {e}", ephemeral=True)

class SetOptionSelect(discord.ui.Select):
    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        options = [
            discord.SelectOption(
                label="Tag Squadriglia",
                description="Imposta il tag della squadriglia",
                value="clan_tag"
            ),
        ]
        super().__init__(placeholder="Scegli cosa impostare...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        modal = InputTagModal(self.guild_id)
        await interaction.response.send_modal(modal)

class Set(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="set", description="Imposta il TAG squadriglia del server")
    async def set(self, interaction: discord.Interaction):
        view = discord.ui.View(timeout=60)
        view.add_item(SetOptionSelect(interaction.guild.id))
        await interaction.response.send_message("⚙️ Scegli cosa vuoi impostare:", view=view, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Set(bot))
