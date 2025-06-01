import discord
from discord.ext import commands
from discord import app_commands
from functions.preferences import load_preferences, save_preferences
from functions.search_for_clan import search_for_clan

# Modal per inserire il tag della squadriglia
class InputModal(discord.ui.Modal):
    def __init__(self, guild_id):
        super().__init__(title="Imposta Tag Squadriglia")
        self.guild_id = guild_id
        self.input = discord.ui.TextInput(label="Inserisci il TAG della squadriglia (es: WTI)", required=True)
        self.add_item(self.input)

    async def on_submit(self, interaction: discord.Interaction):
        prefs = load_preferences(self.guild_id)
        tag = self.input.value.strip().upper()
        prefs["clan_tag"] = tag

        # Recupera il nome squadriglia online
        clan_data = await search_for_clan(tag)
        if clan_data:
            prefs["clan_name"] = clan_data.get("long_name", "")
            save_preferences(self.guild_id, prefs)
            await interaction.response.send_message(
                f"✅ Tag impostato su: `{tag}`\n📛 Nome squadriglia: **{prefs['clan_name']}**",
                ephemeral=True
            )
        else:
            save_preferences(self.guild_id, prefs)
            await interaction.response.send_message(
                f"⚠️ Tag impostato su: `{tag}`, ma la squadriglia non è stata trovata online.",
                ephemeral=True
            )

# Select principale per scegliere cosa configurare
class SetOptionSelect(discord.ui.Select):
    def __init__(self, guild_id):
        self.guild_id = guild_id
        options = [
            discord.SelectOption(label="Tag Squadriglia", description="Imposta il tag (es: WTI)", value="clan_tag"),
            discord.SelectOption(label="Lingua", description="Imposta la lingua del server", value="language"),
            discord.SelectOption(label="Canale Andamento", description="Scegli il canale per i log", value="log_channel"),
        ]
        super().__init__(placeholder="Scegli cosa impostare...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        choice = self.values[0]

        if choice == "language":
            view = LanguageSelectView(self.guild_id)
            await interaction.response.edit_message(content="🌍 Seleziona la lingua:", view=view)

        elif choice == "clan_tag":
            modal = InputModal(self.guild_id)
            await interaction.response.send_modal(modal)

        elif choice == "log_channel":
            channels = interaction.guild.text_channels
            view = ChannelSelectView(self.guild_id, channels)
            await interaction.response.edit_message(content="📢 Seleziona il canale per l'andamento:", view=view)

# Selettore lingua
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

# Selettore canale testo
class ChannelSelect(discord.ui.Select):
    def __init__(self, guild_id, channels):
        self.guild_id = guild_id
        options = [
            discord.SelectOption(label=channel.name, value=str(channel.id))
            for channel in channels if isinstance(channel, discord.TextChannel)
        ]
        super().__init__(placeholder="Seleziona un canale testuale...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_channel_id = int(self.values[0])
        prefs = load_preferences(self.guild_id)
        prefs["log_channel"] = selected_channel_id
        save_preferences(self.guild_id, prefs)

        channel = interaction.guild.get_channel(selected_channel_id)
        await interaction.response.edit_message(
            content=f"✅ Canale log impostato su: {channel.mention}",
            view=None
        )

class ChannelSelectView(discord.ui.View):
    def __init__(self, guild_id, channels):
        super().__init__(timeout=60)
        self.add_item(ChannelSelect(guild_id, channels))

# Comando principale
class Set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="set", description="Configura le preferenze del server")
    async def set(self, interaction: discord.Interaction):
        view = discord.ui.View()
        view.add_item(SetOptionSelect(interaction.guild.id))
        await interaction.response.send_message("⚙️ Scegli cosa vuoi impostare:", view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Set(bot))
