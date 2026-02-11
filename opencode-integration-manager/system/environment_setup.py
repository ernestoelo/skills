#!/usr/bin/env python3
"""
Environment Setup - Configuración de entorno de desarrollo
Sigue las mejores prácticas de sys-env para setup seguro.
"""

import subprocess
import logging
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)


class EnvironmentSetup:
    """Configurador de entorno de desarrollo con verificación de seguridad."""

    def __init__(self):
        self.home_dir = Path.home()

    def setup_development_environment(self) -> bool:
        """
        Configura el entorno completo de desarrollo.

        Returns:
            bool: True si la configuración fue exitosa
        """
        try:
            logger.info("🔧 Setting up development environment...")

            setup_steps = [
                self._setup_git_config,
                self._setup_github_cli,
                self._setup_python_environment,
                self._setup_nodejs_environment,
                self._setup_git_hooks,
                self._verify_setup,
            ]

            for step in setup_steps:
                if not step():
                    logger.error(f"Setup step failed: {step.__name__}")
                    return False

            logger.info("✅ Development environment setup completed")
            return True

        except Exception as e:
            logger.error(f"Environment setup failed: {e}")
            return False

    def _setup_git_config(self) -> bool:
        """Configura Git con información básica."""
        try:
            logger.info("Setting up Git configuration...")

            # Configurar usuario si no está configurado
            result = subprocess.run(
                ["git", "config", "--global", "user.name"],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0 or not result.stdout.strip():
                logger.warning("Git user.name not configured")
                # No fallar, solo advertir

            # Configurar email si no está configurado
            result = subprocess.run(
                ["git", "config", "--global", "user.email"],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0 or not result.stdout.strip():
                logger.warning("Git user.email not configured")
                # No fallar, solo advertir

            # Configurar configuraciones útiles
            configs = [
                ("init.defaultBranch", "main"),
                ("core.autocrlf", "input"),
                ("pull.rebase", "false"),
                ("credential.helper", "store"),
            ]

            for key, value in configs:
                subprocess.run(["git", "config", "--global", key, value], check=True)

            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Git configuration failed: {e}")
            return False

    def _setup_github_cli(self) -> bool:
        """Configura GitHub CLI."""
        try:
            logger.info("Setting up GitHub CLI...")

            # Verificar si está autenticado
            result = subprocess.run(
                ["gh", "auth", "status"], capture_output=True, text=True
            )

            if result.returncode != 0:
                logger.warning("GitHub CLI not authenticated")
                logger.info("Run 'gh auth login' to authenticate")
                # No fallar, solo advertir
            else:
                logger.info("GitHub CLI is authenticated")

            # Configurar preferencias
            try:
                subprocess.run(["gh", "config", "set", "editor", "code"], check=False)
                subprocess.run(
                    ["gh", "config", "set", "git_protocol", "https"], check=False
                )
            except subprocess.CalledProcessError:
                pass  # No crítico

            return True

        except FileNotFoundError:
            logger.warning("GitHub CLI not installed")
            return False

    def _setup_python_environment(self) -> bool:
        """Configura el entorno Python."""
        try:
            logger.info("Setting up Python environment...")

            # Verificar Python
            result = subprocess.run(
                ["python3", "--version"], capture_output=True, text=True, check=True
            )

            python_version = result.stdout.strip()
            logger.info(f"Python version: {python_version}")

            # Instalar/actualizar pip
            subprocess.run(
                ["python3", "-m", "pip", "install", "--user", "--upgrade", "pip"],
                check=True,
            )

            # Instalar herramientas de desarrollo Python
            dev_tools = [
                "setuptools",
                "wheel",
                "virtualenv",
                "pydantic",
                "requests",
                "pyyaml",
            ]

            for tool in dev_tools:
                try:
                    subprocess.run(
                        ["python3", "-m", "pip", "install", "--user", tool],
                        check=True,
                        timeout=60,
                    )
                except subprocess.CalledProcessError:
                    logger.warning(f"Failed to install {tool}")
                    continue

            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Python environment setup failed: {e}")
            return False

    def _setup_nodejs_environment(self) -> bool:
        """Configura el entorno Node.js (opcional)."""
        try:
            logger.info("Setting up Node.js environment...")

            # Verificar si Node.js está disponible
            try:
                result = subprocess.run(
                    ["node", "--version"], capture_output=True, text=True, check=True
                )

                node_version = result.stdout.strip()
                logger.info(f"Node.js version: {node_version}")

                # Verificar npm
                result = subprocess.run(
                    ["npm", "--version"], capture_output=True, text=True, check=True
                )

                npm_version = result.stdout.strip()
                logger.info(f"NPM version: {npm_version}")

                # Instalar TypeScript globalmente si no está
                try:
                    subprocess.run(["npm", "list", "-g", "typescript"], check=True)
                except subprocess.CalledProcessError:
                    logger.info("Installing TypeScript globally...")
                    subprocess.run(["npm", "install", "-g", "typescript"], check=True)

                return True

            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.info("Node.js not available - skipping Node.js setup")
                return True  # No fallar si no está disponible

        except Exception as e:
            logger.error(f"Node.js environment setup failed: {e}")
            return False

    def _setup_git_hooks(self) -> bool:
        """Configura hooks de Git para automatización."""
        try:
            logger.info("Setting up Git hooks...")

            # Solo configurar si estamos en un repositorio git
            if not (self.home_dir / ".git").exists():
                logger.info("Not in a git repository - skipping hook setup")
                return True

            hooks_dir = self.home_dir / ".git" / "hooks"

            # Crear hook post-commit para integración automática
            post_commit_hook = hooks_dir / "post-commit"

            hook_content = """#!/bin/bash
#
# Post-commit hook for OpenCode integration automation
# Automatically triggers integration workflows on relevant commits
#

BRANCH=$(git branch --show-current)

# Trigger integration for OpenCode branches
if [[ $BRANCH == *"opencode"* ]] || [[ $BRANCH == *"integration"* ]]; then
    echo "🔄 Detected OpenCode integration commit"

    # Check if integration manager is available
    if [ -d "opencode-integration-manager" ]; then
        echo "🚀 Running integration validation..."
        cd opencode-integration-manager
        python scripts/validate_setup.py
        cd ..
    fi

    # Trigger GitHub Actions if available
    if command -v gh >/dev/null 2>&1; then
        if [ -f ".github/workflows/opencode-integration.yml" ]; then
            echo "🔄 Triggering integration workflow..."
            gh workflow run opencode-integration.yml
        fi
    fi
fi
"""

            if not post_commit_hook.exists():
                post_commit_hook.write_text(hook_content)
                post_commit_hook.chmod(0o755)
                logger.info("✅ Post-commit hook configured")
            else:
                logger.info("Post-commit hook already exists")

            return True

        except Exception as e:
            logger.error(f"Git hooks setup failed: {e}")
            return False

    def _verify_setup(self) -> bool:
        """Verifica que el setup fue exitoso."""
        try:
            logger.info("Verifying environment setup...")

            # Verificar herramientas críticas
            critical_tools = ["git", "python3"]

            for tool in critical_tools:
                try:
                    subprocess.run([tool, "--version"], capture_output=True, check=True)
                except subprocess.CalledProcessError:
                    logger.error(f"Critical tool {tool} not working properly")
                    return False

            # Verificar configuraciones
            checks = [
                (
                    ["git", "config", "--global", "user.name"],
                    "Git user.name configured",
                ),
                (["python3", "-c", "import pydantic"], "Python pydantic available"),
            ]

            for cmd, description in checks:
                try:
                    subprocess.run(cmd, capture_output=True, check=True)
                    logger.info(f"✅ {description}")
                except subprocess.CalledProcessError:
                    logger.warning(f"⚠️ {description} - may need manual configuration")

            logger.info("✅ Environment verification completed")
            return True

        except Exception as e:
            logger.error(f"Environment verification failed: {e}")
            return False

    def get_environment_report(self) -> Dict[str, any]:
        """Genera un reporte del estado del entorno."""
        report = {
            "git_configured": False,
            "github_cli_auth": False,
            "python_ready": False,
            "nodejs_available": False,
            "hooks_configured": False,
        }

        # Verificar Git
        try:
            subprocess.run(
                ["git", "config", "--global", "user.name"],
                capture_output=True,
                check=True,
            )
            report["git_configured"] = True
        except subprocess.CalledProcessError:
            pass

        # Verificar GitHub CLI
        try:
            result = subprocess.run(["gh", "auth", "status"], capture_output=True)
            report["github_cli_auth"] = result.returncode == 0
        except FileNotFoundError:
            pass

        # Verificar Python
        try:
            subprocess.run(
                ["python3", "-c", "import sys; print(sys.version)"],
                capture_output=True,
                check=True,
            )
            report["python_ready"] = True
        except subprocess.CalledProcessError:
            pass

        # Verificar Node.js
        try:
            subprocess.run(["node", "--version"], capture_output=True, check=True)
            report["nodejs_available"] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Verificar hooks
        hook_path = self.home_dir / ".git" / "hooks" / "post-commit"
        report["hooks_configured"] = (
            hook_path.exists() and hook_path.stat().st_mode & 0o111
        )

        return report
