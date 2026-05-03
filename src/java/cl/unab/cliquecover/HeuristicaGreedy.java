package cl.unab.cliquecover;

import java.util.ArrayList;
import java.util.List;

public class HeuristicaGreedy {
    
    public int resolver (Grafo grafo) {
        int v = grafo.getV();
        if (v == 0) return 0;

        List<List<Integer>> cliques = new ArrayList<>();

        for(int i = 0; i < v; i++) {
            boolean asignado = false;

            for (List<Integer> clique : cliques) {
                if (esCompatible(i, clique, grafo)) {
                    clique.add(i);
                    asignado = true;
                    break;
                }
            }

            if (!asignado) {
                List<Integer> nuevoClique = new ArrayList<>();
                nuevoClique.add(i);
                cliques.add(nuevoClique);
            }
        }

        return cliques.size();
    }

    private boolean esCompatible(int vertice, List<Integer> clique, Grafo grafo) {
        for (int nodoEnClique : clique) {
            if (!grafo.sonAdyacentes(vertice, nodoEnClique)) {
                return false;
            }
        }
        return true;
    }
}
