from transformers import pipeline, BartTokenizer
from ..utils import extract_text, summarize_text

bart_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

def summarize_bart(file, min_length, max_length):
    text = extract_text(file)
    final_summary = summarize_text(
        text,
        chunk_size=1024,
        summarizer=bart_summarizer,
        tokenizer=bart_tokenizer,
        min_length=min_length,
        max_length=max_length,
        use_reduce_step=True,
    )
    return final_summary
