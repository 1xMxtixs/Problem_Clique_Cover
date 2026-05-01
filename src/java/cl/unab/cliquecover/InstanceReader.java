package cl.unab.cliquecover;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class InstanceReader {

    public static Grafo leerArchivo(String rutaArchivo) throws IOException {
        try (BufferedReader br = new BufferedReader(new FileReader(rutaArchivo))) {
            String linea;
            
            do {
                linea = br.readLine();
            } while (linea != null && linea.trim().startsWith("#"));

            if (linea == null) {
                throw new IllegalArgumentException("El archivo está vacío o mal formateado.");
            }

            String[] partes = linea.trim().split("\\s+");
            int v = Integer.parseInt(partes[0]);
            int e = Integer.parseInt(partes[1]);

            Grafo grafo = new Grafo(v);

            int aristasLeidas = 0;
            while ((linea = br.readLine()) != null) {
                linea = linea.trim();
                if (linea.isEmpty() || linea.startsWith("#")) continue;

                partes = linea.split("\\s+");
                int u = Integer.parseInt(partes[0]);
                int w = Integer.parseInt(partes[1]);
                
                grafo.agregarArista(u, w);
                aristasLeidas++;
            }

            return grafo;
        }
    }
}