#!/usr/bin/env python3
"""
Dependency Checker - Verificación de dependencias del sistema
Sigue las mejores prácticas de sys-env para gestión de dependencias.
"""

import os
import subprocess
import platform
import logging
from typing import List, Dict, Set

logger = logging.getLogger(__name__)


class DependencyChecker:
    """Verificador de dependencias del sistema con soporte multi-plataforma."""

    def __init__(self):
        self.system = platform.system().lower()
        self.package_managers = self._detect_package_managers()

    def check_critical_dependencies(self) -> List[str]:
        """
        Verifica dependencias críticas para la integración.

        Returns:
            List[str]: Lista de dependencias faltantes
        """
        missing_deps = []

        # Dependencias críticas
        critical_deps = [
            ("git", "Git version control"),
            ("python3", "Python 3 runtime"),
            ("gh", "GitHub CLI"),
        ]

        for dep, description in critical_deps:
            if not self._is_command_available(dep):
                missing_deps.append(f"{dep} ({description})")

        # Dependencias opcionales pero recomendadas
        optional_deps = [
            ("node", "Node.js for JavaScript/TypeScript"),
            ("npm", "NPM package manager"),
            ("curl", "HTTP client for downloads"),
        ]

        for dep, description in optional_deps:
            if not self._is_command_available(dep):
                logger.warning(f"Optional dependency missing: {dep} ({description})")

        return missing_deps

    def check_project_dependencies(self, repo_dir: str) -> Dict[str, bool]:
        """
        Verifica dependencias específicas del proyecto.

        Args:
            repo_dir: Directorio del repositorio

        Returns:
            Dict[str, bool]: Estado de cada dependencia
        """
        deps_status = {}

        # Verificar Python packages
        python_deps = ["pydantic", "requests", "pyyaml"]
        for dep in python_deps:
            deps_status[f"python:{dep}"] = self._check_python_package(dep)

        # Verificar Node.js packages si hay package.json
        package_json = os.path.join(repo_dir, "package.json")
        if os.path.exists(package_json):
            node_deps = ["typescript", "@types/node"]
            for dep in node_deps:
                deps_status[f"node:{dep}"] = self._check_node_package(dep)

        return deps_status

    def _is_command_available(self, command: str) -> bool:
        """Verifica si un comando está disponible en el sistema."""
        try:
            result = subprocess.run(
                [command, "--version"], capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0
        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            subprocess.TimeoutExpired,
        ):
            return False

    def _detect_package_managers(self) -> List[str]:
        """Detecta gestores de paquetes disponibles."""
        managers = []

        # Linux package managers
        if self.system == "linux":
            package_managers = [
                ("apt-get", "debian"),
                ("pacman", "arch"),
                ("dnf", "fedora"),
                ("yum", "rhel"),
                ("zypper", "opensuse"),
            ]

            for manager, distro in package_managers:
                if self._is_command_available(manager):
                    managers.append(manager)

        # macOS
        elif self.system == "darwin":
            if self._is_command_available("brew"):
                managers.append("brew")

        # Windows
        elif self.system == "windows":
            managers.append("choco")  # Placeholder

        return managers

    def _check_python_package(self, package: str) -> bool:
        """Verifica si un paquete Python está instalado."""
        try:
            result = subprocess.run(
                ["python3", "-c", f"import {package}"], capture_output=True, timeout=5
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False

    def _check_node_package(self, package: str) -> bool:
        """Verifica si un paquete Node.js está instalado."""
        try:
            result = subprocess.run(
                ["npm", "list", "-g", package],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0 and "empty" not in result.stdout
        except subprocess.TimeoutExpired:
            return False

    def get_system_info(self) -> Dict[str, str]:
        """Obtiene información del sistema."""
        return {
            "system": self.system,
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "package_managers": ", ".join(self.package_managers),
        }

    def recommend_installation_commands(
        self, missing_deps: List[str]
    ) -> Dict[str, str]:
        """
        Recomienda comandos de instalación para dependencias faltantes.

        Args:
            missing_deps: Lista de dependencias faltantes

        Returns:
            Dict[str, str]: Comandos recomendados por dependencia
        """
        recommendations = {}

        for dep in missing_deps:
            dep_name = dep.split()[0]  # Extraer nombre del comando

            if dep_name == "git":
                recommendations[dep] = self._get_git_install_command()
            elif dep_name == "python3":
                recommendations[dep] = self._get_python_install_command()
            elif dep_name == "gh":
                recommendations[dep] = self._get_github_cli_install_command()
            else:
                recommendations[dep] = (
                    f"Please install {dep_name} manually for your system"
                )

        return recommendations

    def _get_git_install_command(self) -> str:
        """Obtiene comando de instalación para Git."""
        if "apt-get" in self.package_managers:
            return "sudo apt-get update && sudo apt-get install -y git"
        elif "pacman" in self.package_managers:
            return "sudo pacman -S git"
        elif "dnf" in self.package_managers:
            return "sudo dnf install -y git"
        elif "brew" in self.package_managers:
            return "brew install git"
        else:
            return "Download from https://git-scm.com/downloads"

    def _get_python_install_command(self) -> str:
        """Obtiene comando de instalación para Python."""
        if "apt-get" in self.package_managers:
            return "sudo apt-get update && sudo apt-get install -y python3 python3-pip"
        elif "pacman" in self.package_managers:
            return "sudo pacman -S python python-pip"
        elif "dnf" in self.package_managers:
            return "sudo dnf install -y python3 python3-pip"
        elif "brew" in self.package_managers:
            return "brew install python"
        else:
            return "Download from https://python.org/downloads"

    def _get_github_cli_install_command(self) -> str:
        """Obtiene comando de instalación para GitHub CLI."""
        if "apt-get" in self.package_managers:
            return """curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh -y"""
        elif "pacman" in self.package_managers:
            return "sudo pacman -S github-cli"
        elif "dnf" in self.package_managers:
            return "sudo dnf install -y gh"
        elif "brew" in self.package_managers:
            return "brew install gh"
        else:
            return "Download from https://cli.github.com/"
