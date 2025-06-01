import discord
from discord.ext import commands
from functions.getData import getData
from functions.compare_utils import load_snapshot, save_snapshot, compare_snapshots
import os

class PointChangeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pointchange")
    async def point_change(self, ctx, *, squadron: str):
        squad_encoded = squadron.replace(" ", "%20")
        players, total_points = await getData(squad_encoded)
        if not players:
            return await ctx.send("Errore nel recupero dati.")

        snapshot_path = f"snapshots/{squadron.upper()}.json"
        new_data = {'players': players, 'total_points': total_points}
        old_data = load_snapshot(snapshot_path)

        if not old_data:
            save_snapshot(snapshot_path, players, total_points)
            return await ctx.send(f"Snapshot salvato per {squadron.upper()}. Ripeti il comando più tardi per vedere i cambiamenti.")

        changes = compare_snapshots(old_data, new_data)

        # Embed
        embed = discord.Embed(title=f"{squadron.upper()} Points Update", color=0x00ff00)
        embed.add_field(name="Point Change", value=f"{old_data['total_points']} → {total_points} 📈", inline=False)

        if not changes:
            embed.add_field(name="Player Changes", value="Nessuna variazione.", inline=False)
        else:
            table = "Name                 Change    Now\n"
            for name, emoji, delta, now in changes:
                table += f"{name:<20} {emoji} {delta:<6} {now}\n"
            embed.add_field(name="Player Changes", value=f"```\n{table}```", inline=False)

        await ctx.send(embed=embed)
        save_snapshot(snapshot_path, players, total_points)

async def setup(bot):
    await bot.add_cog(PointChangeCog(bot))
