class _NodoCola:
    """Nodo enlazado interno de la cola."""
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Cola:
    def __init__(self):
        """Inicializa una cola vacía."""
        self._frente = None
        self._final = None
        self._tamano = 0

    def esta_vacia(self):
        """Devuelve True si la cola no tiene elementos, False en caso contrario."""
        return self._tamano == 0

    def encolar(self, item):
        """Agrega un elemento al final de la cola (enqueue)."""
        nuevo = _NodoCola(item)
        if self._final is None:
            self._frente = nuevo
        else:
            self._final.siguiente = nuevo
        self._final = nuevo
        self._tamano += 1

    def desencolar(self):
        """Remueve y devuelve el primer elemento de la cola (dequeue)."""
        if self.esta_vacia():
            raise IndexError("No se puede desencolar: la cola está vacía.")
        nodo = self._frente
        self._frente = nodo.siguiente
        if self._frente is None:
            self._final = None
        self._tamano -= 1
        return nodo.dato

    def frente(self):
        """Devuelve el primer elemento de la cola sin removerlo (peek/front)."""
        if self.esta_vacia():
            raise IndexError("La cola está vacía.")
        return self._frente.dato

    def __len__(self):
        """Permite usar len() sobre la cola para obtener su tamaño."""
        return self._tamano

    def __str__(self):
        """Representación en cadena para depuración."""
        partes = []
        actual = self._frente
        while actual is not None:
            partes.append(repr(actual.dato))
            actual = actual.siguiente
        return "[" + ", ".join(partes) + "]"