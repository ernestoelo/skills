# Loss Playbook for CLAM and MIL (OncoMETS)

This reference keeps formulas and practical PyTorch intuition short and actionable.

## 1) Weighted BCE
Use when minority classes are systematically under-detected.

Formula:
L = -w_y [ y log(p) + (1 - y) log(1 - p) ]

PyTorch intuition:
- Increasing class weight increases gradient magnitude for minority errors.
- Too large weights can destabilize optimization and inflate false positives.

## 2) Focal Loss
Use when there are many easy negatives dominating the batch.

Formula:
L = -alpha (1 - p_t)^gamma log(p_t)

PyTorch intuition:
- gamma controls focus on hard examples.
- Higher gamma down-weights easy samples and can improve minority recall.

## 3) Balanced Softmax
Use when class priors differ strongly and predicted posteriors are biased.

Concept:
- Adjust logits with class-frequency priors before softmax.

PyTorch intuition:
- Equivalent to prior correction in logit space.
- Useful for long-tail categories with severe count skew.

## 4) Soft Targets for Weak-to-Semi Supervision
Use when combining weak labels, pseudo-labels, and human feedback.

One practical formulation:
y_mix = (1 - alpha - beta) y_weak + alpha y_pseudo + beta y_human

Then optimize cross-entropy or KL with y_mix.

PyTorch intuition:
- alpha and beta trade off trust between generated and human-provided signals.
- Start with conservative beta unless reviewer agreement is high.

## 5) Minimal Decision Rules
- If minority recall is the main pain point, test weighted BCE or focal first.
- If calibration and prior shift are dominant, include balanced softmax.
- If noisy pseudo-labels are introduced, add soft targets and consistency terms.

## 6) Practical Guardrails
- Change one major axis at a time (loss, sampler, threshold).
- Evaluate with at least two seeds before accepting a change.
- Keep a strict rollback condition tied to macro-F1 and minority recall.
