import os
import json
from flask import request, jsonify
from .summarizers.bart_summarizer import summarize_bart
from .summarizers.pegasus_summarizer import summarize_pegasus
from .summarizers.openai_summarizer import summarize_openai
from rouge_score import rouge_scorer


def register_routes(app):
    @app.route("/summarize_bart", methods=["POST"])
    def summarize_bart_endpoint():
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        summary = summarize_bart(file, max_length=1024, min_length=256)
        return jsonify({"summary": summary})

    @app.route("/summarize_pegasus", methods=["POST"])
    def summarize_pegasus_endpoint():
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        summary = summarize_pegasus(file, max_length=1024, min_length=256)
        return jsonify({"summary": summary})

    @app.route("/summarize_openai", methods=["POST"])
    def summarize_openai_endpoint():
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        summary = summarize_openai(file)
        return jsonify({"summary": summary})

    @app.route("/test_eval_wip", methods=["POST"])
    def test_eval_wip():
        studies_file_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "studies.json"
        )

        if not os.path.exists(studies_file_path):
            return jsonify({"error": "Studies file not found"}), 404

        with open(studies_file_path, "r") as f:
            studies = json.load(f)

        scorer = rouge_scorer.RougeScorer(
            ["rouge1", "rouge2", "rougeL"], use_stemmer=True
        )
        results = []

        for study in studies:
            study_id = study["id"]
            text_file = study["text_file"]
            abstract_file = study["abstract_file"]

            text_file_path = os.path.join(
                os.path.dirname(__file__), "..", "output", "texts", text_file
            )
            abstract_file_path = os.path.join(
                os.path.dirname(__file__), "..", "output", "abstracts", abstract_file
            )

            if not os.path.exists(text_file_path) or not os.path.exists(
                abstract_file_path
            ):
                return jsonify({"error": f"File not found for study {study_id}"}), 404

            summary_bart = summarize_bart(text_file_path, max_length=1024, min_length=256)
            summary_pegasus = summarize_pegasus(text_file_path, max_length=1024, min_length=256)
            summary_openai = summarize_openai(text_file_path)

            scores_bart = scorer.score(abstract_file, summary_bart)
            scores_pegasus = scorer.score(abstract_file, summary_pegasus)
            scores_openai = scorer.score(abstract_file, summary_openai)

            results.append(
                {
                    "study_id": study_id,
                    "scores": {
                        "bart": scores_bart,
                        "pegasus": scores_pegasus,
                        "openai": scores_openai,
                    },
                }
            )

        return jsonify(results)
