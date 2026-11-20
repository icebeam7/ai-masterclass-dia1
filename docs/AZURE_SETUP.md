# Paso a paso: preparar Microsoft Foundry

## 1. Preparar acceso a Azure

1. Entra en [Microsoft Foundry](https://ai.azure.com/) con tu suscripción de Azure.

2. Comprueba que tienes una suscripción activa y permisos suficientes para crear un recurso/proyecto y hacer despliegues de modelos.

3. Comprueba los **costos, cuotas y disponibilidad regional** antes de empezar. No todas las suscripciones permiten todos los modelos.

4. Crea un **proyecto Foundry (nuevo)** siguiendo el asistente de la interfaz. Si ya existe uno adecuado, reutilízalo.

## 2. Desplegar el modelo

1. En tu proyecto, localiza el menú **Build** y elige **Models**. También puedes utilizar el **Model catalog**.

2. Busca/selecciona un modelo de texto compatible con **Responses API**, por ejemplo `gpt-5-mini` cuando esté disponible y permitido en tu suscripción.

3. Despliega el modelo y registra **el nombre de la implementación**, no solo el nombre comercial del modelo (aunque es el valor predeterminado). Si eliges otro nombre (por ejemplo `clase1-llm`), usa exactamente ese valor en `.env`.

4. Al implementar el modelo asígnale una capacidad de inferencia suficiente. 

## 3. Copiar endpoint del **proyecto**

Desde la página de información del proyecto, copia el **Project endpoint** de tipo:

```text
https://NOMBRE-RECURSO.services.ai.azure.com/api/projects/NOMBRE-PROYECTO
```

## 4. Autenticación con Microsoft Entra ID

Abre una terminal. Ejecuta este comando y sigue el flujo:

```bash
az login
```

Te pedirá que elijas tu suscripción e inquilino (tenant).

Si el usuario no puede ejecutar inferencias, un administrador debe concederle el rol de **uso/inferencia correspondiente al recurso/proyecto Foundry**.

## 5. Configurar variables locales

```bash
cp .env.example .env
```

Abre `.env` y modifica estas dos variables de entorno:

```dotenv
AZURE_AI_PROJECT_ENDPOINT=https://mi-recurso.services.ai.azure.com/api/projects/mi-proyecto
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-5-mini
SAVE_RUNS=false
```

No compartas `.env` aunque esta muestra no use clave API: puede revelar información interna de tu entorno. Este proyecto no requiere secretos de aplicación.

## 6. Crear entorno virtual e instalar

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 7. Comprobar conexión real

```bash
python -m scripts.check_connection
```

Esta llamada consume tokens.

Verás `Conexión correcta` o una respuesta equivalente y un ID real del servicio. Si falla, consulta [`ERRORES.md`](ERRORES.md). 

## 8. Iniciar laboratorio

```bash
python -m streamlit run app/main.py
```

Usa la dirección local indicada por Streamlit. 

Continúa con [`DEMO.md`](DEMO.md).

## 9. Limpiar recursos después de la clase

Si creaste recursos exclusivamente para el laboratorio, elimina los despliegues o recursos en Azure cuando ya no se necesiten para evitar gastos y cumplir la política interna de costos. Revisa cualquier recurso compartido antes de borrarlo.
