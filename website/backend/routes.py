
from flask import request, jsonify, send_file
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
templatePath = os.path.join(currentPath, "templates")

def register_routes(app):
    @app.route('/download', methods=["GET"])
    def download():
        templateName = request.args.get("templateName", False)
        if templateName:
            templateFilePath = os.path.join(templatePath, templateName + ".zip")
            if os.path.exists(templateFilePath):
                return send_file(templateFilePath), 201
            else:
                print("Dosent exist", templateFilePath)
                return jsonify({"state": "Error", "message": "Template does not exist."})
        else:
            print("Temp Name not given")
            return jsonify({"state": "Error", "message": "Template Name wasnt given"})

    @app.route('/upload', methods=["POST"])
    def upload():
        

        arguements = request.args # zipped folder, name   later username and password perhaps? a way to identify user, possibly cookie.
        keys = list(arguements.keys())
        if len(keys) < 1: # not enough arguements
            return jsonify({"state": "Error", "message": "Not enough arguements given, please give the folder, and the name of the template."})

        name = arguements.get("name")
        if os.path.exists(os.path.join(templatePath, name.lower() + ".zip")):
            return jsonify({"state": "Error", "message": "A template with that name already exists"})

        if not name:
            return jsonify({
                "state": "Error",
                "message": "Name parameter missing"
            }), 400

        os.makedirs(templatePath, exist_ok=True)

        file = request.files["file"]

        zip_path = os.path.join(templatePath, f"{name}.zip")

        file.save(zip_path)

        extract_dir = f"templates/{name.removesuffix('.zip')}"
        os.makedirs(extract_dir, exist_ok=True)
        return jsonify({"state": "Success", "message": "Successfully uploaded template."}), 201
