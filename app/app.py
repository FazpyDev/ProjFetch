import requests
import requests.exceptions
import json
import os
import shutil
import zipfile
from datetime import date

from colorama import Fore, Style

CURRENTPATH = os.path.dirname(os.path.realpath(__file__))
templatePath = os.path.join(CURRENTPATH, "templates")
running = True


settings = {}

def validateSettingKey(keyname, defaultval):
    settingKeys = list(settings.keys())
    if keyname not in settingKeys:
        settings.update({keyname: defaultval})        
        
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

    
print(settings)

def query(color, outputText):
    color_print(color, outputText)
    userInput = input()
    return userInput.lower().startswith('y')

def color_print(color, text):
    print(color + text + Style.RESET_ALL)

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

def querySelector(queryList):
    print("Please select an option: ")
    for i, query in enumerate(queryList):
        print(f"{i+1}. {query}")
    
    userInput = input()
    return int(userInput) -1

def downloadTemplate():
    templateName = input("Enter the name of the template: ").lower()
    path = f"{templateName}.zip"
    r = attemptRequest(templateName)

    if running:
        if r.status_code == 201:

            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            color_print(Fore.GREEN, f"Successfully downloaded: {templateName.lower()}.zip")
        #    os.makedirs(templateName, exist_ok=True)
            target_path = os.path.join(templatePath,templateName)
            shutil.unpack_archive(path, target_path)
            os.remove(path)
        else:
            data = r.json()
            color_print(Fore.RED, f"ERROR: {data.get('message')}")


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

        
        
        NiceDate =  date.today().isoformat()
        templateDetails = {"creator": "Ian", "version": 0.01, "time-created": NiceDate}
        templateDetailsPath = os.path.join(filePath, "TemplateDetails.json")

        with open(templateDetailsPath, "w", encoding="utf-8") as f:
            json.dump(templateDetails, f, indent=4)
 
        zip_path = shutil.make_archive(
            filePath,  
            'zip',
            filePath   
        )
    

    with open(zip_path, "rb") as f:
        r = requests.post(
            f"http://127.0.0.1:5000/upload?name={fileName}",
            files={"file": f}
        )
    os.remove(zip_path)
   # print(r.status_code)
   # print(r.text)
    

def templatesFunc():
    templates = os.listdir(templatePath)
    templateIndex = querySelector(templates)

    chosenTemplate = templates[templateIndex]
    chosentemplatePath = os.path.join(templatePath, chosenTemplate)

    options = querySelector(["Create Project", "Modify", "Details"])

    match options:
        case 0:
            projectName = input("Enter project name: ")
            projectDirectoryPath = input("Enter project Path: ")
            projectPath = os.path.join(projectDirectoryPath, projectName)

            shutil.copytree(chosentemplatePath, os.path.join(projectPath, projectName))
            
            projectTemplateDetailsPath = os.path.join(projectPath, "TemplateDetails.json")
            os.remove(projectTemplateDetailsPath)
        case 1:
            Modification = querySelector(["Name"])
            match Modification:
                case 0:
                    #change the name
                    newName = input("Enter the new name the template should have: ")
                    newNamePath = os.path.join(templatePath, newName)
                    os.rename(chosentemplatePath, newNamePath)
        case 2:
            #extract details and print them out
            TemplateDetailsPath = os.path.join(chosentemplatePath, "TemplateDetails.json")
            with open(TemplateDetailsPath, "r") as f:
                TemplateDetailsObject = json.load(f)

                for key, val in TemplateDetailsObject.items():
                    print(f"{key}: {val}")

def settingsFunc():
    settingSubjectIndex = querySelector(["Paths"])

    match settingSubjectIndex:
        case 0:
            pathSettings = []
            print(settingKeys)
            for key in settingKeys:
                print(key)
                if '-path' in key:
                    print("through")
                    pathSettings.append(key)
            pathSubjectIndex = querySelector(pathSettings)
            selectedPathKey = settingKeys[pathSubjectIndex]

            newVal = input(f"What value do you want to chance {selectedPathKey} to?: ")
            settings.update({selectedPathKey: newVal})



def exit():
    global running
    running = False
    color_print(Fore.BLUE, "Exiting.. Goodbye!")

ModeOptionFunctions = [downloadTemplate, uploadTemplate, templatesFunc, settingsFunc, exit]

while running:

    ModeOption = querySelector(["Download Template", "Upload Template", "Create Project/Templates", "Settings", "Exit"])
    ModeOptionFunctions[ModeOption]()

with open("C:/Projects/ProjFetch/app/settings.json", "w", encoding='utf-8') as f:
    print("Modifying settings.json...")
    json.dump(settings, f, indent=4)

