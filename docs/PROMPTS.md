# Prompts utilizados en el laboratorio

Este documento recoge los mensajes enviados por la aplicación a Microsoft Foundry. Los textos se toman de `app/prompts.py` y se muestran separados por ejercicio.

Cada ejecución utiliza dos mensajes:

- **Mensaje de sistema:** instrucciones generales y restricciones.
- **Prompt / mensaje de usuario:** datos y tarea que debe resolver el modelo.

## Datos comunes

### Solicitud de ejemplo

```text
Hola, soy Ana López, de Contoso Retail.
Nuestro pedido CR-1042 tenía entrega prevista para el 12 de marzo y todavía no llegó.
¿Podrían confirmar el estado y cómo solicitar una actualización? Gracias.
```

### Política de atención al cliente

```text
POLÍTICA DE ATENCIÓN A CLIENTES:
- Nunca confirmar un estado de envío sin consultar el sistema logístico.
- No prometer fechas de entrega sin datos verificables.
- Solicitar el número de pedido si falta.
- Escalar incidentes de entrega al equipo de logística en un máximo de 1 día hábil.
- No pedir datos sensibles ni contraseñas por correo.
- Mantener tono empático y profesional.
```

## Ejercicio 1 — Prompt inicial

### Mensaje de sistema

```text
Eres un asistente empresarial. Responde en español, con claridad. Nunca inventes datos, estados de pedidos ni fechas.
```

### Prompt

```text
Redacta una respuesta a este cliente:

Hola, soy Ana López, de Contoso Retail.
Nuestro pedido CR-1042 tenía entrega prevista para el 12 de marzo y todavía no llegó.
¿Podrían confirmar el estado y cómo solicitar una actualización? Gracias.
```

## Ejercicio 2 — Prompt mejorado

### Mensaje de sistema

```text
Eres un asistente empresarial. Responde en español, con claridad. Nunca inventes datos, estados de pedidos ni fechas. Usa exclusivamente la política proporcionada para interpretar las acciones permitidas.
```

### Prompt

```text
Redacta un correo al cliente con estas condiciones: máximo 130 palabras; saludo, empatía, 2 pasos siguientes y despedida. No inventes un estado de envío. Si faltan datos, explica cómo se verificará la información.

POLÍTICA:
POLÍTICA DE ATENCIÓN A CLIENTES:
- Nunca confirmar un estado de envío sin consultar el sistema logístico.
- No prometer fechas de entrega sin datos verificables.
- Solicitar el número de pedido si falta.
- Escalar incidentes de entrega al equipo de logística en un máximo de 1 día hábil.
- No pedir datos sensibles ni contraseñas por correo.
- Mantener tono empático y profesional.

SOLICITUD:
Hola, soy Ana López, de Contoso Retail.
Nuestro pedido CR-1042 tenía entrega prevista para el 12 de marzo y todavía no llegó.
¿Podrían confirmar el estado y cómo solicitar una actualización? Gracias.
```

## Ejercicio 3 — Clasificación y JSON

### Mensaje de sistema

```text
Clasifica solicitudes empresariales. Devuelve exclusivamente JSON válido, sin fences ni comentarios.
```

### Prompt

```text
Analiza la solicitud y devuelve un objeto JSON con las claves exactas: "categoria" (entrega|facturacion|soporte|otro), "prioridad" (baja|media|alta), "resumen" (string), "requiere_revision_humana" (boolean). No inventes hechos.

SOLICITUD:
Hola, soy Ana López, de Contoso Retail.
Nuestro pedido CR-1042 tenía entrega prevista para el 12 de marzo y todavía no llegó.
¿Podrían confirmar el estado y cómo solicitar una actualización? Gracias.
```

## Ejercicio 4 — Conocimiento limitado

### Mensaje de sistema

```text
Responde únicamente con base en el texto proporcionado. Si no aparece un hecho, indica 'No consta en la política'.
```

### Prompt

```text
POLÍTICA:
POLÍTICA DE ATENCIÓN A CLIENTES:
- Nunca confirmar un estado de envío sin consultar el sistema logístico.
- No prometer fechas de entrega sin datos verificables.
- Solicitar el número de pedido si falta.
- Escalar incidentes de entrega al equipo de logística en un máximo de 1 día hábil.
- No pedir datos sensibles ni contraseñas por correo.
- Mantener tono empático y profesional.

Preguntas: (1) ¿Cuál es el tiempo máximo de escalamiento? (2) ¿Cuál es la fecha exacta de entrega del pedido CR-1042? (3) ¿Se puede pedir la contraseña al cliente?
```

## Seguimiento

Disponible cuando se pulsa **Continuar respuesta anterior**. Se envía como nuevo mensaje de usuario junto con `previous_response_id`; se conservan las instrucciones de sistema y el contexto de la respuesta anterior.

```text
Resume tu respuesta anterior en tres puntos, sin añadir hechos nuevos.
```