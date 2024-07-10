# Automatic Summarization Tool

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running the Application](#running-the-application)
6. [Usage](#usage)
7. [API Documentation](#api-documentation)
8. [Contributing](#contributing)
9. [License](#license)
10. [Acknowledgments](#acknowledgments)

## Project Overview

The Automatic Summarization Tool is a full-stack web application designed to summarize research papers using various state-of-the-art natural language processing models. It provides a user-friendly interface for uploading documents, selecting summarization models, and evaluating the quality of generated summaries.

- [Frontend Documentation](frontend/README.md)
- [Backend Documentation](backend/README.md)

## Features

- Support for multiple summarization models (BART, PEGASUS, OpenAI GPT)
- File upload for PDF and text documents
- Text extraction and preprocessing
- Summary evaluation using ROUGE and BERTScore metrics
- Visualization of evaluation results

## Technology Stack

### Frontend
- React
- TypeScript
- CSS (with standard stylesheets)
- Vite (build tool)

### Backend
- Python
- Flask
- Transformers (Hugging Face)
- OpenAI API
- rouge_score (for ROUGE metrics)
- bert_score (for BERTScore metrics)
- Matplotlib (for visualizations)

## Dependencies

### Frontend Dependencies
- react
- react-dom
- typescript

### Backend Dependencies
- flask
- flask-cors
- transformers
- torch(PyTorch, required by Transformers)
- openai
- python-dotenv
- pypdf
- rouge-score
- bert-score
- matplotlib

For a complete list of dependencies and their versions, please refer to the `package.json` file in the frontend directory and the `requirements.txt` file in the backend directory.


## Project Structure

```
automatic-summarization-tool/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types/
│   │   ├── utils/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── package.json
│   └── README.md
├── backend/
│   ├── app/
│   │   ├── summarizers/
│   │   ├── scripts/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── evaluate_summaries.py
│   │   └── utils.py
│   ├── data/
│   ├── output/
│   ├── requirements.txt
│   ├── run.py
│   └── README.md
└── README.md (this file)
```

## Getting Started

### Prerequisites

- Node.js (v14 or later)
- Python (v3.8 or later)
- pip (Python package manager)
- Virtual environment tool (e.g., venv)

### Installation

1. Set up the frontend:
   ```
   cd frontend
   npm install
   ```

2. Set up the backend:
   ```
   cd ../backend
   python -m venv venv or python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the `backend` directory
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`

### Running the Application

1. Start the backend server:
   ```
   cd backend
   python run.py
   ```

2. In a new terminal, start the frontend development server:
   ```
   cd frontend
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:5173` (or the port specified by Vite).

## Usage

1. Upload a PDF or text file containing the research paper you want to summarize. As this is a POC (Proof of Concept), please use one of the provided research papers in `data/research-papers`.
2. Select a summarization model (BART, PEGASUS, or OpenAI).
3. Click the "Summarize" button to generate a summary.
4. View the generated summary and evaluation metrics.
5. Optionally, compare summaries from different models using the evaluation results.

For more detailed usage instructions, refer to the frontend and backend documentation.

## API Documentation

The backend provides the following API endpoints:

- `POST /summarize_bart`: Summarize text using the BART model
- `POST /summarize_pegasus`: Summarize text using the PEGASUS model
- `POST /summarize_openai`: Summarize text using OpenAI's model
- `POST /evaluate_summaries`: Evaluate the quality of generated summaries

For detailed API specifications, refer to the [Backend Documentation](backend/README.md#api-endpoints).


---

For more detailed information about the frontend or backend implementation, please refer to their respective README files linked at the top of this document.

This documentation was partially generated with generative AI.