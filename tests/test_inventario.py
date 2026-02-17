import os
import pytest
from datetime import datetime
from src.models import LoteProducto

def test_insertar_raiz(inventario, producto_ejemplo):
    #Verificamos que el primer insert sea la raiz
    inventario.insertar(producto_ejemplo)
    assert inventario.root is not None
    assert inventario.root.data.sku == 50
    assert inventario._size == 1

def test_insertar_duplicado_suma_cantidad(inventario, producto_ejemplo):
    inventario.insertar(producto_ejemplo)
    inventario.insertar(producto_ejemplo)

    buscado = inventario.buscar(50)
    assert buscado.cantidad == 20
    assert inventario._size == 1

def test_buscar_existente(inventario_poblado):
    prod = inventario_poblado.buscar(70)
    assert prod is not None
    assert prod.nombre == "Prod-70"

def test_buscar_existente(inventario_poblado):
    prod = inventario_poblado.buscar(999)
    assert prod is None

def test_recorrido_in_order_ordenado(inventario_poblado):
    skus = [p.sku for p in inventario_poblado.recorrer_inorder()]
    assert skus == [20, 30, 40, 50, 60, 70, 80]

def tes_persistencia_json(inventario_poblado, tmp_path):
    archivo_test = tmp_path / "test_db.json"

    inventario_poblado.guardar_en_json(str(archivo_test))
    assert os.path.exists(archivo_test)

    from src.inventory import ArbolInventario
    nuevo_inv = ArbolInventario()
    nuevo_inv.cargar_desde_json(str(archivo_test))

    assert nuevo_inv._size == 7
    assert nuevo_inv.buscar(50).nombre == "Prod-50"

def test_eliminar_nodo_hoja(inventario_poblado):
    #Nodo 20 es hoja porque hizo izquierdo del 30, sin hijos propios
    exito = inventario_poblado.eliminar(20)
    assert exito is True
    assert inventario_poblado.buscar(20) is None

def test_eliminar_nodo_dos_hijos(inventario_poblado):
    # El 30 tiene dos hijos 20 y 40
    inventario_poblado.eliminar(30)
    assert inventario_poblado.buscar(30) is None
    # Verificar que sus hijos no se perdieron
    assert inventario_poblado.buscar(20) is not None
    assert inventario_poblado.buscar(40) is not None
