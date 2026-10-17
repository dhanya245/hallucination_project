# P1 Research Results

## 1. Baseline DeBERTa

| Metric | Result |
|---|---:|
| Accuracy | 77.96% |
| Precision | 69.71% |
| Recall | 87.61% |
| F1 score | 77.64% |
| ECE | 0.1008 |
| Brier score | 0.1704 |
| AUROC | 0.8830 |

## 2. Baseline vs. Contrastive Classifier

| Metric | Baseline | Contrastive |
|---|---:|---:|
| Accuracy | 0.7796 | 0.7214 |
| F1 | 0.7764 | 0.7332 |
| ECE | 0.1008 | 0.2340 |
| Brier score | 0.1704 | 0.2474 |
| AUROC | 0.8830 | 0.8642 |

The contrastive classifier did not improve the measured classification or
calibration metrics in this experiment.

## 3. Baseline Performance by Task

| Task | Examples | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| DM | 187 | 0.7968 | 0.7812 | 0.8152 | 0.7979 |
| MT | 187 | 0.8396 | 0.7525 | 0.9383 | 0.8352 |
| PG | 125 | 0.6640 | 0.5195 | 0.8889 | 0.6557 |

PG had the weakest F1 and the highest false-positive rate.

## 4. Temperature Scaling

Five overlapping stratified splits produced the following mean metrics:

| Metric | Original | Temperature-scaled |
|---|---:|---:|
| NLL | 0.5204 | 0.4663 |
| Brier score | 0.1618 | 0.1529 |
| ECE | 0.0989 | 0.0565 |

Held-out paired-bootstrap confidence intervals included zero for all three
metric differences. These results are promising but inconclusive.

## 5. Controlled Confidence Head

The controlled head preserved baseline classifier predictions exactly.
However, its error-detection AUROC was lower than baseline softmax confidence
for DM, MT, and PG. Therefore, this experiment does not establish an
improvement in error detection.

## 6. Methodology

- Training data: 6,000 SHROOM examples with Gemini-generated labels.
- Baseline: DeBERTa sequence classifier.
- Validation: 499 labeled SHROOM development examples.
- Contrastive experiment: reliable/hallucinated pairs with a confidence
  objective inspired by ADVICE.
- Calibration experiment: post-hoc temperature scaling.
- Metrics: accuracy, precision, recall, F1, ECE, Brier score, and AUROC.

The confidence objective is ADVICE-inspired; it is not an exact reproduction
of the ADVICE method.

## 7. Data Quality

- 5,909 unique normalized examples among the 6,000 training rows.
- 89 duplicate groups.
- 3 groups with conflicting labels.
- 2 normalized example matches between training and validation.

## 8. Limitations

- Gemini-generated training labels may contain annotation errors.
- The validation set was reused during experiment development.
- The five random splits overlap and are not independent datasets.
- An independent labeled test set has not yet been established.
- Confidence-head and calibration results require further independent
  evaluation before generalization claims can be made.

## 9. Overall Conclusion

The baseline remains the strongest evaluated classifier. Temperature scaling
shows preliminary calibration improvements, while the contrastive classifier
and controlled confidence head did not demonstrate overall improvement.
Further work should prioritize independent evaluation, robustness analysis,
and transparent reporting of negative findings.

## Official SHROOM Test Evaluation

The saved baseline DeBERTa classifier was evaluated separately on the two
official labeled SHROOM test tracks. No retraining or test-set tuning was
performed for this evaluation.

| Metric | Model-agnostic (n=1500) | Model-aware (n=1500) |
|---|---:|---:|
| Accuracy | 0.7873 | 0.7680 |
| Precision | 0.6820 | 0.6490 |
| Recall | 0.8953 | 0.8022 |
| F1 | 0.7742 | 0.7175 |
| AUROC | 0.8997 | 0.8580 |
| ECE | 0.0867 | 0.0840 |
| Binary Brier score | 0.1555 | 0.1751 |
| Log loss | 0.5073 | 0.5594 |

The model-agnostic track produced higher F1 and AUROC. Both tracks showed
relatively high recall, while precision was lower, indicating false-positive
hallucination predictions remain an important limitation.

### Training–Test Exact-Overlap Audit

Exact normalized string matching was performed between the 6,000-example
weakly labeled training sample and each official test track. The normalization
lowercased text, trimmed leading/trailing whitespace, and collapsed repeated
whitespace.

- Model-agnostic: 18 exact reference–hypothesis pair matches and 19 exact
  hypothesis matches among 1,500 examples.
- Model-aware: zero exact pair matches and zero exact hypothesis matches
  among 1,500 examples.

For the model-agnostic track, excluding the 19 exact hypothesis matches
produced F1 = 0.7758 and AUROC = 0.8997, compared with F1 = 0.7742 and
AUROC = 0.8997 on all 1,500 examples. The results were materially unchanged
under this sensitivity analysis.

This audit only detects exact normalized matches. It does not rule out
semantic paraphrase overlap or overlap with other development sources.
The model-aware track had no exact matches under the same check; it should
not be described as proven free of every possible form of overlap.

### Metric Convention Correction

The official-test Brier scores are reported as binary Brier scores calculated
from P(Hallucination): 0.1555 for model-agnostic and 0.1751 for model-aware.
Earlier values were twice as large because squared errors were summed across
both class probabilities. The corrected values are saved in the official-test
metric JSON files.

### Interpretation and Limitations

These results provide an official-test evaluation of the saved baseline.
They do not establish that the confidence-aware experiments outperform the
baseline. The validation set was reused during development, and exact-string
audits cannot establish complete independence. Results should be interpreted
alongside the separate confidence-head and temperature-scaling experiments.

## Literature Review Synthesis and Candidate Research Gaps

### Related work

The literature review covers the SHROOM shared task and systems using
entailment recognition, semantic similarity, pretrained-model fine-tuning,
LLM prompting, and consistency-based detection. It also covers neural
probability calibration, temperature scaling, and answer-dependent
verbalized confidence. The full working review is in
`results/literature_review.md`.

The HIT-MI&T SHROOM system is a close methodological reference, but this
project should not be described as a reproduction of that system. Similarly,
ADVICE motivates answer-dependent confidence estimation in LLM verbalized
confidence; our auxiliary confidence head and contrastive classifier are
different methods and are described only as ADVICE-inspired.

### Candidate research gaps

These gaps are provisional and require further full-text review and literature
search before any novelty claim.

1. **Confidence-aware error detection:** Test whether an auxiliary confidence
   objective improves the ranking of incorrect predictions while preserving
   classification performance. In the current experiments, the controlled
   confidence head did not improve error-detection AUROC, and the contrastive
   classifier did not outperform the baseline F1. These negative findings
   must remain part of the results.

2. **Task- and track-specific reliability:** Report DM, MT, and PG separately
   because aggregate metrics can conceal task-specific weaknesses. The
   official-test baseline has relatively low PG precision in both tracks,
   making false-positive analysis important.

3. **Weak-label and overlap sensitivity:** Document label conflicts,
   duplicates, exact train–test matches, and sensitivity analyses. The
   model-agnostic overlap sensitivity results changed only slightly after
   excluding 19 exact hypothesis matches. Exact-string matching does not rule
   out semantic overlap.

### Evidence-based interpretation

The saved baseline achieves F1 = 0.7742 and AUROC = 0.8997 on the official
model-agnostic track, and F1 = 0.7175 and AUROC = 0.8580 on the official
model-aware track. These are baseline results; they do not demonstrate that
the confidence-aware experiments improve official-test performance.

Temperature scaling showed promising preliminary validation results, but
the reported bootstrap confidence intervals included zero. Therefore, its
improvement should be described as inconclusive rather than established.

### Literature-review limitations

The working review is a starting point, not a systematic review. Individual
paper records, claims, and full-text methods must be checked before final
submission. The proposed gaps are research questions supported by the current
project's motivation and results; they are not claims that no prior work
exists.

## Exploratory Official-Test Failure Analysis

A stratified exploratory sample of 36 baseline errors was reviewed: up to
three false positives and three false negatives for each task (DM, MT, PG)
in each official SHROOM track. The sample was selected with random seed 42.
Examples were provisionally categorized by comparing the reference and
hypothesis, with annotator disagreement noted where available.

The observed examples included:
- Semantic and paraphrase mismatches, including cases where lexical overlap
  obscured a change in meaning.
- Omitted details or overly general hypotheses that lost specificity.
- Unsupported additions and changes to logical, grammatical, or structural
  relations.
- Borderline examples where the hypothesis appeared to be a plausible
  paraphrase or the annotator labels were divided.

These categories are exploratory and overlap conceptually. The manual labels
were assigned by one reviewer and have not been independently validated.
Because the sample contains only 36 errors, the category frequencies must not
be interpreted as estimates of the prevalence of error types across the full
test sets. The findings are useful for generating hypotheses and guiding
future error analysis, not for establishing causal explanations of model
behavior.

The detailed examples and annotations are stored in
`results/official_test/failure_analysis_sample_completed.csv`; grouped counts
are stored in `results/official_test/failure_analysis_grouped.json`.
