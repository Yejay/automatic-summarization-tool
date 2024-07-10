# Automatic Summarization Tool Backend: Code Documentation

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Code Structure](#2-code-structure)
3. [Core Components](#3-core-components)
4. [Summarization Models](#4-summarization-models)
5. [Data Processing](#5-data-processing)
6. [Visualization Scripts](#6-visualization-scripts)
7. [Key Functions and Workflows](#7-key-functions-and-workflows)
8. [Extension and Customization](#8-extension-and-customization)
9. [Testing](#9-testing)
10. [Performance Considerations](#10-performance-considerations)

## 1. Project Overview

The Automatic Summarization Tool Backend is a Flask-based application that provides APIs for summarizing research papers and evaluating the quality of these summaries. It supports multiple summarization models and uses advanced metrics for evaluation.

## 2. Code Structure

```
app/
├── __init__.py
├── routes.py
├── evaluate_summaries.py
├── utils.py
├── summarizers/
│   ├── __init__.py
│   ├── bart_summarizer.py
│   ├── pegasus_summarizer.py
│   └── openai_summarizer.py
└── scripts/
    └── diagram.py
```

## 3. Core Components

### Main Application (app/__init__.py)

This file initializes the Flask application and sets up any necessary configurations.

```python
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    with app.app_context():
        from .routes import register_routes
        register_routes(app)
    return app
```

Key points:
- Uses Flask for the web framework
- Enables CORS for cross-origin requests
- Registers routes using a separate function for better organization

### API Routes (app/routes.py)

Defines the API endpoints for the application.

```python
def register_routes(app):
    @app.route("/summarize_bart", methods=["POST"])
    def summarize_bart_endpoint():
        # Implementation

    @app.route("/summarize_pegasus", methods=["POST"])
    def summarize_pegasus_endpoint():
        # Implementation

    @app.route("/summarize_openai", methods=["POST"])
    def summarize_openai_endpoint():
        # Implementation

    @app.route("/evaluate_summaries", methods=["POST"])
    def evaluate_summaries_route():
        # Implementation
```

Key points:
- Each summarization model has its own endpoint
- Evaluation endpoint for assessing summary quality
- All endpoints use POST method for data submission

### Summary Evaluation (app/evaluate_summaries.py)

Contains the logic for evaluating summaries using ROUGE and BERTScore metrics.

```python
from bert_score import score
from rouge_score import rouge_scorer

def evaluate_summaries(studies_file_path):
    # Load studies
    # For each study:
    #   - Load reference and generated summaries
    #   - Calculate ROUGE scores
    #   - Calculate BERTScore
    #   - Compile results
    # Return compiled results
```

Key points:
- Uses `rouge_score` for ROUGE metric calculation
- Uses `bert_score` for semantic similarity evaluation
- Processes multiple studies and summarization models

### Utility Functions (app/utils.py)

Provides utility functions for text processing and file handling.

```python
from pypdf import PdfReader

def extract_text(file):
    # Extract text from PDF or text file

def clean_text(text):
    # Remove URLs, email addresses, special characters
    # Normalize whitespace
    # Remove references

def split_text(text, tokenizer, chunk_size, chunk_overlap=150):
    # Split text into chunks for processing

def summarize_chunk(chunk, summarizer, min_length, max_length):
    # Summarize a single chunk of text

def combine_summaries(summaries):
    # Combine multiple summary chunks
```

Key points:
- Handles both PDF and text file inputs
- Implements text cleaning and normalization
- Provides functions for text chunking and recombining

## 4. Summarization Models

### BART Summarizer (app/summarizers/bart_summarizer.py)

Implements text summarization using the BART model.

```python
from transformers import pipeline, BartTokenizer

bart_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

def summarize_bart(file, min_length, max_length):
    # Extract text
    # Process and summarize text
    # Return summary
```

### PEGASUS Summarizer (app/summarizers/pegasus_summarizer.py)

Implements text summarization using the PEGASUS model.

```python
from transformers import pipeline, PegasusTokenizer

pegasus_summarizer = pipeline("summarization", model="google/pegasus-pubmed")
pegasus_tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-pubmed")

def summarize_pegasus(file, min_length, max_length):
    # Extract text
    # Process and summarize text
    # Return summary
```

### OpenAI Summarizer (app/summarizers/openai_summarizer.py)

Implements text summarization using OpenAI's GPT models.

```python
from openai import OpenAI
from dotenv import load_dotenv

client = OpenAI()

def summarize_openai(file, max_tokens):
    # Extract text
    # Send text to OpenAI API for summarization
    # Return summary
```

Key points for all summarizers:
- Each summarizer uses a different underlying model or API
- They share a similar interface for consistency
- Text extraction and processing use shared utility functions

## 5. Data Processing

Data processing is primarily handled in `utils.py` and includes:
- Text extraction from PDF and text files
- Text cleaning and normalization
- Chunking of large texts for processing
- Combining summarized chunks

## 6. Visualization Scripts

### Diagram Generator (app/scripts/diagram.py)

Generates visualizations for analysis of summarization results.

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def generate_processing_time_chart(studies, bart_times, pegasus_times, gpt_times):
    # Generate bar chart of processing times

def generate_metric_comparison_charts(precision, recall, f1):
    # Generate charts comparing different metrics across models
```

Key points:
- Uses matplotlib and seaborn for chart generation
- Creates visualizations for processing times and evaluation metrics

## 7. Key Functions and Workflows

1. Summarization Workflow:
   - Receive file through API
   - Extract and preprocess text
   - Split text into chunks if necessary
   - Apply chosen summarization model
   - Combine chunks if split
   - Return final summary

2. Evaluation Workflow:
   - Load study data
   - For each study:
     - Load reference and generated summaries
     - Calculate ROUGE scores
     - Calculate BERTScore
   - Compile and return results

3. Visualization Workflow:
   - Collect summarization and evaluation data
   - Generate processing time charts
   - Generate metric comparison charts
   - Save or return visualizations

## 8. Extension and Customization

To add a new summarization model:
1. Create a new file in the `summarizers` directory
2. Implement the summarization function with a consistent interface
3. Add a new route in `routes.py` for the new model
4. Update the evaluation logic in `evaluate_summaries.py` if necessary

To modify evaluation metrics:
1. Update the `evaluate_summaries` function in `evaluate_summaries.py`
2. Ensure new metrics are calculated and returned in the results


## 10. Performance Considerations

- Text chunking is used to handle large documents efficiently
- Consider implementing caching for API responses
- For large-scale processing, consider implementing a task queue system (e.g., Celery)
- Monitor API rate limits, especially for the OpenAI summarizer

---

This documentation provides an in-depth look at the code structure and implementation details of the Automatic Summarization Tool Backend. For setup instructions, API usage, and deployment guidelines, please refer to the separate developer documentation.

This documentation was partially generated with generative AI.