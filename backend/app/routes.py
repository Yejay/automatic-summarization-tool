import os
import json
import numpy as np
from flask import request, jsonify
from .summarizers.bart_summarizer import summarize_bart
from .summarizers.pegasus_summarizer import summarize_pegasus
from .summarizers.openai_summarizer import summarize_openai
from .evaluate_summaries import evaluate_summaries
from rouge_score import rouge_scorer


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

    # @app.route("/test_eval_wip", methods=["POST"])
    # def test_eval_wip():
    #     studies_file_path = os.path.join(
    #         os.path.dirname(__file__), "..", "data", "studies.json"
    #     )

    #     if not os.path.exists(studies_file_path):
    #         return jsonify({"error": "Studies file not found"}), 404

    #     with open(studies_file_path, "r") as f:
    #         studies = json.load(f)

    #     scorer = rouge_scorer.RougeScorer(
    #         ["rouge1", "rouge2", "rougeL"], use_stemmer=True
    #     )
    #     results = []

    #     for study in studies:
    #         study_id = study["id"]
    #         text_file = study["text_file"]
    #         abstract_file = study["abstract_file"]

    #         text_file_path = os.path.join(
    #             os.path.dirname(__file__), "..", "output", "texts", text_file
    #         )
    #         abstract_file_path = os.path.join(
    #             os.path.dirname(__file__), "..", "output", "abstracts", abstract_file
    #         )

    #         if not os.path.exists(text_file_path) or not os.path.exists(
    #             abstract_file_path
    #         ):
    #             return jsonify({"error": f"File not found for study {study_id}"}), 404

    #         with open(abstract_file_path, "r") as f:
    #             reference_summary = f.read()

    #         summary_bart = summarize_bart(
    #             text_file_path, min_length=256, max_length=1024
    #         )
    #         summary_pegasus = summarize_pegasus(
    #             text_file_path, min_length=256, max_length=1024
    #         )
    #         summary_openai = summarize_openai(text_file_path, max_tokens=1024)

    #         scores_bart = scorer.score(abstract_file, summary_bart)
    #         scores_pegasus = scorer.score(abstract_file, summary_pegasus)
    #         scores_openai = scorer.score(abstract_file, summary_openai)

    #         composite_score_bart = np.mean(
    #             [
    #                 scores_bart["rouge1"].fmeasure,
    #                 scores_bart["rouge2"].fmeasure,
    #                 scores_bart["rougeL"].fmeasure,
    #             ]
    #         )
    #         composite_score_pegasus = np.mean(
    #             [
    #                 scores_pegasus["rouge1"].fmeasure,
    #                 scores_pegasus["rouge2"].fmeasure,
    #                 scores_pegasus["rougeL"].fmeasure,
    #             ]
    #         )
    #         composite_score_openai = np.mean(
    #             [
    #                 scores_openai["rouge1"].fmeasure,
    #                 scores_openai["rouge2"].fmeasure,
    #                 scores_openai["rougeL"].fmeasure,
    #             ]
    #         )

    #         # results.append(
    #         #     {
    #         #         "study_id": study_id,
    #         #         "scores": {
    #         #             "bart": scores_bart,
    #         #             "pegasus": scores_pegasus,
    #         #             "openai": scores_openai,
    #         #         },
    #         #     }
    #         # )

    #         results.append(
    #             {
    #                 "study_id": study_id,
    #                 "scores": {
    #                     "bart": {
    #                         "rouge1": [
    #                             scores_bart["rouge1"].precision,
    #                             scores_bart["rouge1"].recall,
    #                             scores_bart["rouge1"].fmeasure,
    #                         ],
    #                         "rouge2": [
    #                             scores_bart["rouge2"].precision,
    #                             scores_bart["rouge2"].recall,
    #                             scores_bart["rouge2"].fmeasure,
    #                         ],
    #                         "rougeL": [
    #                             scores_bart["rougeL"].precision,
    #                             scores_bart["rougeL"].recall,
    #                             scores_bart["rougeL"].fmeasure,
    #                         ],
    #                         "composite": composite_score_bart,
    #                     },
    #                     "pegasus": {
    #                         "rouge1": [
    #                             scores_pegasus["rouge1"].precision,
    #                             scores_pegasus["rouge1"].recall,
    #                             scores_pegasus["rouge1"].fmeasure,
    #                         ],
    #                         "rouge2": [
    #                             scores_pegasus["rouge2"].precision,
    #                             scores_pegasus["rouge2"].recall,
    #                             scores_pegasus["rouge2"].fmeasure,
    #                         ],
    #                         "rougeL": [
    #                             scores_pegasus["rougeL"].precision,
    #                             scores_pegasus["rougeL"].recall,
    #                             scores_pegasus["rougeL"].fmeasure,
    #                         ],
    #                         "composite": composite_score_pegasus,
    #                     },
    #                     "openai": {
    #                         "rouge1": [
    #                             scores_openai["rouge1"].precision,
    #                             scores_openai["rouge1"].recall,
    #                             scores_openai["rouge1"].fmeasure,
    #                         ],
    #                         "rouge2": [
    #                             scores_openai["rouge2"].precision,
    #                             scores_openai["rouge2"].recall,
    #                             scores_openai["rouge2"].fmeasure,
    #                         ],
    #                         "rougeL": [
    #                             scores_openai["rougeL"].precision,
    #                             scores_openai["rougeL"].recall,
    #                             scores_openai["rougeL"].fmeasure,
    #                         ],
    #                         "composite": composite_score_openai,
    #                     },
    #                 },
    #             }
    #         )

    #     return jsonify(results)
