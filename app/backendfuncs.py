import requests, os, shutil
from clifunctions import *

from templateFuncs import updateTemplateDetails, zipFiles

currentpath = os.path.dirname(os.path.realpath(__file__))
templatePath = os.path.join(currentpath, "templates")


def attemptRequest(templateName):
    r = requests.get(f"http://127.0.0.1:5000/download?templateName={templateName}", stream=True)
    r.raise_for_status()
    return r

def downloadFile(path, r):
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

def downloadTemplate():
    templateName = input("Enter the name of the template: ").lower()
    path = f"{templateName}.zip"
    r = attemptRequest(templateName)

    if r.status_code == 201:

        downloadFile(path, r)
        color_print(Fore.GREEN, f"Successfully downloaded: {templateName.lower()}.zip")
    #    os.makedirs(templateName, exist_ok=True)
        target_path = os.path.join(templatePath,templateName)
        shutil.unpack_archive(path, target_path)
        os.remove(path)
    else:
        data = r.json()
        color_print(Fore.RED, f"ERROR: {data.get('message')}")

def uploadFile(path, fileName):
    with open(path, "rb") as f:
        r = requests.post(
            f"http://127.0.0.1:5000/upload?name={fileName}",
            files={"file": f}
        )

def uploadTemplate():
    filePath = input("Enter folder path: ")

    if not os.path.exists(filePath):
        print("Path does not exist")
        return

    fileName = input("Template name: ")

    if filePath.endswith(".zip"):
        print("Most be a folder!")
        return
    else:
        if not os.path.isdir(filePath):
            print("You must provide a folder (not a file)")
            return

        #Create/modify TemplateDetails.json
        updateTemplateDetails(filePath)
    
        zip_path = zipFiles(filePath)
    
    uploadFile(zip_path, fileName)
    os.remove(zip_path)
