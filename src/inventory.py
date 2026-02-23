from typing import Optional, Generator, List
from src.models import LoteProducto
from src.node import NodoInventario
import json
import os

class ArbolInventario:
    def __init__(self):
        self.root: Optional[NodoInventario] = None
        self._size: int = 0  # Para benchmark rápido de tamaño

    def insertar(self, lote: LoteProducto) -> None:
        if not self.root:
            self.root = NodoInventario(lote)
            self._size += 1
        else:
            self._insertar_recursivo(self.root, lote)

    def _insertar_recursivo(self, actual: NodoInventario, lote: LoteProducto) -> None:
        if lote.sku < actual.data.sku:
            if actual.left is None:
                actual.left = NodoInventario(lote)
                self._size += 1
            else:
                self._insertar_recursivo(actual.left, lote)
        elif lote.sku > actual.data.sku:
            if actual.right is None:
                actual.right = NodoInventario(lote)
                self._size += 1
            else:
                self._insertar_recursivo(actual.right, lote)
        else:
            print(f"⚠ SKU {lote.sku} existente. Actualizando inventario (+{lote.cantidad}).")
            actual.data.cantidad += lote.cantidad

    def buscar(self, sku: int) -> Optional[LoteProducto]:
        return self._buscar_recursivo(self.root, sku)

    def _buscar_recursivo(self, actual: Optional[NodoInventario], sku: int) -> Optional[LoteProducto]:
        if actual is None or actual.data.sku == sku:
            return actual.data if actual else None
        
        if sku < actual.data.sku:
            return self._buscar_recursivo(actual.left, sku)
        return self._buscar_recursivo(actual.right, sku)

    # RETO: Uso de Generadores (yield) para eficiencia de memoria en recorridos masivos
    def recorrer_inorder(self) -> Generator[LoteProducto, None, None]:
        yield from self._inorder_recursivo(self.root)

    def _inorder_recursivo(self, actual: Optional[NodoInventario]) -> Generator[LoteProducto, None, None]:
        if actual:
            yield from self._inorder_recursivo(actual.left)
            yield actual.data
            yield from self._inorder_recursivo(actual.right)

    # -- Persistencia de datos

    # Guardar el arbol en el disco usando json pre-order
    
    def guardar_en_json(self, ruta_archivo: str):
        print(f"Guardando archivo en {ruta_archivo}...")

        # Obtener la lista de los diccionarios

        lista_datos = [p.to_dict() for p in self.recorrer_preorder()]

        # Asegurarnos que ese directorio existe
        os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)

        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(lista_datos, f, indent=4)
        print("Guardado exitoso")
    
    def cargar_desde_json(self, ruta_archivo: str):
        #Leer el json y poblar arbol
        if not os.path.exists(ruta_archivo):
            print(f"⚠ La ruta para el archivo({ruta_archivo}) no existe.")
            return
        
        print(f"Cargando el inventario desde {ruta_archivo}...")
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            lista_datos = json.load(f)

        self.root = None # Limpiar el arbol
        self._size = 0

        for item in lista_datos:
            producto = LoteProducto.from_dict(item)
            self.insertar(producto)
        
        print(f"Carga completada. {self._size} productos recuperados")

    def recorrer_preorder(self) -> Generator[LoteProducto, None, None]:
        yield from self._preorder_recursivo(self.root)

    def _preorder_recursivo(self, actual: Optional[NodoInventario]) -> Generator[LoteProducto, None, None]:
        if actual:
            yield actual.data #raiz
            yield from self._preorder_recursivo(actual.left)
            yield from self._preorder_recursivo(actual.right)
    
    def eliminar(self, sku: int) -> bool:
        self.root, eliminado = self._eliminar_recursivo(self.root, sku)
        if eliminado:
            self._size -= 1
        return eliminado

    def _eliminar_recursivo(self, actual: Optional[NodoInventario], sku: int):
        if not actual:
            return actual, False
        
        if sku < actual.data.sku:
            actual.left, eliminado = self._eliminar_recursivo(actual.left, sku)
        elif sku > actual.data.sku:
            # CORRECCIÓN 1: Debe ser actual.right
            actual.right, eliminado = self._eliminar_recursivo(actual.right, sku)
        else:
            # Caso 1 y 2: Sin hijos o con un solo hijo
            if not actual.left:
                return actual.right, True
            if not actual.right:
                return actual.left, True
            
            # Caso 3 Dos Hijos
            temp = self._min_value_node(actual.right)
            # CORRECCIÓN 2: Asignar el dato al nodo actual
            actual.data = temp.data
            actual.right, _ = self._eliminar_recursivo(actual.right, temp.data.sku)
            return actual, True
        
        return actual, eliminado
    
    def _min_value_node(self, nodo: NodoInventario) -> NodoInventario:
        current = nodo

        while current.left is not None:
            current = current.left
        
        return current
    
    def imprimir_arbol(self):
        if not self.root:
            print("el inventario esta vacio")
        else:
            self._imprimir_recursivo(self.root, 0, "Raíz: ")
    
    def _imprimir_recursivo(self, actual: Optional[NodoInventario], nivel: int, prefijo: str):
        if actual is not None:
            print(" " * (nivel * 4) + f"{prefijo}[{actual.data.sku}] {actual.data.nombre}")
            if actual.left or actual.right:
                if actual.left:
                    self._imprimir_recursivo(actual.left, nivel + 1, "Izq-- ")
                else:
                    print(" " * ((nivel + 1) * 4) + "Izq-- Vacío")
                
                if actual.right:
                    self._imprimir_recursivo(actual.right, nivel + 1, "Der-- ")
                else:
                    print(" " * ((nivel + 1) * 4) + "Der-- Vacío")