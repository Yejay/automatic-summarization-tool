from openai import OpenAI
from dotenv import load_dotenv
from ..utils import extract_text
import os

load_dotenv()

client = OpenAI()

def summarize_openai(file):
    text = extract_text(file)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": "You are a sports scientist, specializing in summarizing research papers.",
            },
            {
                "role": "user",
                "content": "Summarize the following text:\n" + text,
            },
        ],
        temperature=0.7,
        max_tokens=64,
        top_p=1,
    )
    summary = response.choices[0].message.content
    return summary
