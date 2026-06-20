import os
import shutil
import json
from colorama import Fore
from clifunctions import query, querySelector
from projectFuncs import createProject, configureProject

current_path = os.path.dirname(os.path.realpath(__file__))
template_path = os.path.join(current_path, "templates")

def manage_templates():
    chosen_template = choose_template()
    chosen_template_path = os.path.join(template_path, chosen_template)

    options = querySelector(["Create Project", "Details"])

    match options:
        case 0:
            project_path = createProject(chosen_template_path)

            if not query(Fore.MAGENTA, "Would you like to use some plugins (if it has some)? (Y/N)"):
                return
            
            configureProject(project_path, chosen_template_path)        

        case 1:
            details_path = os.path.join(chosen_template_path, "TemplateDetails.json")
            with open(details_path, "r", encoding="utf-8") as f:
                details_object = json.load(f)

                for key, val in details_object.items():
                    print(f"{key}: {val}")

def choose_template():
    templates = os.listdir(template_path)
    template_index = querySelector(templates)

    return templates[template_index]

def load_template_plugin_config(chosen_template_path):
    config_path = os.path.join(chosen_template_path, "TemplatePluginConfig.json")
    with open(config_path, "r", encoding='utf-8') as f:
        return json.load(f)