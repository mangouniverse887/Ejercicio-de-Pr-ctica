import usuarios

from Materiales import (
    comprar_material, listar_material, consultar_material, actualizar_material, inactivar_material
)
from Servicios_procesos import(
    cargar_datos, crear_servicio, crear_proceso, ejecutar_proceso
)

AZUL = "\033[34m"
VERDE = "\033[32m"
ROJO = "\033[31m"
AMARILLO = "\033[33m"
CELESTE = "\033[36m"
MORADO = "\033[35m"
RESET = "\033[0m"

def gestionar_usuarios():
    while True:
        print(f"{AZUL}1. Crear | 2. Listar | 3. Actualizar | 4. Eliminar |{ROJO} 5. Volver al menú{RESET}")
        sub_op = input("Elige acción: ")
        if sub_op =="1":
            id_u = input("ID: ")
            nom = input("Nombres: ")
            ape = input("Apellidos: ")
            tel = input("Teléfono: ")
            dire = input("Dirección: ")
            t_usu = input("Tipo (trabajador/admin): ")
            if usuarios.crear_usuario(id_u, nom, ape, tel, dire, t_usu):
                print(f"{VERDE}Usuario creado con éxito.{RESET}")
            else:
                print(f"{ROJO}Error: Datos inválidos o el usuario y a existe.{RESET}")
        elif sub_op == "2":
            lista = usuarios.listar_usuarios()
            for u in lista:
                print(f"- ID {u['id']}: {u['nombres']} {u['apellidos']} (Rol: {u['tipo_usuario']})")
        elif sub_op == "3":
            id_u = input("ID a actualizar: ")
            print("Deje el campo vacío y presione Enter si NO desea modificarlo: ")
            nuevo_nom = input("Nuevo nombre: ")
            nuevo_ape = input("Nuevo apellido: ")
            nuevo_tel = input("Nuevo teléfono: ")
            nuevo_dir = input("Nueva dirección: ")
            nuevo_tipo = input("Nuevo tipo (residente/admin): ")
            usuarios.actualizar_usuario(
                id_u,
                nombres=nuevo_nom if nuevo_nom != "" else None,
                apellidos=nuevo_ape if nuevo_ape != "" else None,
                telefono=nuevo_tel if nuevo_tel != "" else None,
                direccion=nuevo_dir if nuevo_dir != "" else None,
                tipo_usuario=nuevo_tipo if nuevo_tipo != "" else None
            )
            print(f"{VERDE}Proceso de actualización finalizado.{RESET}")
        elif sub_op == "4":
            id_u = input("ID a Eliminar: ")
            if usuarios.eliminar_usuario(id_u):
                print(f"{VERDE}Usuario eliminado del sistema.{RESET}")
            else:
                print(f"{ROJO}Error al eliminar (Usuario no encontrado){RESET}")
        elif sub_op == "5":
            break

