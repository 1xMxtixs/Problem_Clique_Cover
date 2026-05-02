from grafo import Grafo

def leer_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as file:
            lineas = file.readlines()

        grafo = None
        for linea in lineas:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue

            partes = linea.split()

            if grafo is None:
                v = int(partes[0])
                grafo = Grafo(v)
            else:
                u, w = int(partes[0]), int(partes[1])
                grafo.agregar_arista(u, w)

        return grafo

    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None