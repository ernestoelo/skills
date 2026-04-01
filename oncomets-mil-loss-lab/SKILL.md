---
name: oncomets-mil-loss-lab
description: "Use when designing, comparing, or debugging CLAM/MIL loss functions under class imbalance and weak-to-semi-supervised transitions with human feedback in OncoMETS. Trigger words: loss, CLAM, MIL, imbalance, pseudo-label, FAISS, retraining, perdida, desbalance, pseudoetiqueta, reentrenamiento."
---

# OncoMETS MIL Loss Lab

## Overview
This skill provides a fast, pragmatic workflow to iterate on loss functions for CLAM pipelines with CONCH features.
Use this skill when you need to improve bag-level performance without a large refactor.

## Use When
- You see unstable training, poor minority recall, or weak calibration.
- You need to choose between weighted BCE, focal loss, balanced softmax, or hybrid losses.
- You are planning weak-to-semi-supervised updates with human feedback and pseudo-labels.
- You need to make a decision under tight time and compute budgets.

## Required Inputs
1. Objective and target metric (for example macro-F1, minority recall, AUROC).
2. Current loss, optimizer, and sampling strategy.
3. Class distribution for the specific clinical category model.
4. Current error pattern (false negatives vs false positives).
5. Time budget, GPU budget, and acceptable implementation scope.
6. Feedback channel status (none, FAISS retrieval, manual relabeling queue, retraining plan).

## Workflow
### 1) Diagnose Failure Mode
- Confirm whether the bottleneck is class imbalance, noisy weak labels, instance assignment drift, or optimization instability.
- Check whether the issue is bag-level only or also instance-level.

### 2) Select Candidate Losses
- Pick at most 2-3 candidates for one iteration cycle.
- Prefer low-risk changes first.

Candidate map:

| Situation | Candidate |
|-----------|-----------|
| Strong class imbalance with many easy negatives | Focal loss or weighted BCE |
| Prior shift across classes | Balanced softmax |
| Noisy pseudo-labels | Label smoothing or soft target cross-entropy |
| Weak plus human feedback mix | Convex target mixing with consistency term |

### 3) Define Minimal Experiment Matrix
Run a minimal matrix to keep iteration speed high:

| Axis | Option A | Option B |
|------|----------|----------|
| Loss | Baseline | Candidate |
| Sampler | Baseline | Class-aware sampler |
| Threshold | Fixed 0.5 | Validated threshold |

Do not expand beyond 4-6 runs in one cycle unless the first pass shows clear gains.

### 4) Implementation Guidance
- Keep architecture unchanged in the first pass.
- Change one primary variable per run.
- Log random seed, split, and config hash for reproducibility.

### 5) Evaluation and Decision
Use model-specific go/no-go criteria:
- Minimum plus 2 to 5 points on minority recall or macro-F1, depending on baseline variance.
- No significant regression on overall AUROC.
- Stable training curves across at least 2 seeds.
- Calibration does not degrade materially on validation.

### 6) Prepare Next Action
- If go: produce a small patch plan for production training.
- If no-go: document why and roll back cleanly.
- If mixed: keep the best candidate and test threshold and calibration only.

## Output Contract
Every response should include:
1. Recommended primary loss and fallback option.
2. Why this choice fits the current failure mode.
3. Minimal experiment plan (numbered).
4. Estimated effort and risk.
5. Stop/go criteria and rollback condition.

## Guardrails
- Prioritize pragmatic changes over ideal large refactors.
- Avoid changing data pipeline and loss simultaneously in one cycle.
- Keep explanations concise, mathematical, and directly tied to PyTorch behavior.

## References
- See references/loss-playbook.md for formulas and PyTorch snippets.
