from dataclasses import dataclass
from datetime import datetime

@dataclass
class LoteProducto:
    sku: int
    nombre: str
    categoria: str
    cantidad: int
    fecha_ingreso: datetime
    ubicacion_pasillo: str

    def __repr__(self):
        return f"[{self.sku}] {self.nombre} // Cantidad: {self.cantidad}"