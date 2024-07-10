import React from 'react';
import { EvaluationResult } from '../../types';
import { formatScores } from '../../utils/formatters';

interface EvaluationResultsProps {
  results: EvaluationResult[] | null;
}

const EvaluationResults: React.FC<EvaluationResultsProps> = ({ results }) => {
  if (!results) return null;

  return (
    <div style={{ marginTop: '20px' }}>
      <h2>Evaluation Metrics</h2>
      <table className='styled-table'>
        <thead>
          <tr>
            <th>Study ID</th>
            <th>Model</th>
            <th>ROUGE-1</th>
            <th>ROUGE-2</th>
            <th>ROUGE-L</th>
            <th>BERTScore</th>
          </tr>
        </thead>
        <tbody>
          {results.map((result) => (
            <React.Fragment key={result.study_id}>
              <tr>
                <td rowSpan={3}>{result.study_id}</td>
                <td>BART</td>
                <td>{formatScores(result.scores.bart.rouge1)}</td>
                <td>{formatScores(result.scores.bart.rouge2)}</td>
                <td>{formatScores(result.scores.bart.rougeL)}</td>
                <td>{formatScores(result.scores.bart.bertscore)}</td>
              </tr>
              <tr>
                <td>PEGASUS</td>
                <td>{formatScores(result.scores.pegasus.rouge1)}</td>
                <td>{formatScores(result.scores.pegasus.rouge2)}</td>
                <td>{formatScores(result.scores.pegasus.rougeL)}</td>
                <td>{formatScores(result.scores.pegasus.bertscore)}</td>
              </tr>
              <tr>
                <td>OpenAI</td>
                <td>{formatScores(result.scores.openai.rouge1)}</td>
                <td>{formatScores(result.scores.openai.rouge2)}</td>
                <td>{formatScores(result.scores.openai.rougeL)}</td>
                <td>{formatScores(result.scores.openai.bertscore)}</td>
              </tr>
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default EvaluationResults;