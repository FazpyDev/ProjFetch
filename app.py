import requests
import requests.exceptions
import json
import os
import shutil
import zipfile
from datetime import date

from colorama import Fore, Style

CURRENTPATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATEPATH = os.path.join(CURRENTPATH, "templates")
running = True

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
            target_path = os.path.join(TEMPLATEPATH,templateName)
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
    templates = os.listdir(TEMPLATEPATH)
    templateIndex = querySelector(templates)

    chosenTemplate = templates[templateIndex]
    chosenTemplatePath = os.path.join(TEMPLATEPATH, chosenTemplate)

    options = querySelector(["Create Project", "Modify", "Details"])

    match options:
        case 2:
            #extract details and print them out
            TemplateDetailsPath = os.path.join(chosenTemplatePath, "TemplateDetails.json")
            with open(TemplateDetailsPath, "r") as f:
                TemplateDetailsObject = json.load(f)

                for key, val in TemplateDetailsObject.items():
                    print(f"{key}: {val}")

def exit():
    global running
    running = False
    color_print(Fore.BLUE, "Exiting.. Goodbye!")

ModeOptionFunctions = [downloadTemplate, uploadTemplate, templatesFunc, exit]

while running:

    ModeOption = querySelector(["Download Template", "Upload Template", "Create Project/Templates", "Exit"])
    ModeOptionFunctions[ModeOption]()



