# Context Window Limits by Model

| Model | Context Window (Tokens) | Notes |
|-------|--------------------------|-------|
| GPT-4 | 8192 | Standard for most tasks |
| GPT-4 Turbo | 128000 | High capacity for large docs |
| Claude 3 | 200000 | Excellent for robotics logs |
| Llama 3 | 8192 | Common open-source limit |
| Custom RLM | Variable | Depends on implementation |

## Recommendations
- Always check model limits before chunking.
- For Jetson/ZedBox, limit chunks to 4096-8192 to avoid memory issues.
- Use iterative processing to stay within limits.