import json
import os
from datetime import datetime
from Materiales import (
    materiales, cargar_materiales, guardar_material, buscar_material,
    FACTOR_CONVER, TIPO_UNIDAD
)

DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_SERVICIOS = os.path.join(DIRECTORIO_BASE, "servicios.json")
ARCHIVO_PROCESOS = os.path.join(DIRECTORIO_BASE, "procesos.json")
ARCHIVO_PRODUCTOS = os.path.join(DIRECTORIO_BASE, "productos_terminados.json")

servicios = []
procesos = []
productos_terminados = []

def cargar_datos():
    global servicios, procesos, productos_terminados
    cargar_materiales()
    if os.path.exists(ARCHIVO_SERVICIOS):
        with open (ARCHIVO_SERVICIOS, "r", encoding="utf-8") as f:
            servicios = json.load(f)

    if os.path.exists(ARCHIVO_PROCESOS):
        with open(ARCHIVO_PROCESOS, "r", encoding="utf-8") as f:
            procesos = json.load(f)

    if os.path.exists(ARCHIVO_PRODUCTOS):
        with open(ARCHIVO_PRODUCTOS, "r", encoding="utf-8") as f:
            productos_terminados = json.load(f)

def guardar_json(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def crear_servicio():
    print("\n--- CREAR SERVICIO INDIVIDUAL ---")
    id_servicio = input("ID del Servicio: ")
    nombre = input("Nombre del Servicio (ej. Purificado con Ácido, Lavado): ")

    insumos = []
    print("\nAdición de insumos al servicio (Deje el término vacío para finalizar):")
    while True:
        termino = input("\nIngrese ID o Nombre del material requerido: ")
        if not termino:
            break

        mat = buscar_material(termino)
        if mat is None:
            print("Material no encontrado en inventario. Intente nuevamente.")
            continue

        unidad = input(f"Unidad a usar para {mat['nombre']} (ej. ml, L, mg, kg): ").lower()
        if TIPO_UNIDAD.get(unidad) != mat["tipo_maginitud"]:
            print(f"Error: La unidad '{unidad}' no coincide con el tipo de magnitud de del material ({mat['tipo_magnitud']}).")
            continue

        cantidad = float(input(f"Cantidad requerida {unidad}: "))
        insumos.append({
            "material_id": mat["id"],
            "material_nombre": mat["nombre"],
            "cantidad": cantidad,
            "unidad": unidad
            })

    nuevo_servicio = {
        "id": id_servicio,
        "nombre": nombre,
        "Insumos": insumos
    }

    servicios.append(nuevo_servicio)
    guardar_json(ARCHIVO_SERVICIOS, servicios)
    print(f"Servicio '{nombre}' registrado correctamente.")


def crear_proceso():
    print("\n--- CREAR PROCESO DE PRODUCCIÓN (FÓRMULA)---")
    id_proceso = input("ID del Proceso (ej. FORM-309): ")
    nombre = input("Nombre del Proceso/Fórmula: ")

    servicios_proceso = []
    print("\nAsignar Servicios al Proceso (Deje vacío para terminar):")
    while True:
        id_serv = input("ID o Nombre del servicio a incluir en secuencia: ")
        if not id_serv:
            break

        servicio_encontrado = next(
            (s for s in servicios if str(s["id"]) == id_serv or s["nombre"].lower() == id_serv.lower()), None
        )

        if servicio_encontrado is None:
            print("Servicio no encontrado.")
            continue

        servicios_proceso.append(servicio_encontrado["id"])
        print(f"Agregado servicio: {servicio_encontrado['nombre']}")
        
    nuevo_proceso = {
        "id": id_proceso,
        "nombre": nombre,
        "secuencia_servicios": servicios_proceso
        }

    procesos.append(nuevo_proceso)
    guardar_json(ARCHIVO_PROCESOS, procesos)
    print(f"Proceso '{nombre}' registrado correctamente.")


def ejecutar_proceso():
    print("\n--- EJECUTAR PROCESO DE PRODUCCIÓN ---")
    id_proc = input("ID o Nombre del Proceso a ejecutar: ")

    proceso = next(
        (p for p in procesos if str(p["id"]) == id_proc or p["nombre"].lower() == id_proc.lower()), None
    )

    if proceso is None:
        print("Proceso no encontrado.")
        return

    requerimientos_totales = {}

    for id_serv in proceso["secuencia_servicios"]:
        serv = next((s for s in servicios if s["id"] == id_serv), None)
        if serv is None:
            continue

        for insumo in serv["insumos"]:
            mat_id = insumo["material_id"]
            cant_base = insumo["cantidad"] * FACTOR_CONVER[insumo["unidad"]]
            if mat_id in requerimientos_totales:
                requerimientos_totales[mat_id] += cant_base
            else:
                requerimientos_totales[mat_id] = cant_base

    print("\nVerificando disponibilidad en inventario...")
    for mat_id, cant_requerida_base in requerimientos_totales.items():
        mat = buscar_material(mat_id)
        if mat["stock"] < cant_requerida_base:
            print(f"Stock insuficiente de {mat['nombre']}. Requerido: {cant_requerida_base} {mat['unidad_base']}, Disponible: {mat['stock']} {mat['unidad_base']}")
            return

    print("Stock verificado. Procediendo al descuento de materiales...")
    for mat_id, cant_requerida_base in requerimientos_totales.items():
        mat = buscar_material(mat_id)
        mat["stock"] -= cant_requerida_base
        print(f" - {mat['nombre']}: Descontados {cant_requerida_base} {mat['unidad_base']}. (Quedan: {mat['stock']} {mat['unidad_base']})")
    guardar_material()

    nombre_producto = input("\nNombre del producto final resultante: ")
    lote = input("Número de lote/referencia: ")
    cantidad_producida = float(input("Cantitad total producida: "))
    unidad_producida = input("Unidad del producto final (ej. Kgs, Unidades, Litros): ").lower()

    registro_producto = {
        "lote": lote,
        "nombre": nombre_producto,
        "proceso_origen": proceso["nombre"],
        "cantidad": cantidad_producida,
        "unidad": unidad_producida,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    productos_terminados.append(registro_producto)
    guardar_json(ARCHIVO_PRODUCTOS, productos_terminados)

    print(f"\n¡Éxito! Producto final '{nombre_producto}' registrado en 'productos_terminados.json'.")