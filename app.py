# Lista para almacenar los productos
import os

productos = []

# a fines practicos (temporalmente hasta que implementemos Base de Datos) almacenamos en lista o diccionario
# lista_productos = []  # esta variable lista luego se reemplazar por una tabla en SQLite
# inventario = {}  # esta variable diccionario luego se reemplazar por una tabla en SQLite
# Modelo del diccionario para un producto dado
# producto_dic = {
#     "nombre": None,
#     "descripcion": None,
#     "cantidad": 100,
#     "precio": None,
#     "categoria": None,
# }


################################################## Inicio sección declaracion de funciones #################################################
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
    codigoSinValidar = input(
        f"\nPor favor, ingresá el código del {contador+1}° producto (0 para finalizar): "
    )
    # Valido el ingreso con isdigit() por simplicidad, aunque bien podría haberlo manejado con exceptiones (try/except)
    if codigoSinValidar.isdigit():
        # Código ingresado es un entero mayor o igual a 0(condición de salida)
        codigo_validado = int(codigoSinValidar)
        if codigo_validado < 0:
            # Sí el código es un entero menor a 0 entrego codigo_validado con el flag de inválido
            codigo_validado = -1  # -1 es el flag de código inválido
    else:
        # print("El código ingresado es inválido, deben ser enteros mayores a 0")
        # Uso el -1 como valor de código inválido para informarlo a la función que invoca a solicitarCodigoProducto()
        codigo_validado = -1  # -1 es el flag de código inválido
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


def buscarProductoPorCodigo(codigoIngresado):
    # Devuelvo un array con las posiciónes en array productos, en donde los çódigos de productos coinciden con el codigoIngresado.
    # El código debería ser único, por lo que debería traer 0 o 1 matches como máximo.
    posicion = 0
    cantidadPoductos = len(productos)
    respuestas = []
    while posicion < cantidadPoductos:
        if productos[posicion]["codigo"] == codigoIngresado:
            respuestas.append(posicion)
        posicion += 1
    return respuestas


def buscarProductoPorNombre(nombreIngresado):
    # Inicializo el array de 2 posiciones para la respuesta de la búsqueda por nombre. En la posición 0 de respuesta guardo el resultado lógico de la búsqueda.
    # En la posición 1 de respuesta guardo el valor de la posición (índice) en el array de productos, que coincide con nombreIngresado (será -1 en caso de no existir).
    posicion = 0
    cantidadPoductos = len(productos)
    respuestas = (
        []
    )  # array de posiciones en el array productos que matchean la búsqueda por nombre del producto (no es case sensitive)
    while posicion < cantidadPoductos:
        if (
            productos[posicion]["nombre"].lower() == nombreIngresado.lower()
        ):  # hago que la búsqueda no sea case sensitive
            respuestas.append(posicion)
        posicion += 1
    return respuestas


def buscarProductoPorCategoria(categoriaIngresada):
    # Inicializo el array de 2 posiciones para la respuesta de la búsqueda por categoría. En la posición 0 de respuesta guardo el resultado lógico de la búsqueda.
    # En la posición 1 de respuesta guardo el valor de la posición (índice) en el array de productos, que coincide con categoriaIngresada (será -1 en caso de no existir).
    posicion = 0
    cantidadPoductos = len(productos)
    respuestas = (
        []
    )  # array de posiciones en el array productos que matchean la búsqueda por categoria del producto (no es case sensitive)
    while posicion < cantidadPoductos:
        if (
            productos[posicion]["categoria"].lower() == categoriaIngresada.lower()
        ):  # hago que la búsqueda no sea case sensitive
            respuestas.append(posicion)
        posicion += 1
    return respuestas


def ingresarProductoPorCodigoAlInventario(codigoIngresado):
    resultado = False
    respuestaBusquedaCodigo = buscarProductoPorCodigo(
        codigoIngresado
    )  # array de dos posiciones: en la pos 0 está valor logico del match en el Inventario y en la pos 1 el índice del match.
    respuestaBusquedaNombre = (
        []
    )  # Array de posiciones en el array Productos que cumplen con el nombre de producto pasado por parámetro (no es case sensitive).

    if len(respuestaBusquedaCodigo) == 0:
        print(f'Cargando el producto código "{codigoIngresado}" en el inventario.')
        nombre_producto = solicitarNombreProducto()
        respuestaBusquedaNombre = buscarProductoPorNombre(nombre_producto)
        if (
            len(respuestaBusquedaNombre) == 0
        ):  # que el array de matches por nombre tenga len 0 significa que el array está vacío, sin ocurrencias encontradas.
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
            # print(
            #     f'\nEl producto "{codigoIngresado}" se ingresó al inventario exitosamente.\n'
            # )
            resultado = True
        else:
            print(
                f'El producto "{nombre_producto}" ya existe en el inventario.\nDeberá seleccionar la opción "Actualizar producto" del Menú Principal para editar el registro preexistente.'
            )
            resultado = False
    else:
        print(
            f'El producto "{codigoIngresado}" ya existe en el inventario.\nDeberá seleccionar la opción "Actualizar producto" del Menú Principal para editar el registro preexistente.'
        )
        resultado = False

    return resultado


##### Fin Funciones auxiliares carga de Productos en el Inventario #####


def registrarProductos():
    # Cuerpo de la función
    # usar un metodo de sqlite, que le vamos a pasar esta query
    """
    INSERT INTO productos (
        nombre,
        descripcion,
        categoria,
        cantidad,
        precio)
    VALUES
    (variable_nombre, 'Un clásico atemporal de Antoine de Saint-Exupéry', 'infantil', 50, 1580 )
    """

    productos_en_inventario = 0
    clear_terminal()  # limpia la consola antes de iniciar el módulo de carga de productos.
    try:
        # Solicitamos el primer código de producto
        print(f"\nAlta de productos en el inventario:\n\n\n")
        codigo_producto = solicitarCodigoProducto(productos_en_inventario)
        # Usamos el bucle while para ingresar los datos mientras el código no sea 0
        while codigo_producto != 0:
            if codigo_producto != -1:
                if ingresarProductoPorCodigoAlInventario(codigo_producto):
                    productos_en_inventario += 1  # incremento el contador en caso que el producto sea nuevo y con los datos validados.
                else:  # este else es redundante porque la función "ingresarProductoPorCodigoAlInventario" ya informa internamente el resultado de la operación.
                    print(
                        f'La carga de datos sobre el producto "{codigo_producto}" no fue realizada.'
                    )
            else:
                print(
                    "El código ingresado es inválido, debe ser un número entero mayor a 0.\n"
                )
            # Solicitamos nuevamente el código del siguiente producto
            codigo_producto = solicitarCodigoProducto(productos_en_inventario)
    except ValueError:
        print(
            "\nError en la carga de datos al inventario. Salida abrupta del módulo de carga.\n\n\n"
        )


##### Funciones para Listar los Productos cargados en el Inventario #####
def mostrarInfoProducto(producto):
    print(
        "Código: ",
        producto["codigo"],
        "\t\t",
        f"Nombre: '{producto["nombre"]}'",
        "\t\t",
        "Precio(xU.): ",
        producto["precio"],
        "\t\t",
        "Cantidad: ",
        producto["cantidad"],
        "\t\t",
        "Categoria: ",
        producto["categoria"],
        "\t\t",
        "Descripcion: ",
        producto["descripcion"],
    )


def mostrarProductos():
    # Función que muestra los productos almacenados en nuestro inventario
    clear_terminal()  # Limpio la pantalla antes de mostrar los resultados

    print("\nListado de Productos del Inventario")

    print("-" * 200, "\n")

    if len(productos) == 0:
        print("\n")
        print(
            'El inventario está vacío.\nSi desea iniciar la carga productos deberá seleccionar "1. Agregar productos" en el Menú Principal.\n'
        )
    else:
        for producto in productos:
            mostrarInfoProducto(producto)
    print("\n")
    print("-" * 200, "\n")
    input("Presione cualquier tecla para continuar...")


def actualizarProducto():
    # Cuerpo de la función
    print(f"actualizarProducto")
    input("Presione Enter para continuar.")


def eliminarProducto():
    # Cuerpo de la función
    print(f"eliminarProducto")
    input("Presione Enter para continuar.")


def buscarProducto():
    respuestaBusquedaCodigo = []
    respuestaBusquedaNombre = []
    respuestaBusquedaCategoria = []
    clear_terminal()  # Limpio la pantalla antes de mostrar los resultados
    cadenaBusqueda = input(f"Ingrese código, nombre o categoría del producto buscado: ")
    longitudCadena = len(cadenaBusqueda)
    # valida que la cadena no esté vacía
    if longitudCadena > 0:
        # Valido la cadena, si es sólamente numérica muestro el resultado de la búsqueda.
        if cadenaBusqueda.isdigit():
            separador(200)
            contadorCodigos = 0
            respuestaBusquedaCodigo = buscarProductoPorCodigo(
                int(cadenaBusqueda)
            )  # array con las posiciones en el inventario donde matchean los códigos de productos con el valor ingreado.
            if len(respuestaBusquedaCodigo) > 0:
                print(
                    f'Resultado de búsqueda del producto código "{cadenaBusqueda}" en el inventario:'
                )
                subrayar(80)
                while contadorCodigos < len(
                    respuestaBusquedaCodigo
                ):  # recorro el array de resultados de la búsqueda
                    mostrarInfoProducto(
                        productos[respuestaBusquedaCodigo[contadorCodigos]]
                    )
                    contadorCodigos += 1
            else:
                print(
                    f'No hay productos con el código: "{cadenaBusqueda}" en el inventario.'
                )
        separador(200)
        # Valido la cadena ahora por Nombre de producto
        contadorNombres = 0
        respuestaBusquedaNombre = buscarProductoPorNombre(
            cadenaBusqueda
        )  # array de posiciones en el array productos en donde hay match por Nombre de producto (no es case sensitive) y puede ser más de único valor.
        if len(respuestaBusquedaNombre) > 0:
            print(
                f'Resultado de búsqueda del producto nombre "{cadenaBusqueda}" en el inventario: '
            )
            subrayar(80)
            while contadorNombres < len(
                respuestaBusquedaNombre
            ):  # recorro el array de resultados de la búsqueda
                mostrarInfoProducto(productos[respuestaBusquedaNombre[contadorNombres]])
                contadorNombres += 1
        else:
            print(
                f'No hay productos con el nombre: "{cadenaBusqueda}" en el inventario.'
            )
        separador(200)
        # Valido la cadena ahora por Categoria de producto
        contadorCategorias = 0
        respuestaBusquedaCategoria = buscarProductoPorCategoria(
            cadenaBusqueda
        )  # # array de posiciones en el array productos en donde hay match por Categoria de producto (no es case sensitive) y puede ser más de único valor.
        if len(respuestaBusquedaCategoria) > 0:
            print(
                f'Resultado de búsqueda del producto por categoría "{cadenaBusqueda}" en el inventario:'
            )
            subrayar(80)
            while contadorCategorias < len(
                respuestaBusquedaCategoria
            ):  # recorro el array de resultados de la búsqueda
                mostrarInfoProducto(
                    productos[respuestaBusquedaCategoria[contadorCategorias]]
                )
                contadorCategorias += 1
        else:
            print(
                f'No hay productos con la categoría: "{cadenaBusqueda}" en el inventario.'
            )
        separador(200)
    else:
        separador(200)
        print(f"El valor de búsqueda no puede ser vacío. ")
        separador(200)
    input("\nPresione Enter para continuar.")


def reporteBajoStock():
    # Cuerpo de la función
    # Pedir al usuario que ingrese el umbral_minimo_stock
    print(f"buscarProducto")
    input("Presione Enter para continuar.")


##### Funciones para el manejo del Menú Gestión del Inventario #####
def mostrarOpcionesMenu():
    ###### Muestro en el menú las opciones habilitadas
    print("\n--- Menú Principal de Inventario ---")
    print("1. Registrar productos.")
    print("2. Mostrar productos.")
    print("3. Actualizar producto.")
    print("4. Eliminar producto.")
    print("5. Buscar producto.")
    print("6. Reporte Bajo Stock.")
    print("7. Salir")


def ingresarOpcionValida(opcionStr, opcionSalida):
    opcion = 0
    if opcionStr.isdigit():
        # si el caracter ingresado es numérico entonces valida que sea un valor dentro de las opciones disponibles, sino itera hasta conseguir un número dentro del rango de las opciones del Menú.
        opcion = int(opcionStr)
        while opcion < 1 or opcion > int(
            opcionSalida
        ):  # valida que se ingrese una opción válida
            print("error, ingrese opción válida")
            opcionStr = input(f"(1-{opcionSalida}) >\t")
            if opcionStr.isdigit():
                opcion = int(opcionStr)
    else:
        opcion = (
            -1
        )  # valor de opción inválida en caso que el caracter ingresado no sea numérico.
    return opcion


def procesarOpcionElegida(opcion, opcionSalida):
    # Proceso: Elección de opcion y ejecución de las sentencias aoci
    if opcion == 1:
        registrarProductos()
    elif opcion == 2:
        mostrarProductos()
    elif opcion == 3:
        actualizarProducto()
    elif opcion == 4:
        eliminarProducto()
    elif opcion == 5:
        buscarProducto()
    elif opcion == 6:
        reporteBajoStock()
    elif opcion == int(opcionSalida):
        print(f"Elegiste salir del programa de inventario.")
    else:
        print(f"Opción no válida - Ingrese un número del 1 al {opcionSalida}")


# Función principal para el sistema de inventario
def main():
    # Inicio declaracion de variables globales
    opcionSalida = "7"  # variable que setea el número de opción "Salir" en el "Menú Principal de Inventario". Se debe setear como String obligatoriamente.
    opcionStr = ""  # variable que guarda la opción elegida como un String.
    opcion = 0  # Variable que guarda la opción elegida como un Integer.
    # Fin declaracion de variables globales

    # INICIO DEL LOOP DEL PROGRAMA PRINCIPAL
    while opcionStr != opcionSalida:
        clear_terminal()  # Limpio la consola para presentar el menú en pantalla limpia.
        mostrarOpcionesMenu()  # El menú permite según las opciones controlar la Entrada, Proceso y Salida de los Datos.
        opcionStr = input(f"Elija una opción (1-{opcionSalida})\t")
        opcion = ingresarOpcionValida(opcionStr, opcionSalida)
        if opcion > 0 and opcion <= int(opcionSalida):
            ##print("Eligiste la opción ", opcion)
            procesarOpcionElegida(opcion, opcionSalida)  # PROCESO
            if opcion == int(opcionSalida):
                break
        else:
            print(
                f"Opción no válida - Ingrese un número del 1 al {opcionSalida}"
            )  # Salida

        # input("Presione Enter para continuar.")

    print("Fin del programa inventario.")


######################################################### Fin seccion de funciones #########################################################

# Ejecución de la función main()
if __name__ == "__main__":
    main()
