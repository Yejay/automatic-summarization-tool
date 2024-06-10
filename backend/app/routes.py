import os
import json
from flask import request, jsonify
from .summarizers.bart_summarizer import summarize_bart
from .summarizers.pegasus_summarizer import summarize_pegasus
from .summarizers.openai_summarizer import summarize_openai


def register_routes(app):
    @app.route("/summarize_bart", methods=["POST"])
    def summarize_bart_endpoint():
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        max_length = int(request.form.get("max_length", 512))
        min_length = int(request.form.get("min_length", 30))
        summary = summarize_bart(file, max_length=max_length, min_length=min_length)
        return jsonify({"summary": summary})

    @app.route("/summarize_pegasus", methods=["POST"])
    def summarize_pegasus_endpoint():
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        max_length = int(request.form.get("max_length", 512))
        min_length = int(request.form.get("min_length", 30))
        summary = summarize_pegasus(file, max_length=max_length, min_length=min_length)
        return jsonify({"summary": summary})

    @app.route("/summarize_openai", methods=["POST"])
    def summarize_openai_endpoint():
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        summary = summarize_openai(file)
        return jsonify({"summary": summary})
    
    # Test endpoint for evaluating the summarization models
    @app.route("/test_eval_wip", methods=["GET"])
    def test_eval_wip_endpoint():
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Navigate up two directories to the project root
        project_root = os.path.dirname(os.path.dirname(script_dir))

        # Construct the path to the studies.json file
        json_file_path = os.path.join(project_root, "output", "studies.json")

        with open(json_file_path, "r", encoding="utf-8") as json_file:
            studies = json.load(json_file)
        first_study = studies[0]

        # Construct the absolute path for the text file
        text_file_path = os.path.join(project_root, "output", "texts", first_study["text_file"])

        # Load the text of the first study
        with open(text_file_path, "r", encoding="utf-8") as text_file:
            study_text = text_file.read()
        
        model = request.args.get("model", "bart")
        
        if model == "bart":
            summary = summarize_bart_text(study_text)
        elif model == "pegasus":
            summary = summarize_pegasus_text(study_text)
        elif model == "openai":
            summary = summarize_openai_text(study_text)
        else:
            return jsonify({"error": "Invalid model selected"}), 400
        
        return jsonify({"summary": summary})

def summarize_bart_text(text):
    from .summarizers.bart_summarizer import bart_summarizer
    return bart_summarizer(text, max_length=512, min_length=30)[0]["summary_text"]

def summarize_pegasus_text(text):
    from .summarizers.pegasus_summarizer import pegasus_summarizer
    return pegasus_summarizer(text, max_length=512, min_length=30)[0]["summary_text"]

def summarize_openai_text(text):
    from .summarizers.openai_summarizer import openai_summarizer
    return openai_summarizer(text)[0]["summary_text"]
