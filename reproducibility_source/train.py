"""
Safe entry-point scaffold for the hallucination project.

This script intentionally does not train by default. The historical training
source is missing, and the saved loss definition cannot be established exactly.
Use --inspect to verify local data/checkpoints. Use --allow-reconstructed-training
only if you explicitly intend to run a new experiment with the reconstructed
objective in loss.py. Such a run is NOT an exact reproduction of reported results.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--inspect", action="store_true")
    parser.add_argument("--allow-reconstructed-training", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    required = [
        "baseline/config.json",
        "baseline/model.safetensors",
        "data/labeled_6k.json",
        "data/contrastive_pairs.json",
        "confidence/training_history.json",
    ]
    report = {
        "root": str(root),
        "files": {
            rel: {"exists": (root / rel).exists(),
                  "size_bytes": (root / rel).stat().st_size if (root / rel).exists() else None}
            for rel in required
        },
        "training_started": False,
        "note": "This scaffold does not implement historical training."
    }
    print(json.dumps(report, indent=2))

    if args.inspect:
        return
    if args.allow_reconstructed_training:
        raise SystemExit(
            "Safety stop: this scaffold does not implement a complete training loop. "
            "Review model.py and loss.py, then create a separate, explicitly named "
            "new-experiment script rather than overwriting historical checkpoints."
        )
    raise SystemExit(
        "No training performed. Pass --inspect to audit files. "
        "Historical source is missing; do not assume a reconstructed run reproduces it."
    )


if __name__ == "__main__":
    main()
