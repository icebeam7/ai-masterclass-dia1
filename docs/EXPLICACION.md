# Explicación

Esta guía acompaña el bloque práctico de la **primera clase**.

## Contenido

**Introducción:** Enviaremos peticiones reales a un modelo desplegado en Microsoft Foundry desde una aplicación web sencilla. Lo importante es observar cómo cambia el resultado dependiendo de las instrucciones y la información disponible.

**Ejercicio 1:** Tenemos una solicitud de entrega. El modelo puede redactar una respuesta convincente, pero ¿puede confirmar el estado del pedido? No, porque no está conectado al sistema logístico. Debemos distinguir calidad lingüística de exactitud factual.

**Ejercicio 2:** Incorporamos una política interna y un formato objetivo. Revisemos si el resultado respeta el límite de palabras, evita prometer fechas y propone pasos verificables. Un prompt mejorado puede ayudar, pero no garantiza cumplimiento.

**Ejercicio 3:** Muchas aplicaciones necesitan datos estructurados para crear un ticket o clasificar solicitudes. Vamos a solicitar un JSON y validarlo con Python. Que sea JSON válido no significa que la categoría o prioridad sean correctas: necesitamos criterios y evaluación humana o automatizada adicionales.

**Ejercicio 4:** La política nos dice cuánto tardamos en escalar un incidente, pero no informa cuándo llega un pedido específico. Un asistente responsable debe reconocer la ausencia de ese dato. 

En la segunda clase veremos cómo recuperar información desde documentos corporativos con RAG.

## Preguntas de aprendizaje

- ¿Qué respuesta confiarías en enviar sin revisión humana y por qué?
- ¿Qué controles necesitaríamos antes de conectar el asistente a un CRM?
- ¿El JSON válido es necesariamente una clasificación acertada?
- ¿Qué cambia si el cliente incluye datos personales reales?

## Notas operativas

- Deja abierta una terminal autenticada con `az login`.
- Mostrar un prompt en pantalla no expone secretos.
- Usualmente no se obtiene la misma salida en cada ejecución: los modelos son probabilísticos y pueden cambiar según modelo y versión.
- El botón **Continuar** depende de la compatibilidad del modelo/servicio con `previous_response_id`.
- El modo instructor permite editar las instrucciones para explorar variantes. 
- El modo participante es guiado.
