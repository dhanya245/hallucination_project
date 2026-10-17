# Literature Review: Hallucination Detection and Confidence Calibration

**Project:** DeBERTa-based hallucination detection with an ADVICE-inspired
confidence objective  
**Prepared:** 17 October 2026  
**Scope:** SHROOM hallucination detection, entailment/similarity methods,
LLM-based detection, confidence calibration, and answer-dependent confidence.

## Purpose and terminology

This review supports a study comparing a DeBERTa hallucination classifier
with confidence-aware variants. SHROOM includes machine translation (MT),
paraphrase generation (PG), and definition modeling (DM).

Terminology matters:
- **Hallucination detection:** classifying generated output as reliable or
  hallucinated relative to a source/reference or task definition.
- **Calibration:** whether confidence estimates correspond to observed
  correctness frequencies.
- **Error detection:** whether a confidence score ranks incorrect predictions
  above correct predictions.
- **ADVICE-inspired:** our experimental objective is motivated by answer-
  dependent confidence research; it is not a reproduction of the ADVICE method.

The summaries below are concise interpretations of the linked publications.
They are not substitutes for reading the full papers before submission.

## 1. SHROOM shared task and task-specific detectors

### 1.1 Mickus et al. (2024) — SemEval-2024 Task 6: SHROOM

**Venue:** SemEval 2024  
**Link:** https://aclanthology.org/2024.semeval-1.273/

**Problem and method:** Establishes a shared task for identifying fluent but
inaccurate generated text. The benchmark covers MT, PG, and DM and includes
model-agnostic and model-aware tracks. The task paper reports outputs annotated
by five annotators and describes results from many participating teams.

**Finding relevant to this project:** Hallucination detection remains difficult;
the shared-task paper reports that even top systems struggle on challenging
examples.

**Relevance:** Defines the benchmark and supports reporting results separately
by track and task.

**Limitation for our project:** Benchmark scores alone do not establish that a
new confidence objective improves calibration or error detection.

### 1.2 Liu et al. (2024) — HIT-MI&T Lab at SemEval-2024 Task 6

**Venue:** SemEval 2024  
**Link:** https://aclanthology.org/2024.semeval-1.253/

**Method:** Explores entailment recognition, similarity search, factuality
verification, and confidence estimation. The team reports results in both
SHROOM tracks.

**Finding:** The paper demonstrates that multiple forms of evidence can be
used for hallucination detection, including source–hypothesis relationships
and model-aware information.

**Relevance:** This is a close methodological reference for our DeBERTa-based
reference–hypothesis classifier.

**Limitation for our project:** We use a public DeBERTa checkpoint and our own
training procedure. We must not claim an exact reproduction of the HIT-MI&T
system or its reported results.

### 1.3 Arzt et al. (2024) — TU Wien at SemEval-2024 Task 6

**Venue:** SemEval 2024  
**Link:** https://aclanthology.org/2024.semeval-1.173/

**Method:** Combines model-agnostic methods, including word alignment and
fine-tuned pretrained models, with model-aware features and ensemble methods.
The paper also discusses automatic label-generation strategies.

**Relevance:** Shows that synthetic/automatically generated labels and
combining different evidence sources are established approaches in this
benchmark.

**Limitation:** Its ensemble and model-aware design differs from our
single-checkpoint baseline and auxiliary confidence-head experiments.

### 1.4 Obiso et al. (2024) — HaRMoNEE at SemEval-2024 Task 6

**Venue:** SemEval 2024  
**Link:** https://aclanthology.org/2024.semeval-1.191/

**Method:** Studies tuning-based hallucination recognition, including
fine-tuning a pretrained transformer and prompt-tuning large language models.

**Finding:** The paper reports strong submissions across the two SHROOM
subtasks using different tuning strategies.

**Relevance:** Provides a benchmark comparison for learned classifiers and
tuning-based alternatives.

**Limitation:** Reported results depend on each system's training, tuning,
preprocessing, and track setup; they should not be directly compared without
checking evaluation protocols.

### 1.5 Markchom et al. (2024) — NU-RU at SemEval-2024 Task 6

**Venue:** SemEval 2024  
**Link:** https://aclanthology.org/2024.semeval-1.39/

**Method:** Combines hypothesis–target similarity with a SelfCheckGPT-based
approach.

**Relevance:** Motivates comparison between a learned entailment-style
classifier and complementary similarity or consistency signals.

**Limitation:** Similarity does not necessarily imply factual correctness.
A hypothesis may be phrased differently from a correct reference, or share
many words with a reference while introducing a factual error.

### 1.6 Sanayei et al. (2024) — MARiA at SemEval-2024 Task 6

**Venue:** SemEval 2024  
**Link:** https://aclanthology.org/2024.semeval-1.225/

**Method:** Evaluates approaches involving LLM prompting, NLI, and cosine
similarity between source, target, and hypothesis representations.

**Finding:** Performance varies across SHROOM subtasks, highlighting the
importance of task-specific evaluation.

**Relevance:** Supports our task-wise analysis of DM, MT, and PG.

**Limitation:** The method combination differs from our classifier, and results
from separate submissions do not directly establish the value of our proposed
confidence objective.

### 1.7 Grigoriadou et al. (2024) — AILS-NTUA at SemEval-2024 Task 6

**Venue:** SemEval 2024  
**Link:** https://aclanthology.org/2024.semeval-1.222/

**Method:** Evaluates pretrained-model fine-tuning and natural-language
inference, with an ensemble of models among its strongest strategies.

**Relevance:** Provides further evidence that NLI signals and learned
hallucination classifiers can be complementary.

**Limitation:** An ensemble result is not directly comparable with a single
classifier without matching the data split and metric definitions.

### 1.8 Allen et al. (2024) — SHROOM-INDElab

**Venue:** SemEval 2024  
**Link:** https://aclanthology.org/2024.semeval-1.120/

**Method:** Studies zero-shot and few-shot LLM-based classification for
hallucination detection.

**Relevance:** Represents a prompt-based alternative to supervised
fine-tuning and provides context for considering the cost and dependence on
automatically generated labels.

**Limitation:** Prompt-based performance depends on prompts, model versions,
and inference settings, which differ from a saved DeBERTa classifier.

## 2. General hallucination detection and truthfulness

### 2.1 Manakul et al. (2023) — SelfCheckGPT

**Venue:** EMNLP 2023  
**Link:** https://aclanthology.org/2023.emnlp-main.557/

**Method:** Uses consistency across multiple sampled responses to identify
potentially non-factual content without requiring an external database.

**Finding:** The paper reports that sampled-response disagreement can help
identify factual errors.

**Relevance:** Offers a contrasting black-box approach to a single-pass
reference–hypothesis classifier.

**Limitation:** It requires multiple samples and targets a different setting
from our SHROOM classification pipeline. Its results do not prove that
consistency features will improve our model.

### 2.2 Li et al. (2023) — HaluEval

**Venue:** EMNLP 2023  
**Link:** https://aclanthology.org/2023.emnlp-main.397/

**Method:** Introduces a large-scale benchmark with generated and
human-annotated hallucinated samples for evaluating recognition of
hallucinations in LLM outputs.

**Relevance:** Establishes an important broader benchmark beyond SHROOM and
illustrates the need to consider how hallucination examples are constructed
and annotated.

**Limitation:** HaluEval's task design and data distribution differ from SHROOM;
scores should not be treated as directly interchangeable.

### 2.3 Lin et al. (2022) — TruthfulQA

**Venue:** ACL 2022  
**Link:** https://aclanthology.org/2022.acl-long.229/

**Method:** Introduces 817 questions across 38 categories designed to test
whether language models reproduce common false beliefs.

**Finding:** The paper shows that language models can produce untruthful
answers despite their fluency.

**Relevance:** Provides foundational context for the distinction between
plausible-sounding output and truthful output.

**Limitation:** TruthfulQA evaluates model truthfulness on question answering;
it is not a direct benchmark for the source-conditioned SHROOM classifier.

## 3. Confidence estimation and calibration

### 3.1 Guo et al. (2017) — On Calibration of Modern Neural Networks

**Venue:** ICML 2017  
**Link:** https://proceedings.mlr.press/v70/guo17a.html

**Method:** Studies calibration of neural classifiers and evaluates
post-processing techniques, including temperature scaling.

**Finding:** The paper shows that modern neural networks can be poorly
calibrated and that temperature scaling can be an effective post-processing
method.

**Relevance:** Directly motivates our temperature-scaling experiment and
reporting ECE, Brier score, and log loss in addition to F1.

**Limitation:** Temperature scaling adjusts probability sharpness but does not
change the predicted class when a single positive temperature is applied to
the same logits. Calibration improvement is not evidence of improved
classification or error ranking.

### 3.2 Seo, Lim, and Kim (2026) — ADVICE: Answer-Dependent Verbalized
Confidence Estimation

**Venue:** ACL 2026  
**Link:** https://aclanthology.org/2026.acl-long.1098/  
**DOI:** https://doi.org/10.18653/v1/2026.acl-long.1098

**Problem and method:** Studies overconfidence in LLM verbalized confidence
and proposes a fine-tuning framework designed to make confidence depend on
the generated answer.

**Finding:** The authors report improved calibration and generalization in
their studied settings.

**Relevance:** Motivates investigating answer-dependent confidence rather
than assuming that a confidence value is reliable merely because a model
produces one.

**Critical distinction:** ADVICE targets verbalized confidence in LLMs. Our
experiments add an auxiliary scalar confidence head and use contrastive
training on a classifier. These are not the same architecture, objective, or
experimental setting. We therefore describe our work as ADVICE-inspired,
not as an implementation or reproduction of ADVICE.

**Limitation:** ADVICE's reported results do not establish that an auxiliary
confidence head will improve SHROOM error detection.

### 3.3 Zhang et al. (2026) — LoVeC: Reinforcement Learning for Better
Verbalized Confidence in Long-Form Generation

**Venue:** ACL 2026  
**Link:** https://aclanthology.org/2026.acl-long.1539/

**Method:** Studies reinforcement learning for verbalized confidence in
long-form generation and proposes evaluation settings for confidence tagging.

**Relevance:** Shows that confidence estimation and calibration remain active
research topics beyond conventional classifier probability calibration.

**Limitation:** Its generation-oriented method differs substantially from our
binary classifier and should be treated as related work, not a direct
baseline.

## 4. Synthesis: what is established and what remains open?

The literature establishes that:
1. SHROOM supports several families of detection approaches, including NLI,
   similarity, fine-tuned transformers, prompt-based LLMs, and model-aware
   features.
2. Confidence calibration is distinct from classification performance.
   Temperature scaling is a recognized post-processing approach.
3. LLM-generated or automatically generated labels are used in this research
   area, but their quality and the data split remain important methodological
   considerations.
4. Answer-dependent verbalized confidence has been studied in ADVICE, but
   that does not establish that an auxiliary classifier confidence head will
   work on SHROOM.

## 5. Candidate research gaps and how to state them safely

These are **candidate gaps based on this focused review**, not proof that no
prior paper has addressed them. A novelty claim requires a broader database
search, full-text review, and citation chasing.

### Gap A — Does an auxiliary confidence objective improve error detection?

**Question:** Does adding a confidence objective improve the ability to
identify incorrect SHROOM predictions, while preserving classification F1?

**Why it matters:** Calibration and error detection are related but different
properties. A model may become better calibrated without becoming better at
ranking its own errors.

**Evidence from our current experiments:** The controlled head-only experiment
did not improve error-detection AUROC over the baseline softmax score for
DM, MT, or PG. The contrastive classifier also had lower validation F1 than
the baseline. These are negative findings, not evidence of improvement.

**Safe claim:** "We empirically evaluate whether an ADVICE-inspired auxiliary
confidence objective improves calibration and error detection for a
reference-conditioned SHROOM classifier."

### Gap B — How stable is performance across SHROOM tasks and tracks?

**Question:** Do aggregate metrics conceal task-specific weaknesses?

**Evidence from our current results:** PG has low precision on the official
test tracks. The model-agnostic and model-aware results also differ. These
observations motivate per-task analysis, but they do not prove the gap is
novel.

**Safe claim:** "We provide task-wise and track-wise evaluation of classification
and calibration metrics to characterize where errors persist."

### Gap C — How sensitive are conclusions to weak labels and data overlap?

**Question:** Do conclusions remain stable under checks for conflicting
training labels, exact overlap, and alternative calibration splits?

**Evidence from our current work:** The 6,000-row weakly labeled training set
contained duplicate groups and a small number of conflicting groups. The
model-agnostic official test track had 19 exact hypothesis matches with the
training sample; excluding those examples barely changed F1 or AUROC. The
model-aware track had no exact matches under the same normalization.

**Safe claim:** "We document weak-label quality and exact-string overlap and
perform an overlap sensitivity analysis." Do not claim the dataset is fully
independent: semantic overlap and overlap with other development sources have
not been ruled out.

## 6. How this maps to the current project

The current study has three experimental components:

1. **Baseline:** DeBERTa classifier on reference–hypothesis pairs.
2. **Confidence experiments:** contrastive confidence training and a
   controlled confidence head.
3. **Post-hoc calibration:** temperature scaling evaluated with held-out
   validation examples.

Current interpretation:
- The baseline is the strongest classifier in the existing validation
  experiments.
- The contrastive classifier did not improve F1 or calibration in the
  existing validation comparison.
- The controlled confidence head did not improve error-detection AUROC.
- Temperature scaling showed promising validation calibration changes, but
  the reported bootstrap intervals included zero.
- Official SHROOM test evaluation is available for the saved baseline. The
  confidence variants have not been established as superior on the official
  test tracks.

Do not present any confidence method as superior without an appropriately
controlled evaluation. Avoid choosing thresholds or model variants based on
official test outcomes.

## 7. References

1. Mickus et al. (2024). SHROOM shared task.
   https://aclanthology.org/2024.semeval-1.273/
2. Liu et al. (2024). HIT-MI&T DeBERTa-based detector.
   https://aclanthology.org/2024.semeval-1.253/
3. Arzt et al. (2024). TU Wien SHROOM system.
   https://aclanthology.org/2024.semeval-1.173/
4. Obiso et al. (2024). HaRMoNEE tuning-based approaches.
   https://aclanthology.org/2024.semeval-1.191/
5. Markchom et al. (2024). NU-RU similarity and SelfCheckGPT.
   https://aclanthology.org/2024.semeval-1.39/
6. Sanayei et al. (2024). MARiA.
   https://aclanthology.org/2024.semeval-1.225/
7. Grigoriadou et al. (2024). AILS-NTUA.
   https://aclanthology.org/2024.semeval-1.222/
8. Allen et al. (2024). SHROOM-INDElab.
   https://aclanthology.org/2024.semeval-1.120/
9. Manakul et al. (2023). SelfCheckGPT.
   https://aclanthology.org/2023.emnlp-main.557/
10. Li et al. (2023). HaluEval.
    https://aclanthology.org/2023.emnlp-main.397/
11. Lin et al. (2022). TruthfulQA.
    https://aclanthology.org/2022.acl-long.229/
12. Guo et al. (2017). On Calibration of Modern Neural Networks.
    https://proceedings.mlr.press/v70/guo17a.html
13. Seo, Lim, and Kim (2026). ADVICE.
    https://aclanthology.org/2026.acl-long.1098/
14. Zhang et al. (2026). LoVeC.
    https://aclanthology.org/2026.acl-long.1539/

## 8. Verification still required before final submission

- Read full texts for the closest methods, particularly HIT-MI&T, ADVICE,
  SHROOM, and calibration work.
- Search additional databases and citation trails before making a novelty claim.
- Verify all bibliographic details and follow the institution's citation style.
- Compare methods only where dataset, track, and metric definitions match.
- Preserve the negative confidence-head results.
- Report validation reuse and the exact-overlap audit as limitations.
- Do not describe the confidence-aware method as an ADVICE reproduction.
