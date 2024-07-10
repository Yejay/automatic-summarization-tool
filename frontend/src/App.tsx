import React, { useState } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import ModelSelector from './components/ModelSelector';
import Summary from './components/Summary';
import EvaluationResults from './components/EvaluationResults';
import { useSummarization, useEvaluation } from './hooks';
// import { MODELS } from './constants';

function App() {
  const { summary, model, loadingSummarize, setModel, handleSummarize, handleDelete } = useSummarization();
  const { evaluationResults, loadingEvaluate, handleEvaluation } = useEvaluation();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileSelected = (file: File) => {
    setSelectedFile(file);
  };

  const onSummarizeClick = () => {
    if (selectedFile) {
      handleSummarize(selectedFile);
    }
  };

  return (
    <div id='root'>
      <h1>Automatic Summarization Tool</h1>
      <div className='card'>
        <FileUpload onFileSelected={handleFileSelected} />
        <ModelSelector selectedModel={model} onModelChange={setModel} />
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px', marginTop: '20px' }}>
          <button 
            onClick={onSummarizeClick} 
            style={{ width: '25%', padding: '10px', backgroundColor: '#646cffaa', border: 'none', borderRadius: '5px' }}
            disabled={!selectedFile || loadingSummarize}
          >
            {loadingSummarize ? 'Summarizing...' : 'Summarize'}
          </button>
          {loadingSummarize && <div className='spinner'></div>}
          <Summary summary={summary} onDelete={handleDelete} />
          <div className='divider'></div>
          <h2>Understanding ROUGE and BERTScore Metrics</h2>
          <p>
            ROUGE (Recall-Oriented Understudy for Gisting Evaluation) is a set of metrics for evaluating automatic summarization and machine translation. Below is a brief explanation of
            what each ROUGE score indicates:
          </p>
          <ul>
            <li>
              <strong>ROUGE-1</strong>: Measures the overlap of unigrams (single words) between the system and reference summaries. Higher values indicate better performance.
            </li>
            <li>
              <strong>ROUGE-2</strong>: Measures the overlap of bigrams (two consecutive words) between the system and reference summaries. Higher values indicate better performance.
            </li>
            <li>
              <strong>ROUGE-L</strong>: Measures the longest common subsequence (LCS) between the system and reference summaries. Higher values indicate better performance.
            </li>
            <li>
              <strong>BERTScore</strong>: Evaluates text generation based on semantic similarity using BERT embeddings. Higher values indicate better semantic similarity.
            </li>
          </ul>
          <button 
            onClick={handleEvaluation} 
            style={{ width: '25%', padding: '10px', backgroundColor: '#646cffaa', border: 'none', borderRadius: '5px' }}
            disabled={loadingEvaluate}
          >
            {loadingEvaluate ? 'Evaluating...' : 'Evaluate Summaries'}
          </button>
          {loadingEvaluate && <div className='spinner'></div>}
        </div>
        <EvaluationResults results={evaluationResults} />
      </div>
    </div>
  );
}

export default App;