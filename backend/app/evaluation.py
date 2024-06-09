from rouge_score import rouge_scorer

def calculate_rouge_scores(references, generated_summaries):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = []
    for ref, gen in zip(references, generated_summaries):
        score = scorer.score(ref, gen)
        scores.append(score)
    return scores

def print_scores(model_name, scores):
    print(f"ROUGE Scores for {model_name}:")
    for i, score in enumerate(scores):
        print(f"Document {i+1}:")
        print(f"  ROUGE-1: {score['rouge1']}")
        print(f"  ROUGE-2: {score['rouge2']}")
        print(f"  ROUGE-L: {score['rougeL']}")