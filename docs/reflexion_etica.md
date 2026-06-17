# Reflexión Ética Final

## Sistema de Clasificación de Riesgo Académico Estudiantil

**Versión:** Final (actualizada tras el desarrollo completo)  
**Fecha:** Junio 2026  
**Basada en:** Reflexión inicial de la Entrega 1, enriquecida con aprendizajes del proceso.

---

## 1. Declaración fundamental

> **El resultado de este modelo es un apoyo a la decisión pedagógica, no una decisión automática.**  
> Ninguna clasificación generada por el sistema debe usarse como veredicto definitivo sobre un estudiante. La decisión final siempre recae en el profesional educativo responsable.

---

## 2. Riesgos identificados

### 2.1 Riesgo de sesgo por variables demográficas

**Descripción:** Las variables `Ethnicity` y `ParentalEducation` podrían capturar desigualdades estructurales más que capacidades individuales del estudiante. Si el modelo aprende que ciertos grupos étnicos o de bajo nivel educativo familiar tienen peor rendimiento, podría perpetuar y reforzar esas desigualdades al usarse en contextos reales.

**Nivel:** Alto.

### 2.2 Riesgo de estigmatización

**Descripción:** Presentar una predicción de categoría D o F a un docente podría generar expectativas negativas sobre el estudiante (efecto Pigmalión inverso), afectando el trato que recibe independientemente de su evolución real.

**Nivel:** Alto.

### 2.3 Limitaciones del dataset

**Descripción:** El dataset no especifica país ni región de origen. Aplicarlo en instituciones educativas colombianas podría generar predicciones sesgadas si los patrones del dataset no son representativos del contexto local (calendario, sistema de evaluación, condiciones socioeconómicas).

**Nivel:** Moderado.

### 2.4 Ausencia de variables temporales

**Descripción:** El modelo predice el rendimiento final sin información de la progresión durante el año. Un estudiante con dificultades en el primer bimestre que mejora progresivamente sería clasificado igual que uno que no mejora.

**Nivel:** Moderado.

### 2.5 Métricas honestas pero limitadas

**Descripción:** El F1-score macro del modelo (≈0.50) indica que la clasificación tiene errores significativos, especialmente en categorías intermedias (B/C/D). Una predicción incorrecta presentada sin incertidumbre podría llevar a intervenciones innecesarias o a ignorar casos reales de riesgo.

**Nivel:** Moderado.

---

## 3. Grupos potencialmente afectados

| Grupo | Riesgo específico |
|-------|-------------------|
| Estudiantes de grupos étnicos minoritarios | Mayor probabilidad de ser clasificados en categorías de riesgo si el modelo captura desigualdades sistémicas como patrones predictivos. |
| Estudiantes con bajo apoyo parental | El modelo puede inferir riesgo a partir de condiciones familiares fuera del control del estudiante, estigmatizando en lugar de apoyar. |
| Estudiantes en proceso de mejora | Sin variables temporales, el modelo no puede capturar mejoras en el rendimiento. |
| Docentes con alta carga académica | Podrían delegar decisiones al modelo sin revisión crítica, especialmente si el dashboard no presenta las advertencias con suficiente visibilidad. |

---

## 4. Acciones de mitigación implementadas

| Riesgo | Acción tomada |
|--------|---------------|
| Data leakage por GPA | Variable excluida del modelo. Métricas reportadas son genuinas (~0.50 F1 macro). |
| Transparencia de métricas | Las métricas reales se muestran en el dashboard leídas desde `model_metadata.json`. No se inflan resultados. |
| Advertencia ética en dashboard | Mensaje de advertencia visible en la pestaña de predicción antes y después de generar resultados. |
| Interpretación en lenguaje natural | El resultado incluye un mensaje explicativo contextualizado, no solo la etiqueta de clase. |
| Distribución de probabilidades | Se muestra la probabilidad de cada categoría para que el usuario vea la incertidumbre del modelo. |

### Mitigación pendiente (fuera del alcance de este diplomado)

- **Fairness analysis por grupo étnico:** Analizar si el error del modelo es sistemáticamente mayor en grupos específicos y excluir `Ethnicity` si se detecta sesgo estadístico significativo.
- **Validación externa:** Probar el modelo con datos de instituciones colombianas antes de cualquier despliegue real.
- **Pruebas de usuario:** Validar con docentes reales que el dashboard es interpretado correctamente y que la advertencia ética es leída y comprendida.

---

## 5. Limitaciones conocidas del sistema

1. **Precisión limitada:** F1-score macro ≈ 0.50 significa que el modelo acierta aproximadamente en la mitad de las clasificaciones multiclase.
2. **Contexto no validado:** El dataset no proviene de Colombia ni de un contexto educativo equivalente.
3. **Sin actualización en tiempo real:** El modelo no se actualiza con nuevos datos de manera automática.
4. **Variables proxy:** Variables como `ParentalSupport` y `ParentalEducation` pueden funcionar como proxies de condiciones socioeconómicas, introduciendo sesgos estructurales.
5. **Despliegue local:** El sistema corre localmente y requiere que el docente ingrese los datos manualmente. No está integrado con sistemas de gestión académica.

---

## 6. Conclusión

Este sistema tiene valor como herramienta de exploración de datos y apoyo a la reflexión pedagógica. No tiene valor como sistema de decisión automática. Su uso responsable requiere que los docentes y coordinadores que lo utilicen comprendan sus limitaciones, que el resultado sea un insumo más dentro de un proceso de seguimiento integral, y que nunca reemplace la observación directa y el juicio profesional sobre el estudiante.
