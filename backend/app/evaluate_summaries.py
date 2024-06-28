import os
import json
from bert_score import score
from rouge_score import rouge_scorer

def load_text(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def evaluate_summaries(studies_file_path):
    if not os.path.exists(studies_file_path):
        raise FileNotFoundError(f"Studies file not found: {studies_file_path}")

    with open(studies_file_path, 'r') as f:
        studies = json.load(f)

    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    results = []

    for study in studies:
        study_id = study["id"]
        bart_sum_path = os.path.join("output", "summaries", study["BART_sum"])
        pegasus_sum_path = os.path.join("output", "summaries", study["PEGASUS_sum"])
        openai_sum_path = os.path.join("output", "summaries", study["OpenAI_sum"])
        abstract_path = os.path.join("output", "abstracts", study["abstract_file"])

        if not os.path.exists(bart_sum_path) or not os.path.exists(pegasus_sum_path) or not os.path.exists(openai_sum_path) or not os.path.exists(abstract_path):
            raise FileNotFoundError(f"Summary or abstract file not found for study {study_id}")

        reference = load_text(abstract_path)
        bart_summary = load_text(bart_sum_path)
        pegasus_summary = load_text(pegasus_sum_path)
        openai_summary = load_text(openai_sum_path)

        # Calculate ROUGE scores
        bart_rouge = scorer.score(reference, bart_summary)
        pegasus_rouge = scorer.score(reference, pegasus_summary)
        openai_rouge = scorer.score(reference, openai_summary)

        # Calculate BERTScore
        bart_P, bart_R, bart_F1 = score([bart_summary], [reference], lang="en", return_hash=False)
        pegasus_P, pegasus_R, pegasus_F1 = score([pegasus_summary], [reference], lang="en", return_hash=False)
        openai_P, openai_R, openai_F1 = score([openai_summary], [reference], lang="en", return_hash=False)

        results.append({
            "study_id": study_id,
            "scores": {
                "bart": {
                    "rouge1": [bart_rouge['rouge1'].precision, bart_rouge['rouge1'].recall, bart_rouge['rouge1'].fmeasure],
                    "rouge2": [bart_rouge['rouge2'].precision, bart_rouge['rouge2'].recall, bart_rouge['rouge2'].fmeasure],
                    "rougeL": [bart_rouge['rougeL'].precision, bart_rouge['rougeL'].recall, bart_rouge['rougeL'].fmeasure],
                    "bertscore": [bart_P.mean().item(), bart_R.mean().item(), bart_F1.mean().item()]
                },
                "pegasus": {
                    "rouge1": [pegasus_rouge['rouge1'].precision, pegasus_rouge['rouge1'].recall, pegasus_rouge['rouge1'].fmeasure],
                    "rouge2": [pegasus_rouge['rouge2'].precision, pegasus_rouge['rouge2'].recall, pegasus_rouge['rouge2'].fmeasure],
                    "rougeL": [pegasus_rouge['rougeL'].precision, pegasus_rouge['rougeL'].recall, pegasus_rouge['rougeL'].fmeasure],
                    "bertscore": [pegasus_P.mean().item(), pegasus_R.mean().item(), pegasus_F1.mean().item()]
                },
                "openai": {
                    "rouge1": [openai_rouge['rouge1'].precision, openai_rouge['rouge1'].recall, openai_rouge['rouge1'].fmeasure],
                    "rouge2": [openai_rouge['rouge2'].precision, openai_rouge['rouge2'].recall, openai_rouge['rouge2'].fmeasure],
                    "rougeL": [openai_rouge['rougeL'].precision, openai_rouge['rougeL'].recall, openai_rouge['rougeL'].fmeasure],
                    "bertscore": [openai_P.mean().item(), openai_R.mean().item(), openai_F1.mean().item()]
                }
            }
        })

    return results
