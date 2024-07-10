export interface EvaluationResult {
    study_id: string;
    scores: {
      bart: { rouge1: number[]; rouge2: number[]; rougeL: number[]; bertscore: number[] };
      pegasus: { rouge1: number[]; rouge2: number[]; rougeL: number[]; bertscore: number[] };
      openai: { rouge1: number[]; rouge2: number[]; rougeL: number[]; bertscore: number[] };
    };
  }