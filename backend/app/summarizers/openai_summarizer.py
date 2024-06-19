# Import necessary modules
from openai import OpenAI
from dotenv import load_dotenv
from ..utils import extract_text
import os

# Load environment variables from a .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI()


# Function to summarize a text file using the OpenAI GPT-3 model
def summarize_openai(file, max_tokens):
    # Extract the text from the file
    text = extract_text(file)
    # Create a chat completion with the GPT-3 model
    # The model is given the role of a sports scientist specializing in summarizing research papers
    # The user's message is to summarize the extracted text
    # The temperature is set to 0.7 to balance between randomness and determinism in the output
    # The maximum number of tokens in the output is set to 64
    # The top_p parameter is set to 1 to use nucleus sampling, which can improve the quality of the output
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
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
    # Extract the content of the model's message from the response
    summary = response.choices[0].message.content
    # Return the summary
    return summary
