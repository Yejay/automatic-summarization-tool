import { useState } from 'react';
import { evaluateSummaries } from '../services/api';
import { EvaluationResult } from '../types';

export const useEvaluation = () => {
  const [evaluationResults, setEvaluationResults] = useState<EvaluationResult[] | null>(null);
  const [loadingEvaluate, setLoadingEvaluate] = useState<boolean>(false);

  const handleEvaluation = async () => {
    setLoadingEvaluate(true);
    try {
      const results = await evaluateSummaries();
      setEvaluationResults(results);
    } catch (error) {
      console.error('Error evaluating summaries:', error);
    } finally {
      setLoadingEvaluate(false);
    }
  };

  return { evaluationResults, loadingEvaluate, handleEvaluation };
};