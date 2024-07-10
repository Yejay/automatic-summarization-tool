import re
import unicodedata
from pypdf import PdfReader
from io import BytesIO

def extract_text(file):
    if isinstance(file, str):
        if file.endswith(".pdf"):
            with open(file, "rb") as f:
                pdf = PdfReader(f)
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
        else:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
    else:
        if file.filename.endswith(".pdf"):
            pdf = PdfReader(BytesIO(file.read()))
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        else:
            text = file.read().decode("utf-8", errors="ignore")
    return text

def is_reference(line):
    patterns = [
        r"^\[\d+\]",  # [1], [2], etc. (IEEE)
        r"^\d+\.",  # 1. 2. etc. (numerische Stile)
        r"^\(\d+\)",  # (1), (2), etc.
        r"\(\d{4}\)",  # (2020), (2019), etc. (APA)
        r"^\d{4}",  # 2020, 2019 am Anfang der Zeile
        r"\d{4}\)$",  # 2020), 2019) am Ende der Zeile
        r"et al\., \d{4}",  # et al., 2020 (Harvard)
        r"\[\d{4}\]",  # [2020], [2019] (Jahr in eckigen Klammern)
        r"doi:.*$",  # DOI-Links
        r"http[s]?://\S+",  # URLs
    ]
    for pattern in patterns:
        if re.search(pattern, line):
            return True
    return False

def clean_text(text):
    # Remove URLs and email addresses
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)

    # Remove numbers and special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Normalize whitespace and remove extra spaces
    text = ' '.join(text.split())

    # Split text into lines and remove references and empty lines
    lines = text.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip() and not is_reference(line)]

    # Combine lines back into a single string
    combined_lines = []
    for i in range(len(cleaned_lines)):
        if i > 0 and cleaned_lines[i][0].islower():
            combined_lines[-1] += " " + cleaned_lines[i]
        else:
            combined_lines.append(cleaned_lines[i])

    # Join the lines into a single text
    normalized_text = "\n".join(combined_lines)
    
    # Normalize unicode characters
    normalized_text = unicodedata.normalize("NFKD", normalized_text)
    return normalized_text

# Function to split text into chunks
def split_text(text, tokenizer, chunk_size, chunk_overlap=150):
    if not isinstance(text, str):
        raise ValueError(f"Expected text to be a str, but got {type(text)}")
    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, max_length=chunk_size, padding=False
    )
    input_ids = inputs["input_ids"].squeeze(0).tolist()
    total_tokens = len(input_ids)

    chunks = []
    start = 0
    while (start < total_tokens):
        end = min(start + chunk_size, total_tokens)
        chunk = tokenizer.decode(input_ids[start:end], skip_special_tokens=True)
        chunks.append(chunk)
        start += chunk_size - chunk_overlap
    return chunks


def summarize_chunk(chunk, summarizer, min_length, max_length):
    input_length = len(chunk.split())
    dynamic_max_length = min(max_length, max(min_length, input_length // 2))
    summary = summarizer(
        chunk, min_length=min_length, max_length=dynamic_max_length, do_sample=False
    )
    return summary[0]["summary_text"]

def combine_summaries(summaries):
    return " ".join(summaries)


def summarize_text(
    text,
    chunk_size,
    summarizer,
    tokenizer,
    min_length,
    max_length,
    use_reduce_step,
):
    cleaned_text = clean_text(text)

    chunks = split_text(cleaned_text, tokenizer, chunk_size)

    first_round_summaries = [
        summarize_chunk(chunk, summarizer, min_length, max_length) for chunk in chunks
    ]

    if not use_reduce_step:
        return combine_summaries(first_round_summaries)

    combined_text = combine_summaries(first_round_summaries)
    final_chunks = split_text(combined_text, tokenizer, chunk_size)

    final_summaries = [
        summarize_chunk(chunk, summarizer, min_length, max_length)
        for chunk in final_chunks
    ]

    return combine_summaries(final_summaries)
