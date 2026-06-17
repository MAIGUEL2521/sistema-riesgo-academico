# Ficha de Formulación del Proyecto Integrador

## 1. Datos del estudiante

- **Nombre completo:** Jesus Gabriel Maiguel Yerena
- **Programa:** Tecnología en Desarrollo de Software
- **Diplomado:** Desarrollo Web para Analítica de Datos
- **Fecha:** Junio 16 de 2026

---

## 2. Nombre del proyecto

**Sistema de Clasificación de Riesgo Académico Estudiantil mediante Machine Learning**

---

## 3. Planteamiento del problema

En instituciones de educación secundaria de Colombia y América Latina, los coordinadores académicos y docentes enfrentan una limitación crítica: la identificación tardía de estudiantes con bajo rendimiento académico. Actualmente, los reportes de notas se generan al final del periodo, cuando las posibilidades de intervención pedagógica son mínimas. Esta situación afecta a estudiantes de bachillerato que, pese a presentar señales tempranas de dificultad —ausentismo frecuente, poco tiempo de estudio, baja participación familiar—, no reciben acompañamiento oportuno.

Por ello, se propone desarrollar una aplicación web analítica que, a partir del dataset *Students Performance Dataset* de Kaggle (2.392 registros, 15 variables académicas y socioeducativas), permita clasificar el nivel de rendimiento final del estudiante en cinco categorías (A, B, C, D o F), con el fin de apoyar decisiones de intervención pedagógica temprana por parte de coordinadores y docentes de bachillerato. La solución se implementará como un dashboard interactivo que visualice los factores de riesgo y las predicciones del modelo de clasificación.

---

## 4. Pregunta analítica

¿Es posible clasificar el nivel de rendimiento académico (A/B/C/D/F) de un estudiante de bachillerato a partir de variables como tiempo de estudio semanal, porcentaje de asistencia, número de tutorías, participación de los padres y actividades extracurriculares, con el fin de apoyar decisiones de intervención pedagógica temprana?

---

## 5. Tipo de tarea y métrica de evaluación

- **Tipo de tarea:** [x] Clasificación multiclase
- **Variable objetivo:** `GradeClass` (0=A, 1=B, 2=C, 3=D, 4=F)
- **Métrica principal:** F1-score macro
- **Justificación de la métrica:** El dataset presenta desbalance moderado entre las categorías de rendimiento (C es la clase más frecuente con 26.9%, F la menos frecuente con 9.4%). El F1-score macro calcula el F1 de cada clase de forma independiente y promedia los resultados sin ponderar por frecuencia, garantizando que ninguna categoría sea ignorada durante la evaluación. Esto es preferible al accuracy cuando las clases no están balanceadas, ya que el accuracy puede ser engañosamente alto si el modelo predice siempre la clase mayoritaria.

---

## 6. Descripción del dataset

- **Nombre:** Students Performance Dataset
- **Fuente (URL):** https://www.kaggle.com/datasets/rabieelkharoua/students-performance-dataset
- **Autor:** Rabie El Kharoua
- **Año de publicación:** 2024
- **Licencia:** CC BY 4.0 (permite uso académico con atribución)
- **Número de filas:** 2.392
- **Número de columnas:** 15
- **Descripción general:** Dataset que contiene información detallada de estudiantes de bachillerato, incluyendo características demográficas, hábitos de estudio, nivel de participación parental, actividades extracurriculares y rendimiento académico final. Fue diseñado para tareas de clasificación y predicción de desempeño estudiantil.

---

## 7. Variables

- **Variable objetivo (y):** `GradeClass` — Categoría de rendimiento académico final (0=A, 1=B, 2=C, 3=D, 4=F)

- **Variables de entrada principales (X):**
  - `StudyTimeWeekly`: Horas de estudio semanales (numérica continua, rango 0–20)
  - `Absences`: Número de ausencias registradas en el año escolar (numérica discreta, rango 0–30)
  - `Tutoring`: Si el estudiante recibe tutorías adicionales (binaria: 0=No, 1=Sí)
  - `ParentalSupport`: Nivel de apoyo y participación de los padres (ordinal: 0=None a 4=Very High)
  - `ParentalEducation`: Nivel educativo de los padres (ordinal: 0=None a 4=Higher)
  - `Extracurricular`: Participación en actividades extracurriculares (binaria: 0=No, 1=Sí)
  - `Sports`: Participación en deportes (binaria: 0=No, 1=Sí)
  - `Music`: Participación en actividades musicales (binaria: 0=No, 1=Sí)
  - `Volunteering`: Participación en voluntariado (binaria: 0=No, 1=Sí)
  - `Age`: Edad del estudiante (numérica discreta: 15–18 años)
  - `Gender`: Género del estudiante (binaria: 0=Male, 1=Female)
  - `Ethnicity`: Grupo étnico (categórica: 0–3)
  - `GPA`: Promedio académico acumulado (numérica continua, rango 0.0–4.0)

---

## 8. Usuario final y decisión

- **Usuario:** Coordinador académico o docente tutor de bachillerato
- **Decisión que apoyará:** Identificar estudiantes con riesgo de bajo rendimiento (categorías D o F) antes del cierre del periodo académico, para activar rutas de acompañamiento pedagógico, citaciones a padres de familia o asignación de tutorías de refuerzo.

---

## 9. Implicaciones éticas

**Riesgo identificado:** El modelo puede generar predicciones sesgadas hacia grupos étnicos o socioeconómicos si las variables `Ethnicity` y `ParentalEducation` tienen alta correlación con `GradeClass`, lo que podría llevar a estigmatizar estudiantes de ciertos grupos.

**Acción de mitigación:** Se realizará análisis de equidad (fairness analysis) por grupos étnicos y niveles de educación parental. Si se detecta sesgo estadísticamente significativo, las variables `Ethnicity` y `ParentalEducation` serán excluidas del modelo final. Los resultados del clasificador se presentarán como herramienta de apoyo a la decisión docente, nunca como veredicto definitivo sobre el estudiante.

---

## 10. URL del repositorio GitHub

https://github.com/tu-usuario/sistema-riesgo-academico

