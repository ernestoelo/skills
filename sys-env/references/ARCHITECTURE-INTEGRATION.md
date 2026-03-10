# Integration Guide: python-environments.md with @architect

This document explains how to use the python-environments.md reference guide when working with @architect skill for development projects.

## When to Use This Guide with @architect

### Scenario 1: Creating New Development Project
```bash
# 1. Let @architect scaffold the project
@architect create-project my-project --type python

# 2. BEFORE any system package installations, run:
/home/p3g4sus/.copilot/skills/sys-env/scripts/check-python-env.sh

# 3. Deactivate conda if active
conda deactivate

# 4. Install system dependencies
yay -S system-package-names

# 5. Create project-specific environment (never use miniforge base)
cd my-project
python3.14 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

### Scenario 2: Installing vs. Developing
```
Decision:
├─ Is this a CLI TOOL being DEPLOYED? (e.g., GNS3, Docker wrapper)
│  └─> Use: pipx install tool-name (managed by pipx, isolated)
│
├─ Is this a LIBRARY for my PROJECT? 
│  └─> Use: venv inside project (python3.14 -m venv)
│  └─> Or: conda create -n project-name (separate from base)
│
└─ Is this a SYSTEM-LEVEL DEPENDENCY?
   └─> Use: yay -S package (after `conda deactivate`)
```

## Best Practices When Using @architect

1. **Always Document Environment Setup in README**
```markdown
## Development Setup

### Prerequisites
- Arch Linux with conda deactivated: `conda deactivate`
- System packages: `yay -S base-devel git ...`

### Project Environment
```bash
# Create isolated environment
python3.14 -m venv ./venv
source ./venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
```

2. **Never Use miniforge base for Projects**
```bash
# ❌ DON'T DO THIS:
conda activate base  # Uses miniforge base
pip install -r requirements.txt

# ✅ DO THIS INSTEAD:
python3.14 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

3. **CI/CD Pipeline Integration**
```yaml
# In your CI config (GitHub Actions, GitLab CI, etc.):
before_script:
  - conda deactivate || true  # Disable conda for system operations
  - yay -S --noconfirm base-devel git python3
```

4. **Pre-Project Checklist (from @architect)**
- [ ] Run `check-python-env.sh` - verify safe state
- [ ] `conda deactivate` - disable miniforge
- [ ] Install system deps with pacman/yay
- [ ] Create project venv: `python3.14 -m venv ./venv`
- [ ] Activate venv: `source ./venv/bin/activate`
- [ ] Install project deps: `pip install -r requirements.txt`

## Troubleshooting Integration Issues

### "ImportError: No module named X" after yay -S
**Root Cause:** Package installed in conda, not system location  
**Fix:** See full troubleshooting section in references/python-environments.md

### @architect Project Tools Failing
**Check:** 
```bash
conda deactivate  # Already done?
echo $CONDA_DEFAULT_ENV  # Should be empty
which python3  # Should be /usr/bin/python3.14, NOT miniforge
```

### Script Dependencies Missing (pytest, black, etc.)
**Solution:** Install in project venv, not system
```bash
source ./venv/bin/activate
pip install pytest black mypy  # Now in venv, not system
```

## Quick Reference: Commands

```bash
# Safety check
/home/p3g4sus/.copilot/skills/sys-env/scripts/check-python-env.sh

# Auto-disable conda
/home/p3g4sus/.copilot/skills/sys-env/scripts/check-python-env.sh --auto-fix

# Create new isolated environment
python3.14 -m venv ./project-venv
source ./project-venv/bin/activate

# Switch between conda environments
conda activate ocv  # If working with computer vision
conda activate viz  # If working with visualization
conda deactivate    # Back to system Python

# Install CLI tools (isolated)
pipx install gns3-gui  # Isolated from system/miniforge

# List what's installed where
python3 -m pip list  # Current environment
/usr/bin/python3 -m pip list  # System Python only
~/miniforge3/bin/python -m pip list  # miniforge base
```

## Integration with dev-workflow

Document in your project's `.envrc` or `setup.md`:

```markdown
## Environment Setup for Development

This project requires isolated Python environment to avoid conflicts with system packages.

### First Time Setup
1. Verify conda is deactivated: `conda deactivate`
2. Create environment: `python3.14 -m venv ./venv`
3. Activate: `source ./venv/bin/activate`
4. Install: `pip install -r requirements.txt`

### CI/CD Note
CI pipeline automatically deactivates conda before installing system dependencies.
See `.github/workflows/*.yml` for details.
```

## Recommended Structure (via @architect)

```
my-project/
├── .envrc                  # direnv config (auto-activates venv)
├── .python-version         # pyenv version (optional)
├── venv/                   # Project environment (generate with venv or conda)
├── requirements.txt        # Python dependencies (installed in venv)
├── setup.md                # Setup instructions
├── scripts/
│   ├── check-env.sh        # Copy from sys-env/scripts/
│   └── setup-dev.sh        # Auto-setup script
└── README.md
```

## Files to Keep in Sync

- `references/python-environments.md` - Updated with lessons learned
- `/home/p3g4sus/.copilot/skills/sys-env/scripts/check-python-env.sh` - Validation script
- Project `setup.md` or `.envrc` - Environment setup instructions
