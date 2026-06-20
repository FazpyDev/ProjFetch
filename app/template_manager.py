import os
import shutil
import json
from colorama import Fore
from clifunctions import query, querySelector
from projectFuncs import createProject, configureProject

currentpath = os.path.dirname(os.path.realpath(__file__))
templatePath = os.path.join(currentpath, "templates")

def templatesFunc():
    chosenTemplate = chooseTemplate()
    chosentemplatePath = os.path.join(templatePath, chosenTemplate)

    options = querySelector(["Create Project", "Details"])

    match options:
        case 0:
            projectPath = createProject(chosentemplatePath)

            if not query(Fore.MAGENTA, "Would you like to use some plugins (if it has some) ? (Y//N)"):
                return
            
            configureProject(projectPath, chosentemplatePath)        

        case 1:
            TemplateDetailsPath = os.path.join(chosentemplatePath, "TemplateDetails.json")
            with open(TemplateDetailsPath, "r") as f:
                TemplateDetailsObject = json.load(f)

                for key, val in TemplateDetailsObject.items():
                    print(f"{key}: {val}")

def chooseTemplate():
    templates = os.listdir(templatePath)
    templateIndex = querySelector(templates)

    return templates[templateIndex]

def loadTemplatePluginConfig(chosentemplatePath):
    TemplatePluginConfigPath = os.path.join(chosentemplatePath, "TemplatePluginConfig.json")
    with open(TemplatePluginConfigPath, "r", encoding='utf-8') as f:
        return json.load(f)