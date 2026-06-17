"""
Script de entrenamiento local reproducible
Proyecto: Sistema de Clasificación de Riesgo Académico Estudiantil
Ejecutar desde la raíz del proyecto: python src/ml/entrenar_modelo.py
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    f1_score, accuracy_score, precision_score, recall_score, classification_report
)
import joblib
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ── Rutas ──────────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent.parent.parent
DATA_PATH   = BASE / "data" / "processed" / "dataset_limpio.csv"
MODEL_PATH  = BASE / "models" / "modelo_final.pkl"
SCALER_PATH = BASE / "models" / "scaler.pkl"
META_PATH   = BASE / "models" / "model_metadata.json"

def main():
    print("=" * 55)
    print("  Entrenamiento del modelo de riesgo académico")
    print("=" * 55)

    # 1. Carga
    print("\n[1/5] Cargando dataset procesado...")
    df = pd.read_csv(DATA_PATH)
    print(f"      Shape: {df.shape}")

    # 2. Separación X/y y split
    print("[2/5] Preparando datos...")
    X = df.drop(columns=["GradeClass"])
    y = df["GradeClass"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. Escalado (fit solo en train)
    print("[3/5] Escalando variables continuas...")
    cont_cols = ["StudyTimeWeekly", "Absences", "Age"]
    scaler = StandardScaler()
    X_train_sc = X_train.copy()
    X_test_sc  = X_test.copy()
    X_train_sc[cont_cols] = scaler.fit_transform(X_train[cont_cols])
    X_test_sc[cont_cols]  = scaler.transform(X_test[cont_cols])

    # 4. Comparar modelos
    print("[4/5] Entrenando y comparando modelos...")
    models = {
        "RandomForestClassifier":     RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
        "GradientBoostingClassifier": GradientBoostingClassifier(n_estimators=150, random_state=42),
        "LogisticRegression":         LogisticRegression(max_iter=1000, random_state=42),
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train_sc, y_train)
        y_pred = model.predict(X_test_sc)
        results[name] = {
            "f1_macro":        round(f1_score(y_test, y_pred, average="macro"), 4),
            "accuracy":        round(accuracy_score(y_test, y_pred), 4),
            "precision_macro": round(precision_score(y_test, y_pred, average="macro", zero_division=0), 4),
            "recall_macro":    round(recall_score(y_test, y_pred, average="macro"), 4),
        }
        print(f"      {name:32s} F1={results[name]['f1_macro']:.4f}  Acc={results[name]['accuracy']:.4f}")

    best_name  = max(results, key=lambda k: results[k]["f1_macro"])
    best_model = models[best_name]
    best_res   = results[best_name]
    print(f"\n      >>> Mejor modelo: {best_name}")

    # Reporte completo sobre test
    y_pred_best = best_model.predict(X_test_sc)
    print("\n" + classification_report(y_test, y_pred_best, target_names=["A","B","C","D","F"]))

    # 5. Serialización
    print("[5/5] Serializando modelo y metadata...")
    BASE_MODELS = BASE / "models"
    BASE_MODELS.mkdir(parents=True, exist_ok=True)

    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(scaler,     SCALER_PATH)

    # Verificar carga
    _ = joblib.load(MODEL_PATH)
    print(f"      modelo_final.pkl cargado correctamente: {type(_).__name__}")

    metadata = {
        "modelo":              best_name,
        "version":             "1.0",
        "fecha_entrenamiento": "2026-06-10",
        "metrica_principal":   "f1_score_macro",
        "valor_metrica":       best_res["f1_macro"],
        "accuracy":            best_res["accuracy"],
        "precision_macro":     best_res["precision_macro"],
        "recall_macro":        best_res["recall_macro"],
        "variables_entrada":   list(X.columns),
        "variable_objetivo":   "GradeClass",
        "clases":              {"0":"A (Excelente)","1":"B (Bueno)","2":"C (Promedio)","3":"D (Bajo)","4":"F (Reprobado)"},
        "nota_gpa":            "GPA excluido (correlacion -0.97 con target = data leakage)",
        "observaciones":       "Semilla 42. Comparados: RandomForest, GradientBoosting, LogisticRegression.",
    }
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"      model_metadata.json guardado.")
    print("\n[OK] Entrenamiento completado.\n")

if __name__ == "__main__":
    main()
