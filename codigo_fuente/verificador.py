from codigo_fuente.lista_enlazada import ListaEnlazada
from codigo_fuente.tabla_hash import TablaHash


def _construir_adyacencia(ids, aristas):
    adyacencia = TablaHash()
    for id_sensor in ids:
        adyacencia.insertar(id_sensor, ListaEnlazada())
    for arista in aristas:
        adyacencia.buscar(arista.origen).agregar_al_final(arista.destino)
        adyacencia.buscar(arista.destino).agregar_al_final(arista.origen)
    return adyacencia


def _dfs(adyacencia, actual, padre, visitados):
    visitados.insertar(actual, True)
    hay_ciclo = False
    for vecino in adyacencia.buscar(actual):
        if not visitados.contiene(vecino):
            if _dfs(adyacencia, vecino, actual, visitados):
                hay_ciclo = True
        elif vecino != padre:
            hay_ciclo = True
    return hay_ciclo


def es_conexo(ids, aristas):
    ids = list(ids)
    if not ids:
        return True
    adyacencia = _construir_adyacencia(ids, aristas)
    visitados = TablaHash()
    _dfs(adyacencia, ids[0], None, visitados)
    return visitados.obtener_tamano() == len(ids)


def tiene_ciclos(ids, aristas):
    ids = list(ids)
    adyacencia = _construir_adyacencia(ids, aristas)
    visitados = TablaHash()
    for id_sensor in ids:
        if not visitados.contiene(id_sensor):
            if _dfs(adyacencia, id_sensor, None, visitados):
                return True
    return False


def verificar_arbol(grafo, arbol):
    ids = [sensor.id for sensor in grafo.vertices]
    aristas = list(arbol)
    esperadas = len(ids) - 1
    conexo = es_conexo(ids, aristas)
    sin_ciclos = not tiene_ciclos(ids, aristas)
    return {
        'aristas_esperadas': esperadas,
        'aristas_obtenidas': len(aristas),
        'conexo': conexo,
        'sin_ciclos': sin_ciclos,
        'costo_total': sum(arista.costo for arista in aristas),
        'valido': len(aristas) == esperadas and conexo and sin_ciclos,
    }


def verificar_red_operativa(grafo, aristas):
    ids = [sensor.id for sensor in grafo.vertices]
    aristas = list(aristas)
    return {
        'aristas': len(aristas),
        'conexa': es_conexo(ids, aristas),
        'costo_total': sum(arista.costo for arista in aristas),
    }