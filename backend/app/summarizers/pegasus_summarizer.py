from transformers import pipeline, PegasusTokenizer
from ..utils import extract_text, split_text, map_reduce_summarize

# Initialize Pegasus summarizer and tokenizer
pegasus_summarizer = pipeline("summarization", model="google/pegasus-pubmed")
pegasus_tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-pubmed")

def summarize_pegasus(file):
    text = extract_text(file)
    combined_summary = map_reduce_summarize(text, 1024, pegasus_summarizer, pegasus_tokenizer)
    return combined_summary
