# AI Fundamentals for Enterprise — Clase 1
## Laboratorio utilizando Microsoft Foundry

Una aplicación **Streamlit** permite ejecutar cuatro experimentos contra un **modelo realmente desplegado en Microsoft Foundry** mediante **Responses API**. 

## Qué aprenderás

1. Generar texto con un LLM usando instrucciones y un prompt.
2. Mejorar la calidad de una respuesta con restricciones empresariales.
3. Solicitar una clasificación en JSON y validarla con Python.
4. Mostrar el riesgo de inferir datos que una política empresarial no contiene.

**Caso ficticio:** Un cliente pregunta por un pedido retrasado. Se emplean nombres, políticas y números inventados exclusivamente para el ejercicio. No se consulta un ERP ni se verifica realmente el estado del pedido.

## Requisitos

- Python 3.11 o 3.12, Git (opcional) y Azure CLI (`az`).
- Suscripción de Azure con permisos para crear/utilizar recursos de Microsoft Foundry.
- Un **proyecto Foundry (nuevo)** con un modelo compatible con **Responses API**, desplegado y accesible en la región elegida. La disponibilidad y los precios varían por región y modelo.
- Acceso a Internet. Se aplican costos de inferencia.

## Inicio rápido (macOS/Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
az login
az account set --subscription "TU_SUBSCRIPTION_ID"

# Edita .env con el endpoint de proyecto y el nombre de la implementación.
python -m scripts.check_connection
python -m streamlit run app/main.py
```

Abre la URL local que informa Streamlit (normalmente http://localhost:8501).

**Windows PowerShell**: crea entorno con `py -3.11 -m venv .venv`; actívalo con `.venv\Scripts\Activate.ps1`; copia con `Copy-Item .env.example .env`; usa los mismos comandos `python ...`.

**IMPORTANTE:** `.env` contiene configuración local y se excluye de Git. El backend usa **Microsoft Entra ID/DefaultAzureCredential**, no API keys; `az login` proporciona credenciales locales. No coloques secretos en el código ni subas archivos de datos reales.

## Documentación

- [`docs/AZURE_SETUP.md`](docs/AZURE_SETUP.md): configuración paso a paso del proyecto y la implementación de un modelo en Foundry.
- [`docs/EXPLICACION.md`](docs/EXPLICACION.md): Explicación de cada prueba.
- [`docs/DEMO.md`](docs/DEMO.md): ejercicios a realizar.
- [`docs/ERRORES.md`](docs/ERRORES.md): solución de problemas frecuentes.
- [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md): componentes, límites y recomendaciones.

## Estructura

```text
app/
  foundry.py       # Cliente real de Microsoft Foundry + Responses API
  main.py          # Web UI Streamlit: participante e instructor
  prompts.py       # Datos, prompts y validador de JSON
scripts/
  check_connection.py # Smoke test real (consume tokens)
tests/
  test_prompts.py  # Pruebas locales sin llamadas al modelo
data/               # Carpeta base; registros opcionales en data/runs/ (Git ignored)
docs/               # Guías
.env.example        # Configuración sin secretos
requirements.txt
```

## Pruebas

```bash
python -m pytest -q
```

Estas pruebas validan la lógica local; **no prueban el servicio Azure**. Para comprobar la integración, ejecuta `python -m scripts.check_connection` con un proyecto real.

## Compartir en GitHub

```bash
git init
git add .
git commit -m "Laboratorio clase 1: Foundry Responses"
# Crea un repositorio vacío en GitHub y ejecuta los comandos que te indique la plataforma.
```

Antes de publicar: revisa que no estén incluidos `.env`, `data/runs/`, documentos confidenciales ni identificadores internos. Puedes entregar la carpeta ZIP directamente a los alumnos.

## Referencias oficiales

- [Quickstart del SDK de Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/quickstarts/get-started-code)
- [SDK Python Azure AI Projects](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-projects-readme)
- [Responses API en Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses)

> Este repositorio es un laboratorio educativo para entorno local, no una aplicación lista para producción. Requiere autenticación y recursos reales proporcionados por el instructor o cada participante.
