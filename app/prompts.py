"""Datos de demostración 100 % ficticios; no son documentos reales."""

SAMPLE_REQUEST = """Hola, soy Ana López, de Contoso Retail.
Nuestro pedido CR-1042 tenía entrega prevista para el 12 de marzo y todavía no llegó.
¿Podrían confirmar el estado y cómo solicitar una actualización? Gracias."""

POLICY = """POLÍTICA DE ATENCIÓN A CLIENTES:
- Nunca confirmar un estado de envío sin consultar el sistema logístico.
- No prometer fechas de entrega sin datos verificables.
- Solicitar el número de pedido si falta.
- Escalar incidentes de entrega al equipo de logística en un máximo de 1 día hábil.
- No pedir datos sensibles ni contraseñas por correo.
- Mantener tono empático y profesional."""

BASE_SYSTEM = "Eres un asistente empresarial. Responde en español, con claridad. Nunca inventes datos, estados de pedidos ni fechas."

EXERCISES = {
    "01 · Prompt inicial": {
        "goal": "Ver qué hace un LLM con instrucciones sencillas.",
        "system": BASE_SYSTEM,
        "user": f"Redacta una respuesta a este cliente:\n\n{SAMPLE_REQUEST}",
    },
    "02 · Prompt mejorado": {
        "goal": "Comparar instrucciones vagas con restricciones empresariales explícitas.",
        "system": BASE_SYSTEM + " Usa exclusivamente la política proporcionada para interpretar las acciones permitidas.",
        "user": (
            "Redacta un correo al cliente con estas condiciones: máximo 130 palabras; "
            "saludo, empatía, 2 pasos siguientes y despedida. No inventes un estado de envío. "
            "Si faltan datos, explica cómo se verificará la información.\n\n"
            f"POLÍTICA:\n{POLICY}\n\nSOLICITUD:\n{SAMPLE_REQUEST}"
        ),
    },
    "03 · Clasificación y JSON": {
        "goal": "Pedir una salida estructurada y validarla localmente con Python.",
        "system": "Clasifica solicitudes empresariales. Devuelve exclusivamente JSON válido, sin fences ni comentarios.",
        "user": (
            "Analiza la solicitud y devuelve un objeto JSON con las claves exactas: "
            '"categoria" (entrega|facturacion|soporte|otro), '
            '"prioridad" (baja|media|alta), '
            '"resumen" (string), "requiere_revision_humana" (boolean). '
            "No inventes hechos.\n\nSOLICITUD:\n" + SAMPLE_REQUEST
        ),
    },
    "04 · Conocimiento limitado": {
        "goal": "Observar grounding básico y reconocer límites sin RAG.",
        "system": "Responde únicamente con base en el texto proporcionado. Si no aparece un hecho, indica 'No consta en la política'.",
        "user": (
            f"POLÍTICA:\n{POLICY}\n\n"
            "Preguntas: (1) ¿Cuál es el tiempo máximo de escalamiento? "
            "(2) ¿Cuál es la fecha exacta de entrega del pedido CR-1042? "
            "(3) ¿Se puede pedir la contraseña al cliente?"
        ),
    },
}

FOLLOWUP = "Resume tu respuesta anterior en tres puntos, sin añadir hechos nuevos."

EXPECTED_KEYS = {"categoria", "prioridad", "resumen", "requiere_revision_humana"}


def validate_classification(raw: str) -> tuple[bool, str]:
    import json
    import re

    cleaned = raw.strip()
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.IGNORECASE)
    try:
        obj = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        return False, f"No es JSON válido: {exc}"
    if not isinstance(obj, dict) or set(obj) != EXPECTED_KEYS:
        return False, f"Las claves deben ser exactamente: {sorted(EXPECTED_KEYS)}"
    if obj["categoria"] not in ("entrega", "facturacion", "soporte", "otro"):
        return False, "Categoría no válida"
    if obj["prioridad"] not in ("baja", "media", "alta"):
        return False, "Prioridad no válida"
    if not isinstance(obj["resumen"], str) or not obj["resumen"].strip():
        return False, "El resumen debe ser texto no vacío"
    if not isinstance(obj["requiere_revision_humana"], bool):
        return False, "requiere_revision_humana debe ser booleano"
    return True, "JSON válido y esquema básico correcto (no garantiza exactitud semántica)."
