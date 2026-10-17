
import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    roc_auc_score,
    brier_score_loss
)

def expected_calibration_error(y_true, probs, n_bins=10):
    confidences = np.maximum(probs, 1 - probs)
    predictions = (probs >= 0.5).astype(int)
    correctness = (predictions == y_true).astype(float)
    edges = np.linspace(0, 1, n_bins + 1)
    ece = 0.0

    for i in range(n_bins):
        mask = (confidences > edges[i]) & (confidences <= edges[i + 1])
        if mask.any():
            ece += mask.mean() * abs(
                correctness[mask].mean() - confidences[mask].mean()
            )
    return float(ece)

def calculate_metrics(y_true, predictions, probs):
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, predictions, average="binary", zero_division=0
    )
    return {
        "accuracy": float(accuracy_score(y_true, predictions)),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "ece": expected_calibration_error(y_true, probs),
        "brier_score": float(brier_score_loss(y_true, probs)),
        "auroc": float(roc_auc_score(y_true, probs))
    }

class DebertaConfidenceModel(nn.Module):
    def __init__(self, baseline_model):
        super().__init__()
        self.deberta = baseline_model.deberta
        self.pooler = baseline_model.pooler
        self.dropout = baseline_model.dropout
        self.classifier = baseline_model.classifier
        self.confidence_head = nn.Linear(1024, 1)

    def forward(self, input_ids=None, attention_mask=None,
                token_type_ids=None, **kwargs):
        outputs = self.deberta(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids
        )
        pooled = self.pooler(outputs.last_hidden_state)
        pooled = self.dropout(pooled)
        logits = self.classifier(pooled)
        confidence = torch.sigmoid(
            self.confidence_head(pooled)
        ).squeeze(-1)
        return {"logits": logits, "confidence": confidence}

class ContrastiveConfidenceModel(nn.Module):
    def __init__(self, confidence_model):
        super().__init__()
        self.confidence_model = confidence_model
