import os
from clifunctions import *
import shutil
import json
from datetime import date

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
            #extract details and print them out
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

def loadTemplateModules(TemplatePluginConfig):
        modules = []
        TemplatePluginConfigValues = list(TemplatePluginConfig.values())
        for plugin in list(TemplatePluginConfigValues):
            module = plugin.get('module')
            if module:
                modules.append(module)

        return modules

def zipFiles(source):
    return shutil.make_archive(source, 'zip', source)

def updateTemplateDetails(filePath):

        NiceDate =  date.today().isoformat()
        templateDetails = {"creator": "Ian", "version": 0.01, "time-created": NiceDate}
        templateDetailsPath = os.path.join(filePath, "TemplateDetails.json")

        with open(templateDetailsPath, "w", encoding="utf-8") as f:
            json.dump(templateDetails, f, indent=4)
    
def getArguements(TemplatePluginConfigValues, selectedModuleIndex):
    pluginConfig = TemplatePluginConfigValues[selectedModuleIndex]
    arguementsNeeded = pluginConfig.get("arguments")

    passedArguments = []

    for argument in arguementsNeeded:
        argumentName = argument.get('name')
        argumentType = argument.get('type')

        argumentVal = input(f"Please enter a {argumentType} for {argumentName}: ")
        passedArguments.append(argumentVal)

    return passedArguments
