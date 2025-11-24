"""
servicios.py: Funciones de lógica de negocio del inventario (CRUD + estadísticas).
El inventario es una lista de diccionarios con claves: nombre, precio, cantidad.
"""

from typing import List, Dict, Optional, Tuple

Producto = Dict[str, object]  # {"nombre": str, "precio": float, "cantidad": int}


def agregar_producto(inventario: List[Producto], nombre: str, precio: float, cantidad: int) -> bool:
    if not isinstance(nombre, str) or nombre.strip() == "":
        return False
    if not isinstance(precio, (int, float)) or precio < 0:
        return False
    if not isinstance(cantidad, int) or cantidad < 0:
        return False

    # Evitar duplicados por nombre
    if any(p["nombre"].lower() == nombre.lower() for p in inventario):
        return False

    inventario.append({"nombre": nombre.strip(), "precio": float(precio), "cantidad": int(cantidad)})
    return True


def mostrar_inventario(inventario: List[Producto]) -> str:
    if not inventario:
        return "Inventario vacío."
    lineas = ["Inventario:", "-" * 40]
    for p in inventario:
        subtotal = p["precio"] * p["cantidad"]
        lineas.append(f'- {p["nombre"]}: precio={p["precio"]:.2f}, cantidad={p["cantidad"]}, subtotal={subtotal:.2f}')
    return "\n".join(lineas)


def buscar_producto(inventario: List[Producto], nombre: str) -> Optional[Producto]:
    nombre = nombre.strip().lower()
    for p in inventario:
        if p["nombre"].lower() == nombre:
            return p
    return None


def actualizar_producto(
    inventario: List[Producto],
    nombre: str,
    nuevo_precio: Optional[float] = None,
    nueva_cantidad: Optional[int] = None
) -> bool:
    producto = buscar_producto(inventario, nombre)
    if producto is None:
        return False

    if nuevo_precio is not None:
        if not isinstance(nuevo_precio, (int, float)) or nuevo_precio < 0:
            return False
        producto["precio"] = float(nuevo_precio)

    if nueva_cantidad is not None:
        if not isinstance(nueva_cantidad, int) or nueva_cantidad < 0:
            return False
        producto["cantidad"] = int(nueva_cantidad)

    return True


def eliminar_producto(inventario: List[Producto], nombre: str) -> bool:
    idx = None
    for i, p in enumerate(inventario):
        if p["nombre"].lower() == nombre.strip().lower():
            idx = i
            break
    if idx is None:
        return False
    inventario.pop(idx)
    return True


def calcular_estadisticas(inventario: List[Producto]) -> Dict[str, object]:
    if not inventario:
        return {
            "unidades_totales": 0,
            "valor_total": 0.0,
            "producto_mas_caro": None,
            "producto_mayor_stock": None,
        }

    # Opcional: lambda para subtotal de cada producto
    subtotal = lambda p: p["precio"] * p["cantidad"]

    unidades_totales = sum(p["cantidad"] for p in inventario)
    valor_total = sum(subtotal(p) for p in inventario)

    # Producto más caro (por precio unitario)
    p_caro = max(inventario, key=lambda p: p["precio"])
    producto_mas_caro = (p_caro["nombre"], p_caro["precio"])

    # Producto con mayor stock (por cantidad)
    p_stock = max(inventario, key=lambda p: p["cantidad"])
    producto_mayor_stock = (p_stock["nombre"], p_stock["cantidad"])

    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": producto_mas_caro,
        "producto_mayor_stock": producto_mayor_stock,
    }
