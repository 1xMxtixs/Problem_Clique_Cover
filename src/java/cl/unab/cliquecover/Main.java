package cl.unab.cliquecover;

public class Main {

    public static void main(String[] args) {
        String rutaArchivo = "test.txt"; 
        
        if (args.length > 0) {
            rutaArchivo = args[0];
        }

        try {
            System.out.println("=========================================");
            System.out.println("Iniciando prueba de Clique Cover");
            System.out.println("Instancia: " + rutaArchivo);
            
            Grafo grafo = InstanceReader.leerArchivo(rutaArchivo);
            System.out.println("Grafo cargado con éxito: " + grafo.getV() + " vértices y " + grafo.getE() + " aristas.");
            System.out.println("=========================================\n");

            // --- Solución Base (Backtracking) ---
            
            System.out.println(">> Ejecutando Solución Base (Backtracking)...");
            Backtracking solverBase = new Backtracking ();
            long inicioBase = System.nanoTime();

            int optimo = solverBase.resolver(grafo);
            long finBase = System.nanoTime();
            double tiempoBaseMs = (finBase - inicioBase) / 1_000_000.0;

            System.out.println("RESULTADO BASE: " + optimo + " cliques.");
            System.out.println("TIEMPO BASE   : " + String.format("%.4f", tiempoBaseMs) + " ms.\n");

            // --- Solución Mejorada (Greedy) ---

            System.out.println(">> Ejecutando Solución Mejorada (Greedy)...");
            HeuristicaGreedy solverGreedy = new HeuristicaGreedy();
            long inicioGreedy = System.nanoTime();

            int aproximado = solverGreedy.resolver(grafo);

            long finGreedy = System.nanoTime();
            double tiempoGreedyMs = (finGreedy - inicioGreedy) / 1_000_000.0;

            System.out.println("RESULTADO GREEDY: " + aproximado + " cliques.");
            System.out.println("TIEMPO GREEDY   : " + String.format("%.4f", tiempoGreedyMs) + " ms.");
            System.out.println("=========================================");

        } catch (Exception e) {
            System.err.println("Hubo un error al ejecutar la prueba:");
            e.printStackTrace();
        }
    }
}