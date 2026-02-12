---
name: diagram
description: Generates diagrams using PlantUML, providing templates and examples for architecture, documentation, and visualization.
---

# Diagram Generator Skill

Generates diagrams using PlantUML for architecture, workflows, and documentation. Provides bundled templates and examples for quick setup and reproducibility.

## When to Use
- Creating system architecture diagrams.
- Documenting workflows like Gitflow.
- Generating visual overviews for projects.
- Ensuring consistency in team diagrams.

## Uso
Sigue este flujo unificado para la generación y automatización de diagramas:

1. **Instala PlantUML**: En Arch Linux, ejecuta `sudo pacman -S plantuml` (consulta compatibilidades y mejores prácticas en @sys-env).
2. **Elige plantilla**: Usa los recursos en assets/ (examples/, imgs/, templates/) como referencia.
3. **Edita archivos .puml**: Crea o edita archivos con sintaxis PlantUML (`@startuml ... @enduml`).
4. **Genera diagramas automáticamente**: Ejecuta el script `scripts/generate_diagrams.sh [directorio]` para convertir todos los .puml a PNG usando PlantUML (ver scripts/README.md). Esto facilita la integración y reproducibilidad, alineado con @architect y @dev-workflow.
5. **Integra y versiona**: Añade los PNG generados a la documentación/repositorios y versiona los .puml en Git.

## Anatomía
Estructura de la skill:
- SKILL.md (metadatos e instrucciones)
- scripts/ (automatización y utilidades)
- references/ (documentación adicional)
- assets/ (recursos: examples/, imgs/, templates/)
- README.md

## Buenas prácticas
- Usa los assets para mantener consistencia visual.
- Versiona los archivos .puml en Git (como código fuente).
- Automatiza la generación de diagramas con scripts/ para reproducibilidad.
- Integra con @dev-workflow para flujos de trabajo robustos.
- Consulta @sys-env antes de instalar dependencias o modificar el entorno.

## Recursos
- Assets incluidos: ver assets/ para plantillas y ejemplos.
- scripts/: utilidades para automatización.
- Documentación de PlantUML.
- Inspiración: @anthropic-examples (theme-showcase.pdf para estilos de diagramas).
- Referencias cruzadas: @architect para estructura y automatización, @dev-workflow para integración, @sys-env para entorno seguro.