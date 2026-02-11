#!/usr/bin/env python3
"""
Quality Checker - Verificación de calidad de código
Sigue las mejores prácticas de code-review para control de calidad.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class QualityChecker:
    """Verificador de calidad de código con métricas y estándares."""

    def __init__(self, repo_dir: Path):
        self.repo_dir = repo_dir

    def check_quality(self) -> bool:
        """
        Ejecuta verificaciones de calidad de código.

        Returns:
            bool: True si todas las verificaciones pasan
        """
        try:
            logger.info("🔍 Checking code quality standards...")

            quality_checks = []

            # Verificar estándares básicos
            quality_checks.append(self._check_file_sizes())
            quality_checks.append(self._check_line_lengths())
            quality_checks.append(self._check_file_permissions())
            quality_checks.append(self._check_required_files())

            # Verificar estándares específicos por lenguaje
            if self._has_python_files():
                quality_checks.append(self._check_python_standards())

            if self._has_typescript_files():
                quality_checks.append(self._check_typescript_standards())

            # Reportar resultados
            all_passed = all(quality_checks)

            if all_passed:
                logger.info("✅ All quality checks passed")
            else:
                logger.warning("⚠️ Some quality checks failed")

            return all_passed

        except Exception as e:
            logger.error(f"Quality check failed: {e}")
            return False

    def _check_file_sizes(self) -> bool:
        """Verifica que los archivos no excedan límites de tamaño."""
        max_size_mb = 10  # 10MB límite
        large_files = []

        for file_path in self.repo_dir.rglob("*"):
            if file_path.is_file() and not file_path.is_symlink():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                if size_mb > max_size_mb:
                    large_files.append(f"{file_path.name}: {size_mb:.1f}MB")

        if large_files:
            logger.warning(f"Large files found (>{max_size_mb}MB):")
            for file_info in large_files:
                logger.warning(f"  {file_info}")
            return False

        return True

    def _check_line_lengths(self) -> bool:
        """Verifica longitud máxima de líneas."""
        max_length = 120
        long_lines = []

        # Extensiones a verificar
        text_extensions = {".py", ".ts", ".js", ".md", ".txt", ".json", ".yaml", ".yml"}

        for file_path in self.repo_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in text_extensions:
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line_num, line in enumerate(f, 1):
                            if len(line.rstrip()) > max_length:
                                long_lines.append(
                                    f"{file_path.name}:{line_num} ({len(line.rstrip())} chars)"
                                )
                                if len(long_lines) >= 10:  # Limitar reporte
                                    break
                except Exception:
                    continue

        if long_lines:
            logger.warning(f"Lines exceeding {max_length} characters:")
            for line_info in long_lines:
                logger.warning(f"  {line_info}")
            return False

        return True

    def _check_file_permissions(self) -> bool:
        """Verifica permisos de archivos."""
        issues = []

        for file_path in self.repo_dir.rglob("*"):
            if file_path.is_file():
                # Verificar archivos ejecutables sin extensión
                if file_path.suffix == "" and os.access(file_path, os.X_OK):
                    # Solo permitir si está en directorios estándar
                    if not any(
                        part in str(file_path) for part in ["scripts", "bin", ".git"]
                    ):
                        issues.append(
                            f"Executable file without extension: {file_path.name}"
                        )

        if issues:
            logger.warning("File permission issues:")
            for issue in issues:
                logger.warning(f"  {issue}")
            return False

        return True

    def _check_required_files(self) -> bool:
        """Verifica archivos requeridos para el proyecto."""
        required_files = ["README.md", ".gitignore"]

        missing_files = []
        for req_file in required_files:
            if not (self.repo_dir / req_file).exists():
                missing_files.append(req_file)

        if missing_files:
            logger.warning("Missing required files:")
            for missing in missing_files:
                logger.warning(f"  {missing}")
            return False

        return True

    def _has_python_files(self) -> bool:
        """Verifica si hay archivos Python."""
        return bool(list(self.repo_dir.glob("**/*.py")))

    def _has_typescript_files(self) -> bool:
        """Verifica si hay archivos TypeScript."""
        return bool(
            list(self.repo_dir.glob("**/*.ts")) or list(self.repo_dir.glob("**/*.tsx"))
        )

    def _check_python_standards(self) -> bool:
        """Verifica estándares específicos de Python."""
        issues = []

        # Verificar imports absolutos vs relativos
        for py_file in self.repo_dir.glob("**/*.py"):
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                    # Contar imports relativos (problemáticos)
                    relative_imports = content.count("from .") + content.count(
                        "from .."
                    )

                    if relative_imports > 5:  # Tolerancia baja
                        issues.append(
                            f"Too many relative imports in {py_file.name} ({relative_imports})"
                        )

            except Exception:
                continue

        # Verificar archivos __init__.py
        python_dirs = set()
        for py_file in self.repo_dir.glob("**/*.py"):
            python_dirs.add(py_file.parent)

        for py_dir in python_dirs:
            if py_dir != self.repo_dir and not (py_dir / "__init__.py").exists():
                issues.append(
                    f"Missing __init__.py in {py_dir.relative_to(self.repo_dir)}"
                )

        if issues:
            logger.warning("Python standards issues:")
            for issue in issues:
                logger.warning(f"  {issue}")
            return False

        return True

    def _check_typescript_standards(self) -> bool:
        """Verifica estándares específicos de TypeScript."""
        issues = []

        # Verificar archivos de configuración
        config_files = ["tsconfig.json", "package.json"]
        for config_file in config_files:
            if not (self.repo_dir / config_file).exists():
                issues.append(f"Missing {config_file}")

        # Verificar uso de any type (básico)
        for ts_file in self.repo_dir.glob("**/*.ts"):
            try:
                with open(ts_file, "r", encoding="utf-8") as f:
                    content = f.read()

                    # Contar usos de 'any' (deberían ser mínimos)
                    any_count = content.count(": any") + content.count("<any>")
                    if any_count > 3:  # Tolerancia baja
                        issues.append(
                            f"Too many 'any' types in {ts_file.name} ({any_count})"
                        )

            except Exception:
                continue

        if issues:
            logger.warning("TypeScript standards issues:")
            for issue in issues:
                logger.warning(f"  {issue}")
            return False

        return True

    def generate_quality_report(self) -> Dict[str, Any]:
        """Genera un reporte detallado de calidad."""
        return {
            "file_sizes": self._check_file_sizes(),
            "line_lengths": self._check_line_lengths(),
            "file_permissions": self._check_file_permissions(),
            "required_files": self._check_required_files(),
            "python_standards": self._check_python_standards()
            if self._has_python_files()
            else True,
            "typescript_standards": self._check_typescript_standards()
            if self._has_typescript_files()
            else True,
        }
