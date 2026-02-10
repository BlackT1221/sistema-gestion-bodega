from datetime import datetime
from src.models import LoteProducto
from src.inventory import ArbolInventario

def run():
    bodega = ArbolInventario()

    #Datos para la demostracion

    datos = [
        LoteProducto(500, "Tarjeta Gráfica RTX 4060", "Hardware", 10, datetime.now(), "A1"),
        LoteProducto(250, "Procesador Intel i7", "Hardware", 25, datetime.now(), "B2"),
        LoteProducto(750, "Monitor 27' 144hz", "Periféricos", 15, datetime.now(), "C1"),
        LoteProducto(100, "Mouse Gamer", "Periféricos", 50, datetime.now(), "D5"),
        LoteProducto(500, "Tarjeta Gráfica RTX 4060", "Hardware", 5, datetime.now(), "A1"), # Duplicado para probar lógica
    ]

    print("--- Inicio de carga de inventario ---")
    
    for d in datos:
        print(d)
        bodega.insertar(d)
    
    print(f"Tamano del inventario (nodos unicos): {bodega._size}")

    print("--- INVENTARIO ORDENADO ---")

    for producto in bodega.recorrer_inorder():
        print(f"SKU: {producto.sku} / {producto.nombre} / {producto.cantidad}")

    print("--- BUSQUEDA ---")
    busqueda = 500
    resultado = bodega.buscar(busqueda)
    if resultado:
        print(f"Producto encontrado: {resultado}")
    else:
        print("producto no encontrado")
    
    
if __name__ == "__main__":
    run()