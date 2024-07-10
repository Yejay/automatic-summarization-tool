import { EvaluationResult } from '../types';
import { API_BASE_URL, MODEL_ENDPOINTS } from '../constants';

export const summarizeText = async (file: File, model: string): Promise<string> => {
  const formData = new FormData();
  formData.append('file', file);

  const endpoint = MODEL_ENDPOINTS[model] || MODEL_ENDPOINTS.bart;

  const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Failed to summarize text');
  }

  const data = await response.json();
  return data.summary;
};

export const evaluateSummaries = async (): Promise<EvaluationResult[]> => {
  const response = await fetch(`${API_BASE_URL}/evaluate_summaries`, {
    method: 'POST',
  });

  if (!response.ok) {
    throw new Error('Failed to evaluate summaries');
  }

  return await response.json();
};