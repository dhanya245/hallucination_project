"""
Explicit, documented ADVICE-inspired contrastive objective reconstruction.

IMPORTANT:
The original loss.py was not present. The exact historical loss formula,
margin, and weighting cannot be verified from the saved artifacts. This
module therefore exposes a transparent reference implementation, not a
claim of exact reproduction.
"""
from __future__ import annotations

import torch
import torch.nn.functional as F


def contrastive_classification_loss(
    reliable_logits: torch.Tensor,
    hallucinated_logits: torch.Tensor,
    margin: float = 0.2,
    contrastive_weight: float = 1.0,
) -> torch.Tensor:
    """
    Reference objective for one reliable and one hallucinated hypothesis.

    Assumes class 0 = Reliable and class 1 = Hallucinated.
    Pulls reliable examples toward class 0 and hallucinated examples toward
    class 1 using cross entropy. The margin term encourages the hallucinated
    logit margin to exceed the reliable margin.

    This is a reconstructed example. Do not use it to claim exact recovery of
    the original training run.
    """
    batch_size = reliable_logits.shape[0]
    device = reliable_logits.device
    reliable_labels = torch.zeros(batch_size, dtype=torch.long, device=device)
    hallucinated_labels = torch.ones(batch_size, dtype=torch.long, device=device)

    ce = (
        F.cross_entropy(reliable_logits, reliable_labels)
        + F.cross_entropy(hallucinated_logits, hallucinated_labels)
    ) / 2.0

    reliable_margin = reliable_logits[:, 0] - reliable_logits[:, 1]
    hallucinated_margin = hallucinated_logits[:, 1] - hallucinated_logits[:, 0]
    ranking = F.relu(margin - hallucinated_margin + reliable_margin).mean()

    return ce + contrastive_weight * ranking


def binary_confidence_loss(
    confidence_logits: torch.Tensor,
    targets: torch.Tensor,
) -> torch.Tensor:
    """Binary confidence-head loss for a caller-supplied target definition."""
    return F.binary_cross_entropy_with_logits(
        confidence_logits.view(-1), targets.float().view(-1)
    )
