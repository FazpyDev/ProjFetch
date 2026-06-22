import json
import os
from clifunctions import color_print
from colorama import Fore, Style
settings = {}

current_path = os.path.dirname(os.path.realpath(__file__))
template_path = os.path.join(current_path, "templates")
SETTINGS_FILE_PATH = "C:/Projects/ProjFetch/app/settings.json"

def initialize_setting_key(key_name, default_value):
    """Ensures a configuration key exists without wiping pre-existing user data."""
    if key_name not in settings:
        settings[key_name] = default_value      

def read_settings_file():
    """Reads configuration data directly from the system storage layer."""
    if not os.path.exists(SETTINGS_FILE_PATH):
        color_print(Fore.RED, "Settings.json does not exist!")
        return
    with open(SETTINGS_FILE_PATH, "r", encoding='utf-8') as f:
        try:
            loaded_data = json.load(f)
            print("Successfully loaded settings")
            
            # Mutate the existing dictionary object to preserve cross-file memory references
            settings.clear()
            settings.update(loaded_data)
        except Exception:
            print("Settings file is empty or invalid")
            settings.clear()

        initialize_setting_key('template-path', template_path)
        initialize_setting_key('projects-path', 'C:\Projects\ProjFetch\app\projects')    

def write_settings_file():
    """Commits current execution settings safely back down to local disk."""
    with open(SETTINGS_FILE_PATH, "w", encoding='utf-8') as f:
        json.dump(settings, f, indent=4)

def get_settings():
    """Exposes settings map cleanly to downstream execution processes."""
    read_settings_file()
    print(settings)
    return settings