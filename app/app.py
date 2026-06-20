import os
from settings import saveSettings, getSettings
from clifunctions import color_print, querySelector
from colorama import Fore, Style
from backendfuncs import downloadTemplate, uploadTemplate
from template_manager import templatesFunc

#FUNCTIONS

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

def getPathSettings():
    pathSettings = []
    print(settingKeys)
    for key in settingKeys:
        print(key)
        if '-path' in key:
            print("through")
            pathSettings.append(key)
    return pathSettings

currentpath = os.path.dirname(os.path.realpath(__file__))
templatePath = os.path.join(currentpath, "templates")
running = True

settings = getSettings()

settingKeys = list(settings.keys())

templatePath = settings.get('template-path', templatePath)
projectPath = settings.get('project-path', '')

ModeOptionFunctions = [downloadTemplate, uploadTemplate, templatesFunc, settingsFunc, exit]

while running:

    ModeOption = querySelector(["Download Template", "Upload Template", "Create Project/Templates", "Settings", "Exit"])
    ModeOptionFunctions[ModeOption]()

saveSettings()

