import React from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import ModelSelector from './components/ModelSelector';
import Summary from './components/Summary';
import EvaluationResults from './components/EvaluationResults';
import SummarizeButton from './components/SummarizeButton';
import { useSummarization, useEvaluation } from './hooks';
// import { MODELS } from './constants';

const MetricsExplanation = React.memo(() => (
  <>
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
  </>
));

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

  return (
    <div id='root'>
      <h1>Automatic Summarization Tool</h1>
      <div className='card'>
        <FileUpload onFileSelected={handleFileSelected} />
        <ModelSelector selectedModel={model} onModelChange={setModel} />
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px', marginTop: '20px' }}>
          <SummarizeButton 
            onSummarize={handleSummarize} 
            isLoading={loadingSummarize} 
            isDisabled={!selectedFile}
          />
          {loadingSummarize && <div className='spinner'></div>}
          {error && <div style={{ color: 'red' }}>{error}</div>}
          <Summary summary={summary} onDelete={handleDelete} />
          <div className='divider'></div>
          <MetricsExplanation />
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