class Grafo:
    def __init__(self, v):
        self.v = v
        self.e = 0
        self.matriz_adyacencia = [[False] * v for _ in range(v)]

    def agregar_arista(self, u, w):
        if not self.matriz_adyacencia[u][w]:
            self.matriz_adyacencia[u][w] = True
            self.matriz_adyacencia[w][u] = True
            self.e += 1

    def son_adyacentes(self, u, w):
        if u == w:
            return True
        return self.matriz_adyacencia[u][w]