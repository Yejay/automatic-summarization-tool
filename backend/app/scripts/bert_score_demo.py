import os
import torch
from transformers import pipeline
from bert_score import score
from rouge_score import rouge_scorer

# Define your references and generated summaries
references = [
    """Background: Suboptimal physical activity levels and tolerance, poor motor skills and poor physical health are
demonstrated in children with Autism Spectrum Disorder (ASD). We speculate that social interaction and
communication deficits in children with ASD are two major factors that hinder these children from actively
participating in group physical activities. While previous studies have demonstrated that exercise intervention improves
motor skills and behavioral outcomes in children with ASD, these programs tend to focus only on a single sport, which
may not cater to the interests of different children with ASD. In this protocol, a game-based exercise training program
designed by a multi-disciplinary team (pediatrics, physical education and psychology) will be implemented by front-
line healthcare providers trained following the train-the-trainer (TTT) model and subjected to validation.
Method: Using a randomized controlled trial design, the effectiveness of the game-based exercise program will be
examined for 112 young children with ASD. These children were randomly assigned to two groups, which will be
tested and trained in either one of the two arms of the waitlist conditions (control and intervention). The assessment
of physical and psychological traits will be conducted at baseline (pre-test), at 16-weeks (post-treatment) and at 32-
weeks (follow-up) of the program.
Discussion: Most of the interventions designed for ASD children target either their psychological traits or physical
conditions, without bridging the two states. With the recognition of bidirectional relations between mental and
physical health, the present game-based exercise program which includes multiple level of difficulties was developed
to equip ASD children with the necessary skills for engaging in sustainable team sports or even professional sport
training. The program, if effective, will provide an entertaining and engaging training for whole-person development
among children with ASD."""
]

generated_summaries = [
    """
The study protocol outlines a randomized controlled trial investigating the impact of a game-based exercise training program on physical fitness and mental health in children with Autism Spectrum Disorder (ASD). Children with ASD often face challenges with physical activity, motor skills, and overall health due to social and communication deficits. Previous research has shown that exercise interventions can improve motor skills and behavioral outcomes in children with ASD. However, existing programs often focus on a single sport, which may not cater to the diverse interests of children with ASD. In this protocol, a multidisciplinary team has developed a game-based exercise program to be implemented by healthcare providers trained under the train-the-trainer model. The program aims to improve physical and psychological traits in young children with ASD. The study will involve 112 participants randomized into control and intervention groups, with assessments conducted at baseline, post-treatment (16 weeks), and follow-up (32 weeks). The program includes various levels of difficulty and elements to engage children in sustainable team sports or professional training. By bridging the gap between mental and physical health, the game-based exercise program is designed to support whole-person development in children with ASD. The study intends to evaluate the efficacy of the program in improving motor skills, physical fitness, and reducing maladaptive behaviors in children with ASD. Additionally, the train-the-trainer model aims to ensure the sustainability and widespread implementation of the program in community settings. The study protocol provides a detailed description of the intervention, assessment methods, sample size calculations, statistical analysis plan, and ethical considerations.
"""
]

# Calculate BERTScore
P, R, F1 = score(generated_summaries, references, lang="en", return_hash=False)

# Calculate ROUGE Score
scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)

# Print BERTScore
print(
    f"BERTScore - Precision: {P.mean():.4f}, Recall: {R.mean():.4f}, F1: {F1.mean():.4f}"
)


# Assuming there's a one-to-one correspondence between generated_summaries and references
for generated_summary, reference in zip(generated_summaries, references):
    scores = scorer.score(reference, generated_summary)  # Note the order of arguments

    # Print ROUGE Scores for each pair
    print(f"ROUGE-1 Score - Precision: {scores['rouge1'].precision:.4f}, Recall: {scores['rouge1'].recall:.4f}, F1: {scores['rouge1'].fmeasure:.4f}")
    print(f"ROUGE-2 Score - Precision: {scores['rouge2'].precision:.4f}, Recall: {scores['rouge2'].recall:.4f}, F1: {scores['rouge2'].fmeasure:.4f}")
    print(f"ROUGE-L Score - Precision: {scores['rougeL'].precision:.4f}, Recall: {scores['rougeL'].recall:.4f}, F1: {scores['rougeL'].fmeasure:.4f}")