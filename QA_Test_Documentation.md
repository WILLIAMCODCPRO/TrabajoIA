# Plan de Pruebas Unitarias

## Resumen
Este documento describe los casos de prueba diseñados para los módulos `estudiantes.py` y `computadores.py`.
Cada caso incluye objetivo, datos de entrada, resultado esperado y el tipo de prueba.

---

## Módulo `estudiantes.py`

### Funcionalidades principales
- Cargar y guardar datos desde/hacia `campers.json`.
- Validar formatos de correo electrónico.
- Registrar nuevos campers.
- Listar campers existentes.
- Actualizar datos de un camper por ID.
- Eliminar campers por ID.

### Casos de prueba

| Caso de prueba | Descripción | Datos de entrada | Resultado esperado | Tipo de prueba |
|---|---|---|---|---|
| `CargaDatos_SinArchivo_RetornaEstructuraVacía` | Verificar que al no existir archivo se devuelve estructura inicial. | Archivo JSON ausente | `{'campers': [], 'ultimo_id': 0}` | Positiva |
| `CargaDatos_JsonInvalido_RetornaEstructuraVacía` | Validar comportamiento ante archivo JSON corrupto. | Archivo con contenido inválido | `{'campers': [], 'ultimo_id': 0}` | Borde |
| `ValidarEmail_Valido_RetornaTrue` | Aceptar un correo con formato correcto. | `usuario@dominio.com` | `True` | Positiva |
| `ValidarEmail_Invalido_RetornaFalse` | Rechazar correo con formato incorrecto. | `usuario.com` | `False` | Negativa |
| `RegistrarCamper_CamperValido_CreaRegistro` | Registrar un nuevo camper con datos correctos. | Nombre, documento numérico, email válido | Registro guardado con `estado: Activo` y `ultimo_id` incrementado | Positiva |
| `RegistrarCamper_CamposVacios_MuestraError` | Rechazar registro si falta algún campo. | Nombre vacío | No hay guardado | Negativa |
| `RegistrarCamper_DocumentoNoNumerico_MuestraError` | Rechazar documento no numérico. | `ABC123` | No hay guardado | Negativa |
| `RegistrarCamper_EmailInvalido_MuestraError` | Rechazar email inválido. | `correo@` | No hay guardado | Negativa |
| `ActualizarCamper_DatosValidos_ActualizaRegistro` | Actualizar nombre, email y estado válidos. | ID existente, nuevo nombre, email válido, estado válido | Datos actualizados en JSON | Positiva |
| `ActualizarCamper_EmailInvalido_NoActualizaEmail` | Mantener email anterior si el email nuevo es inválido. | ID existente, email inválido | Email original preservado | Negativa |
| `EliminarCamper_IDExistente_EliminaRegistro` | Eliminar camper existente por ID. | ID válido | Registro eliminado del archivo | Positiva |
| `EliminarCamper_IDNoExistente_MuestraError` | Manejar intento de eliminación de ID inexistente. | ID no válido | No hay cambios | Negativa |

---

## Módulo `computadores.py`

### Funcionalidades principales
- Cargar y guardar datos desde/hacia `computadoras.json`.
- Seleccionar estado a través de opciones numéricas.
- Registrar nuevos computadores.
- Listar inventario de computadores.
- Actualizar datos de un computador por ID.
- Eliminar computadores por ID.

### Casos de prueba

| Caso de prueba | Descripción | Datos de entrada | Resultado esperado | Tipo de prueba |
|---|---|---|---|---|
| `CargaDatos_SinArchivo_RetornaEstructuraVacía` | Verificar que al no existir archivo se devuelve estructura inicial. | Archivo JSON ausente | `{'computadores': [], 'ultimo_id': 0}` | Positiva |
| `CargaDatos_JsonInvalido_RetornaEstructuraVacía` | Validar comportamiento ante archivo JSON corrupto. | Archivo con contenido inválido | `{'computadores': [], 'ultimo_id': 0}` | Borde |
| `SeleccionarEstado_OpcionValida_RetornaEstado` | Traducir opción numérica válida al estado correspondiente. | `1` | `Disponible` | Positiva |
| `SeleccionarEstado_OpcionInvalida_RetornaNone` | Manejar opción de estado incorrecta. | `0` | `None` | Negativa |
| `RegistrarComputador_DatosValidos_CreaRegistro` | Registrar un equipo con datos completos y válidos. | Inventario, marca, modelo, opción de estado válida | Registro guardado con ID y estado correcto | Positiva |
| `RegistrarComputador_InventarioNegativo_MuestraError` | Rechazar número de inventario negativo o inválido. | `-5` | No hay guardado | Negativa |
| `ActualizarComputador_DatosValidos_ActualizaRegistro` | Actualizar marca, modelo y estado de un equipo existente. | ID válido, datos nuevos, estado válido | Datos actualizados en JSON | Positiva |
| `ActualizarComputador_EstadoInvalido_NoCambiaEstado` | No actualizar el estado cuando la opción es inválida. | ID válido, opción inválida | Estado anterior preservado | Borde |
| `EliminarComputador_IDExistente_EliminaRegistro` | Eliminar equipo existente por ID. | ID válido | Registro eliminado del archivo | Positiva |
| `EliminarComputador_IDNoExistente_MuestraError` | Manejar intento de eliminación de ID inexistente. | ID inválido | No hay cambios | Negativa |

---

## Notas de implementación

- Las pruebas deben ejecutarse en un entorno aislado usando archivos temporales para evitar efectos colaterales.
- Se recomienda utilizar `unittest` con `unittest.mock.patch` para simular entradas de usuario y capturar salidas.
- Cada caso de prueba debe ser independiente y reutilizar un `setUp`/`tearDown` para limpiar el estado.
- Los nombres de prueba son descriptivos y siguen la convención `Accion_Condicion_Resultado`.
