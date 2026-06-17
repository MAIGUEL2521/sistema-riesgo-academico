# Arquitectura del Sistema — Riesgo Académico Estudiantil

## Descripción general

El sistema es una aplicación web analítica local compuesta por tres capas: datos, modelo de machine learning y presentación (dashboard). Su propósito es clasificar el nivel de rendimiento académico de estudiantes de bachillerato para apoyar decisiones de intervención pedagógica temprana.

---

## Diagrama de componentes

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CAPA DE DATOS                                │
│                                                                     │
│  data/raw/students_performance.csv   ──►   data/processed/          │
│       (2.392 registros, 15 cols)           dataset_limpio.csv       │
│                                            (2.392 filas, 13 cols)   │
│                  ▲                                 │                │
│                  │  notebooks/02_eda_limpieza.ipynb│                │
└──────────────────┼─────────────────────────────────┼───────────────┘
                   │                                 │
┌──────────────────┼─────────────────────────────────▼───────────────┐
│                        CAPA DE MODELO                               │
│                                                                     │
│  notebooks/03_modelado.ipynb                                        │
│  src/ml/entrenar_modelo.py                                          │
│        │                                                            │
│        ├─► models/modelo_final.pkl     (LogisticRegression)         │
│        ├─► models/scaler.pkl           (StandardScaler)             │
│        └─► models/model_metadata.json  (métricas y metadatos)       │
└──────────────────────────────────────────┬──────────────────────────┘
                                           │
┌──────────────────────────────────────────▼──────────────────────────┐
│                        CAPA DE PRESENTACIÓN                         │
│                                                                     │
│  app_final.py  (Streamlit)                                          │
│       │                                                             │
│       ├── Pestaña 1: Análisis exploratorio                          │
│       │       - Filtros interactivos (clase, tutoría, extracurr.)   │
│       │       - 3 visualizaciones: distribución, estudio/ausencias, │
│       │         apoyo parental y tutorías                           │
│       │                                                             │
│       └── Pestaña 2: Predicción de riesgo                           │
│               - Formulario de entrada (12 variables)                │
│               - Predicción con probabilidades por clase             │
│               - Interpretación en lenguaje natural                  │
│               - Advertencia ética visible                           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Flujo de datos

```
1. [Fuente]     Kaggle — Students Performance Dataset (CSV)
       │
       ▼
2. [EDA]        notebooks/02_eda_limpieza.ipynb
                - Diagnóstico: shape, nulos, duplicados
                - Eliminación de StudentID y GPA (data leakage)
                - Split 80/20 estratificado (seed=42)
                - StandardScaler en variables continuas
       │
       ▼
3. [Procesado]  data/processed/dataset_limpio.csv
                - 2.392 filas × 13 columnas (sin StudentID ni GPA)
       │
       ▼
4. [Modelado]   notebooks/03_modelado.ipynb
                - Comparación: RandomForest, GradientBoosting, LogisticRegression
                - Selección: LogisticRegression (mayor F1-macro)
       │
       ▼
5. [Artefactos] models/modelo_final.pkl + scaler.pkl + model_metadata.json
       │
       ▼
6. [Dashboard]  app_final.py (Streamlit)
                - Carga recursos al arranque (@st.cache_resource)
                - Tab 1: Visualizaciones con filtros
                - Tab 2: Formulario → predicción → interpretación
```

---

## Tecnologías utilizadas

| Capa | Tecnología | Versión | Rol |
|------|-----------|---------|-----|
| Datos | pandas | 2.2.2 | Manipulación y limpieza |
| Datos | numpy | 1.26.4 | Operaciones numéricas |
| Modelo | scikit-learn | 1.4.2 | Algoritmos ML y preprocesado |
| Modelo | joblib | (con sklearn) | Serialización del modelo |
| Visualización | matplotlib | 3.8.4 | Gráficos en notebooks y dashboard |
| Visualización | seaborn | 0.13.2 | Gráficos estadísticos |
| Dashboard | Streamlit | 1.35.0 | Interfaz web interactiva |
| Notebooks | Jupyter | 1.0.0 | Experimentación y EDA |

---

## Decisiones de diseño relevantes

**Exclusión de GPA:** La variable `GPA` fue eliminada del modelo porque tiene una correlación de -0.97 con `GradeClass`. Incluirla constituiría data leakage grave: el GPA es esencialmente la misma información que la variable objetivo, expresada en otra escala. El análisis honesto sin GPA produce métricas más bajas (~0.50 F1 macro) pero genuinas.

**Selección de LogisticRegression:** Aunque los tres modelos comparados producen resultados similares, se seleccionó LogisticRegression por mayor F1-score macro sobre el conjunto de prueba y por interpretabilidad de coeficientes, que es relevante para el usuario final (coordinadores académicos).

**Escalado correcto:** El `StandardScaler` se ajusta exclusivamente sobre el conjunto de entrenamiento. La transformación del conjunto de prueba y del formulario de predicción usa los parámetros aprendidos del train, evitando fuga de información.
