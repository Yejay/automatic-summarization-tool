from pypdf import PdfReader
from io import BytesIO
import sys

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
    # print(text, file=sys.stderr)
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
    chunks = split_text(text, max_length, tokenizer)
    first_round_summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, do_sample=False)
        first_round_summaries.append(summary[0]["summary_text"])

    combined_text = " ".join(first_round_summaries)
    final_summary = summarizer(combined_text, do_sample=False)
    return final_summary[0]["summary_text"]
