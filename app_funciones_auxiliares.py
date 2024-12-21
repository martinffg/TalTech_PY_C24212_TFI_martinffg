import os

from app_funciones_db import db_insertar_producto, db_obtener_siguiente_id_disponible

# ******************************************************************
# DECLARACION DE FUNCIONES AUXILIARES
# ******************************************************************


def clear_terminal():
    # Para Windows
    if os.name == "nt":
        os.system("cls")
    # Para Linux y macOS
    else:
        os.system("clear")


def separador(espacios):
    print("\n")
    print("-" * espacios)
    print("\n")


def subrayar(espacios):
    print("-" * espacios)
    print("\n")


##### Funciones auxiliares carga de Productos en el Inventario #####
def solicitarCodigoProducto(contador):
    if contador >= 0:
        codigoSinValidar = input(
            ##f"\nPor favor, ingresá el código del {contador+1} ° producto (0 para finalizar): "
            # se quita la posibilidad de ingreso manual del código de producto para delegar dicha tarea en la DB.
            f"\nSe le asignará un çódigo automático al {contador+1}° producto.\n(Presione 0 para finalizar o cualquier otra tecla para continuar): "
        )
        if codigoSinValidar != "0":
            # Si ingresa cualquier otro caracter distinto al 0 de salida, se le asigna automáticamente el siguiente ID disponible
            # en la DB como código de producto para evitar coliciones y validaciones innecesarias.
            codigoSinValidar = str(db_obtener_siguiente_id_disponible())
    else:
        print("Contador inválido, debe ser mayor o igual a 0")
        input("Presione cualquier tecla para continuar...")
    # Valido el ingreso con isdigit() por simplicidad, aunque bien podría haberlo manejado con exceptiones (try/except)
    if codigoSinValidar.isdigit():
        # Código ingresado es un entero mayor o igual a 0(condición de salida)
        codigo_validado = int(codigoSinValidar)
        if codigo_validado < 0:
            # Sí el código es un entero menor a 0 entrego codigo_validado con el flag de inválido
            codigo_validado = -1  # -1 es el flag de código inválido
    else:
        # Uso el -1 como valor de código inválido para informarlo a la función que invoca a solicitarCodigoProducto()
        codigo_validado = -1  # -1 es el flag de código inválido
        print("El código ingresado es inválido, deben ser enteros mayores a 0")
        input("Presione cualquier tecla para continuar...")
    return codigo_validado


def solicitarNombreProducto():
    nombre = ""
    while nombre == "":
        nombre = input("Ingresá el nombre: ")
        if nombre == "":
            print("\nEl nombre del producto no puede quedar vacío.\n")
    return nombre


# defino funciones para validar si una cadena es un float en el formato válido para python
def is_float(cadena):
    try:
        float(cadena)
        return True
    except ValueError:
        return False


def is_float_v2(cadena):
    if cadena.replace(".", "").isnumeric():
        return True
    else:
        return False


def solicitarPrecioUnitarioProducto():
    precio = 0.0
    validacion = False

    while validacion == False:
        precioStr = input("Ingresá el precio unitario en formato 0.0: ")

        validacion = is_float(precioStr)

        if validacion:
            precio = float(precioStr)
            if precio <= 0.0:
                print("\nEl precio del producto debe ser mayor a 0.0\n")
                validacion = False
        else:
            print(
                "\nEl precio ingresado tiene un formato erróneo. Debe ser mayor a 0.0\n"
            )
    return precio


def solicitarCantidadProducto():
    cantidad = 0  # Si solicito cantidad de productos, no puedo agregar un producto nuevo (inventariarlo) sin stock, es decir algo con cant = 0 no es valido.
    while cantidad <= 0:
        cantidadSinValidar = input("Ingresá la cantidad de unidades: ")
        # Valido el ingreso con isdigit() por simplicidad, aunque bien podría haberlo manejado con exceptiones (try/except)
        if cantidadSinValidar.isdigit():
            # Cantidad ingresada es un entero mayor o igual a 0(condición de salida)
            cantidad = int(cantidadSinValidar)
            if (
                cantidad <= 0
            ):  # Sí la cantidad ingresada es un entero menor o igual a 0 lo pongo en 0 para que vuelva a interar y lo informo.
                print("La cantidad ingresada debe ser un número entero mayor a 0.")
                cantidad = 0
            else:
                break
        else:
            print("La cantidad ingresada es incorrecta, debe ser un número mayor a 0.")
            # Uso el -1 como valor de código inválido y vuelve a iterar el while.  Informo el error también.
            cantidad = -1  # -1 es el flag de código inválido
    return cantidad


def buscarProductoPorCodigo(codigoIngresado, productos):
    # Devuelvo un array con las posiciónes en array productos, en donde los çódigos de productos coinciden con el codigoIngresado.
    # El código debería ser único por ser el campo id del inventario, por lo que debería traer 0 o 1 matches como máximo de lo contrario la fuente de datos es inconsistente.
    posicion = 0
    cantidadPoductos = len(productos)
    respuestas = []
    while posicion < cantidadPoductos:
        if productos[posicion]["codigo"] == codigoIngresado:
            respuestas.append(posicion)
        posicion += 1
    return respuestas


def buscarProductoPorNombre(nombreIngresado, productos):
    # Inicializo el array de 2 posiciones para la respuesta de la búsqueda por nombre. En la posición 0 de respuesta guardo el resultado lógico de la búsqueda.
    # En la posición 1 de respuesta guardo el valor de la posición (índice) en el array de productos, que coincide con nombreIngresado (será -1 en caso de no existir).
    posicion = 0
    cantidadPoductos = len(productos)
    respuestas = (
        []
    )  # array de posiciones en el array productos que matchean la búsqueda por nombre del producto (no es case sensitive)
    while posicion < cantidadPoductos:
        if (
            nombreIngresado.lower() in productos[posicion]["nombre"].lower()
        ):  # hago que la búsqueda no sea case sensitive
            respuestas.append(posicion)
        posicion += 1
    return respuestas


def buscarProductoPorCategoria(categoriaIngresada, productos):
    # Inicializo el array de 2 posiciones para la respuesta de la búsqueda por categoría. En la posición 0 de respuesta guardo el resultado lógico de la búsqueda.
    # En la posición 1 de respuesta guardo el valor de la posición (índice) en el array de productos, que coincide con categoriaIngresada (será -1 en caso de no existir).
    posicion = 0
    cantidadPoductos = len(productos)
    respuestas = (
        []
    )  # array de posiciones en el array productos que matchean la búsqueda por categoria del producto (no es case sensitive)
    while posicion < cantidadPoductos:
        if (
            categoriaIngresada.lower() in productos[posicion]["categoria"].lower()
        ):  # hago que la búsqueda no sea case sensitive
            respuestas.append(posicion)
        posicion += 1
    return respuestas


def ingresarProductoPorCodigoAlInventario(codigoIngresado, productos):
    resultado = False
    respuestaBusquedaCodigo = buscarProductoPorCodigo(
        codigoIngresado, productos
    )  # array de dos posiciones: en la pos 0 está valor logico del match en el Inventario y en la pos 1 el índice del match.

    # LA VALIDACIÓN POR NOMBRE DEL PRODUCTO FUE DESHABILITADA, PUES NO ES UN CAMPO UNIQUE.
    # respuestaBusquedaNombre = (
    #     []
    # )  # Array de posiciones en el array Productos que cumplen con el nombre de producto pasado por parámetro (no es case sensitive).

    if (
        len(respuestaBusquedaCodigo) == 0
    ):  # esta búsqueda debería dar vacío SIEMPRE desde ahora que todo se gestiona desde la DB por medio de su próximo ID disponible.
        print(f'Cargando el producto código "{codigoIngresado}" en el inventario.')
        nombre_producto = solicitarNombreProducto()
        # LAS LÍNEAS COMENTADAS SIGUIENTES SON PARA DEFINIR EL CAMPO NOMBRE TAMBIÉN COMO UNIQUE (NO REQUERIDO, SÓLO CÓDIGO ES UNIQUE POR CONSIGNA)
        # respuestaBusquedaNombre = buscarProductoPorNombre(nombre_producto)
        # if (
        #     len(respuestaBusquedaNombre) == 0
        # ):  # que el array de matches por nombre tenga len 0 significa que el array está vacío, sin ocurrencias encontradas.
        ## CARGA DE LOS DATOS DEL PRODUCTO CON CÓDIGO NUEVO (CAMPO UNIQUE) ## ESTE BLOQUE SE MOVIÓ UN NIVEL MENOS POR INDEXACIÓN AL COMENTAR LA VALICACIÓN POR NOMBRE.
        precio_unitario = solicitarPrecioUnitarioProducto()
        cantidad = solicitarCantidadProducto()
        descripcion = input(f"Descripción: ")
        categoria = input(f"Categoria: ")
        # Agregamos los datos del producto como una lista dentro de la lista de productos
        productos.append(
            # [codigoIngresado, nombre_producto, precio_unitario, cantidad]
            {
                "codigo": codigoIngresado,
                "nombre": nombre_producto,
                "descripcion": descripcion,
                "cantidad": cantidad,
                "precio": precio_unitario,
                "categoria": categoria,
            }
        )
        # Ahora agrego también el producto ingresado a la Base de Datos para que haya consistencia entre la DB y los vectores.
        respuestaDB = db_insertar_producto(
            codigoIngresado,
            nombre_producto,
            descripcion,
            cantidad,
            precio_unitario,
            categoria,
        )
        if respuestaDB:
            resultado = True
        else:
            resultado = False
        ## FIN CARGA DE LOS DATOS DEL PRODUCTO CON CÓDIGO NUEVO (CAMPO UNIQUE) ## ESTE BLOQUE SE MOVIÓ UN NIVEL MENOS POR INDEXACIÓN AL COMENTAR LA VALICACIÓN POR NOMBRE.
        # LAS LÍNEAS COMENTADAS SIGUIENTES SON TAMBIÉN PARA DEFINIR EL CAMPO NOMBRE TAMBIÉN COMO UNIQUE (NO REQUERIDO, SÓLO CÓDIGO ES UNIQUE POR CONSIGNA)
        # else:
        #     print(
        #         f'El producto "{nombre_producto}" ya existe en el inventario.\nDeberá seleccionar la opción "Actualizar producto" del Menú Principal para editar el registro preexistente.'
        #     )
        #     resultado = False
    else:
        print(
            f'El producto ID: "{codigoIngresado}" ya existe en el inventario.\nDeberá seleccionar la opción "Actualizar producto" del Menú Principal para editar el registro preexistente.'
        )
        resultado = False

    return resultado
