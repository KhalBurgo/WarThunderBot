import discord
from discord.ext import commands
from functions.getData import getData
from functions.compare_utils import load_snapshot, save_snapshot, compare_snapshots
from functions.search_for_clan import search_for_clan
import os

class PointChangeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pointchange")
    async def point_change(self, ctx, tag: str):
        tag = tag.upper().strip()
        clan_data = await search_for_clan(tag)

        if not clan_data:
            return await ctx.send(f"❌ Squadriglia con tag `{tag}` non trovata.")

        clan_name = clan_data.get("long_name")
        squad_encoded = clan_name.replace(" ", "%20")
        players, total_points = await getData(squad_encoded)

        if not players:
            return await ctx.send("❌ Errore nel recupero dei dati della squadriglia.")

        # Creazione percorso cartella Data/<guild_id>/
        folder_path = f"Data/{ctx.guild.id}"
        os.makedirs(folder_path, exist_ok=True)
        snapshot_path = f"{folder_path}/{clan_name}.json"
        new_data = {'players': players, 'total_points': total_points}
        old_data = load_snapshot(snapshot_path)

        if not old_data:
            save_snapshot(snapshot_path, players, total_points)
            return await ctx.send(f"📸 Primo snapshot salvato per **{clan_name}**.\nRiesegui il comando più tardi per vedere i cambiamenti.")

        changes = compare_snapshots(old_data, new_data)

        # Embed
        embed = discord.Embed(title=f"{clan_name} - Aggiornamento Punti", color=0x00ff00)
        embed.add_field(name="📊 Punti Totali", value=f"{old_data['total_points']} → {total_points} 📈", inline=False)

        if not changes:
            embed.add_field(name="👥 Variazioni Giocatori", value="Nessuna variazione.", inline=False)
        else:
            table = "Name                 Change    Now\n"
            for name, emoji, delta, now in changes:
                table += f"{name:<20} {emoji} {delta:<6} {now}\n"
            embed.add_field(name="👥 Variazioni Giocatori", value=f"```\n{table}```", inline=False)

        await ctx.send(embed=embed)
        save_snapshot(snapshot_path, players, total_points)

async def setup(bot):
    await bot.add_cog(PointChangeCog(bot))
