from app_funciones_menu import *


# Función principal para el sistema de inventario
def main():
    # Inicio declaracion de variables globales
    opcionSalida = "7"  # variable que setea el número de opción "Salir" en el "Menú Principal de Inventario". Se debe setear como String obligatoriamente.
    opcionStr = ""  # variable que guarda la opción elegida como un String.
    opcion = 0  # Variable que guarda la opción elegida como un Integer.
    # Fin declaracion de variables globales

    ############################################ Cuerpo de la función principal del programa: main() ############################################
    # Inicializamos la base de datos y creamos la tabla (si no existe)
    db_inicializar_tabla_productos()
    cargarDatosEnMemoria()
    # INICIO DEL LOOP DEL PROGRAMA PRINCIPAL
    while opcionStr != opcionSalida:
        clear_terminal()  # Limpio la consola para presentar el menú en pantalla limpia.
        mostrarOpcionesMenu()  # El menú permite según las opciones controlar la Entrada, Proceso y Salida de los Datos.
        opcionStr = input(f"\tElija una opción (1-{opcionSalida})\t")
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

    print("Fin del programa inventario.")


# Fin Función principal para el sistema de inventario

# Ejecución de la función main()
if __name__ == "__main__":
    main()
