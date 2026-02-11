#!/usr/bin/env python3
"""
Package Installer - Instalación automática de paquetes
Sigue las mejores prácticas de sys-env para instalación segura.
"""

import os
import subprocess
import platform
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


class PackageInstaller:
    """Instalador de paquetes con soporte multi-plataforma y verificación de seguridad."""

    def __init__(self):
        self.system = platform.system().lower()
        self.package_manager = self._detect_package_manager()

    def install_package(self, package: str, assume_yes: bool = False) -> bool:
        """
        Instala un paquete de forma segura.

        Args:
            package: Nombre del paquete a instalar
            assume_yes: Asumir 'yes' para todas las preguntas

        Returns:
            bool: True si la instalación fue exitosa
        """
        try:
            logger.info(f"Installing package: {package}")

            # Verificar si ya está instalado
            if self._is_package_installed(package):
                logger.info(f"Package {package} already installed")
                return True

            # Obtener comando de instalación
            install_cmd = self._get_install_command(package, assume_yes)
            if not install_cmd:
                logger.error(f"No installation command available for {package}")
                return False

            # Ejecutar instalación
            logger.info(f"Running: {' '.join(install_cmd)}")
            result = subprocess.run(
                install_cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutos timeout
            )

            if result.returncode == 0:
                logger.info(f"✅ Package {package} installed successfully")

                # Verificar instalación
                if self._is_package_installed(package):
                    return True
                else:
                    logger.error(f"Package {package} installation verification failed")
                    return False
            else:
                logger.error(f"Package installation failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error(f"Package installation timed out for {package}")
            return False
        except Exception as e:
            logger.error(f"Package installation error: {e}")
            return False

    def _detect_package_manager(self) -> Optional[str]:
        """Detecta el gestor de paquetes disponible."""
        managers = []

        if self.system == "linux":
            # Verificar gestores de paquetes comunes
            if self._is_command_available("apt-get"):
                managers.append("apt")
            if self._is_command_available("pacman"):
                managers.append("pacman")
            if self._is_command_available("dnf"):
                managers.append("dnf")
            if self._is_command_available("yum"):
                managers.append("yum")
            if self._is_command_available("zypper"):
                managers.append("zypper")

        elif self.system == "darwin":
            if self._is_command_available("brew"):
                managers.append("brew")

        # Retornar el primer gestor disponible
        return managers[0] if managers else None

    def _is_command_available(self, command: str) -> bool:
        """Verifica si un comando está disponible."""
        try:
            subprocess.run(
                [command, "--version"], capture_output=True, check=True, timeout=5
            )
            return True
        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            subprocess.TimeoutExpired,
        ):
            return False

    def _is_package_installed(self, package: str) -> bool:
        """Verifica si un paquete está instalado."""
        try:
            if self.package_manager == "apt":
                result = subprocess.run(
                    ["dpkg", "-l", package], capture_output=True, text=True
                )
                return result.returncode == 0 and "ii" in result.stdout

            elif self.package_manager == "pacman":
                result = subprocess.run(["pacman", "-Q", package], capture_output=True)
                return result.returncode == 0

            elif self.package_manager == "dnf":
                result = subprocess.run(["rpm", "-q", package], capture_output=True)
                return result.returncode == 0

            elif self.package_manager == "brew":
                result = subprocess.run(["brew", "list", package], capture_output=True)
                return result.returncode == 0

            else:
                # Método genérico: verificar comando
                return self._is_command_available(package)

        except Exception:
            return False

    def _get_install_command(
        self, package: str, assume_yes: bool
    ) -> Optional[List[str]]:
        """Obtiene el comando de instalación para el gestor de paquetes."""
        yes_flag = "-y" if assume_yes else ""

        if self.package_manager == "apt":
            return ["sudo", "apt-get", "update"] + (
                ["&&", "sudo", "apt-get", "install", yes_flag, package]
                if yes_flag
                else ["&&", "sudo", "apt-get", "install", package]
            )

        elif self.package_manager == "pacman":
            return [
                "sudo",
                "pacman",
                "-S",
                "--noconfirm" if assume_yes else "--confirm",
                package,
            ]

        elif self.package_manager == "dnf":
            return ["sudo", "dnf", "install", "-y" if assume_yes else "", package]

        elif self.package_manager == "yum":
            return ["sudo", "yum", "install", "-y" if assume_yes else "", package]

        elif self.package_manager == "zypper":
            return ["sudo", "zypper", "install", "-y" if assume_yes else "", package]

        elif self.package_manager == "brew":
            return ["brew", "install", package]

        else:
            logger.warning(f"No package manager detected for system: {self.system}")
            return None

    def install_python_package(self, package: str, use_venv: bool = True) -> bool:
        """
        Instala un paquete Python de forma segura.

        Args:
            package: Nombre del paquete Python
            use_venv: Usar entorno virtual si está disponible

        Returns:
            bool: True si la instalación fue exitosa
        """
        try:
            logger.info(f"Installing Python package: {package}")

            # Verificar si ya está instalado
            if self._is_python_package_installed(package):
                logger.info(f"Python package {package} already installed")
                return True

            # Determinar comando de instalación
            if use_venv and self._is_venv_active():
                pip_cmd = ["pip", "install", package]
            else:
                pip_cmd = ["python3", "-m", "pip", "install", package]

            # Ejecutar instalación
            result = subprocess.run(
                pip_cmd, capture_output=True, text=True, timeout=120
            )

            if result.returncode == 0:
                logger.info(f"✅ Python package {package} installed successfully")
                return self._is_python_package_installed(package)
            else:
                logger.error(f"Python package installation failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error(f"Python package installation timed out for {package}")
            return False
        except Exception as e:
            logger.error(f"Python package installation error: {e}")
            return False

    def _is_python_package_installed(self, package: str) -> bool:
        """Verifica si un paquete Python está instalado."""
        try:
            result = subprocess.run(
                ["python3", "-c", f"import {package}"], capture_output=True, timeout=5
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False

    def _is_venv_active(self) -> bool:
        """Verifica si hay un entorno virtual activo."""
        return os.environ.get("VIRTUAL_ENV") is not None

    def get_system_info(self) -> dict:
        """Obtiene información del sistema para debugging."""
        return {
            "system": self.system,
            "package_manager": self.package_manager,
            "venv_active": self._is_venv_active(),
            "python_version": platform.python_version(),
        }
