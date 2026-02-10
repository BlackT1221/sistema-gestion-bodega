from typing import Optional
from src.models import LoteProducto

class NodoInventario:
    def __init__(self, data: LoteProducto):
        self.data: LoteProducto = data
        self.right: Optional['NodoInventario'] = None
        self.left: Optional['NodoInventario'] = None

    def __repr__(self):
        return f"Node({self.data.sku})"