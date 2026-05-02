class GreedySolver:
    def resolver(self, grafo):
        if grafo.v == 0:
            return 0

        nodos = sorted(
            range(grafo.v),
            key=lambda x: sum(grafo.matriz_adyacencia[x]),
            reverse=True
        )

        cliques = []

        for u in nodos:
            colocado = False
            for clique in cliques:
                if all(grafo.son_adyacentes(u, v) for v in clique):
                    clique.append(u)
                    colocado = True
                    break

            if not colocado:
                cliques.append([u])

        return len(cliques)


class BacktrackingSolver:
    def __init__(self, grafo):
        self.grafo = grafo
        self.v = grafo.v
        self.asignacion = [-1] * self.v
        self.tamanos_cliques = []

    def resolver(self):
        if self.v == 0:
            return 0

        for k in range(1, self.v + 1):
            self.tamanos_cliques = [0] * k
            self.asignacion = [-1] * self.v

            if self._backtrack(0, k):
                return k

        return self.v

    def _backtrack(self, vertice_actual, k):
        if vertice_actual == self.v:
            return True

        intento_nuevo_clique = False

        for i in range(k):
            if self.tamanos_cliques[i] == 0:
                if intento_nuevo_clique:
                    continue
                intento_nuevo_clique = True

            if self._es_valido(vertice_actual, i):
                self.asignacion[vertice_actual] = i
                self.tamanos_cliques[i] += 1

                if self._backtrack(vertice_actual + 1, k):
                    return True

                self.asignacion[vertice_actual] = -1
                self.tamanos_cliques[i] -= 1

        return False

    def _es_valido(self, vertice, clique_id):
        for j in range(vertice):
            if self.asignacion[j] == clique_id:
                if not self.grafo.son_adyacentes(vertice, j):
                    return False
        return True