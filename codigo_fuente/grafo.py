from codigo_fuente.nodo import NodoSensor
from codigo_fuente.arista import Arista
from codigo_fuente.lista_enlazada import ListaEnlazada
from codigo_fuente.tabla_hash import TablaHash


class Grafo:
    def __init__(self):
        self.vertices = ListaEnlazada()
        self.aristas = ListaEnlazada()
        self.adyacencias = TablaHash()
        self.sensores_por_id = TablaHash()

    def agregar_vertice(self, sensor: NodoSensor):
        if sensor.id not in self.adyacencias:
            self.vertices.agregar_al_final(sensor)
            self.adyacencias.insertar(sensor.id, ListaEnlazada())
            self.sensores_por_id.insertar(sensor.id, sensor)

    def agregar_arista(self, id_u, id_v, costo):
        if id_u not in self.adyacencias or id_v not in self.adyacencias:
            raise ValueError(f"Sensor inexistente: {id_u} o {id_v}")
        if id_u == id_v:
            raise ValueError(f"Un sensor no puede enlazarse consigo mismo: {id_u}")

        menor, mayor = sorted((id_u, id_v))
        arista_directa = Arista(menor, mayor, costo)
        arista_inversa = Arista(mayor, menor, costo)

        self.adyacencias.buscar(menor).agregar_al_final(arista_directa)
        self.adyacencias.buscar(mayor).agregar_al_final(arista_inversa)
        self.aristas.agregar_al_final(arista_directa)

    def obtener_sensor(self, id_sensor):
        return self.sensores_por_id.buscar(id_sensor)

    def obtener_vecinos(self, id_sensor):
        vecinos = self.adyacencias.buscar(id_sensor)
        return vecinos if vecinos is not None else ListaEnlazada()

    def cantidad_vertices(self):
        return self.vertices.obtener_tamano()

    def cantidad_aristas(self):
        return self.aristas.obtener_tamano()