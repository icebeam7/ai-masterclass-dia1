"""Integración real con Microsoft Foundry mediante Responses API.
"""
import os
from dataclasses import dataclass

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class ModelResult:
    text: str
    response_id: str
    model: str
    input_tokens: int | None
    output_tokens: int | None


def configuration() -> tuple[str, str]:
    endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT", "").strip()
    model = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME", "").strip()
    if not endpoint or "TU-RECURSO" in endpoint or "TU-PROYECTO" in endpoint:
        raise ValueError("Configura AZURE_AI_PROJECT_ENDPOINT en .env con tu Project endpoint real.")
    if not endpoint.startswith("https://") or "/api/projects/" not in endpoint:
        raise ValueError("El endpoint debe tener formato https://...services.ai.azure.com/api/projects/...")
    if not model:
        raise ValueError("Configura AZURE_AI_MODEL_DEPLOYMENT_NAME en .env.")
    return endpoint, model


def query_model(system: str, user: str, previous_response_id: str | None = None) -> ModelResult:
    endpoint, model = configuration()
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=True)
    try:
        with AIProjectClient(endpoint=endpoint, credential=credential) as project:
            with project.get_openai_client() as client:
                kwargs = {"model": model, "instructions": system, "input": user}
                if previous_response_id:
                    kwargs["previous_response_id"] = previous_response_id
                response = client.responses.create(**kwargs)
                usage = getattr(response, "usage", None)
                return ModelResult(
                    text=response.output_text or "[No se recibió texto; revisa la respuesta del modelo]",
                    response_id=response.id,
                    model=response.model or model,
                    input_tokens=getattr(usage, "input_tokens", None),
                    output_tokens=getattr(usage, "output_tokens", None),
                )
    finally:
        credential.close()
