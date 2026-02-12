# Scripts de Recursive Context

Incluye utilidades para dividir archivos grandes en bloques y facilitar el procesamiento recursivo de contexto.

- `context_loader.py`: Divide archivos de texto en chunks de 4096 caracteres para análisis incremental.

## Uso rápido

```bash
cd scripts
python3 context_loader.py ../ejemplo.txt
```

Puedes adaptar el chunk_size en el script según la ventana de contexto de tu modelo.
