# Loss Playbook for CLAM_MB (OncoMETS)

Anchored to the real codebase at `sebastianDonoso/testMIL/CLAM/`.

## Current Baseline

Bag loss: `nn.CrossEntropyLoss()` — set in `core_utils.py:123`
Instance loss: `SmoothTop1SVM(n_classes=2)` — set in `core_utils.py:141-144`
Combination: `total_loss = 0.7 * bag_loss + 0.3 * instance_loss` — `core_utils.py:249`

## 1) Weighted CE (replace bag loss)

Where: `core_utils.py:123`, replace `nn.CrossEntropyLoss()` with weighted version.

```python
# Compute weights from dataset class distribution
class_counts = [len(dataset.slide_cls_ids[c]) for c in range(len(dataset.slide_cls_ids))]
weights = 1.0 / torch.tensor(class_counts, dtype=torch.float)
weights = weights / weights.sum() * len(weights)
loss_fn = nn.CrossEntropyLoss(weight=weights.to(device))
```

Intuition: increases gradient magnitude for minority classes. Too-large weights destabilize training and inflate false positives.

## 2) Focal Loss (replace bag loss)

Where: `core_utils.py:123`, define custom FocalLoss class.

```python
class FocalLoss(nn.Module):
    def __init__(self, alpha=0.25, gamma=2.0, n_classes=2):
        super().__init__()
        self.gamma = gamma
        self.alpha = alpha

    def forward(self, logits, targets):
        ce = F.cross_entropy(logits, targets, reduction='none')
        pt = torch.exp(-ce)
        loss = self.alpha * (1 - pt) ** self.gamma * ce
        return loss.mean()
```

Intuition: gamma controls focus on hard examples. Higher gamma down-weights easy negatives. Start with alpha=0.25, gamma=2.0.

## 3) Balanced Softmax (replace bag loss)

Where: `core_utils.py:123`, adjust logits before standard CE.

```python
# Prior correction in logit space
class_freq = torch.tensor(class_counts, dtype=torch.float).to(device)
log_prior = torch.log(class_freq / class_freq.sum())

class BalancedSoftmaxLoss(nn.Module):
    def __init__(self, log_prior):
        super().__init__()
        self.log_prior = log_prior

    def forward(self, logits, targets):
        adjusted = logits + self.log_prior
        return F.cross_entropy(adjusted, targets)
```

Intuition: compensates for class-frequency bias in learned logits. Ideal for extreme count skew (tipo_histologico with 18 classes).

## 4) Soft Targets for Semi-Supervised Transition

Where: `model_clam.py:inst_eval()` L107-123 (modify target generation).

```python
# Replace hard fabricated targets with mixed soft targets
# y_attention: current top-k assignment (1s and 0s)
# y_faiss: nearest-neighbor propagated labels (confidence-weighted)
# y_human: manual annotations when available

y_mix = (1 - alpha - beta) * y_attention + alpha * y_faiss + beta * y_human
# Use KL divergence or soft cross-entropy instead of SmoothTop1SVM
instance_loss = F.cross_entropy(logits, y_mix)
```

Start with alpha=0.1, beta=0.05 (conservative trust in external labels). Increase beta as reviewer agreement data accumulates.

## 5) Instance Loss Swap (replace SmoothTop1SVM)

Where: `core_utils.py:141-147`, change `instance_loss_fn`.

The current SmoothTop1SVM is imported from `topk.svm`. A simpler first experiment: swap to `nn.CrossEntropyLoss()` for instance loss (already supported via `--inst_loss ce` flag).

This removes the SVM margin behavior and may stabilize training when combined with focal bag loss.

## Decision Rules

1. If minority recall is the main pain point: test focal loss (bag) first.
2. If calibration or prior shift dominates: include balanced softmax.
3. If attention-based pseudo-labels are noisy: test CE instance loss swap first (zero code change, just `--inst_loss ce`).
4. If human feedback is being integrated: implement soft target mixing in inst_eval().

## Practical Guardrails

- Change one major axis at a time (bag loss, instance loss, sampler).
- Evaluate with at least 2 seeds before accepting.
- Rollback condition: macro-F1 or minority recall drops more than 3%.
- Fast validation task: `invasion_linfatica_vascular` (2 classes, 41 samples).
