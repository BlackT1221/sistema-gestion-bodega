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

    # Serializamos: Pasar el objeto a diccionario

    def to_dict(self):
        return {
            "sku": self.sku,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "cantidad": self.cantidad,
            "fecha_ingreso": self.fecha_ingreso.isoformat(),
            "ubicacion_pasillo": self.ubicacion_pasillo
        }

    #des-serializar

    @staticmethod
    def from_dict(data: dict):
        # Convertir el string de la fecha en formato datetime
        data["fecha_ingreso"] = datetime.fromisoformat(data["fecha_ingreso"])
        return LoteProducto(**data) # Desempaquetado de datos