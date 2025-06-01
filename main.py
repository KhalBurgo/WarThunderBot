import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

load_dotenv()
from config import DEBUG, GUILD  # ← DEV

# Configurazione base del logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

logger.info(f"🔑 TOKEN caricato: {'✅' if os.getenv('TOKEN') else '❌'}")
logger.info(f"🛡️ GUILD_ID: {os.getenv('GUILD_ID')}")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Blocco on_ready
@bot.event
async def on_ready():
    logger.info(f"✅ Bot connesso come {bot.user}")

    # Caricamento dei COG
    try:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "__init__.py":
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logger.info(f"📦 Cog caricato: {filename}")
    except Exception as e:
        logger.error(f"❌ Errore durante il caricamento dei cog: {e}")

    # Sync dei comandi
    try:
        if DEBUG:
            synced = await bot.tree.sync(guild=GUILD)
            logger.info(f"🔧 [DEBUG] {len(synced)} comandi sincronizzati nella GUILD di test ({GUILD.id})")
        else:
            synced = await bot.tree.sync()
            logger.info(f"🌐 [PROD] {len(synced)} comandi sincronizzati globalmente")

        for cmd in synced:
            logger.info(f"🔸 {cmd.name}")
    except Exception as e:
        logger.error(f"❌ Errore durante la sincronizzazione dei comandi: {e}")

    # ✅ Avvia il task pianificato una sola volta
    from scheduler import start_daily_task
    start_daily_task(bot)

    logger.info("🚀 Avvio completato. Il bot è pronto!")

# Gestione errori dei comandi slash
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    logger.error(f"❌ Errore comando slash: {error}")
    try:
        await interaction.response.send_message("❌ Si è verificato un errore nel comando.", ephemeral=True)
    except Exception:
        pass

# TOKEN + Controllo errori
token = os.getenv("TOKEN")
if not token:
    logger.error("❌ TOKEN non trovato nel file .env")
    exit(1)
bot.run(token)
