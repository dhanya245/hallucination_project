import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class HallucinationInference:
    """Inference for the fine-tuned SHROOM hallucination classifier."""

    def __init__(self, model_dir, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        self.model.to(self.device)
        self.model.eval()
        self.id2label = {0: "Reliable", 1: "Hallucinated"}

    @torch.inference_mode()
    def predict(self, question, context, answer):
        for name, value in (
            ("question", question),
            ("context", context),
            ("answer", answer),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string.")

        # Training used reference + hypothesis, not the question.
        inputs = self.tokenizer(
            context,
            answer,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        logits = self.model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)[0]
        pred_id = int(torch.argmax(probs).item())

        return {
            "prediction": self.id2label[pred_id],
            "prediction_id": pred_id,
            "confidence": float(probs[pred_id].item()),
            "class_probabilities": {
                self.id2label[i]: float(probs[i].item())
                for i in range(len(probs))
            },
            "note": (
                "Confidence is the model's softmax score, not a calibrated "
                "probability. The question is accepted but not used by this model."
            ),
        }
