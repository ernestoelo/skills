---
name: dataset-structure
description: Canonical structure and format for YOLO training datasets. Use to scaffold, validate, and reuse dataset folders for segmentation training workflows. Inspired by dev-workflow and architect skills.
license: Apache-2.0
---

# Dataset Structure Skill

This skill defines the standard folder and file structure for YOLO segmentation training datasets, ensuring reproducibility and compatibility with Ultralytics workflows.

## Anatomy

```
dataset/
├── data.yaml         # Dataset config (classes, train/val paths)
├── images/
│   └── train/        # Training images (.jpg, .png)
├── labels/
│   └── train/        # Segmentation labels (.txt, YOLO format)
├── train.txt         # (Optional) List of image paths for custom splits
```

## data.yaml Format
- `names`: List or dict of class names (e.g. `{0: salmon}`)
- `train`: Path to training images folder or train.txt
- `val`: Path to validation images folder or val.txt

Example:
```
names:
  0: salmon
train: images/train
val: images/train
```

## File Naming
- Images: `frame_XXXXX.jpg`
- Labels: `frame_XXXXX.txt` (one per image)

## Best Practices
- Each image in `images/train/` must have a matching label in `labels/train/`.
- Use relative paths in data.yaml for portability.
- Validate structure with scripts or checklist before training.

## Integration
- Use with @dev-workflow for project validation.
- Scaffold new datasets with @architect skill for reproducibility.

## References
- See dev-workflow/SKILL.md and architect/SKILL.md for validation and scaffolding patterns.
- For advanced splits, use train.txt/val.txt with absolute or relative paths.

---
