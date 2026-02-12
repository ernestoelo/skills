#!/bin/bash
# Script para generar todos los diagramas PNG a partir de archivos .puml usando PlantUML
# Uso: ./generate_diagrams.sh [directorio]
# Si no se especifica directorio, busca en el directorio actual y subcarpetas

set -e

DIR=${1:-.}

# Verifica que plantuml esté instalado
if ! command -v plantuml &> /dev/null; then
  echo "Error: PlantUML no está instalado. Instálalo con 'sudo pacman -S plantuml' (ver @sys-env)."
  exit 1
fi

# Busca y procesa todos los archivos .puml
echo "Buscando archivos .puml en $DIR ..."
find "$DIR" -type f -name '*.puml' | while read -r file; do
  echo "Generando diagrama para $file ..."
  plantuml "$file"
done

echo "Diagramas generados correctamente."
