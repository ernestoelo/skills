#!/bin/bash
#
# sync-to-opencode.sh
# Sincroniza automáticamente todas las skills de ~/.copilot/skills/ 
# a ~/.config/opencode/skills/ usando symlinks
#

set -e

COPILOT_SKILLS="$HOME/.copilot/skills"
OPENCODE_SKILLS="$HOME/.config/opencode/skills"

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         SINCRONIZACIÓN DE SKILLS: Copilot → OpenCode        ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Crear directorio de OpenCode si no existe
if [ ! -d "$OPENCODE_SKILLS" ]; then
    echo -e "${YELLOW}📁 Creando directorio: $OPENCODE_SKILLS${NC}"
    mkdir -p "$OPENCODE_SKILLS"
fi

echo -e "${BLUE}🔍 Buscando skills en: $COPILOT_SKILLS${NC}"
echo ""

# Contador de skills procesadas
new_count=0
existing_count=0
total_count=0

# Iterar sobre todos los directorios que contienen SKILL.md
for skill_path in "$COPILOT_SKILLS"/*/SKILL.md; do
    # Verificar que el archivo existe (evita error si no hay matches)
    [ -e "$skill_path" ] || continue
    
    # Obtener el nombre del directorio (skill)
    skill_dir=$(dirname "$skill_path")
    skill_name=$(basename "$skill_dir")
    
    # Verificar que no es .git u otro directorio especial
    if [[ "$skill_name" == .* ]]; then
        continue
    fi
    
    total_count=$((total_count + 1))
    symlink_path="$OPENCODE_SKILLS/$skill_name"
    
    # Verificar si el symlink ya existe
    if [ -L "$symlink_path" ]; then
        # Verificar que apunta al lugar correcto
        current_target=$(readlink "$symlink_path")
        if [ "$current_target" = "$skill_dir" ]; then
            echo -e "  ✅ ${GREEN}$skill_name${NC} → ya sincronizada"
            existing_count=$((existing_count + 1))
        else
            echo -e "  ⚠️  ${YELLOW}$skill_name${NC} → apunta a ubicación incorrecta, recreando..."
            rm "$symlink_path"
            ln -s "$skill_dir" "$symlink_path"
            new_count=$((new_count + 1))
        fi
    elif [ -e "$symlink_path" ]; then
        # Existe pero no es un symlink (archivo o directorio regular)
        echo -e "  ❌ ${YELLOW}$skill_name${NC} → existe como archivo/directorio regular (no symlink)"
        echo -e "     Por favor, elimina manualmente: $symlink_path"
    else
        # No existe, crear symlink
        echo -e "  🆕 ${GREEN}$skill_name${NC} → creando symlink..."
        ln -s "$skill_dir" "$symlink_path"
        new_count=$((new_count + 1))
    fi
done

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                        RESUMEN                               ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo -e "  Total de skills encontradas: ${GREEN}$total_count${NC}"
echo -e "  Skills ya sincronizadas:     ${GREEN}$existing_count${NC}"
echo -e "  Skills nuevas sincronizadas: ${GREEN}$new_count${NC}"
echo ""

if [ $new_count -gt 0 ]; then
    echo -e "${GREEN}✨ ¡Sincronización completada! Se agregaron $new_count nueva(s) skill(s).${NC}"
else
    echo -e "${GREEN}✅ Todas las skills ya estaban sincronizadas.${NC}"
fi

echo ""
echo -e "${BLUE}📍 Ubicación de skills en OpenCode: $OPENCODE_SKILLS${NC}"
echo ""
