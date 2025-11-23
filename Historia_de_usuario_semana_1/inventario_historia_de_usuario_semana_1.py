##

nombre_producto = input(" Porfavor ingresa el nombre del producto ")
while True:
    try:
        precio_producto = float(input(" Ingresa el valor del producto: "))
        break
    except ValueError:
        print(" X Error: Ingresa dato valido ")

while True:
    try:
        cantidad_producto = int(input(" Ingresa la cantidad del producto: "))
        break
    except ValueError:
        print(" X Error: Ingresa un numero entero valido ")


print(f" || Nombre del producto:  {nombre_producto} || precio: {precio_producto} ||cantidad: {cantidad_producto} ||")



consto_total = precio_producto * cantidad_producto

print(f"El precio total de {cantidad_producto} productos es {consto_total}")      