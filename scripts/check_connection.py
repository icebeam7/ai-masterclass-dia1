"""Prueba real de conectividad y autenticación (puede generar consumo)."""
from app.foundry import configuration, query_model

if __name__ == "__main__":
    endpoint, model = configuration()
    print(f"Project endpoint: {endpoint}")
    print(f"Implementación: {model}")
    result = query_model("Responde solo en español.", "Escribe únicamente: Conexión correcta")
    print("Modelo que respondió:", result.model)
    print("Texto:", result.text)
    print("Response ID:", result.response_id)
