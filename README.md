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
- Summary generation with customizable parameters
- Summary evaluation using ROUGE and BERTScore metrics
- Visualization of evaluation results
- RESTful API for integration with other applications

## Technology Stack

### Frontend
- React
- TypeScript
- Tailwind CSS
- Vite (build tool)

### Backend
- Python
- Flask
- Transformers (Hugging Face)
- PyTorch
- OpenAI API
- NLTK
- Matplotlib (for visualizations)

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

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/automatic-summarization-tool.git
   cd automatic-summarization-tool
   ```

2. Set up the frontend:
   ```
   cd frontend
   npm install
   ```

3. Set up the backend:
   ```
   cd ../backend
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

4. Set up environment variables:
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

1. Upload a PDF or text file containing the research paper you want to summarize.
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

## Contributing

We welcome contributions to the Automatic Summarization Tool! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature-name`)
6. Create a new Pull Request

For more information on contributing, please see our [Contributing Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE.md).

## Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/transformers/) for providing pre-trained models
- [OpenAI](https://openai.com/) for their GPT models and API
- [NLTK](https://www.nltk.org/) for natural language processing utilities
- [Flask](https://flask.palletsprojects.com/) for the backend web framework
- [React](https://reactjs.org/) for the frontend library
- All contributors and supporters of this project

---

For more detailed information about the frontend or backend implementation, please refer to their respective README files linked at the top of this document.
