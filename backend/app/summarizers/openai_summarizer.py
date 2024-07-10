from openai import OpenAI
from dotenv import load_dotenv
from ..utils import extract_text
import os

load_dotenv()

client = OpenAI()

def summarize_openai(file, max_tokens):
    text = extract_text(file)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a sports scientist, specializing in summarizing research papers.",
            },
            {
                "role": "user",
                "content": "Summarize the following text, your answer should be a continuous text. No formatting or markdown in your response. Your response should be 1000 Tokens long:\n"
                + text,
            },
        ],
        temperature=0.7,
        top_p=1,
    )
    summary = response.choices[0].message.content
    return summary
