def extract_plugin_modules(plugin_config):
    """Parses plugin configurations and returns a list of active module names."""
    modules = []
    plugin_config_values = list(plugin_config.values())
    
    for plugin in plugin_config_values:
        module_name = plugin.get('module')
        if module_name:
            modules.append(module_name)

    return modules

def prompt_plugin_arguments(plugin_config_values, selected_module_index):
    """Prompts the user via CLI for required variables based on chosen plugin configuration."""
    plugin_config = plugin_config_values[selected_module_index]
    required_arguments = plugin_config.get("arguments", [])
    collected_arguments = []

    for argument in required_arguments:
        argument_name = argument.get('name')
        argument_type = argument.get('type')

        user_value = input(f"Please enter a {argument_type} for {argument_name}: ")
        collected_arguments.append(user_value)

    return collected_arguments
