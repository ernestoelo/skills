# Recursive Context Workflow Details

## Unified Workflow (RLM + Transparency)

1. **Preparation and Compatibility**:
   - Use `scripts/env_check.py` to verify Python, libraries (pypdf, spacy, pytesseract), and hardware (Jetson/ZedBox).
   - Ensures safe execution without resource issues.

2. **Reception of Information**:
   - Receive large input file (PDF, log, text) and operation type (e.g., "robotics-log analysis").

3. **Chunking Initial**:
   - Run `scripts/context_loader.py` to divide input into logical blocks (by tokens, headings, timestamps).
   - Extract metadata: length, structure, first/last lines.
   - Output: JSON with chunks for iterative access.

4. **Topic Extraction**:
    - Use `scripts/topic_extractor.py` to analyze chunks for valuable topics.
    - Employ NLP (spaCy) and RegEx for keywords/entities.
    - Provide evidence: fragments with locations.

5. **Transparencia de Contexto**:
   - Display model context window (e.g., "4096 tokens").
   - Explain division in iterations to avoid saturation.

6. **Iteración y Recomendación**:
   - Process each chunk in sub-llamadas RLM.
   - Recommend focus based on problem (e.g., odometry errors).
   - Accumulate results in variables.

7. **Outputs y Evidencia**:
   - Chunks JSON, topics report with evidence.
   - Recommendations with context notes.
   - Summary of full coverage.

8. **Version Control y Packaging**:
   - Follow dev-workflow: branches, commits semánticos.
   - Package with `package_skill.py`.

## Robotics Examples
- **Logs ZED**: Chunk by timestamps, extract depth anomalies.
- **Código C++**: Chunk by functions, recommend focus on calibration.

This workflow ensures scalability, transparency, and anti-hallucinations.