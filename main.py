import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()
from config import DEBUG, GUILD # ← DEV
print("🔑 TOKEN caricato:", "✅" if os.getenv("TOKEN") else "❌")
print("🛡️ GUILD_ID:", os.getenv("GUILD_ID"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=None, intents=intents)

# Blocco on_ready
@bot.event
async def on_ready():
    print(f"✅ Bot connesso come {bot.user}")

    # Caricamento dei COG
    try:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "__init__.py":
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"📦 Cog caricato: {filename}")
    except Exception as e:
        print(f"❌ Errore durante il caricamento dei cog: {e}")

    # Sync dei comandi
    try:
        if DEBUG:
            synced = await bot.tree.sync(guild=GUILD)
            print(f"🔧 [DEBUG] {len(synced)} comandi sincronizzati nella GUILD di test ({GUILD.id})")
        else:
            synced = await bot.tree.sync()
            print(f"🌐 [PROD] {len(synced)} comandi sincronizzati globalmente")

        for cmd in synced:
            print(f"🔸 {cmd.name}")
    except Exception as e:
        print(f"❌ Errore durante la sincronizzazione dei comandi: {e}")

    print("🚀 Avvio completato. Il bot è pronto!")

# Gestione errori dei comandi slash
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    print(f"❌ Errore comando slash: {error}")
    try:
        await interaction.response.send_message("❌ Si è verificato un errore nel comando.", ephemeral=True)
    except Exception:
        pass

#  Render
keep_alive()

# TOKEN + Controllo errori
token = os.getenv("TOKEN")
if not token:
    print("❌ TOKEN non trovato nel file .env")
    exit(1)
bot.run(token)
