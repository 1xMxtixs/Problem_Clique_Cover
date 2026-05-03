package cl.unab.cliquecover;

import java.util.Arrays;

public class Backtracking  {

    private Grafo grafo;
    private int[] asignacion; 
    private int[] tamanosCliques; 

    public int resolver(Grafo grafo) {
        this.grafo = grafo;
        int v = grafo.getV();
        
        if (v == 0) return 0;

        this.asignacion = new int[v];
        
        for (int k = 1; k <= v; k++) {
            this.tamanosCliques = new int[k];
            Arrays.fill(asignacion, -1); 
            
            if (backtrack(0, k)) {
                return k; 
            }
        }
        
        return v; 
    }

    private boolean backtrack(int verticeActual, int k) {
        if (verticeActual == grafo.getV()) {
            return true;
        }

        boolean intentoNuevoClique = false;

        for (int i = 0; i < k; i++) {
            
            if (tamanosCliques[i] == 0) {
                if (intentoNuevoClique) continue; 
                intentoNuevoClique = true;
            }

            if (esValido(verticeActual, i)) {
                asignacion[verticeActual] = i;
                tamanosCliques[i]++;

                if (backtrack(verticeActual + 1, k)) {
                    return true;
                }

                asignacion[verticeActual] = -1;
                tamanosCliques[i]--;
            }
        }

        return false;
    }

    private boolean esValido(int verticeActual, int cliqueId) {
        for (int j = 0; j < verticeActual; j++) {
            if (asignacion[j] == cliqueId) {
                if (!grafo.sonAdyacentes(verticeActual, j)) {
                    return false;
                }
            }
        }
        return true;
    }
}