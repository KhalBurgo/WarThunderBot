import discord

def create_embed(players, summary, squadron_name, embed_type=None):
    embed = discord.Embed(title=f"Squadron Info: {squadron_name}",
                          color=0x00ff00)

    if embed_type in ["members", "logs"]:
        players_sorted = sorted(players, key=lambda x: x['points'], reverse=True)

        # "logs" mostra solo i nomi, senza punti
        if embed_type == "logs":
            player_list = [player['name'] for player in players_sorted]
        else:
            player_list = [
                player['name'].replace('_', '\\_') + f": {player['points']} points"
                for player in players_sorted
            ]

        player_chunks = []
        current_chunk = ""

        for player in player_list:
            if len(current_chunk) + len(player) + 1 > 1024:
                player_chunks.append(current_chunk.strip())
                current_chunk = player + "\n"
            else:
                current_chunk += player + "\n"

        if current_chunk:
            player_chunks.append(current_chunk.strip())

        for chunk in player_chunks:
            embed.add_field(name="\u00A0", value=chunk, inline=False)

    elif embed_type == "points":
        embed.add_field(name="Total Points", value=summary['total_points'], inline=False)
    else:
        embed.add_field(name="Total Members", value=summary['total_members'], inline=False)
        embed.add_field(name="Total Points", value=summary['total_points'], inline=False)

        players_sorted = sorted(players, key=lambda x: x['points'], reverse=True)
        player_list = [
            player['name'].replace('_', '\\_') + f": {player['points']} points"
            for player in players_sorted
        ]

        player_chunks = []
        current_chunk = ""

        for player in player_list:
            if len(current_chunk) + len(player) + 1 > 1024:
                player_chunks.append(current_chunk.strip())
                current_chunk = player + "\n"
            else:
                current_chunk += player + "\n"

        if current_chunk:
            player_chunks.append(current_chunk.strip())

        for chunk in player_chunks:
            embed.add_field(name="\u00A0", value=chunk, inline=False)

    return embed
