from transformers import pipeline, PegasusTokenizer
from ..utils import extract_text, summarize_text

pegasus_summarizer = pipeline("summarization", model="google/pegasus-pubmed")
pegasus_tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-pubmed")

def summarize_pegasus(file, min_length, max_length):
    text = extract_text(file)
    final_summary = summarize_text(
        text,
        chunk_size=1024,
        summarizer=pegasus_summarizer,
        tokenizer=pegasus_tokenizer,
        min_length=min_length,
        max_length=max_length,
        use_reduce_step=True,
    )
    return final_summary
