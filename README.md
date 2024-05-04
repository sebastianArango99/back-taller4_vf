# API REST para Gestión de Tareas de Conversión

Este proyecto implementa una API REST para la gestión de tareas de conversión de formatos de archivos. En el archivo PDF llamado Entrega 1 Arquitectura, consideraciones y conclusiones se pueden encontrar la información general de la aplicación. A continuación se detallan los endpoints disponibles:

## /api/auth/signup

**Descripción**: Permite crear una cuenta de usuario, con los campos usuario, correo electrónico y contraseña. El usuario y el correo electrónico deben ser únicos en la plataforma, y la contraseña debe seguir unos lineamientos mínimos de seguridad. Además, se solicita dos veces la contraseña para confirmar su correcta ingresión.

- **Método**: POST
- **Retorno**: application/json, con un mensaje de confirmación si la cuenta pudo o no ser creada.
- **Parámetros**:
  - username (String)
  - password1 (String)
  - email (String)

## /api/auth/login

**Descripción**: Permite recuperar el token de autorización para consumir los recursos del API suministrando un nombre de usuario y una contraseña correcta de una cuenta registrada.

- **Método**: POST
- **Retorno**: application/json, con un token de autorización.
- **Parámetros**:
  - username (String)
  - password (String)

## /api/tasks

**Descripción**: Permite recuperar todas las tareas de conversión de un usuario autorizado en la aplicación.

- **Método**: GET
- **Retorno**: application/json, con un diccionario de todas las tareas de conversión de un usuario.
- **Parámetros de autorización**: Bearer Token.
- **Parámetros de Consulta**:
  - max (int): Parámetro opcional que filtra la cantidad de resultados de una consulta.
  - order (int): Especifica si los resultados se ordenan de forma ascendente (0) o de forma descendente (1) según el ID de la tarea.

## /api/tasks

**Descripción**: Permite crear una nueva tarea de conversión de formatos. El usuario requiere autorización.

- **Método**: POST
- **Retorno**: application/json, con un mensaje de confirmación indicando que la tarea fue creada.
- **Parámetros**:
  - fileName (File): Ruta del archivo a subir a la aplicación.
  - newFormat (String): Formato al que desea cambiar el archivo cargado.

**Nota**: Los campos id, timeStamp y status se generan automáticamente en la aplicación. El id es un campo único y auto-numérico. El timeStamp corresponde a la fecha y hora de carga del archivo. Finalmente, el status corresponde a la notificación en la aplicación si el archivo ya fue o no procesado. Para los archivos cargados su estado por defecto es uploaded, en el momento de realizar la conversión este campo pasa a processed.

## /api/tasks/<int:id_task>

**Descripción**: Permite recuperar la información de una tarea en la aplicación. El usuario requiere autorización.

- **Método**: GET
- **Retorno**: application/json, con un diccionario de la tarea especificada por un usuario.
- **Parámetros de autorización**: Bearer Token.

## /api/tasks/<int:id_task>

**Descripción**: Permite eliminar una tarea en la aplicación. El usuario requiere autorización.

- **Método**: DELETE
- **Retorno**: Ninguno.
- **Parámetros de autorización**: Bearer Token.

## /api/files/<filename>

**Descripción**: Permite recuperar el archivo original o procesado.

- **Método**: GET
- **Retorno**: Retorna el archivo.
- **Parámetros de autorización**: Bearer Token.

---
*Universidad de los Andes*
