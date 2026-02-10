from typing import Optional, Generator
from src.models import LoteProducto
from src.node import NodoInventario

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