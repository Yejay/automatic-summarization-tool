# Automatic Summarization Tool Documentation

## Table of Contents

1. [Application Overview](#1-application-overview)
2. [Core Components](#2-core-components)
3. [Custom Hooks](#3-custom-hooks)
4. [Services and API](#4-services-and-api)
5. [Utilities and Constants](#5-utilities-and-constants)
6. [Styling and CSS](#6-styling-and-css)
7. [Types](#7-types)
8. [Application Entry Point](#8-application-entry-point)
9. [Conclusion](#conclusion)

## 1. Application Overview

The Automatic Summarization Tool is a React-based web application that allows users to upload text files, generate summaries using different models, and evaluate the quality of these summaries using various metrics. The application is built with TypeScript and uses modern React patterns such as hooks for state management and componentization for better code organization.

### Main Structure

- `src/`: Root directory for all source code
  - `components/`: React components used throughout the application
  - `hooks/`: Custom React hooks for state management and logic
  - `services/`: API service for communication with the backend
  - `types/`: TypeScript type definitions
  - `utils/`: Utility functions
  - `App.tsx`: Main application component
  - `main.tsx`: Entry point of the application

### Key Features

1. File upload functionality
2. Model selection for summarization
3. Text summarization
4. Summary evaluation using ROUGE and BERTScore metrics
5. Display of evaluation results

## 2. Core Components

### App.tsx

`App.tsx` is the main component of the application. It orchestrates the overall structure and flow of the user interface.

Key responsibilities:
- Imports and uses custom hooks (`useSummarization` and `useEvaluation`)
- Renders child components (`FileUpload`, `ModelSelector`, `Summary`, `EvaluationResults`, `SummarizeButton`)
- Manages the overall layout and user interaction flow

```typescript
import React from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import ModelSelector from './components/ModelSelector';
import Summary from './components/Summary';
import EvaluationResults from './components/EvaluationResults';
import SummarizeButton from './components/SummarizeButton';
import { useSummarization, useEvaluation } from './hooks';
import { MODELS } from './constants';

// ... (MetricsExplanation component)

function App() {
  const { 
    summary, 
    model, 
    loadingSummarize, 
    selectedFile, 
    error,
    setModel, 
    handleFileSelected, 
    handleSummarize, 
    handleDelete 
  } = useSummarization();
  const { evaluationResults, loadingEvaluate, handleEvaluation } = useEvaluation();

  // ... (component JSX)
}

export default App;
```

### FileUpload.tsx

`FileUpload.tsx` is responsible for handling file uploads through drag-and-drop or file selection.

Key features:
- Drag and drop functionality
- File input for manual selection
- Display of selected file name
- Callback to parent component with selected file

```typescript
import React, { useState, useRef } from 'react';

interface FileUploadProps {
  onFileSelected: (file: File) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileSelected }) => {
  // ... (component logic and JSX)
};

export default FileUpload;
```

### ModelSelector.tsx

`ModelSelector.tsx` allows users to choose the summarization model.

Key features:
- Displays available models from the `MODELS` constant
- Handles model selection and updates parent component

```typescript
import React from 'react';
import { MODELS } from '../../constants';

interface ModelSelectorProps {
  selectedModel: string;
  onModelChange: (model: string) => void;
}

const ModelSelector: React.FC<ModelSelectorProps> = ({ selectedModel, onModelChange }) => {
  // ... (component logic and JSX)
};

export default ModelSelector;
```

### Summary.tsx

`Summary.tsx` displays the generated summary and provides an option to delete it.

Key features:
- Renders the summary text
- Provides a delete button to clear the summary

```typescript
import React from 'react';

interface SummaryProps {
  summary: string;
  onDelete: () => void;
}

const Summary: React.FC<SummaryProps> = ({ summary, onDelete }) => {
  // ... (component logic and JSX)
};

export default Summary;
```

### SummarizeButton.tsx

`SummarizeButton.tsx` is a reusable button component for triggering the summarization process.

Key features:
- Displays appropriate text based on loading state
- Disables button when necessary (e.g., during summarization or when no file is selected)

```typescript
import React from 'react';

interface SummarizeButtonProps {
  onSummarize: () => void;
  isLoading: boolean;
  isDisabled: boolean;
}

const SummarizeButton: React.FC<SummarizeButtonProps> = ({ onSummarize, isLoading, isDisabled }) => {
  // ... (component logic and JSX)
};

export default SummarizeButton;
```

### EvaluationResults.tsx

`EvaluationResults.tsx` displays the evaluation metrics for the generated summaries.

Key features:
- Renders a table with evaluation scores (ROUGE-1, ROUGE-2, ROUGE-L, BERTScore) for each model
- Uses the `formatScores` utility function to format the scores

```typescript
import React from 'react';
import { EvaluationResult } from '../../types';
import { formatScores } from '../../utils/formatters';

interface EvaluationResultsProps {
  results: EvaluationResult[] | null;
}

const EvaluationResults: React.FC<EvaluationResultsProps> = ({ results }) => {
  // ... (component logic and JSX)
};

export default EvaluationResults;
```

## 3. Custom Hooks

### useSummarization

Location: `src/hooks/useSummarization.ts`

The `useSummarization` hook manages the state and logic for the summarization process.

Key features:
- Manages state for summary, selected model, loading state, selected file, and errors
- Provides functions for file selection, summarization, and summary deletion
- Interacts with the API service to generate summaries

```typescript
import { useState } from 'react';
import { summarizeText } from '../services/api';

export const useSummarization = () => {
  const [summary, setSummary] = useState<string>('');
  const [model, setModel] = useState<string>('bart');
  const [loadingSummarize, setLoadingSummarize] = useState<boolean>(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  // ... (hook logic)

  return { 
    summary, 
    model, 
    loadingSummarize, 
    selectedFile, 
    error,
    setModel, 
    handleFileSelected, 
    handleSummarize, 
    handleDelete 
  };
};
```

### useEvaluation

Location: `src/hooks/useEvaluation.ts`

The `useEvaluation` hook manages the state and logic for the summary evaluation process.

Key features:
- Manages state for evaluation results and loading state
- Provides a function to trigger the evaluation process
- Interacts with the API service to fetch evaluation results

```typescript
import { useState } from 'react';
import { evaluateSummaries } from '../services/api';
import { EvaluationResult } from '../types';

export const useEvaluation = () => {
  const [evaluationResults, setEvaluationResults] = useState<EvaluationResult[] | null>(null);
  const [loadingEvaluate, setLoadingEvaluate] = useState<boolean>(false);

  // ... (hook logic)

  return { evaluationResults, loadingEvaluate, handleEvaluation };
};
```

## 4. Services and API

### api.ts

Location: `src/services/api.ts`

The `api.ts` file contains functions for interacting with the backend API.

Key functions:
- `summarizeText`: Sends a file to the server for summarization
- `evaluateSummaries`: Requests evaluation of generated summaries

```typescript
import { EvaluationResult } from '../types';
import { API_BASE_URL, MODEL_ENDPOINTS } from '../constants';

export const summarizeText = async (file: File, model: string): Promise<string> => {
  // ... (API call logic)
};

export const evaluateSummaries = async (): Promise<EvaluationResult[]> => {
  // ... (API call logic)
};
```

## 5. Utilities and Constants

### formatters.tsx

Location: `src/utils/formatters.tsx`

Contains utility functions for formatting data.

Key function:
- `formatScores`: Formats evaluation scores for display

```typescript
import React from 'react';

export const formatScores = (scores: number[] | undefined): React.ReactNode => {
  // ... (formatting logic)
};
```

### constants.ts

Location: `src/constants.ts`

Defines constant values used throughout the application.

Key constants:
- `API_BASE_URL`: Base URL for API calls
- `MODEL_ENDPOINTS`: Endpoints for different summarization models
- `MODELS`: Available summarization models

## 6. Styling and CSS

### App.css

Location: `src/App.css`

Contains styles specific to the main App component and some global styles.

Key features:
- Defines layout and styling for the main application container
- Styles for the file upload area, buttons, and tables
- Defines animations (e.g., spinner for loading states)

### index.css

Location: `src/index.css`

Contains global styles applied to the entire application.

Key features:
- Sets base font styles and colors
- Defines dark and light color schemes
- Sets basic styles for elements like buttons and links

## 7. Types

### index.ts (in types folder)

Location: `src/types/index.ts`

Defines TypeScript interfaces used throughout the application.

Key type:
- `EvaluationResult`: Defines the structure of evaluation results

```typescript
export interface EvaluationResult {
  study_id: string;
  scores: {
    bart: { rouge1: number[]; rouge2: number[]; rougeL: number[]; bertscore: number[] };
    pegasus: { rouge1: number[]; rouge2: number[]; rougeL: number[]; bertscore: number[] };
    openai: { rouge1: number[]; rouge2: number[]; rougeL: number[]; bertscore: number[] };
  };
}
```

## 8. Application Entry Point

### main.tsx

Location: `src/main.tsx`

The entry point of the React application.

Key responsibilities:
- Renders the main App component
- Sets up React strict mode

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

## Conclusion

This Automatic Summarization Tool is a well-structured React application that demonstrates good practices in component organization, state management with hooks, and TypeScript usage. The separation of concerns between components, hooks, and services makes the code modular and maintainable.

Key strengths of the application:
1. Modular component structure
2. Use of custom hooks for logic separation
3. TypeScript for improved type safety
4. Clear separation of API services
5. Responsive design with CSS

Areas for potential improvement or expansion:
1. Implement error handling and user feedback for API failures
2. Add unit and integration tests
3. Implement caching mechanisms for API responses
4. Consider adding more customization options for summarization
5. Explore options for visualizing evaluation results (e.g., charts or graphs)

This documentation was partially generated with generative AI.