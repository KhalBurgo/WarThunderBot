def parse_clan_data(data):
    if data.get("status") != "ok":
        return []

    clans = []
    for entry in data.get("data", []):
        clan_info = {
            "position": entry.get("pos"),
            "long_name": entry.get("name"),
            "short_name": entry.get("tagl"),
            "tag": entry.get("lastPaidTag")[1:-1] if entry.get("lastPaidTag") else None,
            "members": entry.get("members_cnt"),
            "wins": entry.get("astat", {}).get("wins_hist"),
            "battles": entry.get("astat", {}).get("battles_hist"),
            "a_kills": entry.get("astat", {}).get("akills_hist"),
            "g_kills": entry.get("astat", {}).get("gkills_hist"),
            "deaths": entry.get("astat", {}).get("deaths_hist"),
            "playtime": entry.get("astat", {}).get("ftime_hist"),
            "clanrating": entry.get("astat", {}).get("dr_era5_hist"),
        }
        clans.append(clan_info)

    return clans
