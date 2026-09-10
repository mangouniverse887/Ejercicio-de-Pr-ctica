import json
import os
AZUL = "\033[34m"
VERDE = "\033[32m"
ROJO = "\033[31m"
AMARILLO = "\033[33m"
CELESTE = "\033[36m"
MORADO = "\033[35m"
RESET = "\033[0m"

TIPO_UNIDAD = {
    "l": "volumen", "ml": "volumen",
    "kg": "masa", "g": "masa", "mg": "masa",
    "m": "Longitud", "cm": "longitud"
}

FACTOR_CONVER = {
    "ml": 1, "l": 1000,
    "mg": 1, "g": 1000, "kg": 1000000,
    "cm": 1, "m": 100
}

UNIDAD_BASE = {
    "volumen": "ml",
    "masa": "mg",
    "longitud": "cm"
}

DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(DIRECTORIO_BASE, "materiales.json")

materiales = []

def cargar_materiales ():
    global materiales
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            materiales = json.load(archivo)

def guardar_material():
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(materiales, archivo, indent=4, ensure_ascii=False)

def buscar_material(termino):
    termino_str = str(termino).strip().lower()

    for material in materiales:
        id_str = str(material["id"]).strip().lower()
        nombre_str = material["nombre"].strip().lower()

        if id_str == termino_str or nombre_str == termino_str:
            return material

    return None

    
def comprar_material():
    print("\n--- AÑADIR MATERIAL ---")
    termino = input("Ingrese el ID o Nombre del material: ").strip()
    material = buscar_material(termino)
    
    if material is not None:
        print(f"Material encontrado: {material['nombre']} (Stock actual: {material['stock']:.2f} {material['unidad_base']})")
        unidad_compra = input("Unidad de la nueva compra (ej. L, ml, kg, mg): ").strip().lower()

        if TIPO_UNIDAD.get(unidad_compra) != material.get("tipo_magnitud"):
            print("Error: La unidad no coincide con el tipo de magnitud del material")
            return

        cantidad_compra = float(input("Cantidad comprada: "))
        cantidad_base = cantidad_compra * FACTOR_CONVER[unidad_compra]
        material["stock"] += cantidad_base
        guardar_material()
        print("Stock actualizado correctamente.")

    else:
        print("El material no existe. Procediendo a registrar uno nuevo. (Ingrese N/A para cancelar)")

        id_material = input("Ingrese el ID del material: ").strip()
        if buscar_material(id_material) is not None:
            print("Error: Ya existeun material registrado con ese ID exacto.")
            return
        if id_material.lower() == "n/a":
            print("Registro de material cancelado.")
            return
        nombre = input("Nombre del material: ").strip()
        categoria = input("Cateogría: ").strip()
        unidad = input("unidad de medida inicial (ej. ml, L, mg, kg): ").strip().lower()

        if unidad not in TIPO_UNIDAD:
            print("Unidad no reconocida, operación cancelada.")
            return

        cantidad = float(input("Cantidad disponible (0 si es inagotable): "))
        valor_unitario = float(input("Valor unitario: "))
        es_inagotable = input("¿Es un recurso inagotable? (s/n): ").strip().lower() == 's'

        tipo_mag = TIPO_UNIDAD[unidad]
        uni_base = UNIDAD_BASE[tipo_mag]
        stock_base = cantidad * FACTOR_CONVER[unidad]

        nuevo_material = {
            "id": id_material,
            "nombre": nombre,
            "categoria": categoria,
            "tipo_magnitud": tipo_mag,
            "unidad_base": uni_base,
            "stock": stock_base,
            "valor_unit": valor_unitario,
            "inagotable": es_inagotable
        }

        materiales.append(nuevo_material)
        guardar_material()
        print("Material añadido correctamente.")
def listar_material():
    print("\n--- LISTA DE MATERIALES ---")

    if len(materiales) == 0:
        print("No hay materiales registrados.")
        return

    for material in materiales:
        print("-"*30)
        print("ID: ", material["id"])
        print("Nombre: ", material["nombre"])
        print("Categoria: ", material["categoria"])
        print("cantidad disponible: ", material["stock"])
        print("Valor unitario: ", material["valor_unit"])


def consultar_material():
    print("\n--- CONSULTAR MATERIAL ---")

    id_buscar = input("Ingrese el ID del material: ").strip()
    material = buscar_material(id_buscar)

    if material is None:
        print("No se encontró el material.")
        return

    print("\nMaterial encontrado:")
    print("ID:", material["id"])
    print("Nombre:", material["nombre"])
    print("Categoría:", material["categoria"])
    print("cantidad disponible: ", material["stock"])
    print("Valor unitario: ", material["valor_unit"])

def actualizar_material():
    print("\n--- ACTUALIZAR MATERIAL ---")
    
    id_buscar = int(input("Ingrese el ID del material: "))
    material = buscar_material(id_buscar)

    if material is None:
        print("No se encontró el material.")
        return

    print("Deje el campo vacío si no desea modificarlo.")

    nombre = input("Nuevo nombre: ")
    categoria = input("Nueva categoría: ")
    stock = input("Nueva cantidad disponible: ")
    valor = input("Nuevo valor unitario: ")

    if nombre != "":
        material["nombre"] = nombre

    if categoria != "":
        material["categoria"] = categoria

    if stock != "":
        material["stock"] = int(stock)

    if valor != "":
        material["valor_unit"] = float(valor)

    guardar_material()

    print("Material actualizado correctamente.")

def inactivar_material():
    print("\n--- INACTIVAR MATERIAL ---")

    id_buscar = int(input("Ingrese el ID del material: "))

    material = buscar_material(id_buscar)

    if material is None:
        print("No se encontró el material.")
        return

    material["estado"] = "agotado"

    guardar_material()

    print("Material inactivado correctamente.")
