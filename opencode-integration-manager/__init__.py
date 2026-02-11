#!/usr/bin/env python3
"""
OpenCode Integration Manager
Sistema automatizado para integrar cambios en OpenCode siguiendo las mejores prácticas
de architect, dev-workflow, mcp-builder, sys-env y code-review.
"""

__version__ = "1.0.0"
__author__ = "OpenCode Integration Team"
__description__ = "Automated OpenCode integration system"

# Import main components for easy access
from .scripts.run_integration import OpenCodeIntegrationManager

__all__ = ["OpenCodeIntegrationManager", "__version__", "__author__", "__description__"]
