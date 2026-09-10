import sys
import os
import usuarios
import menu_admin_func
from Materiales import AZUL, VERDE, MORADO, AMARILLO, ROJO, RESET
from Materiales import (
    comprar_material, listar_material, consultar_material, actualizar_material, inactivar_material
)
from Servicios_procesos import (
    cargar_datos, crear_servicio, crear_proceso, ejecutar_proceso
)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def iniciar_sistema():
    print("="*40)
    print("--- PROGRAMA CONTROL Y PRODUCCIÓN ---")
    print("="*40)
    id_ingreso = input("Por favor, ingrese su ID (cédula) para iniciar: ")
    usuario_actual = usuarios.buscar_usuario(id_ingreso)
    if not usuario_actual:
        print("Usuario no encontrado. Contacte a un administrador para registrarse.")
        return
    print(f"\n ¡Hola, {usuario_actual['nombres']} {usuario_actual['apellidos']}!")
    while True:
        tipo = usuario_actual.get("tipo_usuario", "").lower()
        if tipo == "admin":
            print("\n--- MENÚ ADMIN ---")
            print(f"{AZUL}1. Gestionar Usuarios{RESET}")
            print(f"{VERDE}2. Gestionar Materiales e Inventario{RESET}")
            print(f"{MORADO}3. Gestionar Servicios y Procesos{RESET}")
            print(f"{AMARILLO}4. Ejecutar Producción{RESET}")
            print(f"{ROJO}5. Salir del programa{RESET}")
            opcion = input("\nElige una opción (1-5): ")
            if opcion == "1":
                menu_admin_func.gestionar_usuarios()
            elif opcion == "2":
                menu_materiales()
            elif opcion == "3":
                menu_servicios_procesos()
            elif opcion == "4":
                ejecutar_proceso()
            elif opcion == "5":
                print("\nCerrando el sistema... Datos guardados correctamente.")
                sys.exit()
            else:
                print("\nOpción inválida. Intente de nuevo.\n")
        elif tipo == "trabajador":
            print("\n--- MENÚ TRABAJADOR ---")
            print(f"{VERDE}1. Gestionar Materiales e Inventario{RESET}")
            print(f"{MORADO}2. Gestionar Servicios y Procesos{RESET}")
            print(f"{AMARILLO}3. Ejecutar Producción{RESET}")
            print(f"{ROJO}4. Salir del programa{RESET}")
            opcion = input("\nElige una opción (1-4): ")
            if opcion == "1":
                menu_materiales()
            elif opcion == "2":
                menu_servicios_procesos()
            elif opcion == "3":
                ejecutar_proceso()
            elif opcion == "4":
                print("\nCerrando el sistema... Datos guardados correctamente.")
                sys.exit()
            else:
                print("\nOpción inválida. Intente de nuevo.\n")

def menu_materiales():
    while True:
        print("=== GESTIÓN DE MATERIALES INVENTARIO ===")
        print("1. Añadir / Comprar material (Actualiza stock existente u orígenes)")
        print("2. Listar todos los materiales")
        print("3. Consultar material")
        print("4. Actualizar datos de un material")
        print("5. Inactivar material (Marcar como agotado)")
        print("6. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            comprar_material()
        elif opcion == "2":
            listar_material()
        elif opcion == "3":
            consultar_material()
        elif opcion == "4":
            actualizar_material()
        elif opcion == "5":
            inactivar_material()
        elif opcion == "6":
            break
        else:
            print("Opción inválida. Intente de nuevo.\n")
        limpiar_pantalla()

def menu_servicios_procesos():
    while True:
        print("=== GESTIÓN DE SERVICIOS Y PROCESOS DE PRODUCCIÓN ===")
        print("1. Crear Servicio Individual (Definir insumos)")
        print("2. Crear Proceso / Fórmula (Secuencia de servicios)")
        print("3. Volver al menú principal")

        opcion = input("\nSelecione una opción: ").strip()

        if opcion == "1":
            crear_servicio()
        elif opcion == "2":
            crear_proceso()
        elif opcion == "3":
            break
        else:
            print("Opción inválida. Intente de nuevo.\n")
        limpiar_pantalla()

def menu_principal():
    cargar_datos()

    while True:
        print("=" * 50)
        print("     SISTEMA CENTRAL DE CONTROL Y PRODUCCIÓN      ")
        print("=" * 50)
        print("1. Modulo de Materiales e Inventario")
        print("2. Módulo de Servicios y Procesos (Fórmulas)")
        print("3. Ejecutar Producción")
        print("4. Salir")

        opcion = input("\nSeleccione una opción (1-4): ").strip()

        if opcion == "1":
            limpiar_pantalla()
            menu_materiales()
        elif opcion == "2":
            limpiar_pantalla()
            menu_servicios_procesos()
        elif opcion == "3":
            limpiar_pantalla()
            ejecutar_proceso()
            limpiar_pantalla()
        elif opcion == "4":
            print("\nCerrando el sistema... Dat os guardados correctamente.")
            sys.exit()
        else:
            print("\nOpción inválida, Ingrese un número entre 1 y 4. \n")


if __name__ == "__main__":
    iniciar_sistema()