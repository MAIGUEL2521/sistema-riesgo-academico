"""
api.py — API FastAPI (componente opcional)
Proyecto: Sistema de Clasificación de Riesgo Académico Estudiantil
Ejecutar: uvicorn api:app --reload
Endpoints: GET /health  |  GET /metrics  |  POST /predict
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import json
from pathlib import Path

# ── Rutas ─────────────────────────────────────────────────────────────────────
BASE   = Path(__file__).parent
MODEL  = BASE / "models" / "modelo_final.pkl"
SCALER = BASE / "models" / "scaler.pkl"
META   = BASE / "models" / "model_metadata.json"

# ── Carga del modelo al arranque ───────────────────────────────────────────────
try:
    modelo = joblib.load(MODEL)
    scaler = joblib.load(SCALER)
    with open(META, encoding="utf-8") as f:
        metadata = json.load(f)
    MODEL_LOADED = True
    print(f"[OK] Modelo cargado: {metadata['modelo']}")
except Exception as e:
    MODEL_LOADED = False
    print(f"[ERROR] No se pudo cargar el modelo: {e}")

# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="API — Riesgo Académico Estudiantil",
    description=(
        "API de predicción del nivel de rendimiento académico (A/B/C/D/F) "
        "a partir de variables estudiantiles. Componente opcional del proyecto integrador."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Esquema de entrada ─────────────────────────────────────────────────────────
class EstudianteInput(BaseModel):
    Age:               int   = Field(..., ge=15, le=18,  description="Edad (15-18)")
    Gender:            int   = Field(..., ge=0,  le=1,   description="0=Masculino, 1=Femenino")
    Ethnicity:         int   = Field(..., ge=0,  le=3,   description="Grupo étnico (0-3)")
    ParentalEducation: int   = Field(..., ge=0,  le=4,   description="Nivel educativo padres (0-4)")
    StudyTimeWeekly:   float = Field(..., ge=0,  le=20,  description="Horas de estudio semanales (0-20)")
    Absences:          int   = Field(..., ge=0,  le=30,  description="Número de ausencias (0-30)")
    Tutoring:          int   = Field(..., ge=0,  le=1,   description="Tutorías (0=No, 1=Sí)")
    ParentalSupport:   int   = Field(..., ge=0,  le=4,   description="Apoyo parental (0=Ninguno a 4=Muy alto)")
    Extracurricular:   int   = Field(..., ge=0,  le=1,   description="Extracurriculares (0=No, 1=Sí)")
    Sports:            int   = Field(..., ge=0,  le=1,   description="Deportes (0=No, 1=Sí)")
    Music:             int   = Field(..., ge=0,  le=1,   description="Música (0=No, 1=Sí)")
    Volunteering:      int   = Field(..., ge=0,  le=1,   description="Voluntariado (0=No, 1=Sí)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "Age": 16, "Gender": 0, "Ethnicity": 1,
                "ParentalEducation": 2, "StudyTimeWeekly": 10.5,
                "Absences": 3, "Tutoring": 1, "ParentalSupport": 3,
                "Extracurricular": 1, "Sports": 0, "Music": 0, "Volunteering": 1
            }
        }
    }

# ── Esquema de salida ──────────────────────────────────────────────────────────
class PrediccionOutput(BaseModel):
    clase_predicha:   int
    etiqueta:         str
    nivel_riesgo:     str
    confianza:        float
    probabilidades:   dict
    interpretacion:   str
    advertencia:      str

# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health", tags=["Sistema"])
def health_check():
    """Verifica el estado de la API y si el modelo está cargado."""
    return {
        "status":        "ok" if MODEL_LOADED else "error",
        "modelo_cargado": MODEL_LOADED,
        "modelo":         metadata.get("modelo", "N/A") if MODEL_LOADED else None,
        "version_api":    "1.0.0",
    }


@app.get("/metrics", tags=["Modelo"])
def get_metrics():
    """Retorna las métricas del modelo leídas desde model_metadata.json."""
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="Modelo no disponible.")
    return {
        "modelo":            metadata["modelo"],
        "version":           metadata["version"],
        "fecha_entrenamiento": metadata["fecha_entrenamiento"],
        "metrica_principal": metadata["metrica_principal"],
        "valor_metrica":     metadata["valor_metrica"],
        "accuracy":          metadata["accuracy"],
        "precision_macro":   metadata["precision_macro"],
        "recall_macro":      metadata["recall_macro"],
        "variables_entrada": metadata["variables_entrada"],
        "variable_objetivo": metadata["variable_objetivo"],
        "clases":            metadata["clases"],
        "observaciones":     metadata.get("observaciones", ""),
    }


@app.post("/predict", response_model=PrediccionOutput, tags=["Predicción"])
def predict(estudiante: EstudianteInput):
    """
    Recibe variables del estudiante y retorna la predicción de su categoría
    de rendimiento académico junto con las probabilidades por clase.
    """
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="Modelo no disponible.")

    import pandas as pd

    # Orden de variables igual al entrenamiento
    feature_order = metadata["variables_entrada"]
    data = {
        "Age":               estudiante.Age,
        "Gender":            estudiante.Gender,
        "Ethnicity":         estudiante.Ethnicity,
        "ParentalEducation": estudiante.ParentalEducation,
        "StudyTimeWeekly":   estudiante.StudyTimeWeekly,
        "Absences":          estudiante.Absences,
        "Tutoring":          estudiante.Tutoring,
        "ParentalSupport":   estudiante.ParentalSupport,
        "Extracurricular":   estudiante.Extracurricular,
        "Sports":            estudiante.Sports,
        "Music":             estudiante.Music,
        "Volunteering":      estudiante.Volunteering,
    }
    X = pd.DataFrame([data])[feature_order]

    # Escalar variables continuas
    X_sc = X.copy()
    X_sc[["StudyTimeWeekly", "Absences", "Age"]] = scaler.transform(
        X[["StudyTimeWeekly", "Absences", "Age"]]
    )

    clase      = int(modelo.predict(X_sc)[0])
    proba      = modelo.predict_proba(X_sc)[0]
    confianza  = round(float(proba[clase]) * 100, 2)

    etiquetas = {0:"A - Excelente", 1:"B - Bueno", 2:"C - Promedio", 3:"D - Bajo", 4:"F - Reprobado"}
    etiqueta  = etiquetas[clase]

    if clase in {3, 4}:
        riesgo = "ALTO"
        interp = (
            f"El modelo clasifica al estudiante en la categoria {etiqueta}. "
            "Se recomienda activar rutas de acompanamiento pedagogico: "
            "seguimiento docente, citacion a padres y asignacion de tutorias de refuerzo."
        )
    elif clase == 2:
        riesgo = "MODERADO"
        interp = (
            f"El estudiante se clasifica en la categoria {etiqueta}. "
            "No hay riesgo inmediato, pero puede beneficiarse de mayor apoyo en estudio y asistencia."
        )
    else:
        riesgo = "BAJO"
        interp = (
            f"El perfil del estudiante es consistente con la categoria {etiqueta}. "
            "Se recomienda mantener el seguimiento habitual."
        )

    probabilidades = {
        etiquetas[i]: round(float(p) * 100, 2)
        for i, p in enumerate(proba)
    }

    return PrediccionOutput(
        clase_predicha = clase,
        etiqueta       = etiqueta,
        nivel_riesgo   = riesgo,
        confianza      = confianza,
        probabilidades = probabilidades,
        interpretacion = interp,
        advertencia    = (
            "Este resultado es una estimacion generada por el modelo. "
            "Debe ser revisado por un coordinador o docente responsable antes de "
            "tomar cualquier decision pedagogica."
        ),
    )
