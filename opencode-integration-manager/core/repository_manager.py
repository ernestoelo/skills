#!/usr/bin/env python3
"""
Repository Manager - Gestión de repositorios Git
Sigue las mejores prácticas de dev-workflow para manejo de repositorios.
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class RepositoryManager:
    """Gestor de repositorios Git con automatización completa."""

    def __init__(self, work_dir: Path):
        self.work_dir = work_dir
        self.repo_dir = work_dir / "target_repo"

    def prepare_repository(
        self,
        target_repo: str,
        branch_prefix: str = "integration/opencode",
        fork: bool = True,
    ) -> bool:
        """
        Prepara el repositorio de destino siguiendo dev-workflow best practices.

        Args:
            target_repo: URL del repositorio objetivo
            branch_prefix: Prefijo para la rama de integración
            fork: Si debe hacer fork en lugar de trabajar directamente

        Returns:
            bool: True si la preparación fue exitosa
        """
        try:
            logger.info(f"Preparing repository: {target_repo}")

            # 1. Crear directorio de trabajo
            self.repo_dir.mkdir(parents=True, exist_ok=True)

            # 2. Clonar o hacer fork
            if fork:
                success = self._fork_and_clone(target_repo)
            else:
                success = self._clone_repository(target_repo)

            if not success:
                return False

            # 3. Crear rama de integración
            branch_name = self._create_integration_branch(branch_prefix)
            if not branch_name:
                return False

            # 4. Configurar upstream si es necesario
            self._setup_upstream(target_repo)

            logger.info(f"Repository prepared successfully on branch: {branch_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to prepare repository: {e}")
            return False

    def _fork_and_clone(self, target_repo: str) -> bool:
        """Hace fork del repositorio y clona el fork."""
        try:
            # Usar GitHub CLI para hacer fork
            logger.info("Creating fork...")
            result = subprocess.run(
                ["gh", "repo", "fork", target_repo, "--clone=false"],
                capture_output=True,
                text=True,
                cwd=self.work_dir,
            )

            if result.returncode != 0:
                logger.warning(
                    f"Fork may have failed or already exists: {result.stderr}"
                )
                # Continuar asumiendo que el fork ya existe

            # Obtener URL del fork
            result = subprocess.run(
                ["gh", "repo", "view", "--json", "url", "-q", ".url"],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                fork_url = result.stdout.strip()
            else:
                # Fallback: asumir que el fork está en el usuario actual
                fork_url = self._get_fork_url(target_repo)

            # Clonar el fork
            logger.info(f"Cloning fork: {fork_url}")
            result = subprocess.run(
                ["git", "clone", fork_url, "target_repo"],
                cwd=self.work_dir,
                capture_output=True,
                text=True,
            )

            return result.returncode == 0

        except Exception as e:
            logger.error(f"Failed to fork and clone: {e}")
            return False

    def _clone_repository(self, target_repo: str) -> bool:
        """Clona el repositorio directamente."""
        try:
            logger.info(f"Cloning repository: {target_repo}")
            result = subprocess.run(
                ["git", "clone", target_repo, "target_repo"],
                cwd=self.work_dir,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Failed to clone repository: {e}")
            return False

    def _get_fork_url(self, target_repo: str) -> str:
        """Genera URL del fork basado en la URL original."""
        # Extraer owner del repo
        if "github.com/" in target_repo:
            parts = target_repo.split("github.com/")[1].split("/")
            if len(parts) >= 2:
                owner = parts[0]
                repo = parts[1].replace(".git", "")

                # Obtener usuario actual de GitHub
                result = subprocess.run(
                    ["gh", "auth", "status", "--show-token"],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    # Extraer username del token (esto es un aproximado)
                    # En la práctica, usaríamos la API de GitHub
                    pass

        # Fallback: asumir que el usuario es el mismo que está corriendo
        return target_repo.replace(
            "github.com/",
            "github.com/" + os.getenv("GITHUB_USER", "current-user") + "/",
        )

    def _create_integration_branch(self, branch_prefix: str) -> Optional[str]:
        """Crea una rama de integración con timestamp."""
        try:
            os.chdir(self.repo_dir)

            # Generar nombre de rama único
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            branch_name = f"{branch_prefix}-{timestamp}"

            # Crear y cambiar a la rama
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)

            logger.info(f"Created integration branch: {branch_name}")
            return branch_name

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create integration branch: {e}")
            return None

    def _setup_upstream(self, target_repo: str):
        """Configura el upstream si es necesario."""
        try:
            # Añadir upstream si no existe
            result = subprocess.run(
                ["git", "remote", "get-url", "upstream"], capture_output=True, text=True
            )

            if result.returncode != 0:
                # Upstream no existe, añadirlo
                subprocess.run(
                    ["git", "remote", "add", "upstream", target_repo], check=True
                )
                logger.info("Added upstream remote")

        except subprocess.CalledProcessError:
            # Upstream ya existe o no se puede añadir
            pass

    def get_current_branch(self) -> Optional[str]:
        """Obtiene el nombre de la rama actual."""
        try:
            os.chdir(self.repo_dir)
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def push_changes(self, force: bool = False) -> bool:
        """Hace push de los cambios."""
        try:
            os.chdir(self.repo_dir)

            args = ["git", "push"]
            if force:
                args.extend(["--force-with-lease"])
            else:
                args.extend(["-u", "origin", "HEAD"])

            result = subprocess.run(args, capture_output=True, text=True)
            return result.returncode == 0

        except Exception as e:
            logger.error(f"Failed to push changes: {e}")
            return False

    def get_repo_info(self) -> dict:
        """Obtiene información del repositorio."""
        try:
            os.chdir(self.repo_dir)

            # Obtener información básica
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True,
                text=True,
                check=True,
            )
            origin_url = result.stdout.strip()

            branch = self.get_current_branch()

            return {
                "origin_url": origin_url,
                "branch": branch,
                "has_upstream": self._has_upstream(),
                "is_clean": self._is_working_tree_clean(),
            }

        except Exception as e:
            logger.error(f"Failed to get repo info: {e}")
            return {}

    def _has_upstream(self) -> bool:
        """Verifica si existe upstream."""
        try:
            subprocess.run(
                ["git", "remote", "get-url", "upstream"],
                capture_output=True,
                check=True,
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def _is_working_tree_clean(self) -> bool:
        """Verifica si el working tree está limpio."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True,
            )
            return len(result.stdout.strip()) == 0
        except subprocess.CalledProcessError:
            return False
