import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from functions.getData import getData
from functions.preferences import load_preferences
from functions.compare_utils import load_snapshot, save_snapshot, compare_snapshots
import discord

scheduler = AsyncIOScheduler()

def start_daily_task(bot):
    @scheduler.scheduled_job("cron", hour=16, minute=40)
    async def daily_point_update():
        print("⏰ Esecuzione giornaliera /pointchange")

        for guild in bot.guilds:
            prefs = load_preferences(guild.id)
            clan_name = prefs.get("clan_name")
            channel_id = prefs.get("log_channel")

            # Se mancano le preferenze richieste, salta
            if not clan_name or not channel_id:
                print(f"⚠️ Salto server {guild.name}: clan_name o channel_log mancante")
                continue

            try:
                encoded_name = clan_name.replace(" ", "%20")
                players, total_points = await getData(encoded_name)
                if not players:
                    print(f"❌ Dati non trovati per {clan_name}")
                    continue

                # Gestione cartelle per server Discord (guild.id)
                folder_path = f"Data/{guild.id}"
                os.makedirs(folder_path, exist_ok=True)
                snapshot_path = f"{folder_path}/{clan_name}.json"
                print(f"Salvataggio snapshot in: {snapshot_path}")

                new_data = {'players': players, 'total_points': total_points}
                old_data = load_snapshot(snapshot_path)

                if not old_data:
                    save_snapshot(snapshot_path, players, total_points)
                    print(f"📸 Snapshot salvato per {clan_name}")
                    continue

                changes = compare_snapshots(old_data, new_data)
                save_snapshot(snapshot_path, players, total_points)

                embed = discord.Embed(title=f"{clan_name} Points Update", color=0x00ff00)
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
