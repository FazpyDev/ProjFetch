import importlib
import os
import shutil

from clifunctions import querySelector
from plugin_engine import extract_plugin_modules, prompt_plugin_arguments
def configureProject(projectPath, chosentemplatePath):
        from template_manager import (
                loadTemplatePluginConfig
        )

        TemplatePluginConfig = loadTemplatePluginConfig(chosentemplatePath)
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

def createProject(chosentemplatePath):
        projectName = input("Enter project name: ")
        projectDirectoryPath = input("Enter project Path: ")
        projectPath = os.path.join(projectDirectoryPath, projectName)

        shutil.copytree(chosentemplatePath, projectPath) #os.path.join(projectPath, projectName)
        
        projectTemplateDetailsPath = os.path.join(projectPath, "TemplateDetails.json")
        os.remove(projectTemplateDetailsPath)

        return projectPath
