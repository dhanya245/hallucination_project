
# Priority Paper Screening Notes

Status: First-pass screening based on publisher abstracts and metadata.
This is NOT a full-text review.

## 1. A Head to Predict and a Head to Question (2025)
- Venue: EMNLP 2025
- URL: https://aclanthology.org/2025.emnlp-main.1809/
- Method from abstract: supervised pretrained uncertainty quantification heads using transformer attention-map and logit features.
- Reported scope: claim-level hallucination detection, in-domain/out-of-domain prompts, and cross-lingual generalization.
- Relevance: closest methodological comparison to an auxiliary confidence head.
- Full text still needed: architecture details, training objective, datasets, exact baselines, metrics, and whether its setup transfers to a DeBERTa entailment detector.

## 2. Beyond Output Confidence: Epistemic-Aware Hallucination Detection with Answer-Level Signals (2026)
- Venue: ACL Findings 2026
- URL: https://aclanthology.org/2026.findings-acl.674/
- Method from abstract: Answer-level Intrinsic Cognition (AIC), combined with conventional output uncertainty.
- Reported scope: three public QA benchmarks and multiple model scales; abstract reports gains over uncertainty-only baselines.
- Relevance: directly challenges the idea that output confidence alone captures epistemic uncertainty.
- Full text still needed: exact AIC computation, stochastic-pass cost, benchmark details, and calibration/error-ranking metrics.

## 3. Simple Factuality Probes Detect Hallucinations in Long-Form Natural Language Generation (2025)
- Venue: EMNLP Findings 2025
- URL: https://aclanthology.org/2025.findings-emnlp.880/
- Method from abstract: lightweight probes over LLM hidden states.
- Reported scope: long-form generation, models up to 405B parameters, OOD evaluation; abstract reports competitive results with lower computation than multi-sample approaches.
- Relevance: supports studying internal representations as factuality signals.
- Full text still needed: exact features, probe architecture, data splits, leakage safeguards, and metric tables.

## 4. Evaluating Evaluation Metrics – The Mirage of Hallucination Detection (2025)
- Venue: EMNLP Findings 2025
- URL: https://aclanthology.org/2025.findings-emnlp.1035/
- Method from abstract: evaluation of six groups of metrics across four datasets, 37 language models from five families, and five decoding methods.
- Reported finding: metrics can disagree with human judgments and generalize inconsistently.
- Relevance: supports careful evaluation and cautious novelty claims.
- Full text still needed: metric definitions, datasets, statistical tests, and recommendations applicable to SHROOM.

## 5. FactSelfCheck: Fact-Level Black-Box Hallucination Detection for LLMs (2026)
- Venue: EACL Findings 2026
- URL: https://aclanthology.org/2026.findings-eacl.296/
- Method from abstract: sampling-based consistency analysis over knowledge-graph triples.
- Reported scope: fine-grained fact-level detection and a dataset called FavaMultiSamples.
- Relevance: adjacent approach; useful for positioning white-box classifier methods against black-box sampling.
- Full text still needed: experimental settings, baselines, computational cost, and exact evaluation metrics.

## Preliminary synthesis
1. Auxiliary uncertainty heads and hidden-state probes are established recent directions.
2. Answer-level epistemic signals are a relevant alternative to output confidence alone.
3. Metric validity and generalization should be treated as research-design concerns.
4. Black-box sampling methods differ substantially from the project's fine-tuned DeBERTa classifier.

## Project-specific interpretation
The current controlled confidence-head experiment did not improve error detection over the baseline, and the contrastive classifier reduced F1. These are preliminary negative findings, not evidence that all confidence-aware approaches fail.

Potential research question:
Does an answer-dependent confidence objective improve error ranking and calibration while preserving classification performance on SHROOM, compared with a DeBERTa entailment baseline?

Do not claim novelty until full-text comparison against the closest 2024–2026 methods is complete.
