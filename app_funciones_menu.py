# ******************************************************************
# DECLARACION DE FUNCIONES
# ******************************************************************
import os
from app_funciones_db import *
from app_funciones_auxiliares import *

############################################################ Variables globales ############################################################

productos = []  # Lista en memoria para almacenar los productos


def cargarDatosEnMemoria():
    registros = db_exportar_registros_a_Lista_Diccionarios()
    for registro in registros:
        productos.append(registro)


############################################################ Fin Variables globales ############################################################


def registrarProductos():
    # Cuerpo de la función
    productos_en_inventario = 0
    clear_terminal()  # limpia la consola antes de iniciar el módulo de carga de productos.
    try:
        # Solicitamos el primer código de producto
        print(f"\nAlta de productos en el inventario:\n\n\n")
        codigo_producto = solicitarCodigoProducto(productos_en_inventario)
        # Usamos el bucle while para ingresar los datos mientras el código no sea 0
        while codigo_producto != 0:  # 0 es el flag de salida del ciclo
            if codigo_producto != -1:  # -1 es el flag de codigo invalido
                if ingresarProductoPorCodigoAlInventario(
                    codigo_producto, productos
                ):  # Ahora el código ingresado es el próximo ID disponible en la DB, pues el campo ID es Autoincremental.
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
        "Codigo: ",
        str(producto["codigo"]).ljust(10)[:10],
        "\t",
        "Nombre: ",
        producto["nombre"].ljust(30)[:30],
        "\t",
        "Descripcion: ",
        producto["descripcion"].ljust(30)[:30],
        "\t",
        "Cantidad: ",
        str(producto["cantidad"]).ljust(10)[:10],
        "\t",
        "Precio(xU.): ",
        str(round(producto["precio"], 2)).ljust(10)[:10],
        "\t",
        "Categoria: ",
        producto["categoria"].ljust(20)[:20],
    )


def mostrarProductos():
    # Función que muestra los productos almacenados en nuestro inventario en memoria y también en la db
    clear_terminal()  # Limpio la pantalla antes de mostrar los resultados en ambos soportes.
    print("\nListado de Productos del Inventario en Memoria")
    print("-" * 200, "\n")
    if len(productos) == 0:
        print("\n")
        print(
            'El inventario está vacío.\nSi desea iniciar la carga productos deberá seleccionar "1. Registrar productos" en el Menú Principal.\n'
        )
    else:
        for producto in productos:
            mostrarInfoProducto(producto)
    print("\n")
    print("-" * 200, "\n")
    input("Presione cualquier tecla para continuar...")
    clear_terminal()  # Limpio la pantalla antes de mostrar los resultados en ambos soportes.
    print("Listado de Productos del Inventario persistidos en la DB en formato JSON")
    print("-" * 200, "\n")
    mostrar_productos_DB_comoJson()
    print("\n")
    print("-" * 200, "\n")
    input("Presione cualquier tecla para continuar...")


def buscarProducto():
    respuestaBusquedaCodigoEnLista = []
    respuestaBusquedaNombreEnLista = []
    respuestaBusquedaCategoriaEnLista = []
    respuestaBusquedaCodigoEnDB = []
    respuestaBusquedaNombreEnDB = []
    respuestaBusquedaCategoriaEnDB = []
    clear_terminal()  # Limpio la pantalla antes de mostrar los resultados
    cadenaBusqueda = input(f"Ingrese código, nombre o categoría del producto buscado: ")
    longitudCadena = len(cadenaBusqueda)
    # valida que la cadena no esté vacía
    if longitudCadena > 0:
        # Valido la cadena, si es sólamente numérica muestro el resultado de la búsqueda.
        if cadenaBusqueda.isdigit():
            separador(200)
            contadorCodigos = 0
            respuestaBusquedaCodigoEnLista = buscarProductoPorCodigo(
                int(cadenaBusqueda), productos
            )  # array con las posiciones en el inventario donde matchean los códigos de productos con el valor ingreado.
            respuestaBusquedaCodigoEnDB = db_obtener_producto_id(int(cadenaBusqueda))
            if len(respuestaBusquedaCodigoEnLista) > 0:
                print(
                    f'Resultado de búsqueda del producto código "{cadenaBusqueda}" en el inventario:'
                )
                subrayar(80)
                while contadorCodigos < len(
                    respuestaBusquedaCodigoEnLista
                ):  # recorro el array de resultados de la búsqueda
                    mostrarInfoProducto(
                        productos[respuestaBusquedaCodigoEnLista[contadorCodigos]]
                    )
                    contadorCodigos += 1
                separador(200)
                print(
                    f'Resultado de búsqueda del producto código "{cadenaBusqueda}" en la BD (formato JSON):'
                )
                subrayar(80)
                print(respuestaBusquedaCodigoEnDB)
            else:
                print(
                    f'No hay productos con el código: "{cadenaBusqueda}" en el inventario.'
                )
        separador(200)

        ############################# Valido la cadena ahora por Nombre de producto
        contadorNombres = 0
        respuestaBusquedaNombreEnLista = buscarProductoPorNombre(
            cadenaBusqueda, productos
        )  # array de posiciones en el array productos en donde hay match por Nombre de producto (no es case sensitive) y puede ser más de único valor.
        respuestaBusquedaNombreEnDB = db_obtener_producto_nombre(cadenaBusqueda)
        if (
            len(respuestaBusquedaNombreEnLista) > 0
            and len(respuestaBusquedaNombreEnDB) > 0
        ):
            print(
                f'Resultado de búsqueda del producto con nombre "{cadenaBusqueda}" en el inventario: '
            )
            subrayar(80)
            while contadorNombres < len(
                respuestaBusquedaNombreEnLista
            ):  # recorro el array de resultados de la búsqueda
                mostrarInfoProducto(
                    productos[respuestaBusquedaNombreEnLista[contadorNombres]]
                )
                contadorNombres += 1
            separador(200)
            print(
                f'Resultado de búsqueda del producto con nombre: "{cadenaBusqueda}" en la BD (formato JSON):'
            )
            subrayar(80)
            print(respuestaBusquedaNombreEnDB)
        else:
            print(
                f'No hay productos con el nombre: "{cadenaBusqueda}" en el inventario.'
            )
        separador(200)

        ############################# Valido la cadena ahora por Categoria de producto
        contadorCategorias = 0
        respuestaBusquedaCategoriaEnLista = buscarProductoPorCategoria(
            cadenaBusqueda, productos
        )  # array de posiciones en el array productos en donde hay match por Categoria de producto (no es case sensitive) y puede ser más de único valor.
        respuestaBusquedaCategoriaEnDB = db_obtener_producto_categoria(cadenaBusqueda)
        if (
            len(respuestaBusquedaCategoriaEnLista) > 0
            and len(respuestaBusquedaCategoriaEnDB) > 0
        ):
            print(
                f'Resultado de búsqueda del producto por categoría "{cadenaBusqueda}" en el inventario:'
            )
            subrayar(80)
            while contadorCategorias < len(
                respuestaBusquedaCategoriaEnLista
            ):  # recorro el array de resultados de la búsqueda
                mostrarInfoProducto(
                    productos[respuestaBusquedaCategoriaEnLista[contadorCategorias]]
                )
                contadorCategorias += 1
            separador(200)
            print(
                f'Resultado de búsqueda del producto por categoría "{cadenaBusqueda}" en la BD (formato JSON):'
            )
            subrayar(80)
            print(respuestaBusquedaCategoriaEnDB)
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


def swappingCodigoProducto(
    posicion,
    codigoIngresado,
):
    # Uso -1 porque no me interesa el orden de ingreso del producto en estos momentos.  Este valor es usado para las salidas por pantalla ordenadas.
    codigo_producto = solicitarCodigoProducto(-1)
    if (
        codigo_producto != codigoIngresado
        and len(buscarProductoPorCodigo(codigo_producto, productos)) == 0
    ):  # me aseguro que el nuevo codigo no se repita con los preexistentes.
        productos[posicion]["codigo"] = codigo_producto
        print("Se realizó el cambio de código de producto de forma correcta.")
    elif len(buscarProductoPorCodigo(codigo_producto, productos)) != 0:
        print(
            "Código de producto preexistente en el inventario.  No se aplicará el cambio. "
        )
    elif codigo_producto == codigoIngresado:
        print(
            "El Código de producto coincide con el preexistente. No se aplicará el cambio. "
        )
    else:
        print("Código de producto inválido.  No se aplicará el cambio. ")


def swappingValoresProductoPorCampo(posicion, campo, opcionCambio):
    respuesta = False
    nuevo_valor = ""

    if opcionCambio == "Y" or opcionCambio == "y":
        seCambia = True
    else:
        seCambia = False

    match campo:
        # Al implementar la DB se limita la opcion de cambiar el codigo de producto ya que se fusiona con el concepto de ID de la tabla, que no debería cambiar por consistencia.
        # case "codigo":
        #     if seCambia:
        #         codigoPrevio = productos[posicion]["codigo"]
        #         productos[posicion]["codigo"] = swappingCodigoProducto(posicion,codigoPrevio)
        #         respuesta = True
        #     else:
        #         respuesta = False
        #     nuevo_valor = productos[posicion]["codigo"]
        case "nombre":
            if seCambia:
                productos[posicion]["nombre"] = solicitarNombreProducto()
                respuesta = True
            else:
                respuesta = False
            nuevo_valor = productos[posicion]["nombre"]
        case "precio":
            if seCambia:
                productos[posicion]["precio"] = solicitarPrecioUnitarioProducto()
                respuesta = True
            else:
                respuesta = False
            nuevo_valor = productos[posicion]["precio"]
        case "cantidad":
            if seCambia:
                productos[posicion]["cantidad"] = solicitarCantidadProducto()
                respuesta = True
            else:
                respuesta = False
            nuevo_valor = productos[posicion]["cantidad"]
        case "descripcion":
            if seCambia:
                productos[posicion]["descripcion"] = input("Descripción: ")
                respuesta = True
            else:
                respuesta = False
            nuevo_valor = productos[posicion]["descripcion"]
        case "categoria":
            if seCambia:
                productos[posicion]["categoria"] = input("Categoria: ")
                respuesta = True
            else:
                respuesta = False
            nuevo_valor = productos[posicion]["categoria"]
        case _:
            print("El campo ingresado no es correcto.")
            respuesta = False
            nuevo_valor = False

    return nuevo_valor, respuesta


def actualizarProductoPorPosicionInventario(posicion, codigoIngresado):

    # Se restringe que el usuario pueda cambiar el código de producto asignado.
    # opcionCodigo = input(
    #     "Desea cambiar el código del producto: (y/Y para ingresar nuevo valor): "
    # )
    # nuevo_codigo, es_nuevo_codigo = swappingValoresProductoPorCampo(posicion, "codigo", opcionCodigo)

    opcionNombre = input(
        "Desea cambiar el nombre del producto: (y/Y para ingresar nuevo valor): "
    )
    nuevo_nombre, es_nuevo_nombre = swappingValoresProductoPorCampo(
        posicion, "nombre", opcionNombre
    )

    opcionPrecio = input(
        "Desea cambiar el precio del producto: (y/Y para ingresar nuevo valor): "
    )
    nuevo_precio, es_nuevo_precio = swappingValoresProductoPorCampo(
        posicion, "precio", opcionPrecio
    )

    opcionCantidad = input(
        "Desea cambiar la cantidad del producto: (y/Y para ingresar nuevo valor): "
    )
    nuevo_cantidad, es_nuevo_cantidad = swappingValoresProductoPorCampo(
        posicion, "cantidad", opcionCantidad
    )

    opcionDescripcion = input(
        "Desea cambiar la descripción del producto: (y/Y para ingresar nuevo valor): "
    )
    nuevo_descripcion, es_nuevo_descripcion = swappingValoresProductoPorCampo(
        posicion, "descripcion", opcionDescripcion
    )

    opcionCategoria = input(
        "Desea cambiar la categoría del producto: (y/Y para ingresar nuevo valor): "
    )
    nuevo_categoria, es_nuevo_categoria = swappingValoresProductoPorCampo(
        posicion, "categoria", opcionCategoria
    )

    ## Ahora impacto la info anterior en una variable tipo producto para luego hacer el update en el mismo objeto en la DB.
    producto_actualizado = {}
    producto_actualizado["codigo"] = codigoIngresado
    producto_actualizado["nombre"] = nuevo_nombre
    producto_actualizado["descripcion"] = nuevo_descripcion
    producto_actualizado["cantidad"] = nuevo_cantidad
    producto_actualizado["precio"] = nuevo_precio
    producto_actualizado["categoria"] = nuevo_categoria

    # lanzo el update a la DB
    db_actualizar_producto(codigoIngresado, producto_actualizado)

    separador(200)
    if (
        es_nuevo_nombre
        or es_nuevo_descripcion
        or es_nuevo_cantidad
        or es_nuevo_precio
        or es_nuevo_categoria
    ):
        print(f'\nEl producto "{codigoIngresado}" fue actualizado exitosamente.\n')
    else:
        print(f'\nEl producto "{codigoIngresado}" NO ha sufrido cambios.\n')
    separador(200)


def actualizarProducto():
    respuestaBusquedaCodigo = []
    clear_terminal()  # Limpio la pantalla antes de mostrar los resultados
    separador(200)
    cadenaBusqueda = input(
        f"Ingrese el código de producto que desea actualizar, pulse y/Y para salir: "
    )
    longitudCadena = len(cadenaBusqueda)
    while cadenaBusqueda != "y" and cadenaBusqueda != "Y":
        # valida que la cadena no esté vacía
        if longitudCadena > 0:
            # Valido la cadena, si es sólamente numérica muestro el resultado de la búsqueda.
            if cadenaBusqueda.isdigit():
                separador(200)
                contadorCodigos = 0
                cadenaBusquedaInt = int(cadenaBusqueda)
                # array con las posiciones en el inventario donde matchean los códigos de productos con el valor ingresado.
                respuestaBusquedaCodigo = buscarProductoPorCodigo(
                    cadenaBusquedaInt, productos
                )
                if (
                    len(respuestaBusquedaCodigo) > 0
                ):  # El código pertenece al inventario
                    print(
                        f'Actualizando producto con código "{cadenaBusqueda}" en el inventario:'
                    )
                    subrayar(80)
                    while contadorCodigos < len(
                        respuestaBusquedaCodigo
                    ):  # recorro el array de resultados de la búsqueda
                        posicionCodigo = respuestaBusquedaCodigo[contadorCodigos]
                        mostrarInfoProducto(productos[posicionCodigo])
                        separador(200)
                        actualizarProductoPorPosicionInventario(
                            posicionCodigo, cadenaBusquedaInt
                        )
                        contadorCodigos += 1
                else:
                    print(
                        f'No hay productos con el código: "{cadenaBusqueda}" en el inventario.'
                    )
            else:
                separador(200)
                print(
                    f"Código inválido, el código de producto sólo admite valores numéricos. "
                )
                separador(200)
        else:
            separador(200)
            print(f"El código de producto ingresado no puede estar vacío. ")
            separador(200)
        cadenaBusqueda = input(
            f"Ingrese el código de producto que desea actualizar, pulse y/Y para salir: "
        )


def eliminarProducto():
    respuestaBusquedaCodigo = []
    clear_terminal()  # Limpio la pantalla antes de mostrar los resultados
    separador(200)
    cadenaBusqueda = input(
        f"Ingrese el código de producto que desea eliminar, pulse 0 para salir: "
    )
    longitudCadena = len(cadenaBusqueda)
    while cadenaBusqueda != "0":
        # valida que la cadena no esté vacía
        if longitudCadena > 0:
            # Valido la cadena, si es sólamente numérica muestro el resultado de la búsqueda.
            if cadenaBusqueda.isdigit():
                separador(200)
                contadorCodigos = 0
                cadenaBusquedaInt = int(cadenaBusqueda)
                respuestaBusquedaCodigo = buscarProductoPorCodigo(
                    cadenaBusquedaInt, productos
                )
                # array con las posiciones en el inventario donde matchean los códigos de productos con el valor ingreado.
                if len(respuestaBusquedaCodigo) > 0:
                    print(
                        f'Eliminando el producto con código "{cadenaBusqueda}" en el inventario:'
                    )
                    subrayar(80)
                    # recorro el array de resultados de la búsqueda
                    while contadorCodigos < len(respuestaBusquedaCodigo):
                        posicionCodigo = respuestaBusquedaCodigo[contadorCodigos]
                        print(f"Eliminando del inventario en memoria: ")
                        subrayar(40)
                        mostrarInfoProducto(productos[posicionCodigo])
                        productoEliminado = productos.pop(posicionCodigo)
                        separador(120)
                        print(f"Eliminando de la DB inventario: ")
                        subrayar(40)
                        print(db_obtener_producto_id(cadenaBusquedaInt))
                        db_eliminar_producto(cadenaBusquedaInt)
                        print("\n")
                        contadorCodigos += 1
                else:
                    print(
                        f'No hay productos con el código: "{cadenaBusqueda}" en el inventario.'
                    )
            else:
                separador(200)
                print(
                    f"Código inválido, el código de producto sólo admite valores numéricos. "
                )
                separador(200)
        else:
            separador(200)
            print(f"El código de producto ingresado no puede estar vacío. ")
            separador(200)
        cadenaBusqueda = input(
            f"\nIngrese el código de producto que desea eliminar, pulse 0 para salir: "
        )
    separador(200)


def reporteBajoStock():

    # Función que muestra el reporte de productos con bajo stock según el umbral definido por el usuario.
    clear_terminal()  # Limpio la pantalla antes de mostrar los resultados
    productosEnDB = (
        []
    )  # declaro variable que alojará los datos recuperados de la DB en Riesgo de bajo Stock.
    # db_obtener_siguiente_id_disponible()>1: me garantiza que la DB tiene al menos un registro, ergo no está vacía.
    if len(productos) > 0 and db_obtener_siguiente_id_disponible() > 1:
        # Pedir al usuario que ingrese el umbral_minimo_stock
        print("Se necesita definir la cantidad de productos como umbral de bajo stock.")
        umbralStockMinimo = solicitarCantidadProducto()
        print(f"Se definió el valor de Umbral de Stock Minimo en {umbralStockMinimo}.")
        separador(200)
        print("\nReporte de Bajo Stock Inventario en Memoria:")
        print("-" * 200, "\n")
        for producto in productos:
            if producto["cantidad"] <= umbralStockMinimo:
                mostrarInfoProducto(producto)
        separador(200)
        print("\nReporte de Bajo Stock DB de Inventario:")
        print("-" * 200, "\n")
        productosEnDB = db_get_productos_by_condicion(umbralStockMinimo)
        for productoDB in productosEnDB:
            print(productoDB)
    else:
        print("\n")
        print(
            'El inventario está vacío.\nSi desea iniciar la carga productos deberá seleccionar "1. Registrar productos" en el Menú Principal.\n'
        )
    print("\n")
    print("-" * 200, "\n")
    input("Presione cualquier tecla para continuar...")


##### Funciones para el manejo del Menú Gestión del Inventario #####
def mostrarOpcionesMenu():
    ###### Muestro en el menú las opciones habilitadas
    print("\t", "-" * 30)
    print("\t  Menú Principal del Inventario")
    print("\t", "-" * 30)
    print(
        """ 
        1. Registrar productos.
        2. Mostrar productos.
        3. Actualizar producto.
        4. Eliminar producto.
        5. Buscar producto.
        6. Reporte Bajo Stock.
        7. Salir.
        """
    )


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
