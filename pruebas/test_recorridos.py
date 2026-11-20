import unittest
from codigo_fuente.grafo import Grafo
from codigo_fuente.nodo import NodoSensor
from codigo_fuente.recorridos import bfs_saltos, bfs_camino

class TestRecorridos(unittest.TestCase):
    
    def setUp(self):
        self.grafo = Grafo()
        self.s1 = NodoSensor("S01", "Lima", -12.0, -77.0, 10, 5, 2)
        self.s2 = NodoSensor("S02", "Callao", -12.1, -77.1, 5, 5, 2)
        self.s3 = NodoSensor("S03", "Ica", -14.0, -75.7, 100, 4, 2)
        self.s4 = NodoSensor("S04", "Pisco", -13.7, -76.2, 20, 4, 2)
        
        for s in [self.s1, self.s2, self.s3, self.s4]:
            self.grafo.agregar_vertice(s)
            
        self.grafo.agregar_arista("S01", "S02", 10.0)
        self.grafo.agregar_arista("S02", "S03", 15.0)
        self.grafo.agregar_arista("S03", "S04", 12.0)

    def test_bfs_saltos(self):
        distancias = bfs_saltos(self.grafo, "S01")
        self.assertEqual(distancias.buscar("S01"), 0)
        self.assertEqual(distancias.buscar("S02"), 1)
        self.assertEqual(distancias.buscar("S03"), 2)
        self.assertEqual(distancias.buscar("S04"), 3)

    def test_bfs_saltos_sensor_inalcanzable(self):
        aislado = NodoSensor("S05", "Tacna", -18.0, -70.2, 562, 5, 2)
        self.grafo.agregar_vertice(aislado)
        distancias = bfs_saltos(self.grafo, "S01")
        self.assertFalse(distancias.contiene("S05"))
        self.assertIsNone(distancias.buscar("S05"))

    def test_bfs_camino_normal(self):
        camino = bfs_camino(self.grafo, "S01", "S04")
        self.assertEqual(camino, ["S01", "S02", "S03", "S04"])

    def test_bfs_camino_en_sentido_inverso(self):
        camino = bfs_camino(self.grafo, "S04", "S01")
        self.assertEqual(camino, ["S04", "S03", "S02", "S01"])

    def test_bfs_camino_origen_igual_destino(self):
        camino = bfs_camino(self.grafo, "S02", "S02")
        self.assertEqual(camino, ["S02"])

    def test_bfs_camino_destino_inexistente(self):
        camino = bfs_camino(self.grafo, "S01", "S99")
        self.assertEqual(camino, [])

    def test_bfs_camino_sin_ruta_a_sensor_aislado(self):
        aislado = NodoSensor("S05", "Tacna", -18.0, -70.2, 562, 5, 2)
        self.grafo.agregar_vertice(aislado)
        camino = bfs_camino(self.grafo, "S01", "S05")
        self.assertEqual(camino, [])

if __name__ == "__main__":
    unittest.main()