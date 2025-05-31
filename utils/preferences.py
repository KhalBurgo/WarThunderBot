import os
import json

def preferences_path(guild_id):
    return f"preferences/{guild_id}-preferences.json"

def load_preferences(guild_id):
    path = preferences_path(guild_id)
    if not os.path.exists(path):
        # Se non esiste, crea un file con preferenze di default
        default_prefs = {
            "clan_name": None,
            "language": "it",
            "prefix": "!"
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(default_prefs, f, indent=4)
        print(f"📁 Creato file di configurazione per il server {guild_id}: {path}")
        return default_prefs

    # Altrimenti carica le preferenze esistenti
    with open(path, "r") as f:
        return json.load(f)

def save_preferences(guild_id, prefs):
    path = preferences_path(guild_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(prefs, f, indent=4)
        