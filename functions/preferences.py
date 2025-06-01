import os
import json

def preferences_path(guild_id):
    # Ora il file preferenze sarà dentro Data/<guild_id>/cartella
    return f"Data/{guild_id}/Settings.json"

def load_preferences(guild_id):
    path = preferences_path(guild_id)
    if not os.path.exists(path):
        default_prefs = {
            "clan_name": None,
            "clan_tag": None,
            "language": None,
            "log_channel": None
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default_prefs, f, indent=4)
        print(f"📁 Creato file di configurazione per il server {guild_id}: {path}")
        return default_prefs

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Errore nel caricamento preferenze server {guild_id}: {e}")
        return {}

def save_preferences(guild_id, prefs):
    path = preferences_path(guild_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(prefs, f, indent=4)
    except Exception as e:
        print(f"❌ Errore nel salvataggio preferenze server {guild_id}: {e}")
     