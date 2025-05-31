import discord
from discord.ext import commands
from discord import app_commands
from utils.preferences import load_preferences, save_preferences

# Modal per inserire testo (nome squadriglia o tag)
class InputModal(discord.ui.Modal):
    def __init__(self, guild_id, field_name, label):
        super().__init__(title=f"Imposta {field_name}")
        self.guild_id = guild_id
        self.field_name = field_name
        self.input = discord.ui.TextInput(label=label, required=True)
        self.add_item(self.input)

    async def on_submit(self, interaction: discord.Interaction):
        prefs = load_preferences(self.guild_id)
        prefs[self.field_name] = self.input.value
        save_preferences(self.guild_id, prefs)
        await interaction.response.send_message(f"✅ {self.field_name} impostato su: {self.input.value}", ephemeral=True)

# Select per scegliere cosa settare
class SetOptionSelect(discord.ui.Select):
    def __init__(self, guild_id):
        self.guild_id = guild_id
        options = [
            discord.SelectOption(label="Squadriglia", description="Imposta il nome della squadriglia", value="clan_name"),
            discord.SelectOption(label="Tag", description="Imposta il tag della squadriglia", value="clan_tag"),
            discord.SelectOption(label="Lingua", description="Imposta la lingua del server", value="language"),
        ]
        super().__init__(placeholder="Scegli cosa impostare...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        choice = self.values[0]

        if choice == "language":
            # Se è lingua, mostra il menu a tendina lingua
            view = LanguageSelectView(self.guild_id)
            await interaction.response.edit_message(content="Seleziona la lingua:", view=view)
        else:
            # Per nome e tag mostra modal input testo
            label = "Nome Squadriglia" if choice == "clan_name" else "Tag Squadriglia"
            modal = InputModal(self.guild_id, choice, label)
            await interaction.response.send_modal(modal)

class LanguageSelect(discord.ui.Select):
    def __init__(self, guild_id):
        self.guild_id = guild_id
        options = [
            discord.SelectOption(label="Italiano 🇮🇹", value="it"),
            discord.SelectOption(label="English 🇬🇧", value="en"),
            discord.SelectOption(label="Français 🇫🇷", value="fr"),
            discord.SelectOption(label="Español 🇪🇸", value="es"),
            discord.SelectOption(label="Русский 🇷🇺", value="ru"),
            discord.SelectOption(label="Deutsch 🇩🇪", value="de"),
        ]
        super().__init__(placeholder="Seleziona la lingua...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_lang = self.values[0]
        prefs = load_preferences(self.guild_id)
        prefs["language"] = selected_lang
        save_preferences(self.guild_id, prefs)
        await interaction.response.edit_message(content=f"✅ Lingua impostata su: {selected_lang}", view=None)

class LanguageSelectView(discord.ui.View):
    def __init__(self, guild_id):
        super().__init__(timeout=60)
        self.add_item(LanguageSelect(guild_id))

class Set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="set", description="Configura le preferenze del server")
    async def set(self, interaction: discord.Interaction):
        view = discord.ui.View()
        view.add_item(SetOptionSelect(interaction.guild.id))
        await interaction.response.send_message("Scegli cosa vuoi impostare:", view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Set(bot))
