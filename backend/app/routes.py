# from flask import Flask, request, jsonify
# from transformers import pipeline, PegasusTokenizer, BartTokenizer
# from pypdf import PdfReader
# from io import BytesIO
# import openai

# app = Flask(__name__)

# # Initialize summarizers
# bart_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
# pegasus_summarizer = pipeline("summarization", model="google/pegasus-pubmed")
# openai.api_key = "your_openai_api_key"

# # Initialize tokenizers
# pegasus_tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-pubmed")
# bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")


# def extract_text(file):
#     if file.filename.endswith(".pdf"):
#         pdf = PdfReader(BytesIO(file.read()))
#         text = ""
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text is not None:
#                 text += page_text
#     else:
#         text = file.read().decode("utf-8", errors="ignore")
#     return text


# def split_text(text, max_length, tokenizer):
#     inputs = tokenizer(
#         text, return_tensors="pt", truncation=True, max_length=max_length, padding=False
#     )
#     input_ids = inputs["input_ids"]
#     chunks = []
#     for i in range(0, len(input_ids[0]), max_length):
#         chunk_ids = input_ids[0][i : i + max_length]
#         chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True)
#         chunks.append(chunk_text)
#     return chunks


# def register_routes(app):
#     @app.route("/summarize_bart", methods=["POST"])
#     def summarize_bart():
#         if "file" not in request.files:
#             return jsonify({"error": "No file provided"}), 400

#         file = request.files["file"]
#         text = extract_text(file)

#         chunks = split_text(text, 1024, bart_tokenizer)
#         summaries = []
#         for chunk in chunks:
#             summary = bart_summarizer(chunk, do_sample=False)
#             summaries.append(summary[0]["summary_text"])

#         combined_summary = " ".join(summaries)
#         return jsonify({"summary": combined_summary})

#     @app.route("/summarize_pegasus", methods=["POST"])
#     def summarize_pegasus():
#         if "file" not in request.files:
#             return jsonify({"error": "No file provided"}), 400

#         file = request.files["file"]
#         text = extract_text(file)

#         chunks = split_text(text, 1024, pegasus_tokenizer)
#         summaries = []
#         for chunk in chunks:
#             summary = pegasus_summarizer(chunk, do_sample=False)
#             summaries.append(summary[0]["summary_text"])

#         combined_summary = " ".join(summaries)
#         return jsonify({"summary": combined_summary})

#     @app.route("/summarize_openai", methods=["POST"])
#     def summarize_openai():
#         if "file" not in request.files:
#             return jsonify({"error": "No file provided"}), 400

#         file = request.files["file"]
#         text = extract_text(file)

#         response = openai.Completion.create(
#             engine="text-davinci-003",
#             prompt=f"Summarize the following text:\n{text}",
#             max_tokens=150,
#             n=1,
#             stop=None,
#             temperature=0.7,
#         )
#         summary = response.choices[0].text.strip()
#         return jsonify({"summary": summary})

from flask import Flask, request, jsonify, Response
from transformers import (
    pipeline,
    PegasusTokenizer,
    BartTokenizer,
    BartForConditionalGeneration,
    PegasusForConditionalGeneration,
)
from pypdf import PdfReader
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv
import sys

load_dotenv()

app = Flask(__name__)


# Initialize summarizers
bart_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
pegasus_summarizer = pipeline("summarization", model="google/pegasus-pubmed")
client = OpenAI()
# Initialize tokenizers
pegasus_tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-pubmed")
bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")


def extract_text(file):
    if file.filename.endswith(".pdf"):
        pdf = PdfReader(BytesIO(file.read()))
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text is not None:
                text += page_text
    else:
        text = file.read().decode("utf-8", errors="ignore")
    return text


def split_text(text, max_length, tokenizer):
    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, max_length=max_length, padding=False
    )
    input_ids = inputs["input_ids"].squeeze(0).tolist()
    chunks = []
    current_length = 0
    current_chunk = []

    for token_id in input_ids:
        current_chunk.append(token_id)
        current_length += 1
        if current_length >= max_length:
            chunks.append(tokenizer.decode(current_chunk, skip_special_tokens=True))
            current_chunk = []
            current_length = 0

    if current_chunk:
        chunks.append(tokenizer.decode(current_chunk, skip_special_tokens=True))

    return chunks


def map_reduce_summarize(text, max_length, summarizer, tokenizer):
    # Split the text into smaller chunks
    chunks = split_text(text, max_length, tokenizer)

    # First round of summarization (map step)
    first_round_summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, do_sample=False)
        first_round_summaries.append(summary[0]["summary_text"])

    # Combine summaries
    combined_text = " ".join(first_round_summaries)

    # Second round of summarization (reduce step)
    final_summary = summarizer(combined_text, do_sample=False)
    return final_summary[0]["summary_text"]


def register_routes(app):
    @app.route("/summarize_bart", methods=["POST"])
    def summarize_bart():
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        text = extract_text(file)

        combined_summary = map_reduce_summarize(
            text, 1024, bart_summarizer, bart_tokenizer
        )
        print(combined_summary, file=sys.stderr)
        return jsonify({"summary": combined_summary})

    @app.route("/summarize_pegasus", methods=["POST"])
    def summarize_pegasus():
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        text = extract_text(file)

        combined_summary = map_reduce_summarize(
            text, 1024, pegasus_summarizer, pegasus_tokenizer
        )
        print(combined_summary, file=sys.stderr)
        return jsonify({"summary": combined_summary})

    @app.route("/summarize_openai", methods=["POST"])
    def summarize_openai():
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        text = extract_text(file)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {
                    "role": "system",
                    "content": "You are a sports scientist, specializing in summarizing research papers.",
                },
                {
                    "role": "user",
                    "content": "Summarize the following text:\n" + text,
                },
            ],
            temperature=0.7,
            max_tokens=64,
            top_p=1,
        )
        summary = response.choices[0].message.content
        print(summary, file=sys.stderr)
        return jsonify({"summary": summary})

    # def summarize_openai():
    #     if "file" not in request.files:
    #         return jsonify({"error": "No file provided"}), 400

    #     file = request.files["file"]
    #     text = extract_text(file)

    #     def generate():
    #         response = client.chat.completions.create(
    #             model="gpt-3.5-turbo-16k",
    #             messages=[
    #                 {
    #                     "role": "system",
    #                     "content": "You are a sports scientist, specializing in summarizing research papers.",
    #                 },
    #                 {
    #                     "role": "user",
    #                     "content": "Summarize the following text:\n" + text,
    #                 },
    #             ],
    #             temperature=0.7,
    #             max_tokens=64,
    #             top_p=1,
    #             stream=True,
    #         )

    #         for chunk in response:
    #             if chunk.choices[0].delta.content is not None:
    #                 yield chunk.choices[0].delta.content

    #     return Response(generate(), mimetype="text/plain")
