import json
import os

def load_snapshot(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_snapshot(file_path, players, total_points):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump({'players': players, 'total_points': total_points}, f, ensure_ascii=False, indent=2)

def compare_snapshots(old_data, new_data):
    result = []

    old_players = {p['name']: p['points'] for p in old_data['players']}
    new_players = {p['name']: p['points'] for p in new_data['players']}

    for name, new_pts in new_players.items():
        old_pts = old_players.get(name, 0)
        change = new_pts - old_pts
        if change != 0:
            emoji = "🌲" if change > 0 else "🔻"
            result.append((name, emoji, abs(change), new_pts))

    result.sort(key=lambda x: x[2], reverse=True)
    return result
