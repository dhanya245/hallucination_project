# P2 Handoff — Hallucination Detection

## 1. Current status
The P1 baseline, evaluation artifacts, inference module, documentation, and backup are saved. The final consistency audit passed.
Do not retrain the baseline without a specific reason.

## 2. Baseline model
- Model directory: `baseline/`
- Base checkpoint: `MoritzLaurer/deberta-v3-large-zeroshot-v1.1-all-33`
- Labels: class 0 = Reliable; class 1 = Hallucinated
- Input pair: context/reference and answer/hypothesis
- Maximum sequence length: 512 tokens
- Model weights: `baseline/model.safetensors`

## 3. Inference interface
```python
from inference import HallucinationInference
detector = HallucinationInference("baseline")
result = detector.predict(
    question="What is the capital of France?",
    context="Paris is the capital of France.",
    answer="Paris is the capital of France."
)
print(result)
```
The `question` parameter is accepted but not used by the current model. The model receives context and answer as a pair.
Confidence is a softmax score and should not automatically be interpreted as a calibrated probability.

## 4. Baseline validation metrics
- Accuracy: 0.7796
- Precision: 0.6971
- Recall: 0.8761
- F1: 0.7764
- ECE: 0.1008
- Brier score: 0.1704
- AUROC: 0.8830

Validation metrics are from the recorded SHROOM validation evaluation; they are not a guarantee of performance on new data.

## 5. Experiment findings
- The contrastive confidence classifier did not improve baseline F1 or calibration.
- The controlled confidence head preserved baseline predictions but did not improve error detection.
- Temperature scaling improved recorded average NLL, Brier score, and ECE across five overlapping splits.
- The bootstrap intervals included zero; temperature-scaling results remain preliminary and inconclusive.
- Describe the method as ADVICE-inspired, not an exact reproduction.

## 6. Important artifacts
- `results/P1_research_results.md` — detailed report
- `results/final_comparison_draft.json` — model comparison metrics
- `results/final_consistency_audit.json` — consistency checks
- `results/inference_smoke_test.json` — inference smoke test record
- `confidence/` — full confidence experiment checkpoints
- `confidence/controlled_head_only/` — controlled confidence-head artifacts
- `P1_progress_checkpoint.json` — progress record

## 7. Training-code status
The recent handoff audit did not find root-level `model.py`, `loss.py`, or `train.py`. The original training scripts and complete end-to-end reproducibility have therefore not yet been verified. Do not claim that the project can be fully retrained from the saved files alone.

## 8. P2 next actions
1. Review the inference interface and P1 research report.
2. Agree on the required integration interface before changing code.
3. Smoke-test inference in the target environment.
4. Preserve the baseline and current metrics as the comparison reference.
5. Document any new changes and evaluate them against the same protocol.

## 9. Backup
A verified ZIP backup was created in `backups/` and downloaded locally. Create a fresh backup after adding this handoff file.
