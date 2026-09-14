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
    cargar_datos()
    limpiar_pantalla()
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
        elif tipo == "empleado":
            print("\n--- MENÚ EMPLEADO ---")
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
        print(f"{VERDE}=== GESTIÓN DE MATERIALES INVENTARIO ==={RESET}")
        print(f"{VERDE}1. Añadir / Comprar material (Actualiza stock existente u orígenes){RESET}")
        print(f"{VERDE}2. Listar todos los materiales{RESET}")
        print(f"{VERDE}3. Consultar material{RESET}")
        print(f"{VERDE}4. Actualizar datos de un material{RESET}")
        print(f"{VERDE}5. Inactivar material (Marcar como agotado){RESET}")
        print(f"{ROJO}6. Volver al menú principal{RESET}")

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
            print(f"{ROJO}Opción inválida. Intente de nuevo.\n{RESET}")
        input("\nPresione Enter para continuar...")
        limpiar_pantalla()

def menu_servicios_procesos():
    while True:
        print(f"{MORADO}=== GESTIÓN DE SERVICIOS Y PROCESOS DE PRODUCCIÓN ==={RESET}")
        print(f"{MORADO}1. Crear Servicio Individual (Definir insumos){RESET}")
        print(f"{MORADO}2. Crear Proceso / Fórmula (Secuencia de servicios){RESET}")
        print(f"{ROJO}3. Volver al menú principal{RESET}")

        opcion = input("\nSelecione una opción: ").strip()

        if opcion == "1":
            crear_servicio()
        elif opcion == "2":
            crear_proceso()
        elif opcion == "3":
            break
        else:
            print(f"{ROJO}Opción inválida. Intente de nuevo.\n{RESET}")
        input("\nPresione Enter para Continuar...")
        limpiar_pantalla()


if __name__ == "__main__":
    iniciar_sistema()