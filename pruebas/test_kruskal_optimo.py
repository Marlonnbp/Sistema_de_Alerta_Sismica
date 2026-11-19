import itertools
import random
import unittest

from codigo_fuente.grafo import Grafo
from codigo_fuente.kruskal import kruskal
from codigo_fuente.nodo import NodoSensor


def crear_grafo(n, aristas):
    g = Grafo()
    for i in range(n):
        g.agregar_vertice(
            NodoSensor("S%02d" % (i + 1), "Ciudad%d" % (i + 1), 0.0, 0.0, 0.0, 1, 1)
        )
    for u, v, costo in aristas:
        g.agregar_arista("S%02d" % (u + 1), "S%02d" % (v + 1), costo)
    return g


def es_conexo(n, subconjunto):
    padre = list(range(n))

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    for u, v, _ in subconjunto:
        padre[raiz(u)] = raiz(v)
    return len({raiz(i) for i in range(n)}) == 1


def costo_minimo_fuerza_bruta(n, aristas):
    mejor = None
    for sub in itertools.combinations(aristas, n - 1):
        if es_conexo(n, sub):
            c = sum(a[2] for a in sub)
            if mejor is None or c < mejor:
                mejor = c
    return mejor


def grafo_aleatorio(n, semilla):
    rnd = random.Random(semilla)
    pares = list(itertools.combinations(range(n), 2))
    aristas = [(u, v, rnd.randint(1, 50)) for u, v in pares]
    return aristas


class TestKruskalOptimo(unittest.TestCase):

    def test_20_grafos_contra_fuerza_bruta(self):
        for semilla in range(20):
            n = 5 + semilla % 2  # alterna 5 y 6 sensores
            aristas = grafo_aleatorio(n, semilla)
            grafo = crear_grafo(n, aristas)
            arbol, costo = kruskal(grafo)
            esperado = costo_minimo_fuerza_bruta(n, aristas)
            with self.subTest(semilla=semilla):
                self.assertEqual(arbol.obtener_tamano(), n - 1)
                self.assertEqual(costo, esperado)


if __name__ == "__main__":
    unittest.main()