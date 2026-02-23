import requests
import random
from datetime import datetime
from src.models import LoteProducto
from src.inventory import ArbolInventario

def obtener_datos_api():
    url = "https://fakestoreapi.com/products"

    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar a la API: {e}")
        return []

def poblar_bodega_desde_api(arbol: ArbolInventario, datos_json: list):
    # Mapear el json y lo va a insertar en el BST
    print(f"Procesando {len(datos_json)} productos")

    for item in datos_json:
        #Mapearlos desde la api a el dataclass
        producto = LoteProducto(
            sku=item["id"],
            nombre=item["title"][:40],
            categoria=item["category"],
            cantidad=random.randint(10, 100),
            fecha_ingreso=datetime.now(),
            ubicacion_pasillo=f"Seccion {item['category'][:3].upper()}"
        )
        arbol.insertar(producto)

def mostrar_menu():
    print("\n" + "="*45)
    print(" 🏢 SISTEMA DE GESTIÓN DE BODEGA V2.0 🏢 ")
    print("="*45)
    print("1. 🌐 Cargar productos desde API (FakeStore)")
    print("2. 📋 Ver Inventario Completo (In-Order)")
    print("3. 🔍 Buscar producto por SKU")
    print("4. 🗑️  Eliminar producto por SKU")
    print("5. 💾 Guardar inventario en disco (JSON)")
    print("6. 📂 Cargar inventario desde disco (JSON)")
    print("7. 🌳 Mostrar estructura del árbol (Visual)")
    print("8. ❌ Salir")
    print("="*45)

def main():
    mi_bodega = ArbolInventario()
    ruta_archivo = "data/dataset.json"

    while True:
        mostrar_menu()
        opcion = input("Seleccionar una opcion (1-8)")

        if opcion == "1":
            poblar_bodega_desde_api(mi_bodega, obtener_datos_api())
        elif opcion == "2":
            if mi_bodega == 0:
                print("La bodega esta vacia")
            else: 
                print(f"\n{'SKU':<5} | {'CATEGORÍA':<15} | {'STOCK':<6} | {'NOMBRE DEL PRODUCTO'}")
                print("-" * 75)
                for prod in mi_bodega.recorrer_inorder():
                    print(f"{prod.sku:<5} | {prod.categoria:<15} | {prod.cantidad:<6} | {prod.nombre}")
        elif opcion == "3":
            try:
                sku_buscar = int(input("Ingresa el SKU a buscar"))
                resultado = mi_bodega.buscar(sku_buscar)
                
                if resultado:
                    print(f"\nProducto encontrado")
                    print(f"    - Nombre: {resultado.nombre}")
                    print(f"    - Categoria: {resultado.categoria}")
                    print(f"    - Stock: {resultado.cantidad}")
                    print(f"    - Ubicacion: {resultado.ubicacion_pasillo}")
                else: 
                    print("El SKU no existe")
            except ValueError:
                print("Ingresa un numero valido")
        elif opcion == "4":
            try:
                sku_eliminar = int(input("Ingresa el SKU a eliminar"))
                if mi_bodega.eliminar(sku_eliminar):
                    print(f"Producto con SKU {sku_eliminar} fue eliminado correctamente")
                else: 
                    print(f"Producto con SKU {sku_eliminar} no encontrado")
            except ValueError:
                print("Ingresa un numero valido")
        elif opcion == "5":
            mi_bodega.guardar_en_json(ruta_archivo)
        elif opcion == "6":
            mi_bodega.cargar_desde_json(ruta_archivo)
        elif opcion == "7":
            if hasattr(mi_bodega, 'imprimir_arbol'):
                print("\nEstructura del arbol binario:")
                mi_bodega.imprimir_arbol()
            else:
                print("El metodo no existe")
        elif opcion == "8":
            print("\n Gracias por usar el sistema")
            break
        
        else:
            print("La opcion no existe")

if __name__ == "__main__":
    main()