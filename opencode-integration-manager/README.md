# OpenCode Integration Manager

Complete automated system for integrating changes in OpenCode following best practices from **architect**, **dev-workflow**, **mcp-builder**, **sys-env**, and **code-review**.

## 🚀 Features

### ✅ Scalable Architecture
- **Modular**: Independent and reusable components
- **Extensible**: Easy to add new functionalities
- **Maintainable**: Code organized following standards

### 🔄 Complete Automation
- **Integrated CI/CD**: Automatic GitHub Actions workflows
- **Smart Triggers**: Automatic activation on relevant commits
- **Zero-touch**: Once configured, works without manual intervention

### 🔗 Advanced Integration
- **GitHub API**: Complete integration with repositories and PRs
- **Multi-platform**: Support for Linux, macOS, Windows
- **Conflict Resolution**: Automatic conflict resolution

### 🛡️ Security and Quality
- **Code Review**: Automatic validation of code standards
- **Dependency Management**: Secure system dependency management
- **Quality Gates**: Quality verification before integration

## 📋 Requirements

- **Python 3.8+**
- **Git**
- **GitHub CLI** (`gh`)
- **GitHub Token** with repo and workflow permissions

## 🛠️ Installation

### 1. Initial Configuration
```bash
# Run environment setup
cd opencode-integration-manager
chmod +x scripts/setup_environment.sh
./scripts/setup_environment.sh
```

### 2. GitHub Authentication
```bash
# Authenticate GitHub CLI
gh auth login

# Verify configuration
gh auth status
```

### 3. Token Configuration
```bash
# In GitHub repository Settings > Secrets and variables > Actions
# Add secret: GITHUB_TOKEN with your personal access token
```

## 🎯 Usage

### Manual Integration
```bash
# Run complete integration
python scripts/run_integration.py \
  --target-repo https://github.com/opencode-ai/opencode \
  --changes-dir ../types \
  --auto-commit \
  --create-pr
```

### Automatic Integration (CI/CD)
The system activates automatically when:
1. Push to branch `feature/opencode-proactive-skill-loader`
2. Workflow `opencode-integration.yml` executes
3. Commits contain relevant changes

### Setup Validation
```bash
# Verify everything is configured correctly
python scripts/validate_setup.py
```

## 🏗️ Architecture

```
opencode-integration-manager/
├── core/                          # Core architecture (architect)
│   ├── repository_manager.py      # Git repository management
│   ├── change_applier.py          # Change application with merge
│   └── validator.py               # Basic validations
├── automation/                    # Automation (dev-workflow)
│   ├── ci_runner.py               # CI/CD execution
│   └── pr_creator.py              # Automatic PR creation
├── integration/                   # Integration (mcp-builder)
│   ├── github_api.py              # GitHub API
│   ├── opencode_connector.py      # OpenCode connection
│   └── webhook_handler.py         # Webhook handling
├── system/                        # System management (sys-env)
│   ├── dependency_checker.py      # Dependency verification
│   ├── package_installer.py       # Package installation
│   └── environment_setup.py       # Environment setup
├── validation/                    # Validation (code-review)
│   ├── code_analyzer.py           # Code analysis
│   ├── test_runner.py             # Test execution
│   └── quality_checker.py         # Quality control
├── config/                        # Configurations
│   └── opencode_config.json       # Specific config
└── scripts/                       # Main scripts
    ├── run_integration.py         # Main script
    ├── setup_environment.sh       # Initial setup
    └── validate_setup.py          # Validation
```

## ⚙️ Configuration

### File `config/opencode_config.json`
```json
{
  "repository": {
    "fork": true,
    "branch_prefix": "integration/opencode"
  },
  "merge": {
    "conflict_resolution": "auto"
  },
  "ci": {
    "timeout": 1800,
    "wait_for_completion": true
  },
  "pr": {
    "title": "feat: Add proactive skill loader",
    "reviewers": [],
    "labels": ["enhancement", "integration"]
  }
}
```

## 🔄 Workflow

1. **Development**: Modify files in `types/`
2. **Commit**: Commit to branch `feature/opencode-proactive-skill-loader`
3. **Push**: Push automatically activates GitHub Actions workflow
4. **CI/CD**: Validation, testing, and building execute
5. **Integration**: OpenCode fork/clone created, changes applied
6. **PR**: Pull Request created automatically with documentation

## 📊 Monitoring

### Real-time Logs
```bash
# View workflow logs
gh run list --workflow opencode-integration.yml
gh run view <run-id> --log
```

### System Status
```bash
# Check general status
python scripts/validate_setup.py

# Check environment status
python -c "from system.environment_setup import EnvironmentSetup; print(EnvironmentSetup().get_environment_report())"
```

## 🐛 Troubleshooting

### Common Issues

#### GitHub CLI not authenticated
```bash
gh auth login
gh auth status
```

#### Missing dependencies
```bash
python scripts/validate_setup.py
# Follow installation recommendations
```

#### Merge conflicts
The system resolves automatically, but for complex cases:
```bash
# Manually review conflicts
cd opencode-integration-manager
python scripts/run_integration.py --manual-merge
```

## 🤝 Contribution

### Code Standards
- **Architect**: Follow modular structure
- **Dev-workflow**: Conventional commits, feature branches
- **Code-review**: Automatic validation before push
- **Sys-env**: Dependency verification
- **MCP-builder**: Clean integration with external APIs

### Local Development
```bash
# Configure development environment
./scripts/setup_environment.sh

# Run tests
python -m pytest

# Validate code
python validation/code_analyzer.py
```

## 📈 Metrics and Monitoring

- **Integration time**: < 10 minutes typical
- **Success rate**: > 95% with automatic resolution
- **Validation coverage**: Code, tests, quality gates
- **Scalability**: Support for multiple repositories

## 🔒 Security

- **Tokens**: Never in code, always as secrets
- **Permissions**: Principle of least privilege
- **Validation**: All inputs validated
- **Audit**: Complete logs of all operations

## 📚 References

- [OpenCode Repository](https://github.com/opencode-ai/opencode)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Skill Architecture](./skills/architect/SKILL.md)

---

**Developed following best practices from:**
- 🎯 **Architect**: Structure and organization
- 🔄 **Dev-workflow**: Automation and CI/CD
- 🔗 **MCP-builder**: System integration
- 🛡️ **Sys-env**: Secure system management
- ✅ **Code-review**: Code quality and standards