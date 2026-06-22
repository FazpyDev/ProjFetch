# ProjFetch

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Status](https://img.shields.io/badge/Status-Active%20Development-orange)
![License](https://img.shields.io/badge/License-MIT-green)

readme created by chatgpt, im sorry i am lazy :( 

A Python-based project scaffolding platform that allows developers to create reusable templates, generate projects from those templates, and extend project creation through a plugin system.

ProjFetch aims to make project setup faster, more consistent, and more customizable by combining template management, project generation, plugin execution, and template sharing into a single workflow.

---

# Features

## Template Management

- Browse installed templates
- View template metadata
- Generate projects from templates
- Upload templates to a backend service
- Download templates from a backend service

## Project Generation

Generate complete projects from reusable templates.

A generated project can include:

- Folder structures
- Configuration files
- Documentation
- Metadata
- Plugins

## Plugin System

Templates can include Python plugins that execute after project creation.

Plugins can:

- Rename files
- Create files
- Generate configuration
- Modify project structures
- Prompt for user input

## Interactive CLI

ProjFetch uses a menu-driven command line interface to guide users through:

- Template selection
- Project creation
- Plugin configuration
- Template uploads and downloads

---

# Project Structure

```text
ProjFetch/
│
├── app/
│   ├── app.py
│   ├── clifunctions.py
│   ├── plugin_engine.py
│   ├── template_manager.py
│   ├── projectFuncs.py
│   ├── backendfuncs.py
│   ├── settings.py
│   │
│   ├── templates/
│   └── projects/
│
└── website/
    └── backend/
        ├── app.py
        ├── routes.py
        └── run.py
```

---

# Installation

## Requirements

- Python 3.10+
- pip

## Clone Repository

```bash
git clone https://github.com/FazpyDev/ProjFetch.git
cd ProjFetch
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running ProjFetch

From the application directory:

```bash
python app.py
```

You will be presented with a menu similar to:

```text
1. Download Template
2. Upload Template
3. Create Project/Templates
4. Projects
5. Settings
6. Exit
```

---

# Creating a Project

1. Select **Create Project/Templates**
2. Choose a template
3. Create a project from that template
4. Optionally run template plugins
5. Enter plugin arguments when prompted

Generated projects are stored in:

```text
app/projects/
```

---

# Templates

Templates are stored inside:

```text
app/templates/
```

Example:

```text
templateplugin/
│
├── TemplateDetails.json
├── TemplatePluginConfig.json
└── plugins/
    └── name_change.py
```

## TemplateDetails.json

Contains metadata about the template.

Example:

```json
{
  "name": "Template Plugin",
  "author": "Author Name",
  "version": "1.0.0"
}
```

---

# Plugin System

The plugin system is one of the main features of ProjFetch.

Plugins are loaded dynamically at runtime.

The engine extracts plugin modules from:
TemplatePluginsConfig.json
```json
{
  "plugin_name": {
    "module": "function_name",
    "text": "This is what will apear for the user when they pick out what plugins to use",
    "arguments": [
        {
            "name": "argument name, shown to user (enter {type} for the argument {name})",
            "type": "datatype (e.g. string, interger, etc.)" 
        }
    ]
  }
}
```

and executes them after collecting any required arguments.

## Example Plugin

 ALL plugins must take project path! I decided this because i believe it is too necessary and saves a lot of pain from the user.

function_name.py
```python
def run(project_path, new_name):
    print(project_path)
```

---

# Plugin Arguments

As earlier above, Plugins can define arguments in:

```text
TemplatePluginConfig.json
```

Example:

*this is all inside the module object in ```TemplatePluginConfig.json```*
```json
{
  "arguments": [
    {
      "name": "project_name",
      "type": "string"
    }
  ]
}
```
# This is how the file Structure looks like for the project/template:
```
Project/Template/
│
├── plugins/
│   ├── __init__.py
│   └── function_name.py
│──Project/TemplateDetails.json
│──TemplatePluginConfig.json
└── website/
    └── backend/
        ├── app.py
        ├── routes.py
        └── run.py
```

During execution ProjFetch automatically prompts the user.

---

# Supported Argument Types

Current types implemented in the plugin engine:

| Type | Python Type |
|--------|--------|
| string | str |
| interger | int |
| float | float |
| boolean | bool |
| array | list |
| object | dict |
| tuple | tuple |
| set | set |
| null | None |

**Note:** Some validation logic is still under development.

---

# Settings

Settings are stored through:

```text
settings.json
```

Current settings include configurable paths such as:

- template-path
- projects-path

These allow users to relocate project and template directories.

---

# Backend Service

ProjFetch includes a Flask backend used for template distribution.

Current functionality:

- Upload templates
- Download templates

Backend source:

```text
website/backend/
```

Future improvements could include:

- User accounts
- Authentication
- Template versioning
- Search
- Ratings and reviews

---

# How Plugins Work

Simplified workflow:

```text
User
 │
 ▼
Select Template
 │
 ▼
Create Project
 │
 ▼
Load Plugin Configuration
 │
 ▼
Collect Arguments
 │
 ▼
Load Plugin Module
 │
 ▼
Execute Plugin
```

This allows templates to perform dynamic setup tasks after project generation.

---

# Current Development Status

ProjFetch is currently in active development.

Implemented:

- CLI menus
- Template management
- Project generation
- Plugin execution
- Backend uploads/downloads

Still being improved:

- Validation
- Error handling
- Testing
- Documentation
- Security

---

# Future Roadmap

## Core Improvements

- Better datatype validation
- Structured logging
- Improved exception handling
- Unit testing

## Template Ecosystem

- Template repository
- Template versioning
- Template dependencies
- Template search

## Security

- Plugin permissions
- Sandboxed execution
- Plugin signing
- Repository moderation

## Community Features

- User accounts
- Ratings
- Reviews
- Contributor profiles

---

# Contributing

Contributions are welcome.

Suggested workflow:

```bash
git checkout -b feature/my-feature
git commit -m "Add feature"
git push origin feature/my-feature
```

Then open a Pull Request.

---

# License

MIT License

See the LICENSE file for more information.
