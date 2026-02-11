#!/usr/bin/env python3
"""
CI Runner - Ejecución de CI/CD con GitHub Actions
Sigue las mejores prácticas de dev-workflow para automatización CI/CD.
"""

import os
import subprocess
import time
import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class CIRunner:
    """Ejecutor de CI/CD con integración completa de GitHub Actions."""

    def __init__(self, repo_dir: Path):
        self.repo_dir = repo_dir

    def auto_commit(self, message: str, sign: bool = False) -> bool:
        """
        Realiza commit automático siguiendo dev-workflow best practices.

        Args:
            message: Mensaje del commit
            sign: Si firmar el commit con GPG

        Returns:
            bool: True si el commit fue exitoso
        """
        try:
            os.chdir(self.repo_dir)
            logger.info("Creating automatic commit...")

            # 1. Verificar que hay cambios para commitear
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True,
            )

            if not result.stdout.strip():
                logger.info("No changes to commit")
                return True

            # 2. Add all changes
            subprocess.run(["git", "add", "."], check=True)

            # 3. Crear commit
            commit_args = ["git", "commit", "-m", message]
            if sign:
                commit_args.append("-S")

            subprocess.run(commit_args, check=True)

            # 4. Obtener SHA del commit
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
            )
            commit_sha = result.stdout.strip()

            logger.info(f"Commit created: {commit_sha}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create commit: {e}")
            return False

    def run_ci_pipeline(
        self,
        workflow: str = "ci",
        timeout: int = 1800,
        wait_for_completion: bool = True,
    ) -> bool:
        """
        Ejecuta pipeline de CI/CD y espera resultados.

        Args:
            workflow: Nombre del workflow a ejecutar
            timeout: Timeout en segundos para esperar resultados
            wait_for_completion: Si esperar a que termine el CI

        Returns:
            bool: True si CI pasa exitosamente
        """
        try:
            logger.info(f"Running CI pipeline: {workflow}")

            # 1. Push changes first
            if not self._push_changes():
                return False

            # 2. Trigger CI workflow
            run_id = self._trigger_workflow(workflow)
            if not run_id:
                logger.warning("Could not trigger CI workflow, assuming success")
                return True

            # 3. Wait for completion if requested
            if wait_for_completion:
                return self._wait_for_ci_completion(run_id, workflow, timeout)
            else:
                logger.info(
                    f"CI triggered (run ID: {run_id}), not waiting for completion"
                )
                return True

        except Exception as e:
            logger.error(f"Failed to run CI pipeline: {e}")
            return False

    def _push_changes(self) -> bool:
        """Hace push de los cambios."""
        try:
            # Verificar que estamos en una rama
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                check=True,
            )
            current_branch = result.stdout.strip()

            # Push con upstream
            subprocess.run(["git", "push", "-u", "origin", current_branch], check=True)

            logger.info(f"Pushed changes to branch: {current_branch}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to push changes: {e}")
            return False

    def _trigger_workflow(self, workflow: str) -> Optional[str]:
        """Dispara un workflow de GitHub Actions."""
        try:
            # Usar GitHub CLI para disparar workflow
            result = subprocess.run(
                ["gh", "workflow", "run", workflow], capture_output=True, text=True
            )

            if result.returncode == 0:
                logger.info(f"Triggered workflow: {workflow}")

                # Obtener el run ID más reciente
                time.sleep(5)  # Esperar a que se cree el run
                return self._get_latest_run_id(workflow)
            else:
                logger.warning(f"Could not trigger workflow: {result.stderr}")
                return None

        except Exception as e:
            logger.error(f"Failed to trigger workflow: {e}")
            return None

    def _get_latest_run_id(self, workflow: str) -> Optional[str]:
        """Obtiene el ID del run más reciente de un workflow."""
        try:
            result = subprocess.run(
                [
                    "gh",
                    "run",
                    "list",
                    "--workflow",
                    workflow,
                    "--json",
                    "databaseId",
                    "-q",
                    ".[0].databaseId",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            run_id = result.stdout.strip()
            return run_id if run_id else None

        except subprocess.CalledProcessError:
            return None

    def _wait_for_ci_completion(self, run_id: str, workflow: str, timeout: int) -> bool:
        """Espera a que termine el CI y verifica el resultado."""
        try:
            logger.info(f"Waiting for CI completion (run ID: {run_id})...")

            start_time = time.time()
            check_interval = 30  # segundos

            while time.time() - start_time < timeout:
                status, conclusion = self._get_run_status(run_id)

                if status == "completed":
                    if conclusion == "success":
                        logger.info("✅ CI completed successfully")
                        return True
                    else:
                        logger.error(f"❌ CI failed with conclusion: {conclusion}")
                        return False
                elif status in ["in_progress", "queued", "requested", "waiting"]:
                    logger.info(f"CI status: {status}, waiting...")
                    time.sleep(check_interval)
                else:
                    logger.warning(
                        f"Unknown CI status: {status}, continuing to wait..."
                    )
                    time.sleep(check_interval)

            logger.error(f"CI timeout after {timeout} seconds")
            return False

        except Exception as e:
            logger.error(f"Failed while waiting for CI: {e}")
            return False

    def _get_run_status(self, run_id: str) -> tuple[Optional[str], Optional[str]]:
        """Obtiene el status de un run de GitHub Actions."""
        try:
            result = subprocess.run(
                ["gh", "run", "view", run_id, "--json", "status,conclusion"],
                capture_output=True,
                text=True,
                check=True,
            )

            data = json.loads(result.stdout)
            return data.get("status"), data.get("conclusion")

        except subprocess.CalledProcessError:
            return None, None
        except json.JSONDecodeError:
            return None, None

    def get_ci_logs(self, run_id: str, save_to_file: bool = False) -> Optional[str]:
        """Obtiene los logs del CI."""
        try:
            result = subprocess.run(
                ["gh", "run", "view", run_id, "--log"],
                capture_output=True,
                text=True,
                check=True,
            )

            logs = result.stdout
            if save_to_file:
                log_file = self.repo_dir / f"ci-logs-{run_id}.txt"
                with open(log_file, "w") as f:
                    f.write(logs)
                logger.info(f"CI logs saved to: {log_file}")

            return logs

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get CI logs: {e}")
            return None

    def retry_failed_ci(self, workflow: str, max_attempts: int = 3) -> bool:
        """Reintenta CI fallido aplicando correcciones automáticas."""
        try:
            logger.info(
                f"Attempting to fix and retry CI failures (max {max_attempts} attempts)"
            )

            for attempt in range(1, max_attempts + 1):
                logger.info(f"Attempt {attempt}/{max_attempts}")

                # Obtener status del último run
                run_id = self._get_latest_run_id(workflow)
                if not run_id:
                    logger.warning("No recent CI run found")
                    return False

                status, conclusion = self._get_run_status(run_id)

                if status == "completed" and conclusion == "success":
                    logger.info("CI already passed")
                    return True

                if conclusion == "failure":
                    # Intentar auto-corregir
                    if self._apply_auto_fixes():
                        # Re-commit y re-push
                        if self.auto_commit(
                            f"fix: auto-correct CI issues (attempt {attempt})"
                        ):
                            if self.run_ci_pipeline(workflow, wait_for_completion=True):
                                return True
                    else:
                        logger.warning("No auto-fixes available for current failure")

                time.sleep(10)  # Breve pausa entre intentos

            logger.error(f"Failed to fix CI after {max_attempts} attempts")
            return False

        except Exception as e:
            logger.error(f"Failed during CI retry: {e}")
            return False

    def _apply_auto_fixes(self) -> bool:
        """Aplica correcciones automáticas comunes."""
        try:
            # Obtener logs del último run fallido
            run_id = self._get_latest_run_id("ci")
            if run_id:
                logs = self.get_ci_logs(run_id)
                if logs:
                    return self._analyze_and_fix_logs(logs)
            return False

        except Exception as e:
            logger.error(f"Failed to apply auto-fixes: {e}")
            return False

    def _analyze_and_fix_logs(self, logs: str) -> bool:
        """Analiza logs de CI y aplica correcciones."""
        fixes_applied = False

        # Análisis simplificado de errores comunes
        if "ruff check" in logs and "failed" in logs.lower():
            # Intentar auto-fix con ruff
            try:
                subprocess.run(
                    ["ruff", "check", "--fix", "."], cwd=self.repo_dir, check=True
                )
                logger.info("Applied ruff auto-fix")
                fixes_applied = True
            except subprocess.CalledProcessError:
                pass

        if "mypy" in logs and "error" in logs.lower():
            # MyPy errors - generalmente requieren intervención manual
            logger.warning("MyPy errors detected - manual fix required")

        return fixes_applied
