"""Inicia: python -m streamlit run app/main.py"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from app.foundry import configuration, query_model
from app.prompts import EXERCISES, FOLLOWUP, validate_classification

st.set_page_config(page_title="AI Fundamentals · Laboratorio 1", page_icon="🧠", layout="wide")
st.title("Masterclass AI Fundamentals for Enterprise")
st.caption("Clase 1 · Laboratorio con Microsoft Foundry")

if "history" not in st.session_state:
    st.session_state.history = []
if "last_id" not in st.session_state:
    st.session_state.last_id = None
if "last_system" not in st.session_state:
    st.session_state.last_system = None
if "last_user" not in st.session_state:
    st.session_state.last_user = None

with st.sidebar:
    st.header("Preparación")
    try:
        _, configured_model = configuration()
        st.success(f"Configuración detectada · {configured_model}")
    except ValueError as exc:
        st.error(str(exc))
    st.info("Se usa tu sesión de Azure CLI mediante DefaultAzureCredential. Ejecuta `az login` antes de iniciar.")
    if st.button("Limpiar historial", use_container_width=True):
        st.session_state.history = []
        st.session_state.last_id = None
        st.session_state.last_system = None
        st.session_state.last_user = None
        st.rerun()
    st.markdown("**Guías:** `README.md` · `docs/EXPLICACION.md` · `docs/DEMO.md`")

mode = st.radio("Modo", ["Participante (guiado)", "Instructor (libre)"], horizontal=True)
exercise_name = st.selectbox("Selecciona el ejercicio", list(EXERCISES))
exercise = EXERCISES[exercise_name]
st.info(f"**Objetivo:** {exercise['goal']}")

if mode.startswith("Instructor"):
    a, b = st.columns(2)
    with a:
        system = st.text_area("Instrucciones de sistema", value=exercise["system"], height=180, key=f"system:{exercise_name}")
    with b:
        user = st.text_area("Prompt / mensaje", value=exercise["user"], height=180, key=f"user:{exercise_name}")
else:
    with st.expander("Ver instrucciones y prompt enviados al modelo", expanded=True):
        st.markdown("**Instrucciones de sistema**")
        st.code(exercise["system"], language="text")
        st.markdown("**Prompt**")
        st.code(exercise["user"], language="text")
    system, user = exercise["system"], exercise["user"]

st.caption("No introduzcas datos personales, secretos ni documentos reales. Cada ejecución puede generar consumo facturable en Azure.")


def run_request(instructions: str, prompt: str, parent_id=None, label=None):
    try:
        with st.spinner("Consultando el modelo real en Microsoft Foundry..."):
            result = query_model(instructions, prompt, parent_id)
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "exercise": label or exercise_name,
            "system": instructions,
            "prompt": prompt,
            "response": result.text,
            "response_id": result.response_id,
            "model": result.model,
            "input_tokens": result.input_tokens,
            "output_tokens": result.output_tokens,
        }
        st.session_state.history.append(record)
        st.session_state.last_id = result.response_id
        st.session_state.last_system = instructions
        st.session_state.last_user = prompt
        if os.getenv("SAVE_RUNS", "false").lower() == "true":
            p = Path("data/runs")
            p.mkdir(parents=True, exist_ok=True)
            (p / f"run-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}.json").write_text(
                json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        return record
    except Exception as exc:
        # No mostramos stack traces ni tokens en pantalla; el tipo guía el diagnóstico.
        st.error(f"No se pudo consultar Foundry ({type(exc).__name__}). Revisa conexión, permisos, cuota y despliegue. Consulta docs/ERRORES.md.")
        return None

c1, c2 = st.columns([1, 1])
with c1:
    if st.button("Ejecutar ejercicio", type="primary", use_container_width=True):
        run_request(system, user)
with c2:
    disabled = st.session_state.last_id is None
    if st.button("Continuar respuesta anterior", disabled=disabled, use_container_width=True,
                 help="Usa previous_response_id; la disponibilidad depende del modelo y del servicio."):
        run_request(st.session_state.last_system, FOLLOWUP, st.session_state.last_id, "Seguimiento")

if st.session_state.history:
    st.subheader("Resultados reales de esta sesión")
    for idx, record in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"{record['exercise']} · {record['timestamp'][:19]} UTC", expanded=idx == 1):
            st.markdown(record["response"])
            st.caption(f"Modelo: {record['model']} · Tokens de entrada: {record['input_tokens']} · Tokens de salida: {record['output_tokens']}")
            st.code(record["response_id"], language="text")
            if record["exercise"] == "03 · Clasificación y JSON":
                ok, message = validate_classification(record["response"])
                (st.success if ok else st.warning)(message)
    st.download_button("Exportar resultados JSON", data=json.dumps(st.session_state.history, indent=2, ensure_ascii=False),
                       file_name="laboratorio-clase1.json", mime="application/json")
else:
    st.info("Ejecuta el primer ejercicio para visualizar aquí las respuestas del modelo.")

st.divider()
st.markdown("**Para reflexionar:** ¿qué información está verificada?, ¿qué cambió al mejorar el prompt?, ¿cuándo se requiere revisión humana?")
