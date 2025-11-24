"""
app.py: Interfaz por consola y menú principal del inventario.
Operaciones: Agregar, Mostrar, Buscar, Actualizar, Eliminar, Estadísticas, Guardar CSV, Cargar CSV, Salir.
No se cierra ante errores: captura excepciones y vuelve al menú.
"""

from typing import List, Dict
from servicios import (
    agregar_producto, mostrar_inventario, buscar_producto,
    actualizar_producto, eliminar_producto, calcular_estadisticas
)
print("¡app.py se está ejecutando!")

from archivos import guardar_csv, cargar_csv

Producto = Dict[str, object]


def input_float(mensaje: str) -> float:
    """Lee un float no negativo con reintento."""
    while True:
        try:
            val = float(input(mensaje).strip())
            if val < 0:
                print("Debe ser no negativo.")
                continue
            return val
        except ValueError:
            print("Entrada inválida. Ingresa un número (ej. 12.5).")


def input_int(mensaje: str) -> int:
    """Lee un int no negativo con reintento."""
    while True:
        try:
            val = int(input(mensaje).strip())
            if val < 0:
                print("Debe ser no negativo.")
                continue
            return val
        except ValueError:
            print("Entrada inválida. Ingresa un entero (ej. 3).")


def mostrar_estadisticas_legible(stats: Dict[str, object]) -> None:
    """Imprime estadísticas con formato claro."""
    print("\nEstadísticas:")
    print("-" * 40)
    print(f"Unidades totales: {stats['unidades_totales']}")
    print(f"Valor total: {stats['valor_total']:.2f}")
    if stats["producto_mas_caro"]:
        nombre, precio = stats["producto_mas_caro"]
        print(f"Producto más caro: {nombre} (precio={precio:.2f})")
    else:
        print("Producto más caro: N/A")
    if stats["producto_mayor_stock"]:
        nombre, cantidad = stats["producto_mayor_stock"]
        print(f"Producto con mayor stock: {nombre} (cantidad={cantidad})")
    else:
        print("Producto con mayor stock: N/A")
    print("-" * 40)


def fusionar_inventarios(inventario: List[Producto], cargados: List[Producto]) -> None:
    """
    Fusión por nombre:
      - Si el nombre existe: suma cantidades; si el precio difiere, actualiza al nuevo.
      - Si no existe: agrega el producto.
    """
    index = {p["nombre"].lower(): p for p in inventario}
    for nuevo in cargados:
        key = nuevo["nombre"].lower()
        if key in index:
            existente = index[key]
            existente["cantidad"] += int(nuevo["cantidad"])
            if float(existente["precio"]) != float(nuevo["precio"]):
                existente["precio"] = float(nuevo["precio"])
        else:
            inventario.append({
                "nombre": nuevo["nombre"],
                "precio": float(nuevo["precio"]),
                "cantidad": int(nuevo["cantidad"])
            })


def menu() -> None:
    inventario: List[Producto] = []  
    while True:
        print("\nMenú Principal")
        print("-" * 40)
        print("1. Agregar")
        print("2. Mostrar")
        print("3. Buscar")
        print("4. Actualizar")
        print("5. Eliminar")
        print("6. Estadísticas")
        print("7. Guardar CSV")
        print("8. Cargar CSV")
        print("9. Salir")
        try:
            opcion = int(input("Selecciona una opción (1-9): ").strip())
        except ValueError:
            print("Opción inválida. Ingresa un número entre 1 y 9.")
            continue

        try:
            if opcion == 1:
                nombre = input("Nombre del producto: ").strip()
                precio = input_float("Precio: ")
                cantidad = input_int("Cantidad: ")
                if agregar_producto(inventario, nombre, precio, cantidad):
                    print("Producto agregado.")
                else:
                    print("No se agregó: nombre duplicado o datos inválidos.")

            elif opcion == 2:
                print(mostrar_inventario(inventario))

            elif opcion == 3:
                nombre = input("Nombre a buscar: ").strip()
                p = buscar_producto(inventario, nombre)
                if p:
                    print(f'Encontrado: {p["nombre"]} | precio={p["precio"]:.2f} | cantidad={p["cantidad"]}')
                else:
                    print("Producto no encontrado.")

            elif opcion == 4:
                nombre = input("Nombre a actualizar: ").strip()
                print("Deja vacío para mantener el valor actual.")
                nuevo_precio_str = input("Nuevo precio: ").strip()
                nueva_cantidad_str = input("Nueva cantidad: ").strip()

                nuevo_precio = None
                nueva_cantidad = None
                if nuevo_precio_str != "":
                    try:
                        val = float(nuevo_precio_str)
                        if val < 0:
                            raise ValueError
                        nuevo_precio = val
                    except ValueError:
                        print("Precio inválido, se mantiene.")
                if nueva_cantidad_str != "":
                    try:
                        val = int(nueva_cantidad_str)
                        if val < 0:
                            raise ValueError
                        nueva_cantidad = val
                    except ValueError:
                        print("Cantidad inválida, se mantiene.")

                if actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad):
                    print("Producto actualizado.")
                else:
                    print("No se pudo actualizar (producto no existe o datos inválidos).")

            elif opcion == 5:
                nombre = input("Nombre a eliminar: ").strip()
                if eliminar_producto(inventario, nombre):
                    print("Producto eliminado.")
                else:
                    print("Producto no encontrado.")

            elif opcion == 6:
                stats = calcular_estadisticas(inventario)
                mostrar_estadisticas_legible(stats)

            elif opcion == 7:
                 guardar_csv(inventario)

            elif opcion == 8:
                cargados, errores = cargar_csv()

                if not cargados and errores == 0:
                    continue

                decision = input("¿Sobrescribir inventario actual? (S/N): ").strip().upper()
                if decision == "S":
                    inventario.clear()
                    inventario.extend(cargados)
                    accion = "reemplazo"
                else:
                    fusionar_inventarios(inventario, cargados)
                    accion = "fusión"

                print(f"Resumen: {len(cargados)} productos cargados, {errores} filas inválidas, acción={accion}.")
                print(mostrar_inventario(inventario))

            elif opcion == 9:
                print("Saliendo...")
                break

            else:
                print("Opción inválida. Elige entre 1 y 9.")

        except Exception as e:
            # Cualquier error inesperado no cierra la app
            print(f"Ocurrió un error: {e}. Volviendo al menú.")


menu()
