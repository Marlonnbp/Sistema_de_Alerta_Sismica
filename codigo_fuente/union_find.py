from codigo_fuente.tabla_hash import TablaHash


class UnionFind:
    def __init__(self, ids):
        self.padre = TablaHash()
        self.rango = TablaHash()
        for elem_id in ids:
            self.padre.insertar(elem_id, elem_id)
            self.rango.insertar(elem_id, 0)

    def find(self, elem_id):
        if elem_id not in self.padre:
            raise ValueError(f"Elemento inexistente: {elem_id}")
        padre = self.padre.buscar(elem_id)
        if padre != elem_id:
            padre = self.find(padre)
            self.padre.insertar(elem_id, padre)  # compresión de caminos
        return padre

    def union(self, a, b):
        raiz_a = self.find(a)
        raiz_b = self.find(b)

        if raiz_a == raiz_b:
            return False

        rango_a = self.rango.buscar(raiz_a)
        rango_b = self.rango.buscar(raiz_b)

        if rango_a < rango_b:
            self.padre.insertar(raiz_a, raiz_b)
        elif rango_a > rango_b:
            self.padre.insertar(raiz_b, raiz_a)
        else:
            self.padre.insertar(raiz_b, raiz_a)
            self.rango.insertar(raiz_a, rango_a + 1)

        return True