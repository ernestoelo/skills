---
name: recursive-context
description: Provides transparent workflows for unlimited context processing using Recursive Language Models (RLM). Divides inputs into blocks, extracts valuable topics with evidence, recommends focus, mentions context windows, and handles iterative processing to avoid hallucinations.
---

# Recursive Context Skill Guide

## Description
The `recursive-context` skill unifies RLM logic with transparent workflows for handling infinite inputs. It treats large contexts as external environments, divides them into blocks, extracts key topics, provides evidence of full coverage, recommends focus based on problem context, mentions model context windows, and processes iteratively to prevent AI hallucinations.

## When to Use the Skill
- **Large inputs:** Documents, logs, or codebases beyond context limits.
- **Transparency needs:** Requiring evidence, recommendations, and iteration breakdowns.

## Usage Guide
### Environment Setup and Compatibility
Check compatibility (sys-env style):
```bash
python3 scripts/env_check.py --libs pypdf spacy pytesseract
```
- Validates Python, libraries, and Jetson resources.

### Input Reception and Chunking
Receive file and divide into blocks:
```bash
python3 scripts/context_loader.py --input /path/to/log.pdf --type robotics-log
```
- Outputs chunks with metadata (length, structure).

### Topic Extraction and Transparency
Extract topics with context info:
```bash
python3 scripts/topic_extractor.py --chunks chunks.json --window 4096
```
- Lists topics with evidence; displays "Context window: 4096 tokens; iterations: 5".

### Iterative Processing and Recommendations
Process chunks iteratively with recommendations:
```bash
for chunk in $(python3 scripts/context_loader.py --list chunks.json); do
  echo "Iterating on $chunk"
  python3 scripts/topic_extractor.py --focus $chunk --problem odometry-errors
done
```
- Accumulates results; recommends focus (e.g., "Focus on timestamps with variance >3m").

## Inputs and Outputs
### Inputs
- **File path:** Input file (PDF, text, log).
- **Type/Problem:** e.g., "robotics-log" or "odometry-analysis".
- **Context details:** Window size, iterations.

### Outputs
- **Chunks:** JSON with blocks and metadata.
- **Topics Report:** Extracted topics with evidence/locations.
- **Recommendations:** Focused areas with context notes.
- **Evidence Summary:** Coverage proof and final synthesis.

## Best Practices and Version History
### Best Practices
- **Chunking:** Limit to context size; use symbolic access.
- **Transparency:** Always show evidence and limits.
- **Robotics:** Validate on ZedBox for logs/odometry.

### Version History
| Version | Date       | Updates |
|---------|------------|---------|
| 1.0.0   | 2026-02-10 | Unified RLM + transparency workflow. |

## Resources
- `references/workflow-details.md`: Step-by-step guide.
- `references/context-limits.md`: Model windows.
- `references/robotics-examples.md`: ZedBox applications.
