import json
import os
DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(DIRECTORIO_BASE, "usuarios.json")


usuarios = []


def cargar_usuarios():
    global usuarios

    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            usuarios = json.load(archivo)
    else:
        usuarios = []


def guardar_usuarios():
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(usuarios, archivo, indent=4, ensure_ascii=False)


def crear_usuario(id_usuario, nombres, apellidos, telefono, direccion, tipo_usuario):
    if buscar_usuario(id_usuario) is not None:
        return False

    tipo_usuario = tipo_usuario.lower()

    if tipo_usuario not in ["empleado", "admin"]:
        return False

    nuevo_usuario = {
        "id": id_usuario,
        "nombres": nombres,
        "apellidos": apellidos,
        "telefono": telefono,
        "direccion": direccion,
        "tipo_usuario": tipo_usuario,
    }

    usuarios.append(nuevo_usuario)
    guardar_usuarios()
    return True



def listar_usuarios():
    return usuarios


def buscar_usuario(id_usuario):
    for usuario in usuarios:
        if str(usuario["id"]) == str(id_usuario):
            return usuario

    return None


def actualizar_usuario(id_usuario, nombres=None, apellidos=None, telefono=None, dirección=None, tipo_usuario=None):

    usuario = buscar_usuario(id_usuario)

    if usuario is None:
        return False

    if nombres is not None:
        usuario["nombres"] = nombres

    if apellidos is not None:
        usuario["apellidos"] = apellidos

    if telefono is not None:
        usuario["telefono"] = telefono

    if dirección is not None:
        usuario["direccion"] = dirección

    if tipo_usuario is not None:
        tipo_usuario = tipo_usuario.lower()
        if tipo_usuario not in ["empleado", "admin"]:
            return False

        usuario["tipo_usuario"] = tipo_usuario

    guardar_usuarios()
    return True


def eliminar_usuario(id_usuario):
    usuario = buscar_usuario(id_usuario)

    if usuario is None:
        return False

    usuarios.remove(usuario)
    guardar_usuarios()
    return True
cargar_usuarios()