![Logo](https://github.com/talentotech-ba/recursos/blob/0dea22ffba99ff1e32e0c6e4d51f738816e7afa5/tt-banner.jpg?raw=true)
- **Repositorio Personal del PFI de Martin Fernandez Gamen - 2024 - Curso Python Inicial Talento Tech - Comision 24212**

### Consigna del Proyecto Final Integrador (PFI)
### Objetivos:

- **El Proyecto Final Integrador (PFI) consiste en el desarrollo de una aplicación Python, que utilizando la terminal o consola permita al usuario gestionar el inventario de una pequeña tienda o comercio.** 

- **La aplicación debe ser capaz de registrar, actualizar, eliminar y mostrar productos en el inventario. Además, debe incluir funcionalidades para realizar búsquedas y generar reportes de productos con bajo stock.**

- **El proyecto incluirá los medios necesarios para interactuar con una base de datos, implementará un menú con las opciones disponibles, y mecanismos (funciones) para el mantenimiento de los datos de los productos, incluyendo:**
  - `Registro`: Alta de productos nuevos.
  - `Visualización`: Consulta de datos de productos.
  - `Actualización`: Modificar la cantidad en stock de un producto.
  - `Eliminación`: Dar de baja productos.
  - `Listado`: Listado completo de los productos en la base de datos.
  - `Reporte de Bajo Stock`: Lista de productos con cantidad bajo mínimo.

- **El archivo principal donde se debe desarrollar el código es `app_main.py`. Todo el trabajo debe realizarse dentro de este archivo.**

### FORMATO DE ENTREGA: 
_**CREAR UNA CARPETA EN DRIVE (PÚBLICA) QUE CONTENGA LOS ARCHIVOS Y CARPETAS QUE CONFORMAN TU PROYECTO.**
_**CÓDIGO COMPLETO PUBLICADO EN GITHUB** 

### Instrucciones para el uso del programa:

* El archivo principal donde se debe desarrolla el código del programa se llama "app.py". Todo el trabajo se realizó dentro de este archivo como fue requerido.
* El archivo "inventario.db" corresponde a la DB sqlite donde se persiste la información manipulada en la aplicación creada.  Contiene datos de prueba iniciales.
* Para poder ejecutar el programa, el equipo en donde se ejecutará deberá contar previamente con el entorno de ejecución Python instalado, por ejemplo: Python 3.12.x entre otros.
* Los archivos: "app.py" como "inventario.db" deberán estar ubicados en la misma carpeta del archivos.
* Para ejecutar el programa se deberá correr a modo de ejemplo la siguiente instrucción por consola en: 
    - WINDOWS: Unidad:\CarpetaDelPrograma\python app_main.py
    - LINUX Ó MACOS:    /RutaFileSystem/python app_main.py 
            o bien      /RutaFileSystem/python3 app_main.py
* Una vez iniciado el programa, se intentarán cargar los datos de la DB inventario, en particular el contenido de la tabla productos en memoria para contar con un soporte ágil en paralelo a la DB.
* Ya en el Menú Principal, podrán acceder a las opciones del menú descriptas en las consignas del TP, con la particularidad de poder hacer cambios múltiples en los registros de la DB,
  ya sean altas de registros nuevos, búsqueda, actualizaciones y eliminaciones de productos cada una con sus submenús independientes.
* Los cambios realizados sobre los registros del Inventario son actualizados no sólo en memoria sino también persistidos en la DB inventario.
* Tanto el Menú Principal como los submenús son muy intuitivos.
* Para salir del programa en ejecución basta sólo con seleccionar las opciones del menú correspondiente.  
* Se recomienda realizar un cierre gracefull del mismo para poder garantizar la integridad de los datos manipulados.

### ESPERO QUE TENGAN UNA EXCELENTE EXPERIENCIA DE USO DEL PROGRAMA.