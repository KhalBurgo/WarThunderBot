# scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import tasks
from functions.getData import getData
from functions.preferences import load_preferences
from functions.compare_utils import load_snapshot, save_snapshot, compare_snapshots
import discord
import os
import json

scheduler = AsyncIOScheduler()

def start_daily_task(bot):
    @scheduler.scheduled_job("cron", hour=0, minute=10)
    async def daily_point_update():
        print("⏰ Esecuzione giornaliera /pointchange")

        for guild in bot.guilds:
            prefs = load_preferences(guild.id)
            squadron_name = prefs.get("clan_name")
            channel_id = prefs.get("log_channel")

            if not squadron_name or not channel_id:
                print(f"⚠️ Salto server {guild.name}: clan_name o channel_log mancante")
                continue

            try:
                players, total_points = await getData(squadron_name.replace(" ", "%20"))
                if not players:
                    print(f"❌ Dati non trovati per {squadron_name}")
                    continue

                snapshot_path = f"snapshots/{squadron_name.upper()}.json"
                new_data = {'players': players, 'total_points': total_points}
                old_data = load_snapshot(snapshot_path)

                if not old_data:
                    save_snapshot(snapshot_path, players, total_points)
                    print(f"📸 Snapshot salvato per {squadron_name}")
                    continue

                changes = compare_snapshots(old_data, new_data)
                save_snapshot(snapshot_path, players, total_points)

                embed = discord.Embed(title=f"{squadron_name.upper()} Points Update", color=0x00ff00)
                embed.add_field(name="Point Change", value=f"{old_data['total_points']} → {total_points} 📈", inline=False)

                if not changes:
                    embed.add_field(name="Player Changes", value="Nessuna variazione.", inline=False)
                else:
                    table = "Name                 Change    Now\n"
                    for name, emoji, delta, now in changes:
                        table += f"{name:<20} {emoji} {delta:<6} {now}\n"
                    embed.add_field(name="Player Changes", value=f"```\n{table}```", inline=False)

                channel = bot.get_channel(channel_id)
                if channel:
                    await channel.send(embed=embed)
                    print(f"📤 Inviato report in {channel.name} ({guild.name})")
                else:
                    print(f"❌ Canale ID {channel_id} non trovato in {guild.name}")

            except Exception as e:
                print(f"❌ Errore durante aggiornamento per {guild.name}: {e}")

    scheduler.start()
