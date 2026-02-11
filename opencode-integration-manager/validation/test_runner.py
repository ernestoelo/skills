#!/usr/bin/env python3
"""
Test Runner - Ejecución de tests automatizada
Sigue las mejores prácticas de dev-workflow para testing.
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


class TestRunner:
    """Ejecutor de tests con soporte para múltiples frameworks."""

    def __init__(self, repo_dir: Path):
        self.repo_dir = repo_dir

    def run_tests(self) -> bool:
        """
        Ejecuta tests del proyecto.

        Returns:
            bool: True si todos los tests pasan
        """
        try:
            logger.info("🧪 Running tests...")

            test_results = []

            # Detectar y ejecutar tests por lenguaje/framework
            if self._has_python_tests():
                test_results.append(self._run_python_tests())

            if self._has_javascript_tests():
                test_results.append(self._run_javascript_tests())

            if self._has_typescript_tests():
                test_results.append(self._run_typescript_tests())

            # Si no se encontraron tests específicos, intentar genérico
            if not test_results:
                logger.info(
                    "No specific test frameworks detected, attempting generic test run"
                )
                test_results.append(self._run_generic_tests())

            # Verificar resultados
            all_passed = all(test_results)

            if all_passed:
                logger.info("✅ All tests passed")
            else:
                logger.error("❌ Some tests failed")

            return all_passed

        except Exception as e:
            logger.error(f"Test execution failed: {e}")
            return False

    def _has_python_tests(self) -> bool:
        """Verifica si hay tests de Python."""
        test_files = [
            "test_*.py",
            "tests/**/*.py",
            "*_test.py",
            "pytest.ini",
            "setup.cfg",
            "pyproject.toml",
        ]

        for pattern in test_files:
            if list(self.repo_dir.glob(pattern)):
                return True

        return False

    def _has_javascript_tests(self) -> bool:
        """Verifica si hay tests de JavaScript."""
        test_files = [
            "**/*.test.js",
            "**/*.spec.js",
            "**/__tests__/**/*.js",
            "jest.config.js",
            "package.json",
        ]

        for pattern in test_files:
            if list(self.repo_dir.glob(pattern)):
                return True

        return False

    def _has_typescript_tests(self) -> bool:
        """Verifica si hay tests de TypeScript."""
        test_files = [
            "**/*.test.ts",
            "**/*.spec.ts",
            "**/__tests__/**/*.ts",
            "jest.config.ts",
            "tsconfig.json",
        ]

        for pattern in test_files:
            if list(self.repo_dir.glob(pattern)):
                return True

        return False

    def _run_python_tests(self) -> bool:
        """Ejecuta tests de Python."""
        try:
            # Intentar pytest primero
            if self._command_available("pytest"):
                logger.info("Running pytest...")
                result = subprocess.run(
                    ["pytest", "-v", "--tb=short"],
                    cwd=self.repo_dir,
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                return result.returncode == 0

            # Intentar unittest
            elif self._command_available("python3"):
                logger.info("Running Python unittest...")
                result = subprocess.run(
                    ["python3", "-m", "unittest", "discover", "-v"],
                    cwd=self.repo_dir,
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                return result.returncode == 0

            else:
                logger.warning("No Python test runner available")
                return True  # No fallar si no hay tests configurados

        except subprocess.TimeoutExpired:
            logger.error("Python tests timed out")
            return False
        except Exception as e:
            logger.error(f"Python test execution failed: {e}")
            return False

    def _run_javascript_tests(self) -> bool:
        """Ejecuta tests de JavaScript."""
        try:
            # Verificar si hay package.json con scripts de test
            package_json = self.repo_dir / "package.json"
            if package_json.exists():
                with open(package_json, "r") as f:
                    import json

                    package_data = json.load(f)
                    if "scripts" in package_data and "test" in package_data["scripts"]:
                        logger.info("Running npm test...")
                        result = subprocess.run(
                            ["npm", "test"],
                            cwd=self.repo_dir,
                            capture_output=True,
                            text=True,
                            timeout=300,
                        )
                        return result.returncode == 0

            # Intentar Jest directamente
            if self._command_available("jest"):
                logger.info("Running Jest...")
                result = subprocess.run(
                    ["npx", "jest", "--passWithNoTests"],
                    cwd=self.repo_dir,
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                return result.returncode == 0

            logger.info("No JavaScript test runner configured")
            return True

        except subprocess.TimeoutExpired:
            logger.error("JavaScript tests timed out")
            return False
        except Exception as e:
            logger.error(f"JavaScript test execution failed: {e}")
            return False

    def _run_typescript_tests(self) -> bool:
        """Ejecuta tests de TypeScript."""
        try:
            # TypeScript tests generalmente usan Jest o similar
            return self._run_javascript_tests()

        except Exception as e:
            logger.error(f"TypeScript test execution failed: {e}")
            return False

    def _run_generic_tests(self) -> bool:
        """Ejecuta tests genéricos si no se detecta framework específico."""
        try:
            # Buscar y ejecutar archivos de test directamente
            test_files = list(self.repo_dir.glob("test_*.py")) + list(
                self.repo_dir.glob("*_test.py")
            )

            if test_files:
                logger.info(f"Running {len(test_files)} generic test files...")
                for test_file in test_files:
                    result = subprocess.run(
                        ["python3", str(test_file)],
                        cwd=self.repo_dir,
                        capture_output=True,
                        text=True,
                        timeout=60,
                    )
                    if result.returncode != 0:
                        logger.error(f"Test {test_file.name} failed: {result.stderr}")
                        return False

                return True
            else:
                logger.info("No test files found")
                return True

        except Exception as e:
            logger.error(f"Generic test execution failed: {e}")
            return False

    def _command_available(self, command: str) -> bool:
        """Verifica si un comando está disponible."""
        try:
            subprocess.run([command, "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
