import os

def run(project_path, new_name):
        #change the name
        parent = os.path.dirname(project_path)
        newNamePath = os.path.join(parent, new_name)
        os.rename(project_path, newNamePath)