from codigo_fuente.cola import Cola
from codigo_fuente.tabla_hash import TablaHash


def bfs_saltos(grafo, origen_id):
    """Devuelve una TablaHash {id_sensor: saltos desde origen_id}.
    Los sensores inalcanzables no aparecen en la tabla."""
    distancias = TablaHash()
    distancias.insertar(origen_id, 0)

    cola = Cola()
    cola.encolar(origen_id)

    while not cola.esta_vacia():
        actual = cola.desencolar()
        distancia_actual = distancias.buscar(actual)

        for arista in grafo.obtener_vecinos(actual):
            vecino = arista.destino if arista.origen == actual else arista.origen

            # la propia tabla de distancias hace de conjunto de visitados
            if not distancias.contiene(vecino):
                distancias.insertar(vecino, distancia_actual + 1)
                cola.encolar(vecino)

    return distancias


def bfs_camino(grafo, origen_id, destino_id):
    """Devuelve la lista de ids del camino con menos saltos, o [] si no existe."""
    if origen_id not in grafo.adyacencias or destino_id not in grafo.adyacencias:
        return []

    predecesores = TablaHash()
    predecesores.insertar(origen_id, None)

    cola = Cola()
    cola.encolar(origen_id)

    encontrado = False
    while not cola.esta_vacia():
        actual = cola.desencolar()

        if actual == destino_id:
            encontrado = True
            break

        for arista in grafo.obtener_vecinos(actual):
            vecino = arista.destino if arista.origen == actual else arista.origen

            if not predecesores.contiene(vecino):
                predecesores.insertar(vecino, actual)
                cola.encolar(vecino)

    if not encontrado:
        return []

    # Reconstruccion de la ruta
    camino = []
    actual = destino_id
    while actual is not None:
        camino.append(actual)
        actual = predecesores.buscar(actual)

    camino.reverse()
    return camino