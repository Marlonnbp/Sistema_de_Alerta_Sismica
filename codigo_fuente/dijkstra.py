from codigo_fuente.cola_prioridad import ColaPrioridad
from codigo_fuente.tabla_hash import TablaHash
from codigo_fuente.pila import Pila


def reconstruir_ruta(predecesores, origen, destino):
    """Reconstruye la ruta origen -> destino con una Pila.

    predecesores: TablaHash {id_sensor: id_del_predecesor}. Devuelve la lista de
    ids en orden, o None si el destino no es alcanzable desde el origen.
    """
    pila = Pila()
    actual = destino
    while actual is not None:
        pila.apilar(actual)
        if actual == origen:
            break
        actual = predecesores.buscar(actual)

    if pila.ver_tope() != origen:
        return None

    ruta = []
    while not pila.esta_vacia():
        ruta.append(pila.desapilar())
    return ruta


def dijkstra(grafo, id_origen, id_destino=None):
    if id_origen not in grafo.adyacencias:
        raise KeyError(f"Sensor inexistente: {id_origen}")

    distancias = TablaHash()
    predecesores = TablaHash()
    visitados = TablaHash()

    distancias.insertar(id_origen, 0)
    predecesores.insertar(id_origen, None)

    cola = ColaPrioridad()
    cola.insertar((0, id_origen))  # el empate se rompe por ID: resultado estable

    while not cola.esta_vacia():
        costo_actual, actual = cola.extraer_minimo()

        if visitados.contiene(actual):
            continue  # entrada vieja: ya se encontró un camino mejor
        visitados.insertar(actual, True)

        if actual == id_destino:
            break

        for arista in grafo.obtener_vecinos(actual):
            vecino = arista.destino
            costo = arista.costo

            if costo <= 0:
                raise ValueError(
                    f"Dijkstra exige costos positivos (enlace {actual}-{vecino}: {costo})"
                )
            if visitados.contiene(vecino):
                continue

            nuevo = costo_actual + costo
            previo = distancias.buscar(vecino)
            if previo is None or nuevo < previo:
                distancias.insertar(vecino, nuevo)
                predecesores.insertar(vecino, actual)
                cola.insertar((nuevo, vecino))

    return distancias, predecesores


def ruta_optima(grafo, id_origen, id_destino):
    distancias, predecesores = dijkstra(grafo, id_origen, id_destino)
    if not distancias.contiene(id_destino):
        return None
    ruta = reconstruir_ruta(predecesores, id_origen, id_destino)
    if ruta is None:
        return None
    return ruta, distancias.buscar(id_destino)


def crear_calcular_ruta(grafo_operativo):
    def calcular_ruta(id_origen, id_destino):
        return ruta_optima(grafo_operativo, id_origen, id_destino)
    return calcular_ruta