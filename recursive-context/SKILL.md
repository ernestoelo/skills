---
name: recursive-context
description: Provides transparent workflows for unlimited context processing using Recursive Language Models (RLM). Divides inputs into blocks, extracts valuable topics with evidence, recommends focus, mentions context windows, and handles iterative processing to avoid hallucinations.
---

# Recursive Context Skill Guide

## Description
The `recursive-context` skill unifies RLM logic with transparent workflows for handling infinite inputs. It treats large contexts as external environments, divides them into blocks, extracts key topics, provides evidence of full coverage, recommends focus based on problem context, mentions model context windows, and processes iteratively to prevent AI hallucinations. Applicable to any textual or structured data, including codes, repositories, .md files, logs, datasets, and more.

## When to Use the Skill
- **Large inputs:** Documents, logs, or codebases beyond context limits.
- **Transparency needs:** Requiring evidence, recommendations, and iteration breakdowns.
- **Code and repositories:** Analysis of large codebases for refactoring, debugging, or incremental processing by commits/branches.
- **Documentation and .md files:** Processing of READMEs, changelogs, wikis, or technical docs.
- **Data and information variety:** Logs, datasets, or any textual context exceeding model limits.

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
- Supports PDF (via pdftotext from pdf skill) and text files; outputs chunks with metadata.

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

### CI/CD Integration and Hooks
- **Validation:** Scripts are linted and tested via "Validate Skills" GitHub Actions workflow on commits.
- **Auto-Correction:** If linting fails, "Auto-Correct CI" triggers up to 5 iterations to fix issues (e.g., unused imports) and re-commits.
- **Hooks:** Pre-commit hooks (via dev-workflow) ensure code quality before pushes; post-commit, CI monitors for failures and notifies via issues if unresolved.
- Follows dev-workflow standards: Semantic commits, branch management, and CI/CD best practices.

## Inputs and Outputs
### Inputs
- **File path:** Input file (PDF, text, code, .md, log, dataset).
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
- **CI/CD:** Commit changes trigger GitHub Actions validation; use auto-correct for linting issues; monitor workflows via dev-workflow scripts.
- **Code Analysis:** Process repositories incrementally by commits or branches for contextual focus; handle .md files for documentation insights.

### Version History
| Version | Date       | Updates |
|---------|------------|---------|
| 1.0.0   | 2026-02-10 | Unified RLM + transparency workflow. |

## Resources
- `references/workflow-details.md`: Step-by-step guide.
- `references/context-limits.md`: Model windows.
- `references/robotics-examples.md`: ZedBox applications.
- `docs/assets/recursive_language_models_paper.pdf`: Full RLM paper for technical details.
- **CI/CD Integration:** See dev-workflow/SKILL.md and references/ci-cd-best-practices.md for automated validation and hooks.
