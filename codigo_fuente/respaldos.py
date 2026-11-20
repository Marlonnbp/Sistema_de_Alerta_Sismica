from codigo_fuente.recorridos import bfs_saltos
from codigo_fuente.cola_prioridad import ColaPrioridad
from codigo_fuente.tabla_hash import TablaHash
from codigo_fuente.lista_enlazada import ListaEnlazada


def seleccionar_respaldos(grafo_base, aristas_descartadas, R=8):
    respaldos_seleccionados = ListaEnlazada()
    contador_respaldos_sensor = TablaHash()  # Control del límite de 2 por sensor

    # Ordenar las aristas descartadas de menor a mayor costo con el heap propio.
    # Desempate por ID de sensor (RN-04) para que el resultado sea reproducible.
    cola = ColaPrioridad()
    for arista in aristas_descartadas:
        u, v = arista.origen, arista.destino
        cola.insertar((arista.costo, min(u, v), max(u, v), arista))

    while not cola.esta_vacia():
        if respaldos_seleccionados.obtener_tamano() >= R:
            break

        arista = cola.extraer_minimo()[3]
        u, v = arista.origen, arista.destino

        # Calculamos los saltos en el árbol base usando el BFS del grafo adaptado
        distancias_desde_u = bfs_saltos(grafo_base, u)
        saltos = distancias_desde_u.get(v, float('inf'))

        # (a) Excluir los que unen sensores a menos de 3 saltos en el árbol
        if saltos < 3:
            continue

        # Verificar la restricción: no más de 2 respaldos en un mismo sensor
        resp_u = contador_respaldos_sensor.buscar(u) or 0
        resp_v = contador_respaldos_sensor.buscar(v) or 0

        if resp_u < 2 and resp_v < 2:
            respaldos_seleccionados.agregar_al_final(arista)
            contador_respaldos_sensor.insertar(u, resp_u + 1)
            contador_respaldos_sensor.insertar(v, resp_v + 1)

    return respaldos_seleccionados