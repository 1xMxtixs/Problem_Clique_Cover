package cl.unab.cliquecover;

public class Main {

    public static void main(String[] args) {
        // Por defecto, leeremos un archivo de prueba.
        // Si le pasas un argumento por consola, leerá ese.
        String rutaArchivo = "test.txt"; 
        
        if (args.length > 0) {
            rutaArchivo = args[0];
        }

        try {
            System.out.println("=========================================");
            System.out.println("Iniciando prueba de Clique Cover");
            System.out.println("Instancia: " + rutaArchivo);
            
            // 1. Cargar el grafo
            Grafo grafo = InstanceReader.leerArchivo(rutaArchivo);
            System.out.println("Grafo cargado con éxito: " + grafo.getV() + " vértices y " + grafo.getE() + " aristas.");

            // 2. Resolver con Fuerza Bruta
            FuerzaBruta solver = new FuerzaBruta();
            
            System.out.println("Calculando mínimo de cliques... (Fuerza Bruta)");
            long tiempoInicio = System.currentTimeMillis();
            
            int minimoCliques = solver.resolver(grafo);
            
            long tiempoFin = System.currentTimeMillis();
            long tiempoTotal = tiempoFin - tiempoInicio;

            // 3. Mostrar resultados
            System.out.println("-----------------------------------------");
            System.out.println("RESULTADO: Se necesitan " + minimoCliques + " cliques.");
            System.out.println("TIEMPO   : " + tiempoTotal + " milisegundos.");
            System.out.println("=========================================");

        } catch (Exception e) {
            System.err.println("Hubo un error al ejecutar la prueba:");
            e.printStackTrace();
        }
    }
}