import importlib
import os
import shutil
import json

from clifunctions import querySelector, query
from plugin_engine import extract_plugin_modules, prompt_plugin_arguments
from settings import get_settings

from colorama import Fore

def configureProject(projectPath, chosentemplatePath):
        from template_manager import (
                load_template_plugin_config
        )

        TemplatePluginConfig = load_template_plugin_config(chosentemplatePath)
        TemplatePluginConfigValues = list(TemplatePluginConfig.values())

        modules = extract_plugin_modules(TemplatePluginConfig)

        selectedModuleIndex = querySelector(modules)
        selectedModule = modules[selectedModuleIndex]

        plugin_directory = os.path.join(chosentemplatePath, "plugins")
        plugin_path = os.path.join(plugin_directory, selectedModule + ".py")
        spec = importlib.util.spec_from_file_location(
            selectedModule, plugin_path
        )

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        passedArguments = prompt_plugin_arguments(TemplatePluginConfigValues,  selectedModuleIndex)

        module.run(projectPath, *passedArguments)

def getProjectDirectory(projectName):
        projectDirectory = ''
        settings = get_settings()
        if settings.get('projects-path'):
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

        shutil.copytree(chosentemplatePath, projectPath) #os.path.join(projectPath, projectName)
        
        projectTemplateDetailsPath = os.path.join(projectPath, "TemplateDetails.json")
        projectDetailsPath = os.path.join(projectPath, "ProjectDetails.json")
        with open(projectDetailsPath, "w", encoding='utf-8') as f:
                json.dump({"template": os.path.basename(chosentemplatePath)}, f, indent=4)

        os.remove(projectTemplateDetailsPath)

        return projectPath
