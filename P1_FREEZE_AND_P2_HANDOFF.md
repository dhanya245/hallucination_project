# P1 Freeze and Revised P1/P2/P3 Work Allocation

Date: 2026-10-17
Status: P1 frozen at research checkpoint; P2 owns continuation.

## 1. P1 — Frozen deliverables

Available artifacts to preserve:
- baseline/ — saved baseline checkpoint
- confidence/ — experimental confidence-model checkpoints
- data/ — datasets, labels, and contrastive pairs
- results/ — validation, official-test, calibration, overlap, and failure-analysis results
- results/literature_review.md — initial literature review
- results/priority_paper_screening_notes.md — initial screening notes
- results/full_text/ — extracted full texts and screening extracts
- inference.py, README.md, requirements.txt — inference and project documentation, where present

### P1 findings to preserve
- The baseline remains the primary classifier.
- The contrastive confidence-model experiment did not improve classification F1.
- The controlled confidence head did not improve error-detection AUROC over the baseline.
- Temperature scaling showed promising preliminary calibration results, but bootstrap confidence intervals included zero.
- Official SHROOM model-agnostic and model-aware test evaluations were completed.
- Exact-overlap audits were performed; semantic overlap was not ruled out.
- Failure-analysis annotations are exploratory and must not be presented as validated population-level findings.

P1 is not required to run further training before this handoff.

## 2. P2 — Next owner and remaining work

Priority order:

1. **Reproducibility:** inspect the saved artifacts and source files; smoke-test baseline inference from a clean runtime. Record missing scripts, dependency issues, and any discrepancy between saved results and fresh inference.
2. **Literature:** continue full-text screening, starting with:
   - A Head to Predict and a Head to Question (EMNLP 2025)
   - Beyond Output Confidence (ACL Findings 2026)
   Compare their actual methods, supervision, datasets, metrics, limitations, and overlap with this project.
3. **Research framing:** update the related-work review and research-gap statement. Do not claim novelty until the closest methods have been compared in full.
4. **Results consolidation:** verify metric definitions, evaluation protocols, model versions, and limitations. Keep validation results separate from official-test results.
5. **Backend/API:** establish a stable prediction interface for P3. Document input schema, output schema, errors, and confidence-score meaning.
6. **Final documentation:** consolidate methodology, experiments, results, limitations, and reproduction instructions.
7. **Further experiments:** propose only if a specific unresolved research question justifies the time and compute cost. Do not retrain by default.

## 3. P3 — Frontend

- Build the UI against the API contract agreed with P2.
- Display only outputs the backend actually returns.
- Handle invalid input, loading, and API errors.
- Test representative examples and complete end-to-end integration after the API is stable.

## 4. Handoff gates

P2 should confirm:
- [ ] Baseline inference works in a clean environment.
- [ ] Checkpoint and tokenizer paths are documented.
- [ ] Existing result files are preserved and interpreted consistently.
- [ ] Known limitations and incomplete reproducibility items are recorded.
- [ ] The two priority papers have been screened beyond their abstracts.
- [ ] Backend API contract is agreed with P3.

P3 should confirm:
- [ ] UI works against the agreed API.
- [ ] Prediction and confidence fields are represented accurately.
- [ ] Error states and end-to-end tests pass.

## 5. Important limitations

- Validation data was reused during development; it is not an untouched test set.
- Exact text overlap checks do not establish semantic independence.
- Literature screening is incomplete; the candidate-paper register must be verified before being described as a screened corpus.
- P1's saved artifacts and consistency checks do not, by themselves, prove full clean-room reproducibility.
- The confidence objective is ADVICE-inspired; do not describe it as an exact reproduction of ADVICE.
- Negative experimental findings must remain in the final report.

## Ownership rule

P1's current checkpoint is frozen. P2 takes ownership of verification, remaining research, final results consolidation, and backend integration. P3 owns frontend development and end-to-end UI testing. Preserve the existing files; record corrections and new experiments as versioned updates.
