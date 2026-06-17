"""
app_final.py — Dashboard de Riesgo Académico Estudiantil
Proyecto Integrador — Diplomado en Desarrollo Web para Analítica de Datos
Ejecutar: streamlit run app_final.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json
from pathlib import Path

# ── Configuración general ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Riesgo Académico — Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Rutas ─────────────────────────────────────────────────────────────────────
BASE   = Path(__file__).parent
MODEL  = BASE / "models" / "modelo_final.pkl"
SCALER = BASE / "models" / "scaler.pkl"
META   = BASE / "models" / "model_metadata.json"
DATA   = BASE / "data" / "processed" / "dataset_limpio.csv"

# ── Carga de recursos (cacheados) ─────────────────────────────────────────────
@st.cache_resource
def cargar_modelo():
    return joblib.load(MODEL)

@st.cache_resource
def cargar_scaler():
    return joblib.load(SCALER)

@st.cache_data
def cargar_datos():
    return pd.read_csv(DATA)

@st.cache_data
def cargar_metadata():
    with open(META, encoding="utf-8") as f:
        return json.load(f)

modelo   = cargar_modelo()
scaler   = cargar_scaler()
df       = cargar_datos()
metadata = cargar_metadata()

# ── Etiquetas de clases ────────────────────────────────────────────────────────
CLASES = {0: "A — Excelente", 1: "B — Bueno", 2: "C — Promedio", 3: "D — Bajo", 4: "F — Reprobado"}
COLORES_CLASE = {0: "#2ecc71", 1: "#3498db", 2: "#f39c12", 3: "#e67e22", 4: "#e74c3c"}
RIESGO_ALTO = {3, 4}  # D y F son categorías de riesgo

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/graduation-cap.png", width=80)
    st.title("Riesgo Académico")
    st.caption("Diplomado — Desarrollo Web para Analítica de Datos")
    st.divider()
    st.markdown("**Modelo activo**")
    st.code(metadata["modelo"], language=None)
    st.markdown(f"**{metadata['metrica_principal'].replace('_',' ').title()}**")
    st.metric(label="", value=f"{metadata['valor_metrica']:.4f}")
    st.markdown(f"**Accuracy:** `{metadata['accuracy']:.4f}`")
    st.divider()
    st.caption(f"Dataset: {len(df)} registros · {df.shape[1]} variables")
    st.caption(f"Entrenado: {metadata['fecha_entrenamiento']}")

# ── Pestañas principales ───────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📊 Análisis Exploratorio", "🔮 Predicción de Riesgo"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — ANÁLISIS EXPLORATORIO
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    st.header("Exploración del Dataset de Rendimiento Estudiantil")
    st.markdown(
        "Visualización interactiva de los factores asociados al rendimiento académico. "
        "Use los filtros para explorar subgrupos específicos."
    )

    # ── Filtros interactivos ──
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filtro_clase = st.multiselect(
            "Filtrar por categoría de rendimiento",
            options=list(CLASES.keys()),
            default=list(CLASES.keys()),
            format_func=lambda x: CLASES[x],
        )
    with col_f2:
        filtro_tutoria = st.multiselect(
            "Tutoría adicional",
            options=[0, 1],
            default=[0, 1],
            format_func=lambda x: "Sí" if x == 1 else "No",
        )
    with col_f3:
        filtro_extracurr = st.multiselect(
            "Actividades extracurriculares",
            options=[0, 1],
            default=[0, 1],
            format_func=lambda x: "Sí" if x == 1 else "No",
        )

    df_filtrado = df[
        df["GradeClass"].isin(filtro_clase) &
        df["Tutoring"].isin(filtro_tutoria) &
        df["Extracurricular"].isin(filtro_extracurr)
    ]
    st.caption(f"Registros visibles: **{len(df_filtrado)}** de {len(df)}")

    st.divider()

    # ── Visualización 1: Distribución de la variable objetivo ──
    st.subheader("1. Distribución de Categorías de Rendimiento")
    col1, col2 = st.columns([2, 1])
    with col1:
        dist = df_filtrado["GradeClass"].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(7, 3.5))
        bars = ax.bar(
            [CLASES[i].split("—")[0].strip() for i in dist.index],
            dist.values,
            color=[COLORES_CLASE[i] for i in dist.index],
            edgecolor="white", linewidth=0.8
        )
        for bar, val in zip(bars, dist.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                    f"{val}\n({val/len(df_filtrado)*100:.1f}%)",
                    ha="center", va="bottom", fontsize=8)
        ax.set_title("Frecuencia por Categoría de Rendimiento", fontsize=11)
        ax.set_ylabel("Cantidad de estudiantes")
        ax.set_xlabel("Categoría")
        sns.despine()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    with col2:
        st.markdown("**Resumen del filtro actual**")
        for cls_id in sorted(df_filtrado["GradeClass"].unique()):
            n = (df_filtrado["GradeClass"] == cls_id).sum()
            st.markdown(f"- {CLASES[cls_id]}: **{n}**")

    # ── Visualización 2: StudyTime y Absences por categoría ──
    st.subheader("2. Horas de Estudio y Ausencias por Categoría")
    col3, col4 = st.columns(2)
    with col3:
        fig2, ax2 = plt.subplots(figsize=(6, 3.5))
        for cls_id in sorted(df_filtrado["GradeClass"].unique()):
            subset = df_filtrado[df_filtrado["GradeClass"] == cls_id]["StudyTimeWeekly"]
            ax2.hist(subset, alpha=0.6, bins=12,
                     label=CLASES[cls_id].split("—")[0].strip(),
                     color=COLORES_CLASE[cls_id])
        ax2.set_title("Horas de Estudio Semanales por Categoría")
        ax2.set_xlabel("Horas/semana")
        ax2.set_ylabel("Frecuencia")
        ax2.legend(fontsize=7)
        sns.despine()
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()
    with col4:
        fig3, ax3 = plt.subplots(figsize=(6, 3.5))
        for cls_id in sorted(df_filtrado["GradeClass"].unique()):
            subset = df_filtrado[df_filtrado["GradeClass"] == cls_id]["Absences"]
            ax3.hist(subset, alpha=0.6, bins=12,
                     label=CLASES[cls_id].split("—")[0].strip(),
                     color=COLORES_CLASE[cls_id])
        ax3.set_title("Ausencias por Categoría")
        ax3.set_xlabel("Número de ausencias")
        ax3.set_ylabel("Frecuencia")
        ax3.legend(fontsize=7)
        sns.despine()
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()

    # ── Visualización 3: Apoyo parental vs rendimiento ──
    st.subheader("3. Apoyo Parental y Tutorías vs Rendimiento")
    col5, col6 = st.columns(2)
    PARENTAL_LABELS = {0: "Ninguno", 1: "Bajo", 2: "Moderado", 3: "Alto", 4: "Muy alto"}

    with col5:
        tabla_parental = df_filtrado.groupby(["ParentalSupport", "GradeClass"]).size().unstack(fill_value=0)
        fig4, ax4 = plt.subplots(figsize=(6, 3.5))
        tabla_parental.plot(kind="bar", stacked=True, ax=ax4,
                            color=[COLORES_CLASE[c] for c in tabla_parental.columns],
                            edgecolor="white")
        ax4.set_xticklabels([PARENTAL_LABELS.get(int(x.get_text()), x.get_text())
                             for x in ax4.get_xticklabels()], rotation=30)
        ax4.set_title("Apoyo Parental vs Categoría de Rendimiento")
        ax4.set_xlabel("Nivel de apoyo parental")
        ax4.set_ylabel("Número de estudiantes")
        ax4.legend([CLASES[c].split("—")[0].strip() for c in tabla_parental.columns],
                   fontsize=7, title="Categoría")
        sns.despine()
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close()

    with col6:
        tutoria_grade = df_filtrado.groupby(["Tutoring", "GradeClass"]).size().unstack(fill_value=0)
        fig5, ax5 = plt.subplots(figsize=(6, 3.5))
        tutoria_grade.plot(kind="bar", stacked=False, ax=ax5,
                           color=[COLORES_CLASE[c] for c in tutoria_grade.columns],
                           edgecolor="white", width=0.6)
        ax5.set_xticklabels(["Sin tutoría", "Con tutoría"], rotation=0)
        ax5.set_title("Tutoría Adicional vs Categoría de Rendimiento")
        ax5.set_xlabel("Tutoría")
        ax5.set_ylabel("Número de estudiantes")
        ax5.legend([CLASES[c].split("—")[0].strip() for c in tutoria_grade.columns],
                   fontsize=7, title="Categoría")
        sns.despine()
        plt.tight_layout()
        st.pyplot(fig5)
        plt.close()

    # ── Estadísticas descriptivas ──
    with st.expander("📋 Ver estadísticas descriptivas del filtro actual"):
        st.dataframe(
            df_filtrado[["StudyTimeWeekly", "Absences", "Age", "ParentalSupport", "GradeClass"]]
            .describe().round(2),
            use_container_width=True
        )

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — PREDICCIÓN
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    st.header("Predicción de Riesgo Académico")
    st.caption(
        f"Modelo: **{metadata['modelo']}** | "
        f"{metadata['metrica_principal'].replace('_',' ').title()}: **{metadata['valor_metrica']:.4f}** | "
        f"Accuracy: **{metadata['accuracy']:.4f}**"
    )

    st.info(
        "⚠️ **Advertencia ética:** El resultado es una estimación generada por el modelo. "
        "Debe ser revisado por un coordinador o docente responsable antes de tomar "
        "cualquier decisión pedagógica. El modelo no reemplaza el criterio profesional."
    )

    st.divider()
    st.subheader("Ingrese los datos del estudiante")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("**Variables académicas**")
        study_time     = st.slider("Horas de estudio semanales", 0.0, 20.0, 7.0, 0.5,
                                    help="Horas promedio dedicadas al estudio fuera de clase")
        absences       = st.slider("Número de ausencias", 0, 30, 5,
                                    help="Total de inasistencias registradas en el año")
        tutoring       = st.selectbox("¿Recibe tutorías adicionales?", [0, 1],
                                       format_func=lambda x: "Sí" if x == 1 else "No")
        parental_sup   = st.selectbox("Nivel de apoyo parental", [0, 1, 2, 3, 4],
                                       format_func=lambda x: {0:"Ninguno",1:"Bajo",2:"Moderado",3:"Alto",4:"Muy alto"}[x])

    with col_b:
        st.markdown("**Variables demográficas**")
        age            = st.slider("Edad del estudiante", 15, 18, 16)
        gender         = st.selectbox("Género", [0, 1],
                                       format_func=lambda x: "Masculino" if x == 0 else "Femenino")
        ethnicity      = st.selectbox("Grupo étnico", [0, 1, 2, 3],
                                       format_func=lambda x: f"Grupo {x}")
        parental_edu   = st.selectbox("Nivel educativo de los padres", [0, 1, 2, 3, 4],
                                       format_func=lambda x: {0:"Ninguno",1:"Secundaria",2:"Técnico",3:"Universidad",4:"Posgrado"}[x])

    with col_c:
        st.markdown("**Actividades extracurriculares**")
        extracurr      = st.selectbox("¿Participa en actividades extracurriculares?", [0, 1],
                                       format_func=lambda x: "Sí" if x == 1 else "No")
        sports         = st.selectbox("¿Participa en deportes?", [0, 1],
                                       format_func=lambda x: "Sí" if x == 1 else "No")
        music          = st.selectbox("¿Participa en música?", [0, 1],
                                       format_func=lambda x: "Sí" if x == 1 else "No")
        volunteering   = st.selectbox("¿Participa en voluntariado?", [0, 1],
                                       format_func=lambda x: "Sí" if x == 1 else "No")

    st.divider()

    if st.button("🔮 Generar predicción", type="primary", use_container_width=True):
        # Construir vector de entrada en el mismo orden que el modelo
        feature_order = metadata["variables_entrada"]
        input_data = {
            "Age":               age,
            "Gender":            gender,
            "Ethnicity":         ethnicity,
            "ParentalEducation": parental_edu,
            "StudyTimeWeekly":   study_time,
            "Absences":          absences,
            "Tutoring":          tutoring,
            "ParentalSupport":   parental_sup,
            "Extracurricular":   extracurr,
            "Sports":            sports,
            "Music":             music,
            "Volunteering":      volunteering,
        }
        X_input = pd.DataFrame([input_data])[feature_order]

        # Escalar variables continuas
        X_sc = X_input.copy()
        X_sc[["StudyTimeWeekly", "Absences", "Age"]] = scaler.transform(
            X_input[["StudyTimeWeekly", "Absences", "Age"]]
        )

        # Predicción
        pred_clase  = int(modelo.predict(X_sc)[0])
        pred_proba  = modelo.predict_proba(X_sc)[0]
        confianza   = float(pred_proba[pred_clase]) * 100

        # ── Resultado principal ──
        st.divider()
        st.subheader("Resultado de la Predicción")

        col_res1, col_res2 = st.columns([1, 2])
        with col_res1:
            color = COLORES_CLASE[pred_clase]
            st.markdown(
                f"""
                <div style="background:{color}22; border-left: 6px solid {color};
                     padding: 18px 20px; border-radius: 8px; text-align:center;">
                  <div style="font-size:2.8rem; font-weight:bold; color:{color};">
                    {CLASES[pred_clase].split("—")[0].strip()}
                  </div>
                  <div style="font-size:1rem; color:#555;">
                    {CLASES[pred_clase].split("—")[1].strip()}
                  </div>
                  <div style="margin-top:8px; font-size:0.9rem; color:#777;">
                    Confianza: <strong>{confianza:.1f}%</strong>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_res2:
            # Mensaje interpretativo
            if pred_clase in RIESGO_ALTO:
                st.error(
                    f"🚨 **Alerta de riesgo académico:** El modelo clasifica al estudiante "
                    f"en la categoría **{CLASES[pred_clase]}**. "
                    "Se recomienda activar rutas de acompañamiento pedagógico: "
                    "seguimiento docente, citación a padres y asignación de tutorías de refuerzo."
                )
            elif pred_clase == 2:
                st.warning(
                    f"⚠️ **Rendimiento promedio:** Categoría **{CLASES[pred_clase]}**. "
                    "El estudiante no está en riesgo inmediato, pero puede beneficiarse "
                    "de mayor apoyo en estudio y asistencia regular."
                )
            else:
                st.success(
                    f"✅ **Buen rendimiento:** Categoría **{CLASES[pred_clase]}**. "
                    "El perfil del estudiante es consistente con un desempeño académico satisfactorio. "
                    "Se recomienda mantener el seguimiento habitual."
                )

            # Distribución de probabilidades
            st.markdown("**Probabilidad por categoría:**")
            for cls_id, prob in enumerate(pred_proba):
                label = CLASES[cls_id].split("—")[0].strip()
                st.progress(float(prob), text=f"{label}: {prob*100:.1f}%")

        # ── Nota ética debajo del resultado ──
        st.info(
            "🔍 **Nota:** Este resultado es una estimación basada en patrones estadísticos. "
            "El modelo no tiene acceso al historial completo del estudiante ni a factores "
            "contextuales. La decisión final siempre debe tomarla un profesional educativo."
        )

        # ── Comparación con dataset ──
        with st.expander("📊 Ver comparación con el dataset"):
            st.markdown(f"Estudiantes similares (misma categoría predicha — **{CLASES[pred_clase]}**):")
            similares = df[df["GradeClass"] == pred_clase][
                ["StudyTimeWeekly", "Absences", "Tutoring", "ParentalSupport"]
            ].describe().round(2)
            st.dataframe(similares, use_container_width=True)

    else:
        st.markdown(
            "<div style='text-align:center; color:#aaa; margin-top:40px;'>"
            "Complete los campos y presione <strong>Generar predicción</strong>."
            "</div>",
            unsafe_allow_html=True,
        )
