
import os
import json
import zipfile
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    DataCollatorWithPadding
)
from torch.utils.data import DataLoader

PROJECT_DIR = "/content/drive/MyDrive/hallucination_project"
BASELINE_DIR = os.path.join(PROJECT_DIR, "baseline")
DATA_DIR = os.path.join(PROJECT_DIR, "data")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Restore tokenizer and saved baseline; do not retrain
tokenizer = AutoTokenizer.from_pretrained(BASELINE_DIR)
baseline_model = AutoModelForSequenceClassification.from_pretrained(
    BASELINE_DIR, num_labels=2
).to(device)
baseline_model.eval()

# Restore SHROOM validation examples
dev_zip = os.path.join(DATA_DIR, "SHROOM_dev-v2.zip")
with zipfile.ZipFile(dev_zip, "r") as z:
    with z.open("SHROOM_dev-v2/val.model-agnostic.json") as f:
        val_data = json.load(f)

val_rows = []
for x in val_data:
    reference = x["tgt"] if x["task"] in ["DM", "MT"] else x["src"]
    label = 1 if x["label"] == "Hallucination" else 0
    val_rows.append({
        "task": x["task"],
        "reference": reference,
        "hypothesis": x["hyp"],
        "label": label
    })

val_dataset = Dataset.from_list(val_rows)

def tokenize_function(batch):
    return tokenizer(
        batch["reference"],
        batch["hypothesis"],
        truncation=True,
        max_length=512
    )

tokenized_val = val_dataset.map(tokenize_function, batched=True)
tokenized_val_clean = tokenized_val.remove_columns(
    ["task", "reference", "hypothesis"]
)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
val_loader = DataLoader(
    tokenized_val_clean,
    batch_size=4,
    shuffle=False,
    collate_fn=data_collator
)

print("Recovery complete.")
print("Device:", device)
print("Baseline loaded; no training performed.")
print("Validation examples:", len(val_dataset))
