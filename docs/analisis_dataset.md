# Análisis Cualitativo del Dataset

## Sistema de Clasificación de Riesgo Académico Estudiantil

**Autor:** Jesus Gabriuel Maiguel Yerena
**Fecha:** Junio 14 de 2026
**Dataset:** Students Performance Dataset — Rabie El Kharoua (Kaggle, 2024)

---

## 1. Descripción general

El dataset *Students Performance Dataset* fue publicado en Kaggle en 2024 por Rabie El Kharoua bajo licencia CC BY 4.0, lo que permite su uso académico con atribución al autor. El conjunto de datos captura información detallada de 2.392 estudiantes de bachillerato, integrando variables demográficas, conductuales y académicas con el propósito de facilitar tareas de clasificación y predicción del rendimiento escolar. Su recopilación responde a la necesidad creciente de aplicar analítica de datos en contextos educativos para apoyar decisiones pedagógicas basadas en evidencia.

---

## 2. Estructura del dataset

El dataset contiene **2.392 filas** y **15 columnas**, distribuidas así:

| Tipo de variable | Columnas |
|-----------------|---------|
| Numéricas continuas | `StudyTimeWeekly`, `GPA` |
| Numéricas discretas | `Age`, `Absences` |
| Ordinales | `ParentalEducation`, `ParentalSupport` |
| Binarias (0/1) | `Gender`, `Tutoring`, `Extracurricular`, `Sports`, `Music`, `Volunteering` |
| Categórica nominal | `Ethnicity` |
| Variable objetivo | `GradeClass` (multiclase: 0=A, 1=B, 2=C, 3=D, 4=F) |

No se identificó la presencia de un identificador único sensible, lo que es adecuado desde el punto de vista de la privacidad.

---

## 3. Variables relevantes

- **`StudyTimeWeekly`**: Refleja directamente el esfuerzo académico. Se espera correlación negativa con `GradeClass` (más estudio → mejor nota → clase más baja numéricamente).
- **`Absences`**: El ausentismo es uno de los predictores más documentados del bajo rendimiento. Se anticipa correlación positiva con `GradeClass`.
- **`Tutoring`**: Indica si el estudiante recibe apoyo académico adicional, factor protector relevante.
- **`ParentalSupport`**: El respaldo familiar es factor protector reconocido en la literatura educativa.
- **`GPA`**: Predictor directo del rendimiento final. Su inclusión debe evaluarse cuidadosamente para evitar fuga de información (*data leakage*).

---

## 4. Calidad de los datos

La exploración inicial con pandas arrojó:

```
Shape: (2392, 15)
Valores nulos por columna: 0 en todas las columnas
Registros duplicados: 0
```

**Interpretación:** El dataset presenta calidad excepcional para uso académico. La ausencia total de valores nulos elimina la necesidad de estrategias de imputación, simplificando el preprocesamiento. La inexistencia de duplicados garantiza que cada registro corresponde a un estudiante único.

La distribución de la variable objetivo `GradeClass` es:

| Clase | Etiqueta | Frecuencia | Porcentaje |
|-------|----------|-----------|------------|
| 0 | A (Excelente) | 518 | 21.7% |
| 1 | B (Bueno) | 559 | 23.4% |
| 2 | C (Promedio) | 644 | 26.9% |
| 3 | D (Bajo) | 447 | 18.7% |
| 4 | F (Reprobado) | 224 | 9.4% |

Este desbalance moderado justifica el uso del **F1-score macro** como métrica principal.

---

## 5. Pertinencia del dataset

El dataset es plenamente pertinente para responder la pregunta analítica. Todas las variables necesarias están presentes: la variable objetivo (`GradeClass`) existe explícitamente, las variables de entrada cubren los principales factores asociados al desempeño escolar (tiempo de estudio, asistencia, apoyo familiar, tutorías), y el tamaño muestral de 2.392 registros es suficiente para entrenar y validar un modelo de clasificación con confianza estadística razonable. La licencia CC BY 4.0 permite uso académico sin restricciones, con atribución al autor.

---

## 6. Limitaciones del dataset

| Tipo de limitación | Descripción |
|--------------------|-------------|
| **Contexto geográfico desconocido** | No especifica el país o región de origen, lo que impide generalizar a un sistema educativo específico como el colombiano. |
| **Ausencia de información temporal** | No incluye variables temporales, lo que impide construir modelos predictivos en tiempo real durante el año escolar. |
| **Posible sesgo de selección** | No se documenta cómo fueron seleccionados los 2.392 estudiantes; incertidumbre sobre representatividad de la muestra. |
| **GPA como posible data leakage** | Si el GPA corresponde al mismo periodo evaluado por `GradeClass`, su inclusión puede inflar artificialmente el rendimiento predictivo. |
| **Variables binarias sin matiz** | Variables como `Extracurricular` solo indican participación (sí/no), sin capturar intensidad ni tipo de actividad. |

---

## Referencias

El Kharoua, R. (2024). *Students Performance Dataset* [Dataset]. Kaggle. https://www.kaggle.com/datasets/rabieelkharoua/students-performance-dataset. Licencia: CC BY 4.0.
