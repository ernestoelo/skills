# Python Development Environments in Arch Linux

## Overview
This guide addresses the complexity of managing multiple Python environments in Arch Linux, particularly when using system packages (pacman), user environments (conda/miniforge), and development tools (poetry, pipx, uv).

## Your Current Environment

### Detected Setup (as of March 2026 — UPDATED)
```yaml
System Python: 3.14.3
Miniforge Python: 3.12.11 (DEACTIVATED by default)
Miniforge Path: /home/p3g4sus/miniforge3
Conda Environments: base only (ocv, viz removed - not needed)
Development Tools: uv 0.10.9, pipx 1.8.0
Auto-activation: NO (manual control via aliases)
```

### Environment Configuration
```bash
# In ~/.zshrc (UPDATED):
# Miniforge is DISABLED by default to avoid pacman/yay conflicts
# No automatic PATH modification on shell startup

# Manual control via aliases:
alias conda-on='export PATH="$HOME/miniforge3/bin:$PATH"'
alias conda-off='export PATH="${PATH#$HOME/miniforge3/bin:}"'
```

## The Core Problem: Pacman ↔ Conda Conflict

### What Happens

When you run `yay -S package-name` with miniforge3 active:

```
┌─────────────────────────────────────────────────────────┐
│ USER EXECUTES: yay -S gns3-gui                         │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │ Is miniforge active?│
        └──────────┬──────────┘
                   │
         ┌─────────▼─────────┐
         │ YES (in PATH)     │
         └────────┬──────────┘
                  │
    ┌─────────────▼─────────────┐
    │ yay sees $CONDA_PREFIX    │
    │ and INSTALLS TO:          │
    │ ~/.../miniforge3/lib/     │  ❌ WRONG LOCATION
    │ (NOT /usr/lib/python)     │
    └───────────────────────────┘
                  │
    ┌─────────────▼──────────────┐
    │ Result:                    │
    │ - Dependencies in 2 places │
    │ - Version conflicts        │
    │ - Import errors           │
    │ - "module not found"      │
    └────────────────────────────┘
```

### Real Example: GNS3 Installation Failure

**What happened:**
```
yay -S gns3-gui gns3-server (with miniforge ACTIVE)
├─ gns3 installed in: /home/p3g4sus/miniforge3/lib/python3.12/site-packages/gns3/
├─ But Arch deps (PyQt6) tried to install in: /usr/lib/python3.12/
├─ Result: ImportError - PyQt6 not found in miniforge context
└─ GNS3 crashed with: "Can't import Qt modules"
```

## Solutions & Best Practices

### Solution 1: Deactivate Miniforge Before Installing (RECOMMENDED)

**When:** Installing system-level packages with `yay -S`  
**How:** Reverse miniforge activation temporarily

```bash
# Option A: Disable miniforge for ONE command
conda deactivate
yay -S package-name
conda activate base  # or 'ocv', 'viz', etc.

# Option B: Disable miniforge for multiple commands
conda deactivate
yay -S package1 package2 package3
pacman -Q | grep package
conda activate base
```

**Why:** Packages install to system locations (/usr/lib/python) where Arch expects them.

### Solution 2: Use Python Virtual Environments Exclusively

**When:** Developing with specific project dependencies  
**How:** Create isolated environments separate from system

```bash
# Create venv (NOT in miniforge)
python3.14 -m venv ~/projects/myproject/.venv

# Activate (replaces miniforge temporarily)
source ~/projects/myproject/.venv/bin/activate

# Now pip install works correctly
pip install your-package

# Exit back to miniforge
deactivate
```

### Solution 3: Use pipx for CLI Tools (BEST for tools like GNS3)

**When:** Installing CLI applications that need isolated environments  
**How:** Let pipx manage its own environment

```bash
# Tools like GNS3 that need GUI:
# Install in pipx, runs in isolated environment
pipx install gns3-gui gns3-server

# Automatically creates and manages environments
# This is what SHOULD have happened initially
```

## Environment Types & When to Use

| Environment Type | Use Case | Activation | Risk |
|---|---|---|---|
| **System Python** (Arch pacman) | System tools, scripts | Always available at `/usr/bin/python3` | ⚠️ Conflicts with conda |
| **miniforge base** | General development | Auto-active (in ~/.zshrc) | ⚠️ Interferes with pacman |
| **conda env (ocv, viz)** | Specialized projects | `conda activate ocv` | ✅ Isolated when active |
| **venv project** | Project isolation | `source .venv/bin/activate` | ✅ Completely isolated |
| **pipx** | CLI applications | Auto-managed by pipx | ✅ Best for tools |
| **uv** | Fast Python management | `uv venv`, `uv run` | ✅ Modern solution |

## Decision Tree: Which Python Environment?

```
Start: Need to install something?
│
├─ Is it a SYSTEM package needed by Arch?
│  └─> Yes: ALWAYS deactivate conda first, use pacman/yay
│
├─ Is it a CLI TOOL (like gns3, docker-compose)?
│  └─> Yes: Use pipx install tool-name
│
├─ Is it for a SPECIFIC PROJECT?
│  └─> Yes: Use venv or conda env, NOT system/miniforge base
│
├─ Is it a GLOBAL PYTHON LIBRARY?
│  └─> Yes: Consider if it should be project-specific instead
│  └─> If truly global: use miniforge base env (AFTER deactivating for pacman)
│
└─ Is it a PERFORMANCE-CRITICAL tool?
   └─> Yes: Use uv (faster than conda for package resolution)
```

## Conda Environment Management (UPDATED)

### List Environments (You have 1: base)
```bash
conda env list
# base (general-purpose, minimal dependencies)
# REMOVED: ocv, viz (unused environments deleted to reduce PATH complexity)
```

### Activate Miniforge When Needed
```bash
# Check if miniforge is in PATH
echo $PATH | grep miniforge

# If not present, activate manually:
conda-on
conda activate base

# Verify:
python --version  # Should show 3.12.11 (miniforge)
which python

# When done with conda work, deactivate:
conda-off
```

### For Project-Specific Python Environments
```bash
# Create isolated environments as needed (NOT in miniforge base):
python3 -m venv ./project-venv
# OR for conda-based projects:
conda create -n project-name python=3.12
conda activate project-name
```

### When Installing in Conda Environments

```bash
# DON'T do this (interferes with Arch):
# yay -S python-package  (while miniforge active)

# DO this instead:
conda activate myenv
pip install pypi-package

# OR use conda-forge channel:
conda activate myenv
conda install -c conda-forge package-name
```

## Checklist: Safe Package Installation in Arch

Before every `yay -S` or `pacman -S`:

- [ ] Check if conda/miniforge is active: `echo $CONDA_DEFAULT_ENV` or `which python3`
- [ ] If active, run: `conda deactivate`
- [ ] Verify: `which python3` should output `/usr/bin/python3`, NOT miniforge
- [ ] Now run: `yay -S package-name` or `pacman -S package-name`
- [ ] Re-activate if needed: `conda activate base`

## Auto-Detection Script for Your Workflow

Place in your utility scripts:

```bash
#!/bin/bash
# Source this before package operations
# Temporarily disables conda in current shell session

if [ -n "$CONDA_DEFAULT_ENV" ]; then
    echo "⚠️  Conda environment active: $CONDA_DEFAULT_ENV"
    echo "Deactivating for safe package management..."
    conda deactivate
    export _CONDA_WAS_ACTIVE=1
else
    echo "✅ Conda not active, safe to proceed"
fi

# Install packages here
# yay -S package-name

# Restore if needed
if [ "$_CONDA_WAS_ACTIVE" = "1" ]; then
    conda activate $CONDA_DEFAULT_ENV
    echo "✅ Conda restored: $CONDA_DEFAULT_ENV"
fi
```

## Integration with Architect Skill

When scaffolding new development projects with @architect:

1. **Always create project-specific environments, never use miniforge base**
   ```bash
   # DO THIS for projects:
   python3.14 -m venv ./venv
   # OR
   conda create -n project-name python=3.12
   ```

2. **Before any infrastructure operations, deactivate conda**
   ```bash
   conda deactivate  # Before: pacman/yay, systemctl, etc.
   ```

3. **Document environment in project** (per @architect)
   ```bash
   # .envrc or project docs should include:
   # "Run: conda deactivate && yay -S system-deps"
   # "Then: conda activate project-env && pip install -r requirements.txt"
   ```

## Integration with dev-workflow Skill

Version reproducibility requires consistency:

```yaml
# In your project's environment spec (@dev-workflow):
system_requirements:
  - deactivate_conda: true  # CI/CD must disable conda
  - python_version: "3.14.3"  # System Python for tools
  
python_dependencies:
  - path: ./venv  # Project venv
  - strategy: "pipenv" or "uv" or "conda"  # Explicit choice
```

## Troubleshooting

### Problem: "module not found" after `yay -S`
**Diagnosis:** Package installed in miniforge, not system
**Fix:** 
```bash
conda deactivate
yay -Rdd broken-package
yay -S broken-package  # Now installs correctly
```

### Problem: Two Python versions conflict
**Diagnosis:** System Python vs miniforge doing different things
**Check:**
```bash
which python3  # Shows which Python is active
/usr/bin/python3 --version  # System version
~/miniforge3/bin/python3 --version  # Miniforge version
```

### Problem: `yay` behaves differently each time
**Diagnosis:** Sometimes conda active, sometimes not
**Solution:** Add check to your shell init:
```bash
# In ~/.zshrc, BEFORE conda init:
if [ -z "$_IN_SYSTEMD_SYSTEM" ]; then
    # Only auto-activate conda in interactive shells
    # NOT during package operations
    export CONDA_AUTO_ACTIVATE=false
fi
```

## References
- [Conda documentation: managing environments](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
- [Python venv official docs](https://docs.python.org/3/library/venv.html)
- [pipx documentation](https://pipx.pypa.io/)
- [uv GitHub repository](https://github.com/astral-sh/uv)
- [Arch Linux Python packaging](https://wiki.archlinux.org/title/Python)

## Next Steps
1. Bookmark this guide for future package installations
2. Add the safety checklist to your development workflow
3. When creating new projects, use @architect with conda environments (not base)
4. Test any system installations on non-critical machines first
