#!/usr/bin/env python3
"""
Script para dividir archivos grandes (txt/pdf) en bloques manejables para procesamiento recursivo.
"""
import sys
import os

def chunk_file(input_path, chunk_size=4096):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    for i in range(0, len(content), chunk_size):
        yield content[i:i+chunk_size]

def main():
    if len(sys.argv) < 2:
        print("Uso: context_loader.py <archivo.txt>")
        sys.exit(1)
    input_path = sys.argv[1]
    for idx, chunk in enumerate(chunk_file(input_path)):
        out = f"chunk_{idx:03d}.txt"
        with open(out, 'w', encoding='utf-8') as f:
            f.write(chunk)
        print(f"Generado: {out}")

if __name__ == "__main__":
    main()
