#!/usr/bin/env python3
"""
Script para automatizar la generación de la estructura estándar de una nueva skill según architect, anthropic-examples y el repositorio anthropics/skills.git.
"""
import os
import sys

TEMPLATE_SKILL_MD = '''---
name: {name}
description: {description}
---

# {title}

Instrucciones principales para la skill {name}.

## Ejemplo de uso
- Añade aquí ejemplos de uso, flujos y buenas prácticas.

## Referencias
- Usa scripts/, references/ y assets/ para organizar recursos.
'''

def scaffold_skill(skill_name, description="Descripción de la skill.", title=None):
    if not title:
        title = skill_name.capitalize()
    base = os.path.abspath(skill_name)
    os.makedirs(os.path.join(base, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(base, "references"), exist_ok=True)
    os.makedirs(os.path.join(base, "assets"), exist_ok=True)
    with open(os.path.join(base, "SKILL.md"), "w") as f:
        f.write(TEMPLATE_SKILL_MD.format(name=skill_name, description=description, title=title))
    with open(os.path.join(base, "README.md"), "w") as f:
        f.write(f"# {title}\n\nEstructura y recursos siguiendo el estándar architect y anthropic-examples. Usa scripts/, references/ y assets/ para organizar ejemplos y utilidades.\n")
    print(f"Skill '{skill_name}' creada con estructura estándar.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python skill_scaffold.py <nombre_skill> [descripcion]")
        sys.exit(1)
    name = sys.argv[1]
    desc = sys.argv[2] if len(sys.argv) > 2 else "Descripción de la skill."
    scaffold_skill(name, desc)
