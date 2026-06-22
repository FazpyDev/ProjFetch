import os
from settings import get_settings, write_settings_file
from clifunctions import color_print, querySelector
from colorama import Fore, Style
from backendfuncs import downloadTemplate, uploadTemplate
from template_manager import manage_templates
from projectFuncs import configureProject, projectsFunc
import json
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

settings = get_settings()

settingKeys = list(settings.keys())

templatePath = settings.get('template-path', templatePath)
projectPath = settings.get('projects-path', '')

ModeOptionFunctions = [downloadTemplate, uploadTemplate, manage_templates, projectsFunc, settingsFunc, exit]

while running:

    ModeOption = querySelector(["Download Template", "Upload Template", "Create Project/Templates", "Projects", "Settings", "Exit"])
    ModeOptionFunctions[ModeOption]()

write_settings_file()

