---
name: oncomets-mil-loss-lab
description: "Guía de agente para diseñar, comparar y debuggear funciones de pérdida en CLAM_MB bajo desbalance de clases y transición semi-supervisada con feedback humano. Trigger: loss, CLAM, MIL, imbalance, pseudo-label, FAISS, inst_eval, perdida, desbalance, reentrenamiento, focal, weighted CE, balanced softmax."
---

# OncoMETS MIL Loss Lab

## Antes de empezar

1. Lee `EnvironBio/references/baseline-config.md` para entender la config actual
2. Lee `EnvironBio/references/task-configs.md` para conocer las 10 tareas clínicas
3. Si necesitas snippets de código, lee `references/loss-playbook.md` (en esta skill)

## Inputs requeridos (preguntar al usuario si no los provee)

1. **¿Qué tarea clínica?** (una de las 10 en task-configs.md)
2. **¿Cuál es el error?** (bajo minority recall, calibración pobre, inestabilidad, overfitting)
3. **¿Métrica objetivo?** (macro-F1, minority recall, AUROC)
4. **¿Budget de tiempo?** (horas disponibles para implementar + entrenar)
5. **¿Hay feedback humano disponible?** (no / FAISS retrieval / labels manuales)

Si el usuario no da esta info, **preguntar antes de proponer nada**.

---

## Workflow del agente

### Paso 1: Diagnosticar

Determinar cuál de estos es el bottleneck principal:

| Síntoma | Probable causa | Verificación |
|---------|---------------|-------------|
| Minority recall ~0 | Desbalance de clases | Revisar distribución en CSV |
| Loss oscila sin converger | Inestabilidad bag_weight vs SmoothTop1SVM | Revisar curvas de entrenamiento |
| Alta confianza en predicciones incorrectas | Pseudo-labels ruidosas (attention top-k) | Inspeccionar attention scores |
| Buen train, mal val | Overfitting por dataset pequeño (23-41 muestras) | Comparar train/val loss |

### Paso 2: Seleccionar candidatos (max 2-3)

| Causa | Candidato | Cambio en |
|-------|-----------|-----------|
| Desbalance + negativos fáciles | Focal loss o weighted CE | bag loss (`core_utils.py:123`) |
| Shift en priors | Balanced softmax | bag loss (`core_utils.py:123`) |
| Pseudo-labels ruidosas | Label smoothing o CE como inst_loss | inst loss (`model_clam.py:115`) |
| Integración feedback humano | Soft target mixing | `inst_eval()` targets |

Ver `references/loss-playbook.md` para implementación PyTorch de cada candidato.

### Paso 3: Definir experimento mínimo

```
Max 4-6 runs por ciclo. Una variable por run.
Fast validation: invasion_linfatica_vascular (2 clases, 41 muestras).
```

| Eje | Opción A (baseline) | Opción B (candidato) |
|-----|---------------------|---------------------|
| Bag loss | CE | 1 candidato |
| Instance loss | SmoothTop1SVM | nn.CrossEntropyLoss (`--inst_loss ce`) |
| Sampler | WeightedRandom | Class-aware custom |

### Paso 4: Implementar

- No tocar arquitectura CLAM_MB en primera iteración
- Log: seed, split, config hash (usar `seed_torch()` de main.py)
- Evaluar con ≥2 seeds

### Paso 5: Decidir go/no-go

| Criterio | Umbral |
|----------|--------|
| Minority recall | +2-5 puntos vs baseline |
| AUROC global | Sin regresión |
| Curvas de entrenamiento | Estables en ≥2 seeds |
| Calibración | No degrada |

### Paso 6: Acción

- **Go**: patch plan para los 10 tasks
- **No-go**: documentar por qué, rollback limpio
- **Mixed**: mantener mejor candidato, iterar solo threshold + calibración

---

## Output contract

Cada respuesta al usuario DEBE incluir:
1. Diagnóstico del failure mode
2. Candidato recomendado + fallback
3. Plan de experimento con `file:line` exactos donde cambiar
4. Esfuerzo estimado (implementación + entrenamiento)
5. Criterio de rollback concreto

---

## Guardrails

- No cambiar data pipeline y loss simultáneamente
- No refactorizar arquitectura durante experimento de loss
- Rollback si macro-F1 o minority recall baja >3%
- Siempre usar `seed_torch()` y evaluar con ≥2 seeds
