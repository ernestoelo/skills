#!/usr/bin/env python3
"""
PR Creator - Creación automática de Pull Requests
Sigue las mejores prácticas de dev-workflow y mcp-builder para PRs.
"""

import os
import subprocess
import json
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)


class PRCreator:
    """Creador automático de Pull Requests con integración GitHub completa."""

    def __init__(self, repo_dir: Path):
        self.repo_dir = repo_dir

    def create_pr(
        self,
        title: str,
        body: str,
        reviewers: List[str] = None,
        labels: List[str] = None,
        draft: bool = False,
    ) -> bool:
        """
        Crea un Pull Request automáticamente.

        Args:
            title: Título del PR
            body: Cuerpo/description del PR
            reviewers: Lista de reviewers requeridos
            labels: Labels para el PR
            draft: Si crear como draft

        Returns:
            bool: True si el PR se creó exitosamente
        """
        try:
            logger.info(f"Creating Pull Request: {title}")

            os.chdir(self.repo_dir)

            # 1. Verificar que estamos en una rama feature
            current_branch = self._get_current_branch()
            if not current_branch or not current_branch.startswith(
                ("feature/", "integration/", "fix/", "feat/")
            ):
                logger.warning(f"Not on a feature branch: {current_branch}")
                # Continuar de todos modos

            # 2. Verificar que hay commits para el PR
            if not self._has_commits_ahead():
                logger.error("No commits ahead of main branch")
                return False

            # 3. Crear PR usando GitHub CLI
            success = self._create_github_pr(
                title=title,
                body=body,
                reviewers=reviewers or [],
                labels=labels or [],
                draft=draft,
            )

            if success:
                logger.info("✅ Pull Request created successfully")
                return True
            else:
                logger.error("❌ Failed to create Pull Request")
                return False

        except Exception as e:
            logger.error(f"Failed to create PR: {e}")
            return False

    def _create_github_pr(
        self,
        title: str,
        body: str,
        reviewers: List[str],
        labels: List[str],
        draft: bool,
    ) -> bool:
        """Crea PR usando GitHub CLI."""
        try:
            # Construir comando
            cmd = ["gh", "pr", "create"]

            # Título
            cmd.extend(["--title", title])

            # Cuerpo
            cmd.extend(["--body", body])

            # Reviewers
            if reviewers:
                for reviewer in reviewers:
                    cmd.extend(["--reviewer", reviewer])

            # Labels
            if labels:
                cmd.extend(["--label", ",".join(labels)])

            # Draft
            if draft:
                cmd.append("--draft")

            # Ejecutar comando
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.repo_dir
            )

            if result.returncode == 0:
                pr_url = result.stdout.strip()
                logger.info(f"PR created: {pr_url}")
                return True
            else:
                logger.error(f"GitHub CLI error: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Failed to execute GitHub CLI: {e}")
            return False

    def _get_current_branch(self) -> Optional[str]:
        """Obtiene el nombre de la rama actual."""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                check=True,
                cwd=self.repo_dir,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def _has_commits_ahead(self) -> bool:
        """Verifica que hay commits por delante de main."""
        try:
            # Verificar si hay commits ahead de origin/main
            result = subprocess.run(
                ["git", "rev-list", "--count", "HEAD..origin/main"],
                capture_output=True,
                text=True,
                cwd=self.repo_dir,
            )

            if result.returncode == 0:
                count = int(result.stdout.strip())
                return count > 0
            else:
                # Si no hay origin/main, verificar con main
                result = subprocess.run(
                    ["git", "rev-list", "--count", "HEAD..main"],
                    capture_output=True,
                    text=True,
                    cwd=self.repo_dir,
                )
                if result.returncode == 0:
                    count = int(result.stdout.strip())
                    return count > 0

            return False

        except subprocess.CalledProcessError:
            return False

    def update_pr(
        self,
        pr_number: Optional[int] = None,
        title: Optional[str] = None,
        body: Optional[str] = None,
        reviewers: Optional[List[str]] = None,
    ) -> bool:
        """Actualiza un PR existente."""
        try:
            # Obtener número del PR si no se proporciona
            if not pr_number:
                pr_number = self._get_current_pr_number()
                if not pr_number:
                    logger.error("Could not determine PR number")
                    return False

            logger.info(f"Updating PR #{pr_number}")

            # Actualizar título si se proporciona
            if title:
                subprocess.run(
                    ["gh", "pr", "edit", str(pr_number), "--title", title],
                    check=True,
                    cwd=self.repo_dir,
                )

            # Actualizar cuerpo si se proporciona
            if body:
                subprocess.run(
                    ["gh", "pr", "edit", str(pr_number), "--body", body],
                    check=True,
                    cwd=self.repo_dir,
                )

            # Actualizar reviewers si se proporcionan
            if reviewers:
                reviewer_str = ",".join(reviewers)
                subprocess.run(
                    [
                        "gh",
                        "pr",
                        "edit",
                        str(pr_number),
                        "--add-reviewer",
                        reviewer_str,
                    ],
                    check=True,
                    cwd=self.repo_dir,
                )

            logger.info(f"PR #{pr_number} updated successfully")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to update PR: {e}")
            return False

    def _get_current_pr_number(self) -> Optional[int]:
        """Obtiene el número del PR actual de la rama."""
        try:
            result = subprocess.run(
                ["gh", "pr", "view", "--json", "number", "-q", ".number"],
                capture_output=True,
                text=True,
                cwd=self.repo_dir,
            )

            if result.returncode == 0:
                return int(result.stdout.strip())

        except (subprocess.CalledProcessError, ValueError):
            pass

        return None

    def wait_for_reviews(
        self,
        pr_number: Optional[int] = None,
        required_approvals: int = 1,
        timeout: int = 3600,
    ) -> bool:
        """
        Espera a que el PR tenga las aprobaciones requeridas.

        Args:
            pr_number: Número del PR (opcional)
            required_approvals: Número de aprobaciones requeridas
            timeout: Timeout en segundos

        Returns:
            bool: True si obtuvo las aprobaciones requeridas
        """
        import time

        try:
            if not pr_number:
                pr_number = self._get_current_pr_number()
                if not pr_number:
                    return False

            logger.info(
                f"Waiting for {required_approvals} approvals on PR #{pr_number}"
            )

            start_time = time.time()
            check_interval = 60  # segundos

            while time.time() - start_time < timeout:
                approvals = self._get_pr_approvals(pr_number)

                if approvals >= required_approvals:
                    logger.info(
                        f"✅ PR has {approvals} approvals (required: {required_approvals})"
                    )
                    return True

                logger.info(
                    f"PR has {approvals}/{required_approvals} approvals, waiting..."
                )
                time.sleep(check_interval)

            logger.warning(f"Timeout waiting for PR approvals after {timeout} seconds")
            return False

        except Exception as e:
            logger.error(f"Failed while waiting for reviews: {e}")
            return False

    def _get_pr_approvals(self, pr_number: int) -> int:
        """Obtiene el número de aprobaciones del PR."""
        try:
            result = subprocess.run(
                ["gh", "pr", "view", str(pr_number), "--json", "reviews"],
                capture_output=True,
                text=True,
                check=True,
                cwd=self.repo_dir,
            )

            data = json.loads(result.stdout)
            reviews = data.get("reviews", [])

            # Contar approved reviews
            approved_count = sum(
                1 for review in reviews if review.get("state") == "APPROVED"
            )

            return approved_count

        except (subprocess.CalledProcessError, json.JSONDecodeError):
            return 0

    def merge_pr(
        self, pr_number: Optional[int] = None, merge_method: str = "squash"
    ) -> bool:
        """
        Hace merge del PR cuando esté aprobado.

        Args:
            pr_number: Número del PR
            merge_method: Método de merge ('merge', 'squash', 'rebase')

        Returns:
            bool: True si el merge fue exitoso
        """
        try:
            if not pr_number:
                pr_number = self._get_current_pr_number()
                if not pr_number:
                    logger.error("Could not determine PR number")
                    return False

            logger.info(f"Merging PR #{pr_number} with method: {merge_method}")

            # Verificar que el PR esté aprobado
            approvals = self._get_pr_approvals(pr_number)
            if approvals == 0:
                logger.warning("PR has no approvals - manual merge required")
                return False

            # Merge usando GitHub CLI
            cmd = [
                "gh",
                "pr",
                "merge",
                str(pr_number),
                "--merge"
                if merge_method == "merge"
                else "--squash"
                if merge_method == "squash"
                else "--rebase",
            ]

            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.repo_dir
            )

            if result.returncode == 0:
                logger.info(f"✅ PR #{pr_number} merged successfully")
                return True
            else:
                logger.error(f"Failed to merge PR: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Failed to merge PR: {e}")
            return False

    def get_pr_status(self, pr_number: Optional[int] = None) -> Dict[str, Any]:
        """Obtiene el status completo del PR."""
        try:
            if not pr_number:
                pr_number = self._get_current_pr_number()

            if not pr_number:
                return {"error": "No PR found for current branch"}

            result = subprocess.run(
                [
                    "gh",
                    "pr",
                    "view",
                    str(pr_number),
                    "--json",
                    "title,state,reviews,mergeStateStatus",
                ],
                capture_output=True,
                text=True,
                check=True,
                cwd=self.repo_dir,
            )

            data = json.loads(result.stdout)

            return {
                "number": pr_number,
                "title": data.get("title"),
                "state": data.get("state"),
                "approvals": self._get_pr_approvals(pr_number),
                "mergeable": data.get("mergeStateStatus") == "CLEAN",
            }

        except Exception as e:
            return {"error": str(e)}
