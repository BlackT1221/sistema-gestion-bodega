import pytest
from datetime import datetime
from src.models import LoteProducto
from src.inventory import ArbolInventario

# Fixture

@pytest.fixture
def producto_ejemplo():
    return LoteProducto(
        sku=50, 
        nombre="Monitor Test", 
        categoria="Tecnología", 
        cantidad=10, 
        fecha_ingreso=datetime.now(), 
        ubicacion_pasillo="A1"
    )

@pytest.fixture
def inventario():
    return ArbolInventario()

@pytest.fixture
def inventario_poblado(inventario):
    # Insertamos datos en desorden

    skus = [50, 30, 70, 20, 40, 60, 80]
    for sku in skus:
        prod = LoteProducto(
            sku=sku, 
            nombre=f"Prod-{sku}", 
            categoria="General", 
            cantidad=5, 
            fecha_ingreso=datetime.now(), 
            ubicacion_pasillo="B2"
        )
        inventario.insertar(prod)
    return inventario

