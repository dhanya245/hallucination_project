# Hallucination Detection — P1 Handoff

## Current status
P1 is frozen at a research checkpoint. P2 owns continuation.

## Start here
1. Read `P1_FREEZE_AND_P2_HANDOFF.md`.
2. Read `README.md` for project setup and inference instructions.
3. Review `results/` for evaluation reports and experimental findings.
4. Access model checkpoints and datasets through the shared Google Drive folder.

## Main findings
- The baseline remains the primary classifier.
- The contrastive confidence experiment did not improve classification F1.
- The controlled confidence head did not improve error-detection AUROC.
- Temperature scaling showed preliminary calibration improvements, but uncertainty remains.
- Official SHROOM model-agnostic and model-aware evaluations are available.

## Important limitations
- Validation data was reused during development.
- Exact-overlap analysis does not rule out semantic overlap.
- Literature verification and full-text screening remain incomplete.
- Reconstructed training scripts may not exactly reproduce the original implementation.
- Do not claim novelty until the closest related methods are fully compared.

## Artifact storage
Large model checkpoints and datasets are intentionally excluded from Git.
P2 must have access to the shared Google Drive folder:
`hallucination_project`

## Next steps for P2
1. Verify baseline inference in a clean environment.
2. Audit source files, dependencies, and saved results.
3. Complete literature screening and refine the research-gap statement.
4. Consolidate the methodology, metrics, and limitations.
5. Agree on a stable backend API with P3.
