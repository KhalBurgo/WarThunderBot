import discord
import os

# 🔧 Modalità Debug
DEBUG = True  # Metti a False per la produzione

# 🧪 GUILD di test (solo per DEBUG)
GUILD_ID = int(os.getenv("GUILD_ID", 0))  # inserisci nel .env
GUILD = discord.Object(id=GUILD_ID)
