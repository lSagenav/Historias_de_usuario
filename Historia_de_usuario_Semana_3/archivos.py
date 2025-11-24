import os
import csv
from typing import List, Dict, Tuple

Producto = Dict[str, object]
HEADER = ["nombre", "precio", "cantidad"]


def guardar_csv(inventario: List[Dict], incluir_header: bool = True) -> bool:
    if not inventario:
        print("No se puede guardar: inventario vacío.")
        return False

    # Ruta fija en la misma carpeta del proyecto para guardar los datos
    ruta = os.path.join(os.path.dirname(__file__), "inventario.csv")

    try:
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if incluir_header:
                writer.writerow(HEADER)
            for p in inventario:
                # Validación extra: asegurar que los campos sean correctos
                try:
                    nombre = str(p["nombre"]).strip()
                    precio = float(p["precio"])
                    cantidad = int(p["cantidad"])
                    writer.writerow([nombre, f"{precio:.6f}", cantidad])
                except (ValueError, KeyError) as e:
                    print(f"Error en producto {p}: {e}")
        print(f"Inventario guardado en: {ruta}")
        return True
    except PermissionError:
        print("Error: permisos insuficientes para escribir el archivo.")
    except OSError as e:
        print(f"Error de escritura: {e}")
    return False


def _validar_header(header: List[str]) -> bool:
    esperado = ["Nombre", "Precio", "Cantidad"]
    return [h.strip().lower() for h in header] == [e.lower() for e in esperado]

def cargar_csv() -> Tuple[List[Producto], int]:
    productos: List[Producto] = []
    errores = 0

    # Ruta fija en la misma carpeta del proyecto para la carga de los datos 
    ruta = os.path.join(os.path.dirname(__file__), "inventario.csv")

    try:
        with open(ruta, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                print("Archivo vacío.")
                return ([], 0)

            if not _validar_header(header):
                print("Encabezado inválido. Se esperaba: Nombre, Precio, Cantidad.")
                return ([], 0)

            for i, row in enumerate(reader, start=2):  # desde línea 2 después del header
                if len(row) != 3:
                    errores += 1
                    continue
                nombre, precio_str, cantidad_str = row
                try:
                    precio = float(precio_str)
                    cantidad = int(cantidad_str)
                    if precio < 0 or cantidad < 0 or not nombre.strip():
                        errores += 1
                        continue
                    productos.append({"nombre": nombre.strip(), "precio": precio, "cantidad": cantidad})
                except ValueError:
                    errores += 1
                    continue

        if errores > 0:
            print(f"{errores} filas inválidas omitidas.")
        print(f"Inventario cargado automáticamente desde '{ruta}'.")
        return (productos, errores)

    except FileNotFoundError:
        print("Error: archivo inventario.csv no encontrado.")
        return ([], 0)
    except UnicodeDecodeError:
        print("Error: problema de codificación. Asegura UTF-8.")
        return ([], 0)
    except Exception as e:
        print(f"Error al cargar CSV: {e}")
        return ([], 0)
