---
name: oncomets-mil-loss-lab
description: "Use when designing, comparing, or debugging CLAM_MB loss functions under class imbalance and weak-to-semi-supervised transitions with human feedback in OncoMETS. Trigger words: loss, CLAM, MIL, imbalance, pseudo-label, FAISS, retraining, inst_eval, perdida, desbalance, pseudoetiqueta, reentrenamiento."
---

# OncoMETS MIL Loss Lab

## Codebase Anchor

The working CLAM codebase is at `sebastianDonoso/testMIL/CLAM/` (relative to `/mnt/disco_duro/onco/`).

Key files for loss experiments:
- `utils/core_utils.py` — `train_loop_clam()` (L225): bag+instance loss combination
- `models/model_clam.py` — `CLAM_MB`, `inst_eval()` (L107): pseudo-label generation via attention top-k
- `main.py` — `TASK_CONFIGS` dict with 10 clinical categories and their label dicts
- `environ/csv/` — ground truth CSVs (23-41 samples per task)

Baseline config (identical across all 10 trained models):
- `CLAM_MB`, `bag_loss=nn.CrossEntropyLoss()`, `inst_loss=SmoothTop1SVM(n_classes=2)`
- `bag_weight=0.7`, `WeightedRandomSampler`, `Adam(lr=2e-4)`, `k_sample=8`

## Use When
- Training is unstable, minority recall is poor, or calibration is weak.
- Choosing between weighted BCE, focal loss, balanced softmax, or hybrid losses.
- Planning weak-to-semi-supervised updates with human feedback and pseudo-labels.
- Making a decision under tight time and compute budgets (20h/week).

## Required Inputs
1. Target metric (macro-F1, minority recall, AUROC).
2. Which of the 10 clinical tasks is being optimized.
3. Current error pattern (false negatives vs false positives, per class).
4. Time budget and acceptable implementation scope.
5. Feedback channel status (none, FAISS retrieval, manual relabeling, retraining plan).

## Workflow

### 1) Diagnose Failure Mode
Confirm whether the bottleneck is:
- Class imbalance (most tasks have 3-18 classes with ~40 total samples)
- Noisy pseudo-labels from attention-based top-k assignment in `inst_eval()`
- Instance assignment drift (attention scores shift during training)
- Optimization instability (bag_weight=0.7 vs SmoothTop1SVM interaction)

### 2) Select Candidate Losses (max 2-3)

| Situation | Candidate | Where to change |
|-----------|-----------|-----------------|
| Imbalance + easy negatives | Focal loss or weighted CE | `core_utils.py:123` (bag) |
| Prior shift across classes | Balanced softmax | `core_utils.py:123` (bag) |
| Noisy attention pseudo-labels | Label smoothing on inst targets | `model_clam.py:115-116` |
| Human feedback integration | Soft target mixing | `model_clam.py:inst_eval()` |

### 3) Define Minimal Experiment Matrix

| Axis | Option A | Option B |
|------|----------|----------|
| Bag loss | CE (baseline) | 1 candidate |
| Instance loss | SmoothTop1SVM (baseline) | nn.CrossEntropyLoss |
| Sampler | WeightedRandom (baseline) | Class-aware custom |

Max 4-6 runs per cycle. Expand only if first pass shows clear gains.

### 4) Implementation Guidance
- Keep architecture (CLAM_MB) unchanged in first pass.
- Change one primary variable per run.
- Log: seed, split, config hash. Use `seed_torch()` from main.py.
- Test with a fast task first (invasion_linfatica_vascular, 2 classes, 41 samples).

### 5) Evaluation and Decision
- Minimum +2-5 points on minority recall or macro-F1.
- No regression on overall AUROC.
- Stable training curves across at least 2 seeds.
- Calibration does not degrade on validation.

### 6) Next Action
- **Go**: patch plan for production training across all 10 tasks.
- **No-go**: document why and roll back cleanly.
- **Mixed**: keep best candidate, test threshold and calibration only.

## Injection Point for Semi-Supervised Transition

The current pseudo-labeling in `CLAM_MB.inst_eval()` (model_clam.py:107-123):

```python
# Current: attention-based pseudo-labels
top_p_ids = torch.topk(A, self.k_sample)[1][-1]      # high attention = positive
top_n_ids = torch.topk(-A, self.k_sample, dim=1)[1][-1]  # low attention = negative
p_targets = create_positive_targets(k_sample, device)  # all 1s
n_targets = create_negative_targets(k_sample, device)   # all 0s
```

To inject human feedback, modify `inst_eval()` to accept an optional `human_labels` dict mapping patch indices to {0,1}. When available, override the fabricated targets. For FAISS: build an index on the 512-dim features, retrieve neighbors of annotated patches, propagate labels with confidence decay.

## Output Contract
Every response must include:
1. Recommended primary loss and fallback option.
2. Why this choice fits the diagnosed failure mode.
3. Minimal experiment plan with specific file:line references.
4. Estimated effort and risk.
5. Stop/go criteria and rollback condition.

## Guardrails
- Do not change data pipeline and loss simultaneously.
- Do not refactor architecture during a loss experiment.
- Always use `seed_torch()` and evaluate with at least 2 seeds.
- Rollback if macro-F1 or minority recall drops more than 3%.

## References
- See `references/loss-playbook.md` for formulas and PyTorch snippets.
