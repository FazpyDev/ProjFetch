from clifunctions import color_print
from colorama import Fore, Style


def extract_plugin_modules(plugin_config):
    """Parses plugin configurations and returns a list of active module names."""
    modules = []
    plugin_config_values = list(plugin_config.values())
    
    for plugin in plugin_config_values:
        module_name = plugin.get('module')
        if module_name:
            modules.append(module_name)

    return modules

type_map = {
    "string": str,
    "integer": int,
    "float": float,
    "boolean": lambda s: s.lower() == "true",
    "array": list,
    "object": dict,
    "tuple": tuple,
    "set": set,
    "null": None
}

def checkCorrectValue(wanted_type, given_value):

    match(wanted_type):
        case "string":
            return True
        case "interger":
            given_value.strip()
            if given_value.lstrip("+-").isdigit() and given_value not in ("+", "-"):
                return True
            return False
        case "float":
            try:
                float(given_value)
                return True
            except ValueError:
                return False
        case "boolean":
            return given_value.lower() == "true" or given_value.lower() == "false"
        case "array":
            #arr = given_value.split(", ")
            return True # not too sure
        case "object":
            #not sure
            return True
        case "tuple":
            #not sure
            return True
        case "set":
            #not sure
            return True
        case "null":
            if not given_value:
                return True
            return False
    return False


def prompt_plugin_arguments(plugin_config_values, selected_module_index):
    """Prompts the user via CLI for required variables based on chosen plugin configuration."""
    plugin_config = plugin_config_values[selected_module_index]
    required_arguments = plugin_config.get("arguments", [])
    collected_arguments = []

    for argument in required_arguments:
        argument_name = argument.get('name')
        argument_type = argument.get('type')
        arguement_python_type = type_map.get(argument_type)

        user_value = input(f"Please enter a {argument_type} for {argument_name}: ")
    

        while not checkCorrectValue(argument_type, user_value):
            color_print(Fore.RED, f"Please enter the correct datatype ({argument_type}) for the arguement {argument_name}: ")
            user_value = input()

        print(checkCorrectValue(argument_type, user_value))
        print(user_value)
        print(arguement_python_type)
        print(argument_type)

        collected_arguments.append(arguement_python_type(user_value))

    return collected_arguments
