import requests
import requests.exceptions
import json
import os
import shutil
import zipfile
from datetime import date
import importlib
import importlib.util

from colorama import Fore, Style

#FUNCTIONS

#CLI functions

def query(color, outputText):
    color_print(color, outputText)
    userInput = input()
    return userInput.lower().startswith('y')

def querySelector(queryList):
    print("Please select an option: ")
    for i, query in enumerate(queryList):
        print(f"{i+1}. {query}")
    
    userInput = input()
    return int(userInput) -1

def color_print(color, text):
    print(color + text + Style.RESET_ALL)

#BACKEND functions

def attemptRequest(templateName):
    try:
        r = requests.get(f"http://127.0.0.1:5000/download?templateName={templateName}", stream=True)
        r.raise_for_status()
    except(requests.exceptions.Timeout):
        if query(Fore.RED, "There has been an issue with the server, would you like to try again? (Y/N): "):
            attemptRequest(templateName)
        else:
            global running
            running = False
    else:
        return r

def downloadFile(path, r):
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

def downloadTemplate():
    templateName = input("Enter the name of the template: ").lower()
    path = f"{templateName}.zip"
    r = attemptRequest(templateName)

    if running:
        if r.status_code == 201:

            downloadFile(path, r)
            color_print(Fore.GREEN, f"Successfully downloaded: {templateName.lower()}.zip")
        #    os.makedirs(templateName, exist_ok=True)
            target_path = os.path.join(templatePath,templateName)
            shutil.unpack_archive(path, target_path)
            os.remove(path)
        else:
            data = r.json()
            color_print(Fore.RED, f"ERROR: {data.get('message')}")

def uploadFile(path, fileName):
    with open(path, "rb") as f:
        r = requests.post(
            f"http://127.0.0.1:5000/upload?name={fileName}",
            files={"file": f}
        )

def uploadTemplate():
    filePath = input("Enter folder path: ")

    if not os.path.exists(filePath):
        print("Path does not exist")
        return

    fileName = input("Template name: ")

    if filePath.endswith(".zip"):
        print("Most be a folder!")
        return
    else:
        if not os.path.isdir(filePath):
            print("You must provide a folder (not a file)")
            return

        #Create/modify TemplateDetails.json
        updateTemplateDetails(filePath)
    
        zip_path = zipFiles(filePath)
    
    uploadFile(zip_path, fileName)
    os.remove(zip_path)

#MODE Functions

def exit():
    global running
    running = False
    color_print(Fore.BLUE, "Exiting.. Goodbye!")

def settingsFunc():
    settingSubjectIndex = querySelector(["Paths"])

    match settingSubjectIndex:
        case 0:
            pathSettings = getPathSettings()
            pathSubjectIndex = querySelector(pathSettings)
            selectedPathKey = settingKeys[pathSubjectIndex]

            newVal = input(f"What value do you want to chance {selectedPathKey} to?: ")
            settings.update({selectedPathKey: newVal})

def configureProject(projectPath, chosentemplatePath):
        TemplatePluginConfig = loadTemplatePluginConfig(chosentemplatePath)
        TemplatePluginConfigValues = list(TemplatePluginConfig.values())

        modules = loadTemplateModules(TemplatePluginConfig)

        selectedModuleIndex = querySelector(modules)
        selectedModule = modules[selectedModuleIndex]

        plugin_directory = os.path.join(chosentemplatePath, "plugins")
        plugin_path = os.path.join(plugin_directory, selectedModule + ".py")
        spec = importlib.util.spec_from_file_location(
            selectedModule, plugin_path
        )

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        passedArguments = getArguements(TemplatePluginConfigValues,  selectedModuleIndex)

        module.run(projectPath, *passedArguments)

def createProject(chosentemplatePath):
        projectName = input("Enter project name: ")
        projectDirectoryPath = input("Enter project Path: ")
        projectPath = os.path.join(projectDirectoryPath, projectName)

        shutil.copytree(chosentemplatePath, projectPath) #os.path.join(projectPath, projectName)
        
        projectTemplateDetailsPath = os.path.join(projectPath, "TemplateDetails.json")
        os.remove(projectTemplateDetailsPath)

        return projectPath

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

def getPathSettings():
    pathSettings = []
    print(settingKeys)
    for key in settingKeys:
        print(key)
        if '-path' in key:
            print("through")
            pathSettings.append(key)
    return pathSettings

def saveSettings():
    with open("C:/Projects/ProjFetch/app/settings.json", "w", encoding='utf-8') as f:
        print("Modifying settings.json...")
        json.dump(settings, f, indent=4)

def validateSettingKey(keyname, defaultval):
    settingKeys = list(settings.keys())
    if keyname not in settingKeys:
        settings.update({keyname: defaultval})        

currentpath = os.path.dirname(os.path.realpath(__file__))
templatePath = os.path.join(currentpath, "templates")
running = True

settings = {}

with open("C:/Projects/ProjFetch/app/settings.json", "r", encoding='utf-8') as f:

    try:
        print("Successfully loaded settings")
        settings = json.load(f)
    except:
        print("settings is empty")
        settings = {}

    validateSettingKey('template-path', templatePath)
    validateSettingKey('project-path', '')    

settingKeys = list(settings.keys())

templatePath = settings.get('template-path', templatePath)
projectPath = settings.get('project-path', '')

ModeOptionFunctions = [downloadTemplate, uploadTemplate, templatesFunc, settingsFunc, exit]

while running:

    ModeOption = querySelector(["Download Template", "Upload Template", "Create Project/Templates", "Settings", "Exit"])
    ModeOptionFunctions[ModeOption]()

saveSettings()

