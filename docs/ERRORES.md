# Solución de problemas

| Síntoma | Causa probable | Cómo resolverlo |
|---|---|---|
| `ValueError` endpoint | `.env` sin completar o URL equivocada | Copia el **Project endpoint** de Foundry, que termina en `/api/projects/NOMBRE` |
| `CredentialUnavailableError` | Sin identidad local | Ejecuta `az login`, confirma `az account show` y utiliza el mismo usuario autorizado |
| `AuthenticationFailed` / 401 | Sesión caducada o tenant equivocado | Repite `az login` si corresponde y verifica la cuenta |
| `PermissionDenied` / 403 | No tienes permisos de inferencia | Solicita rol mínimo apropiado sobre recurso/proyecto; puede tardar en propagarse |
| `NotFound` / 404 | Endpoint, nombre de implementación o ruta incorrectos | Copia el nombre **exacto de la implementación** y comprueba el proyecto |
| `RateLimitError` / 429 | Cuota o límites de solicitudes | Espera según `Retry-After`, baja concurrencia o solicita más cuota |
| `BadRequestError` / 400 | Modelo no soporta Responses API o `previous_response_id` | Cambia a un modelo compatible; no todos admiten las mismas características |
| Error TLS/red | Proxy o firewall corporativo | Comprueba acceso de salida HTTPS a Microsoft Foundry; consulta TI |
| Respuesta sin texto | Salida especial o error del proveedor | Comprueba modelo y configuración; prueba el smoke test y revisa logs del recurso |
| JSON inválido | El modelo generó texto adicional o estructura distinta | Refina el prompt o usa salida estructurada nativa con un modelo compatible; el validador local lo detecta |
| `ModuleNotFoundError` | Entorno virtual incorrecto | Activa `.venv` e instala `pip install -r requirements.txt` |

**Seguridad:** La interfaz evita imprimir el detalle de las excepciones potencialmente sensibles. Para diagnóstico en entornos controlados utiliza herramientas de Azure y trazas según las políticas de la organización. No compartas cadenas de conexión, tokens o secretos.
