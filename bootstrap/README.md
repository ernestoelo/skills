# OncoMETS workspace bootstrap

This folder provides a minimal bootstrap flow to deploy the new OncoMETS AI customization set on a clean remote machine (for example Werner) over SSH.

## What gets installed
- Project-scoped instruction file at .github/copilot-instructions.md.
- Project-local skill link at .github/skills/oncomets-mil-loss-lab.
- Isolated VS Code workspace file with chat.agentSkillsLocations enabled.

## Run
From the cloned skills repository in Werner:

```bash
cd bootstrap/scripts
chmod +x setup_oncomets_workspace.sh
./setup_oncomets_workspace.sh --project-path /path/to/oncomets
```

Optional flags:
- --link-full-library: also exposes the full shared skills repository in workspace settings.
- --force: overwrite existing instruction and workspace files.

## Why this helps
- Keeps customization scope isolated to the OncoMETS workspace.
- Avoids hardcoding sensitive data in shared files.
- Preserves one canonical source of truth in your GitHub skills repository.
