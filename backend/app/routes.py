import os
from flask import request, jsonify
from .summarizers.bart_summarizer import summarize_bart
from .summarizers.pegasus_summarizer import summarize_pegasus
from .summarizers.openai_summarizer import summarize_openai
from .evaluate_summaries import evaluate_summaries


def register_routes(app):
    @app.route("/summarize_bart", methods=["POST"])
    def summarize_bart_endpoint():
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        summary = summarize_bart(file, min_length=256, max_length=1024)
        return jsonify({"summary": summary})

    @app.route("/summarize_pegasus", methods=["POST"])
    def summarize_pegasus_endpoint():
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        summary = summarize_pegasus(file, min_length=256, max_length=1024)
        return jsonify({"summary": summary})

    @app.route("/summarize_openai", methods=["POST"])
    def summarize_openai_endpoint():
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        summary = summarize_openai(file, max_tokens=4096)
        return jsonify({"summary": summary})

    @app.route("/evaluate_summaries", methods=["POST"])
    def evaluate_summaries_route():
        studies_file_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "studies.json"
        )

        results = evaluate_summaries(studies_file_path)
        return jsonify(results)
