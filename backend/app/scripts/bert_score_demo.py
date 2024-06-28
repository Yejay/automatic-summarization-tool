import os
import torch
from transformers import pipeline
from bert_score import score
from rouge_score import rouge_scorer

# Define your references and generated summaries
references = [
    """Childhood growth and its sensitivity to dietary protein is reviewed within a Protein-Stat
model of growth regulation. The coordination of growth of muscle and stature is a combination of
genetic programming, and of two-way mechanical interactions involving the mechanotransduction
of muscle growth through stretching by bone length growth, the core Protein-Stat feature, and the
strengthening of bone through muscle contraction via the mechanostat. Thus, growth in bone length
is the initiating event and this is always observed. Endocrine and cellular mechanisms of growth
in stature are reviewed in terms of the growth hormone-insulin like growth factor-1 (GH-IGF-1)
and thyroid axes and the sex hormones, which together mediate endochondral ossification in the
growth plate and bone lengthening. Cellular mechanisms of muscle growth during development
are then reviewed identifying (a) the difficulties posed by the need to maintain its ultrastructure
during myofibre hypertrophy within the extracellular matrix and the concept of muscle as concentric
“bags” allowing growth to be conceived as bag enlargement and filling, (b) the cellular and molecular
mechanisms involved in the mechanotransduction of satellite and mesenchymal stromal cells, to
enable both connective tissue remodelling and provision of new myonuclei to aid myofibre hypertro-
phy and (c) the implications of myofibre hypertrophy for protein turnover within the myonuclear
domain. Experimental data from rodent and avian animal models illustrate likely changes in DNA
domain size and protein turnover during developmental and stretch-induced muscle growth and
between different muscle fibre types. Growth of muscle in male rats during adulthood suggests that
“bag enlargement” is achieved mainly through the action of mesenchymal stromal cells. Current un-
derstanding of the nutritional regulation of protein deposition in muscle, deriving from experimental
studies in animals and human adults, is reviewed, identifying regulation by amino acids, insulin
and myofibre volume changes acting to increase both ribosomal capacity and efficiency of muscle
protein synthesis via the mechanistic target of rapamycin complex 1 (mTORC1) and the phenomenon
of a “bag-full” inhibitory signal has been identified in human skeletal muscle. The final section
deals with the nutritional sensitivity of growth of muscle and stature to dietary protein in children.
Growth in length/height as a function of dietary protein intake is described in the context of the
breastfed child as the normative growth model, and the “Early Protein Hypothesis” linking high
protein intakes in infancy to later adiposity. The extensive paediatric studies on serum IGF-1 and
child growth are reviewed but their clinical relevance is of limited value for understanding growth
regulation; a role in energy metabolism and homeostasis, acting with insulin to mediate adiposity,
is probably more important. Information on the influence of dietary protein on muscle mass per
se as opposed to lean body mass is limited but suggests that increased protein intake in children
is unable to promote muscle growth in excess of that linked to genotypic growth in length/height.
One possible exception is milk protein intake, which cohort and cross-cultural studies suggest can
increase height and associated muscle growth, although such effects have yet to be demonstrated by
randomised controlled trials."""
]

generated_summaries = [
    """
The regulation of its growth in chil dren and maintenance in adult life is key to understanding human health and wellbeing throughout the life cycle. Low muscle mass and strength during childhood contribute to several adverse health outcomes and is linked to poor health outcomes in later life. Information on the inuence of dietary protein on muscle mass per se as opposed to lean body mass is limited but suggests that increased protein intake in children is unable to promote muscle growth in excess of that linked to genotypic growth in lengthheight. One possible exception is milk protein intake which cohort and crosscultural studies suggest can increase height and associated muscle growth although such effects have yet to be demonstrated by randomised controlled trials. The extensive paediatric studies on serum IGF and child growth are reviewed but their clinical relevance is of limited value for understanding growth regulation. For muscularity it is clear that muscles essential motor function means that the regulation of it growth in children and Maintenance in adultLife is key. To read the rest of the article click here: http:www.dailymail.co.uk/news/features/article-261556/muscle-mass-and-strength-in adolescent men is inversely associated with later cardiovascular disease CVD. To see more about CVD-risk in young men visit: www.daily Mail.com/News/Features/CVD- Risk factors-for-young-men-teenage men are linked to younger men’s muscle mass and strength in adolescent men. Back to the page you came from. The Daily Mail home. Click here to read the page that led to this article. The Digital Mail is proud to announce that we have published a new article on the link between muscle strength and cardiovascular disease in young men. We are happy to share this
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