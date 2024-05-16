# from flask import request, jsonify
# from transformers import pipeline

# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


# def register_routes(app):
#     @app.route("/summarize", methods=["POST"])
#     def summarize():
#         if "file" not in request.files:
#             return jsonify({"error": "No file provided"}), 400

#         file = request.files["file"]
#         # text = file.read().decode("utf-8")
#         text = file.read().decode("utf-8", errors="ignore")
#         summary = summarizer(text, max_length=400, min_length=200, do_sample=False)

#         return jsonify({"summary": summary[0]["summary_text"]})

# from flask import request, jsonify
# from transformers import pipeline
# from pypdf import PdfReader
# from io import BytesIO

# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


# def register_routes(app):
#     @app.route("/summarize", methods=["POST"])
#     def summarize():
#         if "file" not in request.files:
#             return jsonify({"error": "No file provided"}), 400

#         file = request.files["file"]
#         if file.filename.endswith(".pdf"):
#             print("PDF")
#             pdf = PdfReader(BytesIO(file.read()))
#             text = ""
#             for page in pdf.pages:
#                 text += page.extract_text()
#         else:
#             print("Not PDF")
#             # text = file.read().decode("utf-8")
#             text = file.read().decode("utf-8", errors="ignore")
#         # max_length sets the maximum length of the summary, and min_length sets the minimum length of the summary.    
#         summary = summarizer(text, max_length=150, min_length=30, do_sample=False)

#         return jsonify({"summary": summary[0]["summary_text"]})


from flask import request, jsonify
from transformers import pipeline
from pypdf import PdfReader
from io import BytesIO

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

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

def split_text(text, max_length=1024):
    # Split the text into smaller chunks of a specified max length
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    for word in words:
        if current_length + len(word) + 1 <= max_length:
            current_chunk.append(word)
            current_length += len(word) + 1
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word) + 1
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def register_routes(app):
    @app.route("/summarize", methods=["POST"])
    def summarize():
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        text = extract_text(file)

        chunks = split_text(text)
        summaries = []
        for chunk in chunks:
            summary = summarizer(chunk, do_sample=False)
            summaries.append(summary[0]["summary_text"])

        combined_summary = " ".join(summaries)

        return jsonify({"summary": combined_summary})