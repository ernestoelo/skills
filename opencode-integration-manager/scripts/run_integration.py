#!/usr/bin/env python3
"""
OpenCode Integration Manager
Sistema automatizado para integrar cambios en OpenCode siguiendo mejores prácticas
de architect, dev-workflow, mcp-builder, sys-env y code-review.
"""

import argparse
import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import subprocess
import tempfile
import shutil

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class OpenCodeIntegrationManager:
    """Gestor principal de integración con OpenCode."""

    def __init__(self, config_path: str = "config/opencode_config.json"):
        self.config = self.load_config(config_path)
        self.work_dir = Path(tempfile.mkdtemp(prefix="opencode-integration-"))
        logger.info(f"Working directory: {self.work_dir}")

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Carga configuración desde archivo JSON."""
        config_file = Path(__file__).parent / config_path
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")

        with open(config_file, "r") as f:
            return json.load(f)

    def run_integration(
        self,
        target_repo: str,
        changes_dir: str,
        auto_commit: bool = True,
        create_pr: bool = True,
    ) -> bool:
        """Ejecuta el flujo completo de integración."""
        try:
            logger.info("🚀 Starting OpenCode integration...")

            # 1. Configurar entorno
            if not self.setup_environment():
                return False

            # 2. Preparar repositorio
            if not self.prepare_repository(target_repo):
                return False

            # 3. Aplicar cambios
            if not self.apply_changes(changes_dir):
                return False

            # 4. Validar cambios
            if not self.validate_changes():
                return False

            # 5. Commit automático
            if auto_commit and not self.auto_commit():
                return False

            # 6. Ejecutar CI
            if not self.run_ci():
                return False

            # 7. Crear PR
            if create_pr and not self.create_pr():
                return False

            logger.info("✅ Integration completed successfully!")
            return True

        except Exception as e:
            logger.error(f"❌ Integration failed: {e}")
            return False

            readme_path = Path(changes_dir).parent / "OPENCODE_PR_README.md"
            if not readme_path.exists():
                logger.error("Missing file: OPENCODE_PR_README.md")
                return False

            logger.info("All required files found")

            # Simulate PR creation
            logger.info("Simulating PR creation...")
            logger.info("✅ Integration completed successfully!")
            return True

        except Exception as e:
            logger.error(f"❌ Integration failed: {e}")
            return False
        finally:
            # Limpiar directorio temporal
            shutil.rmtree(self.work_dir, ignore_errors=True)

    def setup_environment(self) -> bool:
        """Configura el entorno de desarrollo."""
        logger.info("🔧 Setting up environment...")

        # Importar módulos del sistema
        try:
            from system.dependency_checker import DependencyChecker
            from system.package_installer import PackageInstaller

            checker = DependencyChecker()
            installer = PackageInstaller()

            # Verificar dependencias críticas
            missing_deps = checker.check_critical_dependencies()
            if missing_deps:
                logger.info(f"📦 Installing missing dependencies: {missing_deps}")
                for dep in missing_deps:
                    if not installer.install_package(dep):
                        logger.error(f"Failed to install {dep}")
                        return False

            # Configurar Git
            if not self.configure_git():
                return False

            return True

        except ImportError as e:
            logger.error(f"Failed to import system modules: {e}")
            return False

    def configure_git(self) -> bool:
        """Configura Git con credenciales."""
        try:
            # Configurar usuario de Git
            git_user = self.config.get("git", {}).get("user", {})
            if git_user:
                subprocess.run(
                    [
                        "git",
                        "config",
                        "--global",
                        "user.name",
                        git_user.get("name", "OpenCode Integration"),
                    ],
                    check=True,
                )
                subprocess.run(
                    [
                        "git",
                        "config",
                        "--global",
                        "user.email",
                        git_user.get("email", "integration@opencode.ai"),
                    ],
                    check=True,
                )

            # Configurar token de GitHub
            token = os.getenv("GITHUB_TOKEN")
            if token:
                # Configurar credential helper para GitHub
                subprocess.run(
                    ["git", "config", "--global", "credential.helper", "store"],
                    check=True,
                )
                # Crear archivo de credenciales
                cred_file = Path.home() / ".git-credentials"
                with open(cred_file, "w") as f:
                    f.write(f"https://{token}:x-oauth-basic@github.com\n")
                cred_file.chmod(0o600)

            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to configure Git: {e}")
            return False

    def prepare_repository(self, target_repo: str) -> bool:
        """Prepara el repositorio de destino."""
        logger.info(f"📥 Preparing repository: {target_repo}")

        try:
            from core.repository_manager import RepositoryManager

            manager = RepositoryManager(self.work_dir)
            return manager.prepare_repository(
                target_repo,
                branch_prefix=self.config.get("branch", {}).get(
                    "prefix", "integration/opencode"
                ),
                fork=self.config.get("repository", {}).get("fork", True),
            )

        except ImportError:
            logger.error("Failed to import repository manager")
            return False

    def apply_changes(self, changes_dir: str) -> bool:
        """Aplica los cambios preparados."""
        logger.info(f"🔄 Applying changes from: {changes_dir}")

        try:
            from core.change_applier import ChangeApplier

            applier = ChangeApplier(self.work_dir)
            return applier.apply_changes(
                changes_dir,
                conflict_resolution=self.config.get("merge", {}).get(
                    "conflict_resolution", "auto"
                ),
            )

        except ImportError:
            logger.error("Failed to import change applier")
            return False

    def validate_changes(self) -> bool:
        """Valida los cambios aplicados."""
        logger.info("🔍 Validating changes...")

        try:
            from validation.code_analyzer import CodeAnalyzer
            from validation.test_runner import TestRunner
            from validation.quality_checker import QualityChecker

            analyzer = CodeAnalyzer(self.work_dir)
            test_runner = TestRunner(self.work_dir)
            quality_checker = QualityChecker(self.work_dir)

            # Ejecutar validaciones
            validations = [
                analyzer.analyze_code(),
                test_runner.run_tests(),
                quality_checker.check_quality(),
            ]

            return all(validations)

        except ImportError as e:
            logger.error(f"Failed to import validation modules: {e}")
            return False

    def auto_commit(self) -> bool:
        """Realiza commit automático de los cambios."""
        logger.info("💾 Creating automatic commit...")

        try:
            from automation.ci_runner import CIRunner

            ci_runner = CIRunner(self.work_dir)
            return ci_runner.auto_commit(
                message=self.config.get("commit", {}).get(
                    "message",
                    "feat: integrate proactive skill loader\n\nAutomated integration of proactive skill loading functionality",
                ),
                sign=self.config.get("commit", {}).get("sign", False),
            )

        except ImportError:
            logger.error("Failed to import CI runner")
            return False

    def run_ci(self) -> bool:
        """Ejecuta CI/CD y espera resultados."""
        logger.info("🔄 Running CI/CD...")

        try:
            from automation.ci_runner import CIRunner

            ci_runner = CIRunner(self.work_dir)
            return ci_runner.run_ci_pipeline(
                workflow=self.config.get("ci", {}).get("workflow", "ci"),
                timeout=self.config.get("ci", {}).get("timeout", 1800),
                wait_for_completion=self.config.get("ci", {}).get(
                    "wait_for_completion", True
                ),
            )

        except ImportError:
            logger.error("Failed to import CI runner")
            return False

    def create_pr(self) -> bool:
        """Crea Pull Request automáticamente."""
        logger.info("📝 Creating Pull Request...")

        try:
            from automation.pr_creator import PRCreator

            pr_creator = PRCreator(self.work_dir)
            return pr_creator.create_pr(
                title=self.config.get("pr", {}).get(
                    "title", "feat: Add proactive skill loader"
                ),
                body=self.generate_pr_body(),
                reviewers=self.config.get("pr", {}).get("reviewers", []),
                labels=self.config.get("pr", {}).get(
                    "labels", ["enhancement", "integration"]
                ),
                draft=self.config.get("pr", {}).get("draft", False),
            )

        except ImportError:
            logger.error("Failed to import PR creator")
            return False

    def generate_pr_body(self) -> str:
        """Genera el cuerpo del PR."""
        # Leer documentación preparada
        readme_path = Path(__file__).parent / "OPENCODE_PR_README.md"
        if readme_path.exists():
            with open(readme_path, "r") as f:
                return f.read()

        # Fallback básico
        return """# Proactive Skill Loader Integration

This PR adds automatic skill activation functionality to OpenCode.

## Overview
- Automatic skill activation based on conversation context
- Pattern matching for English and Spanish keywords
- Configurable through OpenCode settings

## Files Changed
- New: `src/types/proactive-loader.ts`
- Modified: `src/types/skill.ts`, `src/types/config.ts`, `src/types/session.ts`

## Testing
- Comprehensive pattern matching tests
- Edge case validation
- TypeScript compilation verified

## Configuration
Enable via OpenCode config:
```json
{
  "skills": {
    "auto_activate": true
  }
}
```"""


def main():
    parser = argparse.ArgumentParser(description="OpenCode Integration Manager")
    parser.add_argument(
        "--config",
        default="config/opencode_config.json",
        help="Configuration file path",
    )
    parser.add_argument("--target-repo", required=True, help="Target repository URL")
    parser.add_argument(
        "--changes-dir", required=True, help="Directory containing changes to apply"
    )
    parser.add_argument(
        "--auto-commit",
        action="store_true",
        default=True,
        help="Automatically commit changes",
    )
    parser.add_argument(
        "--create-pr",
        action="store_true",
        default=True,
        help="Create Pull Request automatically",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    manager = OpenCodeIntegrationManager(args.config)
    success = manager.run_integration(
        args.target_repo, args.changes_dir, args.auto_commit, args.create_pr
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
