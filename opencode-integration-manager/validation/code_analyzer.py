#!/usr/bin/env python3
"""
Code Analyzer - Análisis estático de código
Sigue las mejores prácticas de code-review para validación de código.
"""

import subprocess
import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


class CodeAnalyzer:
    """Analizador estático de código con múltiples lenguajes soportados."""

    def __init__(self, repo_dir: Path):
        self.repo_dir = repo_dir

    def analyze_code(self) -> bool:
        """
        Ejecuta análisis estático de código.

        Returns:
            bool: True si el análisis pasa
        """
        try:
            logger.info("🔍 Analyzing code quality...")

            issues_found = []

            # Detectar lenguajes en el repositorio
            languages = self._detect_languages()

            # Ejecutar análisis por lenguaje
            if "typescript" in languages or "javascript" in languages:
                issues_found.extend(self._analyze_typescript())

            if "python" in languages:
                issues_found.extend(self._analyze_python())

            # Reportar resultados
            if issues_found:
                logger.warning(f"Found {len(issues_found)} code quality issues")
                for issue in issues_found[:10]:  # Mostrar primeros 10
                    logger.warning(f"  {issue}")
                if len(issues_found) > 10:
                    logger.warning(f"  ... and {len(issues_found) - 10} more issues")
                return False
            else:
                logger.info("✅ Code analysis passed")
                return True

        except Exception as e:
            logger.error(f"Code analysis failed: {e}")
            return False

    def _detect_languages(self) -> List[str]:
        """Detecta lenguajes de programación en el repositorio."""
        languages = []

        # Buscar archivos por extensión
        extensions = {
            "typescript": [".ts", ".tsx"],
            "javascript": [".js", ".jsx"],
            "python": [".py"],
            "rust": [".rs"],
            "go": [".go"],
        }

        for lang, exts in extensions.items():
            for ext in exts:
                if list(self.repo_dir.glob(f"**/*{ext}")):
                    languages.append(lang)
                    break

        return languages

    def _analyze_typescript(self) -> List[str]:
        """Analiza código TypeScript/JavaScript."""
        issues = []

        try:
            # Verificar TypeScript compiler
            result = subprocess.run(
                ["npx", "tsc", "--noEmit", "--skipLibCheck"],
                cwd=self.repo_dir,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                # Parsear errores de TypeScript
                for line in result.stdout.split("\n"):
                    if line.strip() and not line.startswith(" "):
                        issues.append(f"TypeScript: {line}")

            # Verificar ESLint si está configurado
            if (self.repo_dir / ".eslintrc.json").exists() or (
                self.repo_dir / ".eslintrc.js"
            ).exists():
                result = subprocess.run(
                    ["npx", "eslint", ".", "--ext", ".ts,.tsx,.js,.jsx"],
                    cwd=self.repo_dir,
                    capture_output=True,
                    text=True,
                )

                if result.returncode != 0:
                    issues.extend(
                        [
                            f"ESLint: {line}"
                            for line in result.stdout.split("\n")
                            if line.strip()
                        ]
                    )

        except FileNotFoundError:
            logger.warning(
                "TypeScript tools not available, skipping TypeScript analysis"
            )
        except Exception as e:
            issues.append(f"TypeScript analysis error: {e}")

        return issues

    def _analyze_python(self) -> List[str]:
        """Analiza código Python."""
        issues = []

        try:
            # Verificar sintaxis Python
            python_files = list(self.repo_dir.glob("**/*.py"))
            for py_file in python_files:
                result = subprocess.run(
                    ["python3", "-m", "py_compile", str(py_file)],
                    capture_output=True,
                    text=True,
                )

                if result.returncode != 0:
                    issues.append(
                        f"Python syntax error in {py_file.name}: {result.stderr}"
                    )

            # Verificar Ruff si está disponible
            try:
                result = subprocess.run(
                    ["ruff", "check", "."],
                    cwd=self.repo_dir,
                    capture_output=True,
                    text=True,
                )

                if result.returncode != 0:
                    issues.extend(
                        [
                            f"Ruff: {line}"
                            for line in result.stdout.split("\n")
                            if line.strip()
                        ]
                    )

            except FileNotFoundError:
                logger.debug("Ruff not available, skipping")

            # Verificar MyPy si está disponible
            try:
                result = subprocess.run(
                    ["mypy", ".", "--ignore-missing-imports"],
                    cwd=self.repo_dir,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode != 0:
                    issues.extend(
                        [
                            f"MyPy: {line}"
                            for line in result.stdout.split("\n")
                            if line.strip()
                        ]
                    )

            except (FileNotFoundError, subprocess.TimeoutExpired):
                logger.debug("MyPy not available or timed out, skipping")

        except Exception as e:
            issues.append(f"Python analysis error: {e}")

        return issues
