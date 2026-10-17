# SHROOM Hallucination Detection

## Project Overview
This project evaluates a DeBERTa-based hallucination detector using SHROOM-style reference and hypothesis pairs.

## Task and Labels
- Class 0: Reliable (Not Hallucination)
- Class 1: Hallucinated
- Input pair: context/reference and answer/hypothesis.
- The question argument is accepted by the inference interface but is not used by the current model.

## Model
- Base checkpoint: MoritzLaurer/deberta-v3-large-zeroshot-v1.1-all-33
- Fine-tuned for this project's hallucination labels.
- Maximum input length: 512 tokens.
- Model files are stored in `baseline/`.

## Data
The project includes a 6,000-example training sample with Gemini-generated weak labels and a SHROOM validation set. Weak labels may contain noise.
The recorded validation label counts are 281 Not Hallucination and 218 Hallucination.

## Experiments
1. Baseline DeBERTa classifier.
2. ADVICE-inspired contrastive confidence experiment.
3. Controlled confidence-head experiment.
4. Temperature scaling for calibration.

The recorded confidence-head experiments did not improve error detection over baseline softmax scores. Temperature scaling showed promising but inconclusive calibration improvements. Refer to `results/P1_research_results.md` and the JSON files under `results/` for exact metrics.

## Inference
```python
from inference import HallucinationInference

detector = HallucinationInference("baseline")
result = detector.predict(
    question="What does a weasel look like?",
    context="Resembling a weasel in appearance.",
    answer="Resembling or characteristic of a weasel."
)
print(result)
```

The confidence output is a softmax score and should not automatically be interpreted as a calibrated probability.

## Main Files
- `baseline/`: baseline model and tokenizer
- `confidence/`: confidence experiment artifacts
- `data/`: datasets and labeling artifacts
- `results/`: evaluation metrics, figures, and reports
- `inference.py`: inference interface
- `recover_project.py` and `project_utils.py`: recovery utilities
- `P1_progress_checkpoint.json`: progress checkpoint

## Limitations
- Gemini-generated labels may contain errors.
- The validation set is limited and is not an independent external test set.
- Some calibration splits overlap.
- Confidence-head experiments did not show improved error detection.
- Temperature-scaling improvements are not conclusive.
- Do not claim an exact reproduction of ADVICE or statistically significant improvements unsupported by the experiments.
