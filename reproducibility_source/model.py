
from pathlib import Path
import torch
from torch import nn
from transformers import AutoModelForSequenceClassification


class ConfidenceModel(nn.Module):
    def __init__(self, baseline_model):
        super().__init__()
        self.confidence_model = baseline_model
        hidden_size = int(getattr(baseline_model.config, "hidden_size", 1024))
        self.confidence_model.confidence_head = nn.Linear(hidden_size, 1)

    def forward(self, input_ids=None, attention_mask=None,
                token_type_ids=None, **kwargs):
        base = self.confidence_model

        outputs = base(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            **kwargs,
        )

        hidden = base.deberta(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            **kwargs,
        )
        pooled = base.pooler(hidden.last_hidden_state)
        if hasattr(base, "dropout"):
            pooled = base.dropout(pooled)

        confidence_logit = base.confidence_head(pooled).squeeze(-1)
        return {
            "logits": outputs.logits,
            "confidence_logit": confidence_logit,
            "confidence": torch.sigmoid(confidence_logit),
        }


def load_confidence_model(
    baseline_dir,
    confidence_checkpoint,
    map_location="cpu",
    strict=True,
):
    baseline = AutoModelForSequenceClassification.from_pretrained(
        str(baseline_dir), local_files_only=True
    )
    model = ConfidenceModel(baseline)
    state = torch.load(
        str(confidence_checkpoint),
        map_location=map_location,
        weights_only=True,
    )
    result = model.load_state_dict(state, strict=strict)
    if not strict:
        print("Missing keys:", result.missing_keys)
        print("Unexpected keys:", result.unexpected_keys)
    return model


def load_controlled_confidence_head(
    checkpoint, hidden_size=1024, map_location="cpu"
):
    head = nn.Linear(hidden_size, 1)
    state = torch.load(
        str(checkpoint), map_location=map_location, weights_only=True
    )
    head.load_state_dict(state, strict=True)
    return head
