# Import necessary modules from the transformers library
from transformers import pipeline, PegasusTokenizer

# Import utility functions from the utils module
from ..utils import extract_text, summarize_text

# Initialize the Pegasus summarizer using the pre-trained "google/pegasus-pubmed" model
pegasus_summarizer = pipeline("summarization", model="google/pegasus-pubmed")
# Initialize the Pegasus tokenizer using the same pre-trained model
pegasus_tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-pubmed")

# Function to summarize a text file using the Pegasus model
def summarize_pegasus(file, min_length, max_length):
    # Extract the text from the file
    text = extract_text(file)
    # Summarize the text using the Pegasus summarizer and tokenizer
    # The text is split into chunks of 512 tokens, and the reduce step is used
    final_summary = summarize_text(
        text,
        chunk_size=1024,
        summarizer=pegasus_summarizer,
        tokenizer=pegasus_tokenizer,
        min_length=min_length,
        max_length=max_length,
        # Set to True to resummarize the combined text after the first round of summarization
        use_reduce_step=True,
    )
    # Return the final summary
    return final_summary
