# Diccionario de Datos

## Sistema de Clasificación de Riesgo Académico Estudiantil

**Dataset:** Students Performance Dataset — Rabie El Kharoua (Kaggle, 2024)  
**Fuente:** https://www.kaggle.com/datasets/rabieelkharoua/students-performance-dataset  
**Licencia:** CC BY 4.0  
**Filas:** 2.392 | **Columnas originales:** 15 | **Columnas en modelo:** 12 + 1 target

---

## Variables del dataset original

| Variable | Tipo | Rol en modelo | Rango / Valores | Descripción |
|----------|------|---------------|-----------------|-------------|
| `StudentID` | Categórica (string) | **Excluida** | EST-0001 a EST-2392 | Identificador único del estudiante. Sin valor predictivo. |
| `Age` | Numérica discreta | Entrada (X) | 15 – 18 | Edad del estudiante en años. |
| `Gender` | Binaria | Entrada (X) | 0 = Masculino, 1 = Femenino | Género del estudiante. |
| `Ethnicity` | Categórica nominal | Entrada (X) | 0, 1, 2, 3 | Grupo étnico del estudiante. Códigos sin etiqueta específica en la fuente. |
| `ParentalEducation` | Ordinal | Entrada (X) | 0 = Ninguno, 1 = Secundaria, 2 = Técnico, 3 = Universidad, 4 = Posgrado | Nivel educativo más alto alcanzado por los padres. |
| `StudyTimeWeekly` | Numérica continua | Entrada (X) — escalada | 0.0 – 20.0 horas | Promedio de horas semanales dedicadas al estudio fuera de clase. |
| `Absences` | Numérica discreta | Entrada (X) — escalada | 0 – 30 | Total de inasistencias registradas durante el año escolar. |
| `Tutoring` | Binaria | Entrada (X) | 0 = No, 1 = Sí | Indica si el estudiante recibe tutorías o apoyo académico adicional. |
| `ParentalSupport` | Ordinal | Entrada (X) | 0 = Ninguno, 1 = Bajo, 2 = Moderado, 3 = Alto, 4 = Muy alto | Nivel de participación y apoyo de los padres en el proceso académico. |
| `Extracurricular` | Binaria | Entrada (X) | 0 = No, 1 = Sí | Participación en actividades extracurriculares (general). |
| `Sports` | Binaria | Entrada (X) | 0 = No, 1 = Sí | Participación en actividades deportivas. |
| `Music` | Binaria | Entrada (X) | 0 = No, 1 = Sí | Participación en actividades musicales. |
| `Volunteering` | Binaria | Entrada (X) | 0 = No, 1 = Sí | Participación en actividades de voluntariado. |
| `GPA` | Numérica continua | **Excluida (data leakage)** | 0.0 – 4.0 | Promedio académico acumulado. Correlación -0.97 con `GradeClass`. Su inclusión inflaría artificialmente las métricas del modelo. |
| `GradeClass` | Categórica ordinal | **Variable objetivo (y)** | 0=A, 1=B, 2=C, 3=D, 4=F | Categoría de rendimiento académico final. Variable a predecir. |

---

## Variable objetivo — GradeClass

| Código | Etiqueta | Descripción | Frecuencia (n=2392) | Porcentaje |
|--------|----------|-------------|---------------------|------------|
| 0 | A — Excelente | Rendimiento sobresaliente | 518 | 21.7% |
| 1 | B — Bueno | Rendimiento por encima del promedio | 559 | 23.4% |
| 2 | C — Promedio | Rendimiento estándar | 644 | 26.9% |
| 3 | D — Bajo | Rendimiento por debajo del promedio | 447 | 18.7% |
| 4 | F — Reprobado | Rendimiento insuficiente / reprobación | 224 | 9.4% |

**Desbalance moderado:** La clase F (9.4%) es aproximadamente 2.9× menos frecuente que la clase C (26.9%). Esto justifica el uso de **F1-score macro** como métrica principal.

---

## Variables excluidas del modelo

| Variable | Razón de exclusión |
|----------|--------------------|
| `StudentID` | Identificador sin contenido predictivo. Incluirlo no aporta información generalizable. |
| `GPA` | Correlación de -0.97 con `GradeClass`. El GPA es la base numérica de la que se deriva la categoría de rendimiento. Incluirlo constituye **data leakage** grave que inflaría artificialmente las métricas hasta ~1.0. |

---

## Notas de preprocesamiento

- No se detectaron valores nulos en ninguna columna (confirmado en `notebooks/02_eda_limpieza.ipynb`).
- No se detectaron registros duplicados.
- Las variables `StudyTimeWeekly`, `Absences` y `Age` fueron estandarizadas con `StandardScaler` (media 0, desviación estándar 1). El scaler fue ajustado exclusivamente sobre el conjunto de entrenamiento.
- Las variables binarias y ordinales no requirieron codificación adicional ya que están representadas como enteros (0/1 o escala ordinal numérica).
