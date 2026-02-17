from datetime import datetime
from src.models import LoteProducto
from src.inventory import ArbolInventario

# Definir la ruta del json
RUTA_JSON = "data/dataset.json"

def run():
    bodega = ArbolInventario()

    # Primer paso: Intentar cargar
    bodega.cargar_desde_json(RUTA_JSON)

    #Si fuera la primera vez

    if bodega._size == 0:
        print("---Primera Ejecucion---")
        datos = [
            LoteProducto(500, "Tarjeta Gráfica RTX 4060", "Hardware", 10, datetime.now(), "A1"),
            LoteProducto(250, "Procesador Intel i7", "Hardware", 25, datetime.now(), "B2"),
            LoteProducto(750, "Monitor 27' 144hz", "Periféricos", 15, datetime.now(), "C1"),
            LoteProducto(100, "Mouse Gamer", "Periféricos", 50, datetime.now(), "D5"),
            LoteProducto(500, "Tarjeta Gráfica RTX 4060", "Hardware", 5, datetime.now(), "A1"), # Duplicado para probar lógica
        ]

        for d in datos:
            bodega.insertar(d)

        bodega.guardar_en_json
    
    print(f"Inventario actual: {bodega._size} productos encontrados.")
    print("Simulando llegada de mercancia nueva...")
    nuevo = LoteProducto(300, "TECLADO MECANICO BLUE SWITCHES", "Periféricos", 20, datetime.now(), "E3")
    bodega.insertar(nuevo)

    bodega.guardar_en_json(RUTA_JSON)

    bodega.imprimir_arbol()
    print("Fin ejecucion")
    
if __name__ == "__main__":
    run()