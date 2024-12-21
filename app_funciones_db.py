import sqlite3

# DECLARACION DE CONSTANTES
PATH_DB = r"./inventario.db"

# VARIABLES GLOBALES


# ******************************************************************
# DECLARACION DE FUNCIONES DE MANIPULACION DE LA DB
# ******************************************************************

# resultados = cursor.fetchall()              # Obtener todos los registros
# for registro in resultados:                 # Mostrar los resultados
#    print("Nombre:", registro[0], "Edad:", registro[1], "Ciudad:", registro[2])
# conexion.close()                             # Cerrar la conexión

# 6. Trabajar con los resultado, mostrandolos en pantalla (PRESENTACION)
# if not resultados:
#     print("No hay registros que mostrar")
# else:
#     print(resultados)
#     for registro in resultados:
#         for campo in registro:
#             print(f"{campo}")


def db_get_productos_como_Lista_Diccionarios():
    listaTuplasProductos = db_obtener_productos_todos()
    cantidadDeRegistrosImportadosDesdeDB = len(listaTuplasProductos)
    listaDiccionariosProductos = []
    producto_diccionario = {}
    if cantidadDeRegistrosImportadosDesdeDB > 0:
        for producto_tupla in listaTuplasProductos:
            producto_diccionario["codigo"] = int(producto_tupla[0])
            producto_diccionario["nombre"] = producto_tupla[1]
            producto_diccionario["descripcion"] = producto_tupla[2]
            producto_diccionario["cantidad"] = int(producto_tupla[3])
            producto_diccionario["precio"] = float(producto_tupla[4])
            producto_diccionario["categoria"] = producto_tupla[5]
            listaDiccionariosProductos.append(dict(producto_diccionario))
            producto_diccionario = {}
    else:
        print("La tabla productos está vacía. No se han obtenido datos. ")
    return listaDiccionariosProductos


def db_exportar_registros_a_Lista_Diccionarios():
    # Exporto los registros de la DB a una lista de diccionarios.
    return db_get_productos_como_Lista_Diccionarios()


def db_abrir_conexion():
    try:
        conexionDB = sqlite3.connect(PATH_DB)
        cursorDB = conexionDB.cursor()
    except sqlite3.Error as e:
        print(f"Error al abrir la conexión contra la DB: {e}")
        conexionDB = None
        cursorDB = None
        input("\nPresione una tecla para continuar... ")
    return conexionDB, cursorDB


def db_cerrar_conexion(conexionDB):
    try:
        if conexionDB:
            conexionDB.commit()
            conexionDB.close()
        else:
            print(
                "Error de conexión inexistente.  Falló durante commit/cierre de la DB.\n"
            )
            input("\nPresione una tecla para continuar... ")
    except sqlite3.Error as e:
        print(f"Falló durante commit/cierre de la DB: {e}")
        input("\nPresione una tecla para continuar... ")


# Esta función permite crear/conectarse con la base "inventario.db", en caso que no existan, crea tanto la DB "inventario" como la tabla "productos"
def db_inicializar_tabla_productos():
    try:
        conexionDB, cursorDB = db_abrir_conexion()
        query = """ 
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT
            )
            """
        cursorDB.execute(query)
        db_cerrar_conexion(conexionDB)
    except Exception as e:
        print(f"Error al crear la tabla productos: {e}")
        input("\nPresione una tecla para continuar... ")


# Esta funcion el valor de ID disponible siguiente a fin de poder cargarlo en el registro en memoria y en el insert a la DB
def db_obtener_siguiente_id_disponible():
    nextAvailableId = 0
    try:
        conexionDB, cursorDB = db_abrir_conexion()
        query = "SELECT MAX(id)+1 FROM productos"
        cursorDB.execute(query)
        resultado = cursorDB.fetchone()  # retorna una lista de tuplas
        nextAvailableId = int(resultado[0])
        conexionDB.close()
    except sqlite3.Error as e:
        print(
            f"Error al intentar obtener el siguiente ID disponible de la tabla productos: {e}"
        )
        conexionDB.close()
        nextAvailableId = 0
        input("\nPresione una tecla para continuar... ")
    return nextAvailableId


# Esta funcion lee todos los datos de la tabla productos y retorna una lista de tuplas con los datos de la tabla
def db_obtener_productos_todos():
    lista_productos = []
    try:
        conexionDB, cursorDB = db_abrir_conexion()
        query = "SELECT * FROM productos"
        cursorDB.execute(query)
        lista_productos = cursorDB.fetchall()  # retorna una lista de tuplas
        conexionDB.close()
    except sqlite3.Error as e:
        print(f"Error al intentar obtener los datos de la tabla productos: {e}")
        conexionDB.close()
        lista_productos = []
        input("\nPresione una tecla para continuar... ")
    return lista_productos


def mostrar_productos_DB_comoJson():
    lista_productos = db_obtener_productos_todos()  # retorna una lista de tuplas
    if not lista_productos:
        print("No hay productos que mostrar")
    else:
        for producto in lista_productos:
            print(producto)


# Esta funcion trae el registro de la tabla productos cuyo id es código (el código del producto se pasará por parámetro) en formato de tupla
def db_obtener_producto_id(id):
    producto = {}
    try:
        conexionDB, cursorDB = db_abrir_conexion()
        query = "SELECT * FROM productos WHERE id = ?"
        placeholder = (id,)
        cursorDB.execute(query, placeholder)
        producto = cursorDB.fetchone()  # retorna una tupla
        conexionDB.close()
    except sqlite3.Error as e:
        print(f"Error al intentar obtener los datos del producto código {id}: {e}")
        conexionDB.close()
        input("\nPresione una tecla para continuar... ")
    return producto


# Esta funcion trae los registros de la tabla productos en donde el nombre contenga la cadena pasada por parámetro sin considerar maýusculas.  La devolución es en formato de lista de tuplas.
def db_obtener_producto_nombre(nombre):
    lista_productos = {}
    try:
        conexionDB, cursorDB = db_abrir_conexion()
        query = "SELECT * FROM productos WHERE lower(nombre) like ?"
        nombreLike = f"%{nombre.lower()}%"
        placeholder = (nombreLike,)
        cursorDB.execute(query, placeholder)
        lista_productos = cursorDB.fetchall()  # retorna una tupla
        conexionDB.close()
    except sqlite3.Error as e:
        print(
            f"Error al intentar obtener los datos de los productos con nombre {nombreLike}: {e}"
        )
        conexionDB.close()
        input("\nPresione una tecla para continuar... ")
    return lista_productos


# Esta funcion trae los registros de la tabla productos en donde el campo categoria contenga la cadena pasada por parámetro sin considerar maýusculas.  La devolución es en formato de lista de tuplas.
def db_obtener_producto_categoria(categoria):
    lista_productos = {}
    try:
        conexionDB, cursorDB = db_abrir_conexion()
        query = "SELECT * FROM productos WHERE lower(categoria) like ?"
        categoriaLike = f"%{categoria.lower()}%"
        placeholder = (categoriaLike,)
        cursorDB.execute(query, placeholder)
        lista_productos = cursorDB.fetchall()  # retorna una tupla
        conexionDB.close()
    except sqlite3.Error as e:
        print(
            f"Error al intentar obtener los datos de los productos con categoria {categoriaLike}: {e}"
        )
        conexionDB.close()
        input("\nPresione una tecla para continuar... ")
    return lista_productos


# Esta funcion recibe como argumento un producto en formato diccionario con las clave/valor de cada campo de la tabla e inserta los datos en la tabla productos
def db_insertar_producto(codigo, nombre, descripcion, cantidad, precio, categoria):
    state = False
    try:
        # Rutima que inserta en la Tabla
        conexionDB, cursorDB = db_abrir_conexion()
        query = "INSERT INTO productos ( id, nombre, descripcion, cantidad, precio, categoria ) VALUES ( ?, ?, ?, ?, ?, ? )"
        # query = "INSERT INTO productos  VALUES ( NULL, ?, ?, ?, ?, ?)" # en caso que no quiera pasar el campo código = Id, debo pasarlo en NULL el parámetro o sacarlo del insert.
        placeholder = (codigo, nombre, descripcion, cantidad, precio, categoria)
        cursorDB.execute(query, placeholder)
        conexionDB.commit()
        state = True
    except Exception as error:
        print(f"Error insertando producto: {error}")
        conexionDB.close()
        state = False
        input("\nPresione una tecla para continuar... ")
    return state


# Esta funcion permite actualizar los valores a cantidad del producto según el id
def db_actualizar_producto(id, producto_actualizado):
    try:
        conexionDB, cursorDB = db_abrir_conexion()
        query = "UPDATE productos SET id = ?, nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ? WHERE id = ?"
        placeholders = (
            producto_actualizado["codigo"],
            producto_actualizado["nombre"],
            producto_actualizado["descripcion"],
            producto_actualizado["cantidad"],
            producto_actualizado["precio"],
            producto_actualizado["categoria"],
            producto_actualizado["codigo"],
        )
        cursorDB.execute(query, placeholders)
        db_cerrar_conexion(conexionDB)
    except Exception as error:
        print(f"Error actualizando el producto: {error}")
        conexionDB.close()
        input("\nPresione una tecla para continuar... ")


# Esta funcion elimina de la tabla el producto con el id que recibe como argumento
def db_eliminar_producto(id):
    try:
        conexionDB, cursorDB = db_abrir_conexion()
        query = "DELETE FROM productos WHERE id = ?"
        placeholders = (id,)
        cursorDB.execute(query, placeholders)
        db_cerrar_conexion(conexionDB)
    except Exception as error:
        print(f"Error eliminando producto: {error}")
        conexionDB.close()
        input("\nPresione una tecla para continuar... ")


# Esta funcion permite obtener una lista de productos (como lista de tuplas) con aquellos registros cuya cantidad < minimo_stock
def db_get_productos_by_condicion(minimo_stock):
    lista_tuplas_productos = []
    try:
        conexionDB, cursorDB = db_abrir_conexion()
        query = "SELECT * FROM productos WHERE cantidad < ?"
        placeholders = (minimo_stock,)
        cursorDB.execute(query, placeholders)
        lista_tuplas_productos = cursorDB.fetchall()  # retorna una lista de tuplas
        conexionDB.close()
    except Exception as error:
        print(f"Error al obtener reporte bajo stock: {error}")
        conexionDB.close()
        lista_tuplas_productos = []
        input("\nPresione una tecla para continuar... ")
    return lista_tuplas_productos
