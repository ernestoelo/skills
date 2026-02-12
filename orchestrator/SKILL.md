---
name: orchestrator
description: Universal master skill that initiates workflows, interconnects other skills via state machine pipelines for complex tasks like PDF processing, dev workflows, and iterative corrections.
---

# Orchestrator Skill Guide

## Description
The `orchestrator` skill acts as the universal master, analyzing user queries to select and execute predefined pipelines of interconnected skills. It uses a state machine to manage workflows, passing data between skills and supporting iteration for error correction.

## When to Use the Skill
- **Complex multi-skill tasks:** E.g., reading PDFs with recursive context, dev workflows with code review and commits.
- **Automated pipelines:** For tasks requiring sequential skill invocation with data flow.
- **Iterative processes:** When corrections or retries are needed based on skill outputs.

## Usage Guide
Invoke with @orchestrator "task description", e.g., @orchestrator "read and summarize this PDF".

Pipelines are defined in `references/pipelines.yaml`.

## Inputs and Outputs
### Inputs
- **Query:** Natural language task description.

### Outputs
- **Pipeline execution:** Results from invoked skills, aggregated.

## Best Practices
- Define pipelines manually in YAML for control.
- Supports iteration up to max retries.

## Resources
- `scripts/orchestrator.py`: Main state machine script.
- `references/pipelines.yaml`: Pipeline configurations.