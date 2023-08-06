import json
import os

def load_config_from_file(file):
    if os.path.exists(file):
        with open(file, encoding="utf8") as f:
            config = json.load(f)
        return config
    return None

def load_config_from_text(text):
    config = json.loads(text)
    return config

def save_config_dict(file, dict):
    with open(file, "w", encoding='utf8') as f:
        json.dump(dict, f, indent=4)

def save_config_text(file, text):
    with open(file, "w", encoding='utf8') as f:
        f.write(text)
