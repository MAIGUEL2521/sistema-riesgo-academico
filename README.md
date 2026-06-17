# 🎓 Sistema de Clasificación de Riesgo Académico Estudiantil

## Descripción

Proyecto integrador del Diplomado en Desarrollo Web para Analítica de Datos. Clasifica el nivel de rendimiento académico de estudiantes de bachillerato en cinco categorías (A/B/C/D/F) usando machine learning, a partir de variables como tiempo de estudio, asistencia, tutorías y apoyo familiar. El objetivo es apoyar decisiones de intervención pedagógica temprana.

---

## Pregunta analítica

¿Es posible clasificar el nivel de rendimiento académico (A/B/C/D/F) de un estudiante de bachillerato a partir de variables como tiempo de estudio semanal, porcentaje de asistencia, número de tutorías, participación de los padres y actividades extracurriculares, con el fin de apoyar decisiones de intervención pedagógica temprana?

> **Nota:** La variable `GPA` fue excluida del modelo por constituir data leakage (correlación -0.97 con la variable objetivo). Las métricas reportadas son genuinas.

---

## Dataset

- **Nombre:** Students Performance Dataset
- **Fuente:** https://www.kaggle.com/datasets/rabieelkharoua/students-performance-dataset
- **Autor:** Rabie El Kharoua (2024) — Licencia CC BY 4.0
- **Registros:** 2.392 estudiantes | 15 variables originales | 12 variables en modelo + target

---

## Arquitectura de la solución

```
data/raw/ ──► [Notebook 02 EDA] ──► data/processed/ ──► [Notebook 03 Modelado] ──► models/ ──► app_final.py
```

Descripción detallada: [`docs/arquitectura.md`](docs/arquitectura.md)

---

## Estructura del repositorio

```
├── README.md
├── .gitignore
├── requirements.txt
├── app_final.py                         ← Dashboard Streamlit
├── data/
│   ├── raw/students_performance.csv
│   └── processed/dataset_limpio.csv
├── notebooks/
│   ├── 01_exploracion.ipynb
│   ├── 02_eda_limpieza.ipynb
│   └── 03_modelado.ipynb
├── src/ml/entrenar_modelo.py
├── models/
│   ├── modelo_final.pkl
│   ├── scaler.pkl
│   └── model_metadata.json
└── docs/
    ├── ficha_proyecto.md
    ├── analisis_dataset.md
    ├── diccionario_datos.md
    ├── arquitectura.md
    ├── reflexion_etica.md
    └── wireframe_dashboard.png
```

---

## Instalación y ejecución

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
pip install -r requirements.txt

# Opcional: reentrenar localmente
python src/ml/entrenar_modelo.py

# Ejecutar dashboard
streamlit run app_final.py
```

---

## Resultados del modelo

| Modelo | F1-score Macro | Accuracy |
|--------|---------------|----------|
| **LogisticRegression (seleccionado)** | **0.4961** | **0.4969** |
| GradientBoostingClassifier | 0.4591 | 0.4697 |
| RandomForestClassifier | 0.4300 | 0.4426 |

Evaluación sobre conjunto de prueba (20%, n=479). Métrica principal: F1-score macro (desbalance moderado entre clases).

---

## Consideraciones éticas

El modelo es apoyo a la decisión docente, no reemplaza el criterio profesional. Ver [`docs/reflexion_etica.md`](docs/reflexion_etica.md).

---

## Autor

Jesus Gabriel Maiguel Yerena — Tecnología en Desarrollo de Software | Diplomado Desarrollo Web Analítica de Datos | ITFIP | Junio 16 2026
