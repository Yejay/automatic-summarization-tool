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
