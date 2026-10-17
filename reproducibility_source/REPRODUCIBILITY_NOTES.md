# Reproducibility and source-recovery note

## What is verified from existing artifacts

### Baseline
The saved `baseline/training_args.bin` records seed 42, one epoch, learning
rate 2e-5, per-device train batch size 1, gradient accumulation 16, warmup
steps 71, weight decay 0.01, gradient checkpointing enabled, linear learning
rate schedule, and `adamw_torch_fused`. The saved model config identifies a
DeBERTa-v2 sequence classifier with 24 layers, hidden size 1024, and two labels.
Label mapping: 0 = Reliable, 1 = Hallucinated.

### Full confidence checkpoint
The saved checkpoint has 396 tensors with names rooted at
`confidence_model.` and `confidence_head.`. It includes the wrapped DeBERTa
sequence classifier and a scalar linear confidence head. The saved history
records two epochs, 2,084 pairs, learning rate 1e-5, batch size 1, gradient
accumulation 16, and average losses 0.304 and 0.1376.

### Controlled head-only checkpoint
The checkpoint contains a single linear layer's `weight` (1 x 1024) and
`bias` (1). The saved history records losses 0.0727212581 and 0.0635338960.
Evaluation metadata says the baseline classifier predictions were unchanged.
The exact original optimizer settings and target construction were not found.

### Contrastive pair data
The 2,084 rows use `task`, `reliable_reference`, `reliable_hypothesis`,
`hallucinated_reference`, and `hallucinated_hypothesis`.

## What is not verified
The original `train.py`, `model.py`, `loss.py`, and `training_config.json`
were missing during the audit. Training histories do not preserve the exact
loss equation, margin, term weights, data ordering, optimizer state, or all
random states. The supplied `loss.py` is a transparent reference
reconstruction, not the historical loss implementation. The supplied
`train.py` is a safe audit scaffold, not a full training reproduction.

## Interpretation
Do not claim that the original experiments can be reproduced bit-for-bit
from the present files. Preserve historical checkpoints and results. If a new
training run is performed, store it under a new output directory and label it
as a reconstructed experiment. Do not overwrite `baseline/` or `confidence/`.

## Metric caveat
`results/verified_model_comparison.json` and `results/model_comparison.json`
contain the same older confidence-head metrics (AUROC 0.780469...). The
controlled head-only experiment has separate metrics in
`confidence/controlled_head_only/evaluation.json` (AUROC 0.839662...).
These are distinct experiment artifacts and must not be silently merged.
