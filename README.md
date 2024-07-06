# Análisis de Seguridad con IA

Este proyecto permite a los usuarios cargar un archivo CSV con datos de seguridad, seleccionar un prompt y proveedor de IA, procesar los datos y visualizar los resultados. La aplicación maneja tanto solicitudes GET como POST para la carga y procesamiento de archivos CSV.

## Caso de Uso 1: Cargar Archivo CSV

**Actor:** Usuario

### Descripción
El usuario carga un archivo CSV que contiene datos de seguridad para ser analizados.

### Precondiciones
- El usuario debe tener un archivo CSV válido con datos de seguridad.

### Flujo Principal
1. El usuario navega a la página principal de la aplicación.
2. El usuario localiza el campo para cargar archivos.
3. El usuario selecciona y carga el archivo CSV desde su dispositivo.
4. La aplicación lee y almacena el contenido del archivo CSV para su posterior procesamiento.

### Postcondiciones
- Los datos del archivo CSV se leen y están disponibles para su análisis.

### Flujo Alternativo
- Si el archivo cargado no es válido (por ejemplo, no es un archivo CSV), la aplicación muestra un mensaje de error y solicita al usuario que cargue un archivo válido.

## Caso de Uso 2: Seleccionar Prompt y Proveedor de IA

**Actor:** Usuario

### Descripción
El usuario selecciona un prompt predefinido y el proveedor de IA para procesar los datos del CSV.

### Precondiciones
- El archivo CSV debe haber sido cargado correctamente (opcional si se permite procesar sin CSV).
- El usuario debe estar en la página principal de la aplicación.

### Flujo Principal
1. El usuario selecciona un prompt predefinido de la lista desplegable.
2. El usuario puede editar el prompt seleccionado si lo desea.
3. El usuario selecciona el proveedor de IA (ChatGPT u OpenLLaMA) de la lista desplegable.

### Postcondiciones
- El prompt y el proveedor de IA seleccionados están listos para ser utilizados en el procesamiento de datos.

## Caso de Uso 3: Procesar Datos

**Actor:** Usuario

### Descripción
El usuario envía el prompt seleccionado y el archivo CSV (si está cargado) para ser procesado por el proveedor de IA seleccionado.

### Precondiciones
- El archivo CSV debe haber sido cargado correctamente (opcional si se permite procesar sin CSV).
- El prompt y el proveedor de IA deben estar seleccionados.

### Flujo Principal
1. El usuario hace clic en el botón "Procesar".
2. La aplicación envía el prompt y los datos del CSV (si están cargados) al proveedor de IA seleccionado.
3. La IA procesa la información y devuelve un análisis detallado.

### Postcondiciones
- Los resultados del análisis se muestran en la interfaz de usuario.
- El prompt utilizado y los resultados se almacenan en un archivo JSON en la carpeta `resultados`.

### Flujo Alternativo
- Si el checkbox "Marcar como OK" está seleccionado, la aplicación devuelve un simple "OK" sin procesar los datos con la IA.

## Caso de Uso 4: Visualizar Resultados

**Actor:** Usuario

### Descripción
El usuario visualiza los resultados del análisis realizado por la IA.

### Precondiciones
- El procesamiento de datos debe haber sido completado con éxito.

### Flujo Principal
1. Los resultados del análisis se muestran en la página principal, incluyendo el prompt utilizado.
2. El usuario puede revisar los resultados y el prompt enviado.

### Postcondiciones
- El usuario tiene acceso a una representación clara y comprensible de los datos de seguridad analizados.

## Caso de Uso 5: Copiar Resultados al Portapapeles

**Actor:** Usuario

### Descripción
El usuario copia los resultados del análisis al portapapeles para utilizarlos en otros documentos o aplicaciones.

### Precondiciones
- Los resultados del análisis deben estar visibles en la página principal.

### Flujo Principal
1. El usuario hace clic en el botón "Copiar Resultados".
2. Los resultados se copian al portapapeles del usuario.

### Postcondiciones
- Los resultados del análisis están disponibles en el portapapeles para su uso en otros contextos.

## Caso de Uso 6: Almacenar Resultados en JSON

**Actor:** Sistema

### Descripción
La aplicación almacena automáticamente los resultados del análisis en un archivo JSON.

### Precondiciones
- El procesamiento de datos debe haber sido completado con éxito.

### Flujo Principal
1. La aplicación genera un archivo JSON con el prompt utilizado, la fecha de ejecución y los resultados del análisis.
2. El archivo JSON se guarda en la carpeta `resultados` con un nombre que incluye la fecha actual.

### Postcondiciones
- Los resultados del análisis están almacenados en un archivo JSON para futura referencia.

## Caso de Uso 7: Manejar Solicitudes GET y POST

**Actor:** Sistema

### Descripción
La aplicación maneja las solicitudes GET y POST para la carga y procesamiento de archivos CSV.

### Precondiciones
- El servidor Flask debe estar en funcionamiento.

### Flujo Principal para Solicitudes GET
1. El sistema recibe una solicitud GET para la página principal.
2. El sistema renderiza y devuelve la plantilla HTML `index.html`.

### Flujo Principal para Solicitudes POST
1. El sistema recibe una solicitud POST con el archivo CSV y los parámetros seleccionados por el usuario.
2. El sistema procesa los datos y devuelve la plantilla HTML `index.html` con los resultados del análisis.

### Postcondiciones
- La aplicación responde adecuadamente a las solicitudes GET y POST, proporcionando la interfaz de usuario y los resultados del análisis.
