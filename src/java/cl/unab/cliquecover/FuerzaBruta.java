package cl.unab.cliquecover;

import java.util.Arrays;

public class FuerzaBruta {

    private Grafo grafo;
    private int[] asignacion; // Guarda a qué clique (0 a K-1) pertenece cada vértice
    private int[] tamanosCliques; // Cuántos vértices tiene cada clique actualmente

    public int resolver(Grafo grafo) {
        this.grafo = grafo;
        int v = grafo.getV();
        
        // Si no hay vértices, se necesitan 0 cliques
        if (v == 0) return 0;

        this.asignacion = new int[v];
        
        // Probamos desde K=1 hasta K=V (en el peor caso, cada nodo es su propio clique)
        for (int k = 1; k <= v; k++) {
            this.tamanosCliques = new int[k];
            Arrays.fill(asignacion, -1); // -1 significa "aún no asignado"
            
            // Iniciamos el backtracking desde el vértice 0
            if (backtrack(0, k)) {
                return k; // Como vamos de menor a mayor, el primer éxito es el óptimo
            }
        }
        
        return v; 
    }

    private boolean backtrack(int verticeActual, int k) {
        // Caso base: Si logramos asignar todos los vértices, ¡ganamos!
        if (verticeActual == grafo.getV()) {
            return true;
        }

        boolean intentoNuevoClique = false;

        // Intentamos poner el vérticeActual en alguno de los K cliques disponibles
        for (int i = 0; i < k; i++) {
            
            if (tamanosCliques[i] == 0) {
                if (intentoNuevoClique) continue; 
                intentoNuevoClique = true;
            }

            // Verificamos si es válido meterlo aquí
            if (esValido(verticeActual, i)) {
                // HACER: Lo asignamos
                asignacion[verticeActual] = i;
                tamanosCliques[i]++;

                // RECURSIÓN: Avanzamos al siguiente vértice
                if (backtrack(verticeActual + 1, k)) {
                    return true;
                }

                // DESHACER (Backtracking): Si no funcionó, lo sacamos y probamos otra opción
                asignacion[verticeActual] = -1;
                tamanosCliques[i]--;
            }
        }

        // Si probamos en los K cliques y ninguno funcionó, esta rama es un callejón sin salida
        return false;
    }

    private boolean esValido(int verticeActual, int cliqueId) {
        // Revisamos todos los vértices que ya procesamos (de 0 a verticeActual - 1)
        for (int j = 0; j < verticeActual; j++) {
            // Si el vértice j está en el mismo clique donde queremos entrar...
            if (asignacion[j] == cliqueId) {
                // ...DEBEN ser adyacentes. Si no lo son, se rompe el clique.
                if (!grafo.sonAdyacentes(verticeActual, j)) {
                    return false;
                }
            }
        }
        return true;
    }
}