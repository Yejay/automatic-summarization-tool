export const API_BASE_URL = 'http://localhost:5000';

export const MODELS = {
  BART: 'bart',
  PEGASUS: 'pegasus',
  OPENAI: 'openai',
};

export const MODEL_ENDPOINTS = {
  [MODELS.BART]: 'summarize_bart',
  [MODELS.PEGASUS]: 'summarize_pegasus',
  [MODELS.OPENAI]: 'summarize_openai',
};