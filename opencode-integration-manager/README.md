opencode-integration-manager/
├── core/                          # Arquitectura central (architect)
│   ├── repository_manager.py      # Gestión de repositorios Git
│   ├── change_applier.py          # Aplicación de cambios con merge inteligente
│   └── validator.py               # Validaciones (linting, tests)
├── automation/                    # Automatización (dev-workflow)
│   ├── ci_runner.py               # Ejecución de CI/CD con GitHub Actions
│   ├── pr_creator.py              # Creación automática de PRs
│   └── workflow_trigger.py        # Triggers de GitHub Actions
├── integration/                   # Integración de sistemas (mcp-builder)
│   ├── github_api.py              # API de GitHub para PRs y repos
│   ├── opencode_connector.py      # Conexión especializada con OpenCode
│   └── webhook_handler.py         # Manejo de webhooks y eventos
├── system/                        # Gestión de sistema (sys-env)
│   ├── dependency_checker.py      # Verificación de dependencias
│   ├── package_installer.py       # Instalación automática de paquetes
│   └── environment_setup.py       # Configuración de entorno de desarrollo
├── validation/                    # Validación de código (code-review)
│   ├── code_analyzer.py           # Análisis estático de código
│   ├── test_runner.py             # Ejecución de tests
│   └── quality_checker.py         # Verificación de calidad de código
├── config/                        # Configuraciones
│   ├── opencode_config.json       # Config específica de OpenCode
│   ├── integration_rules.json     # Reglas de integración automática
│   └── approval_matrix.json       # Matriz de aprobaciones requeridas
└── scripts/
    ├── run_integration.py         # Script principal de integración
    ├── setup_environment.sh       # Setup inicial del entorno
    └── validate_setup.py          # Validación de configuración