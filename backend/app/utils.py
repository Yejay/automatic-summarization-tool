from pypdf import PdfReader
from io import BytesIO


# Function to extract text from a file
def extract_text(file):
    # Check if the file is a PDF
    if file.filename.endswith(".pdf"):
        # Read the PDF file
        pdf = PdfReader(BytesIO(file.read()))
        text = ""
        # Loop through each page in the PDF
        for page in pdf.pages:
            # Extract the text from the page
            page_text = page.extract_text()
            # If the page contains text, add it to the overall text
            if page_text:
                text += page_text
    else:
        # If the file is not a PDF, read the text directly
        text = file.read().decode("utf-8", errors="ignore")
    # Return the extracted text
    return text


# Function to split text into chunks
def split_text(text, tokenizer, chunk_size=512, chunk_overlap=100):
    # Tokenize the text and get the input IDs
    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, max_length=chunk_size, padding=False
    )
    input_ids = inputs["input_ids"].squeeze(0).tolist()
    total_tokens = len(input_ids)

    chunks = []
    start = 0
    # Loop until all tokens have been processed
    while start < total_tokens:
        # Determine the end index for the current chunk
        end = min(start + chunk_size, total_tokens)
        # Decode the tokens to get the chunk text
        chunk = tokenizer.decode(input_ids[start:end], skip_special_tokens=True)
        # Add the chunk to the list of chunks
        chunks.append(chunk)
        # Move the start index to the next chunk, overlapping as specified
        start += chunk_size - chunk_overlap
    # Return the list of chunks
    return chunks


# Function to summarize a chunk of text
def summarize_chunk(chunk, summarizer, max_length=512, min_length=30):
    # Determine the maximum length for the summary
    input_length = len(chunk.split())
    dynamic_max_length = min(max_length, max(min_length, input_length // 2))
    # Generate the summary
    summary = summarizer(chunk, max_length=dynamic_max_length, min_length=min_length, do_sample=False)
    # Return the summary text
    return summary[0]["summary_text"]


# Function to combine multiple summaries into a single text
def combine_summaries(summaries):
    # Join the summaries with spaces in between
    return " ".join(summaries)


# Function to summarize large text
def summarize_text(text, chunk_size, summarizer, tokenizer, max_length=512, min_length=30, use_reduce_step=True):
    # Split the text into chunks
    chunks = split_text(text, tokenizer, chunk_size)

    # Summarize each chunk (map step)
    first_round_summaries = [summarize_chunk(chunk, summarizer, max_length, min_length) for chunk in chunks]

    # If not using the reduce step, return the combined summaries
    if not use_reduce_step:
        return combine_summaries(first_round_summaries)

    # Combine the summaries and split them into chunks again
    combined_text = combine_summaries(first_round_summaries)
    final_chunks = split_text(combined_text, tokenizer, chunk_size)

    # Summarize each final chunk (reduce step)
    final_summaries = [summarize_chunk(chunk, summarizer, max_length, min_length) for chunk in final_chunks]

    # Return the final combined summary
    return combine_summaries(final_summaries)
