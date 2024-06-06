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
    print(text, file=sys.stderr)
    return text

def split_text(text, max_length, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=max_length, padding=False)
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

def combine_summaries(summaries, tokenizer, summarizer, max_length):
    combined_text = " ".join(summaries)
    final_chunks = split_text(combined_text, max_length, tokenizer)
    final_summary = []

    for chunk in final_chunks:
        summary = summarizer(chunk, do_sample=False)
        final_summary.append(summary[0]["summary_text"])

    return " ".join(final_summary)

def map_reduce_summarize(text, max_length, summarizer, tokenizer):
    # Split the text into smaller chunks
    chunks = split_text(text, max_length, tokenizer)

    # First round of summarization (map step)
    first_round_summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, do_sample=False)
        first_round_summaries.append(summary[0]["summary_text"])

    # Combine summaries and perform a second round of summarization (reduce step)
    return combine_summaries(first_round_summaries, tokenizer, summarizer, max_length)
