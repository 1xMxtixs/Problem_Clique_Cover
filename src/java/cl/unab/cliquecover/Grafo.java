package cl.unab.cliquecover;

public class Grafo {
    private final int v; 
    private int e;       
    private final boolean[][] matrizAdyacencia;

    public Grafo(int v) {
        this.v = v;
        this.e = 0;
        this.matrizAdyacencia = new boolean[v][v];
    }

    public void agregarArista(int u, int w) {
        if (!matrizAdyacencia[u][w]) {
            matrizAdyacencia[u][w] = true;
            matrizAdyacencia[w][u] = true;
            this.e++;
        }
    }

    public boolean sonAdyacentes(int u, int w) {
        if (u == w) return true; 
        return matrizAdyacencia[u][w];
    }

    public int getV() {
        return v;
    }

    public int getE() {
        return e;
    }
}