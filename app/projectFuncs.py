import importlib
import os
import shutil
import json

from clifunctions import querySelector, query, color_print
from plugin_engine import extract_plugin_modules, prompt_plugin_arguments
from settings import get_settings

from colorama import Fore

settings = get_settings()
projectsPath = settings.get('projects-path')
templatePath = settings.get('template-path')

def configureProject(projectPath, chosentemplatePath):
        from template_manager import (
                load_template_plugin_config
        )

        TemplatePluginConfig = load_template_plugin_config(chosentemplatePath)
        TemplatePluginConfigValues = list(TemplatePluginConfig.values())

        modules = extract_plugin_modules(TemplatePluginConfig)
        modules.append("Exit")
        selectedModuleIndex = querySelector(modules)
        selectedModule = modules[selectedModuleIndex]
        if selectedModuleIndex == len(modules) -1:
                #exiting
                return
        plugin_directory = os.path.join(chosentemplatePath, "plugins")
        if not os.path.exists(plugin_directory):
                print(chosentemplatePath + " does not have plugins folder inside of it!")
                return
        plugin_path = os.path.join(plugin_directory, selectedModule + ".py")
        if not os.path.exists(plugin_path):
                print(plugin_path + " does not exist! Plugin likely removed during running")
        spec = importlib.util.spec_from_file_location(
            selectedModule, plugin_path
        )

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        passedArguments = prompt_plugin_arguments(TemplatePluginConfigValues,  selectedModuleIndex)

        module.run(projectPath, *passedArguments)

def getProjectDirectory(projectName):
        projectDirectory = ''
        if projectsPath:
                #check if project-path is valid
                userInput = query(Fore.BLUE, "Would you like to use the project path you have in settings? (Y/N) ")
                if userInput:
                        projectDirectory = settings.get('projects-path')
                else:
                        projectDirectory = input("Enter project Path: ")


        return os.path.join(projectDirectory, projectName)

def createProject(chosentemplatePath):
        projectName = input("Enter project name: ")
        projectPath = getProjectDirectory(projectName)
        if not os.path.exists(projectPath):
                color_print(Fore.RED, f"Project path ({projectPath}) does not exist!")
                return
        shutil.copytree(chosentemplatePath, projectPath) #os.path.join(projectPath, projectName)
        
        projectTemplateDetailsPath = os.path.join(projectPath, "TemplateDetails.json")
        projectDetailsPath = os.path.join(projectPath, "ProjectDetails.json")
        if not os.path.exists(projectDetailsPath):
                color_print(Fore.RED, "ProjectDetails.json does not exist! ")
        with open(projectDetailsPath, "w", encoding='utf-8') as f:
                json.dump({"template": os.path.basename(chosentemplatePath)}, f, indent=4)

        if os.path.exists(projectTemplateDetailsPath):
                os.remove(projectTemplateDetailsPath)

        return projectPath

def projectsFunc():
    #get a list of projects
        if not os.path.exists(projectsPath):
                color_print(Fore.RED, "Project Path does not exist! ")
                return
        projects = os.listdir(projectsPath)
        projects.append("Exit")
        selectedProject = querySelector(projects) # projects + "Exit"
        projectName = projects[selectedProject]
        if projectName == "Exit": return
        selectedProjectPath = os.path.join(projectsPath, projectName)

        projectDetailsPath = os.path.join(selectedProjectPath, "ProjectDetails.json")
        if not os.path.exists(projectDetailsPath):
                color_print(Fore.RED, f"Project ({projectName}) inside ({projectsPath}) does not include ProjectDetails.json, either project was not created with this program, or the file got removed! ")

        with open(projectDetailsPath, "r", encoding='utf-8') as f:
                projectDetails = json.load(f)
                projectTemplate = projectDetails.get("template")
                if not projectTemplate:
                        color_print(Fore.RED, f"template key does not exist in ProjectDetails.json, which is inside ({projectName} which is inside ({projectsPath}). Either ProjectDetails.json has been tampered with or created without program. ")
                        return
                chosenTemplatePath = os.path.join(templatePath, projectTemplate)
                configureProject(selectedProjectPath, chosenTemplatePath)

