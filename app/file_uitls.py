import json
import os
import shutil
from datetime import date

def zip_directory(source_dir):
    """Compresses a directory into a zip archive and returns the zip file path."""
    return shutil.make_archive(source_dir, 'zip', source_dir)

def write_template_metadata(folder_path):
    """Generates and writes a standardized TemplateDetails.json configuration file."""
    creation_date = date.today().isoformat()
    template_details = {
        "creator": "Ian", 
        "version": 0.01, 
        "time-created": creation_date
    }
    metadata_path = os.path.join(folder_path, "TemplateDetails.json")

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(template_details, f, indent=4)
