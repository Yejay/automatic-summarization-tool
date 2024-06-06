from transformers import pipeline, BartTokenizer
from ..utils import extract_text, split_text, map_reduce_summarize

# Initialize BART summarizer and tokenizer
bart_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

def summarize_bart(file):
    text = extract_text(file)
    combined_summary = map_reduce_summarize(text, 1024, bart_summarizer, bart_tokenizer)
    return combined_summary
