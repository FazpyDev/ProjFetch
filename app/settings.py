import json
import os

settings = {}

currentpath = os.path.dirname(os.path.realpath(__file__))
templatePath = os.path.join(currentpath, "templates")

def validateSettingKey(keyname, defaultval):
    settingKeys = list(settings.keys())
    if keyname not in settingKeys:
        settings.update({keyname: defaultval})        

def loadSettings():

    with open("C:/Projects/ProjFetch/app/settings.json", "r", encoding='utf-8') as f:

        try:
            print("Successfully loaded settings")
            global settings
            settings = json.load(f)
        except:
            print("settings is empty")
            settings = {}

        validateSettingKey('template-path', templatePath)
        validateSettingKey('project-path', '')    


def saveSettings():
    with open("C:/Projects/ProjFetch/app/settings.json", "w", encoding='utf-8') as f:
        json.dump(settings, f, indent=4)

def getSettings():
    loadSettings()
    print(settings)
    return settings