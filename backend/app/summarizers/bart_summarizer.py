# Import necessary modules from the transformers library
from transformers import pipeline, BartTokenizer

# Import utility functions from the utils module
from ..utils import extract_text, summarize_text

# Initialize the BART summarizer using the pre-trained "facebook/bart-large-cnn" model
bart_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
# Initialize the BART tokenizer using the same pre-trained model
bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")


# Function to summarize a text file using the BART model
def summarize_bart(file, min_length, max_length):
    # Extract the text from the file
    text = extract_text(file)
    # Summarize the text using the BART summarizer and tokenizer
    # The text is split into chunks of 512 tokens, and the reduce step is used
    final_summary = summarize_text(
        text,
        chunk_size=1024,
        summarizer=bart_summarizer,
        tokenizer=bart_tokenizer,
        min_length=min_length,
        max_length=max_length,
        # Set to True to resummarize the combined text after the first round of summarization
        use_reduce_step=True,
    )
    # Return the final summary
    return final_summary
