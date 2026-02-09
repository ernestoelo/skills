# Skills Repository

Este repositorio contiene skills reutilizables para **GitHub Copilot** y **OpenCode**.

## 📚 Skills Disponibles

| Skill | Descripción |
|-------|-------------|
| **architect** | Generador experto de estructuras para VS Code Skills & Agents |
| **dev-workflow** | Estándares oficiales de desarrollo y workflows (Git, AI/ML) |
| **mcp-builder** | Guía completa para crear servidores MCP (Model Context Protocol) |
| **pdf** | Procesamiento completo de PDFs (leer, crear, modificar, OCR) |
| **web-scraper** | Extracción y limpieza de contenido web a Markdown |

## 🔧 Instalación

### Para GitHub Copilot

Las skills ya están en la ubicación correcta: `~/.copilot/skills/`

### Para OpenCode

Este repositorio se sincroniza con OpenCode usando **enlaces simbólicos (symlinks)**.

#### Sincronización Automática

Ejecuta el script de sincronización para crear/actualizar todos los symlinks:

```bash
cd ~/.copilot/skills
./sync-to-opencode.sh
```

Este script:
- ✅ Detecta automáticamente todas las skills en el repositorio
- ✅ Crea symlinks en `~/.config/opencode/skills/`
- ✅ Verifica que los symlinks existentes apunten correctamente
- ✅ Informa qué skills son nuevas y cuáles ya estaban sincronizadas

#### Sincronización Manual (skill individual)

Si prefieres agregar una skill específica manualmente:

```bash
ln -s ~/.copilot/skills/nombre-skill ~/.config/opencode/skills/nombre-skill
```

## 🔄 Workflow de Desarrollo

### Agregar una Nueva Skill

1. **Crear la estructura de la skill:**
   ```bash
   cd ~/.copilot/skills
   mkdir nueva-skill
   cd nueva-skill
   ```

2. **Crear SKILL.md con frontmatter válido:**
   ```markdown
   ---
   name: nueva-skill
   description: Descripción breve de la skill (1-1024 caracteres)
   ---
   
   # Contenido de la skill...
   ```

3. **Agregar archivos de soporte (opcional):**
   ```bash
   mkdir scripts      # Scripts ejecutables (Python, Bash, etc.)
   mkdir references   # Documentación, APIs, guías
   mkdir knowledge    # Templates, specs, etc.
   ```

4. **Hacer commit y push:**
   ```bash
   git add nueva-skill/
   git commit -m "feat: add nueva-skill"
   git push
   ```

5. **Sincronizar con OpenCode:**
   ```bash
   ./sync-to-opencode.sh
   ```

### Actualizar Skills Existentes

1. **Hacer cambios en cualquier skill:**
   ```bash
   cd ~/.copilot/skills/nombre-skill
   # editar archivos
   ```

2. **Commit y push:**
   ```bash
   git add .
   git commit -m "fix: descripción del cambio"
   git push
   ```

3. **Los cambios son automáticos en OpenCode** (gracias a los symlinks)

### Sincronizar desde GitHub

Si alguien más agregó skills, o trabajas desde otra máquina:

#### Opción 1: Sincronización Automática (Configurado)

Este repositorio tiene un **git hook** que sincroniza automáticamente después de cada `git pull`:

```bash
cd ~/.copilot/skills
git pull
# ✨ La sincronización se ejecuta automáticamente
```

También puedes usar el alias `sync-skills`:

```bash
cd ~/.copilot/skills
git sync-skills  # Hace pull y sincroniza en un solo comando
```

#### Opción 2: Sincronización Manual

```bash
cd ~/.copilot/skills
git pull
./sync-to-opencode.sh  # Sincroniza las nuevas skills con OpenCode
```

## 📋 Requisitos para Skills Válidas

Para que una skill sea compatible con OpenCode:

### Frontmatter YAML
- ✅ Campo `name` (requerido): debe coincidir con el nombre del directorio
- ✅ Campo `description` (requerido): 1-1024 caracteres
- ✅ Campo `license` (opcional)
- ✅ Campo `compatibility` (opcional)
- ✅ Campo `metadata` (opcional)

### Nombre de la Skill
Debe cumplir con el patrón: `^[a-z0-9]+(-[a-z0-9]+)*$`

- ✅ Solo minúsculas
- ✅ Números permitidos
- ✅ Separadores con guión simple `-`
- ❌ No puede empezar/terminar con `-`
- ❌ No puede tener `--` consecutivos

Ejemplos válidos: `pdf`, `web-scraper`, `mcp-builder`, `dev-workflow`

### Estructura Recomendada
```
nombre-skill/
├── SKILL.md              (Requerido: Instrucciones para el AI)
├── scripts/              (Opcional: Código ejecutable)
├── references/           (Opcional: Documentación)
└── knowledge/            (Opcional: Templates, specs)
```

## 🎯 Ventajas de esta Configuración

✅ **Un solo repositorio Git**
- Mantén todas tus skills en un solo lugar
- Control de versiones centralizado

✅ **Compatible con ambos sistemas**
- GitHub Copilot: usa directamente `~/.copilot/skills/`
- OpenCode: usa symlinks desde `~/.config/opencode/skills/`

✅ **Sincronización automática**
- Cambios en el repositorio se reflejan en ambos sistemas
- No duplicar archivos ni esfuerzo

✅ **Fácil de mantener**
- Script `sync-to-opencode.sh` para sincronización rápida
- Nuevas skills detectadas automáticamente

## 🔗 Enlaces

- **Repositorio:** https://github.com/ernestoelo/skills
- **OpenCode Docs:** https://opencode.ai/docs/skills
- **GitHub Copilot Docs:** https://docs.github.com/copilot

## 🤖 Automatización

Este repositorio incluye automatización para mantener las skills sincronizadas:

### Git Hook (post-merge)

El hook `.git/hooks/post-merge` se ejecuta automáticamente después de cada `git pull` o `git merge`:

```bash
# Después de hacer git pull, automáticamente:
# 1. Detecta nuevas skills
# 2. Crea symlinks en ~/.config/opencode/skills/
# 3. Muestra reporte de sincronización
```

### Alias de Git

El alias `sync-skills` combina pull y sincronización:

```bash
cd ~/.copilot/skills
git sync-skills  # Equivale a: git pull && ./sync-to-opencode.sh
```

Configuración del alias:
```bash
git config alias.sync-skills '!f() { git pull "$@" && ./sync-to-opencode.sh; }; f'
```

## 📝 Notas

- Este repositorio está sincronizado entre GitHub Copilot y OpenCode
- Los symlinks mantienen ambos sistemas actualizados automáticamente
- El git hook `post-merge` sincroniza automáticamente después de `git pull`
- También puedes ejecutar `./sync-to-opencode.sh` manualmente cuando quieras

