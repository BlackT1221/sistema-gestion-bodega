import sys
import os
import time
import random
import string
from typing import List

# Ajuste para las importaciones
# importar src sin importar donde se ejecute el script

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models import LoteProducto
from src.inventory import ArbolInventario
from datetime import datetime

# Definicion de variables

CANTIDAD_DATOS = 1000000
RANGO_SKU_INICIO = 100000
RANGU_SKU_FIN = 999999

def generar_datos_falsos(n: int) -> List[LoteProducto]:
    # Generar datos de forma masiva
    print(f"Generando {n} productos aleatorios")
    dataset = []

    start_gen = time.perf_counter()

    for _ in range(n):
        # Generar los skus aleatorios.
        sku = random.randint(RANGO_SKU_INICIO, RANGU_SKU_FIN)
        nombre = ''.join(random.choices(string.ascii_uppercase, k=5))
        categoria = random.choice(["Electronica", "Hogar", "Ropa", "Juguetes"])

        producto = LoteProducto(
            sku=sku,
            nombre=f"PROD-{nombre}",
            categoria=categoria,
            cantidad=random.randint(1, 100),
            fecha_ingreso=datetime.now(),
            ubicacion_pasillo=f"P-{random.randint(1, 20)}"
        )

        dataset.append(producto)

    end_gen = time.perf_counter()
    print(f"Datos generados en {end_gen - start_gen:.4f} segundos")
    return dataset

def busqueda_lineal_lista(dataset: List[LoteProducto], sku_objetivo: int):
    # Busqueda elemento por elemento para la lista
    for p in dataset:
        if p.sku == sku_objetivo:
            return p
    return None

def ejecutar_benchmark():
    print("\n" + "="*60)
    print(f"INICIANDO BENCHMARK")
    print("="*60)

    # Primer paso: Generar datos
    datos = generar_datos_falsos(CANTIDAD_DATOS)

    # Segundo paso, elegir el sku a buscar
    target = datos[-1].sku
    print(f"El objetivo es el sku: {target}")

    # Ponlar el arbol
    print("\nPoblando el arbol...")
    bodega = ArbolInventario()

    start_load = time.perf_counter()

    for p in datos:
        bodega.insertar(p)
    
    end_load = time.perf_counter()
    print(f"Tiempo de insercion de datos al arbol es de {end_load - start_load:.4f} segundos")
    print(f"Total de los nodos unicos es de {bodega._size}")

    print("\n" + "-"*30)
    print("Empezamos la carrera de la lista versus el arbol")
    print("-"*30)

    # Hacer busqueda en la lista

    print("Iniciando busqueda lineal de la lista")
    start_list = time.perf_counter()
    res_list = busqueda_lineal_lista(datos, target)
    end_list = time.perf_counter()
    tiempo_lista = end_list - start_list
    print(f"El tiempo de la lista fue de {tiempo_lista:.10f} segundos")

    # Hacer la busqueda en el arbol
    
    print("Iniciando busqueda binaria en el arbol")
    start_tree = time.perf_counter()
    res_tree = bodega.buscar(target)
    end_tree = time.perf_counter()
    tiempo_tree = end_tree - start_tree
    print(f"El tiempo del arbol fue de {tiempo_tree:.10f} segundos")

    # Imprimir resultados

    print("\n" + "="*60)
    print("RESULTADOS FINALES")
    print("="*60)

    if tiempo_tree > 0:
        diferencia = tiempo_lista / tiempo_tree
        print(f"El Arbol Binario fue {diferencia:,.2f} veces mas rapido que la lista")
    else:
        print("El arbol hizo la busqueda en 0 segundos")

    print("\n" + "="*60)

if __name__ == "__main__":
    ejecutar_benchmark()