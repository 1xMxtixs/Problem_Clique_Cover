import sys
import os

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def cargar_grafo(ruta_instancia):
    grafo = {}
    try:
        with open(ruta_instancia, 'r') as f:
            lineas = f.readlines()
            
            if not lineas:
                raise ValueError("El archivo del grafo está vacío.")

            partes = lineas[0].strip().split()
            if len(partes) != 2:
                raise ValueError("La primera línea debe contener 'V E' (cantidad de vértices y aristas).")

            v, e = map(int, partes)
            
            for i in range(v):
                grafo[i] = set()
                
            aristas_leidas = 0
            for linea in lineas[1:]:
                if linea.strip():
                    u, w = map(int, linea.strip().split())
                    if u < 0 or u >= v or w < 0 or w >= v:
                        raise ValueError(f"Arista ({u}, {w}) tiene vértices fuera de rango [0, {v-1}].")
                    grafo[u].add(w)
                    grafo[w].add(u) # Es no dirigido
                    aristas_leidas += 1
                    
        return grafo, v
    except FileNotFoundError:
        print(f"{Colors.FAIL}Error: No se encontró el archivo de instancia '{ruta_instancia}'.{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.FAIL}Error al leer el grafo: {e}{Colors.ENDC}")
        sys.exit(1)

def cargar_solucion(ruta_solucion):
    cliques = []
    try:
        with open(ruta_solucion, 'r') as f:
            for linea in f:
                if linea.strip():
                    clique = list(map(int, linea.strip().split()))
                    if clique: 
                        cliques.append(clique)
        return cliques
    except FileNotFoundError:
        print(f"{Colors.FAIL}Error: No se encontró el archivo de solución '{ruta_solucion}'.{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.FAIL}Error al leer la solución: {e}{Colors.ENDC}")
        sys.exit(1)

def validar(ruta_instancia, ruta_solucion):
    print(f"{Colors.HEADER}{Colors.BOLD}--- Iniciando Validación ---{Colors.ENDC}")
    print(f"Grafo: {ruta_instancia}")
    print(f"Solución: {ruta_solucion}\n")
    
    grafo, total_vertices = cargar_grafo(ruta_instancia)
    cliques = cargar_solucion(ruta_solucion)
    
    vertices_vistos = set()
    vertices_duplicados = set()
    valido = True
    
    for idx, clique in enumerate(cliques):
        for i in range(len(clique)):
            u = clique[i]
            
            if u < 0 or u >= total_vertices:
                print(f"{Colors.FAIL}ERROR: El vértice {u} en el clique {idx} no existe en el grafo (rango 0 a {total_vertices-1}).{Colors.ENDC}")
                valido = False
                continue

            if u in vertices_vistos:
                vertices_duplicados.add(u)
                
            vertices_vistos.add(u)

            for j in range(i + 1, len(clique)):
                v = clique[j]
                if v not in grafo.get(u, set()):
                    print(f"{Colors.FAIL}ERROR CRÍTICO: El grupo {idx} NO es un clique. Los vértices {u} y {v} no están conectados por una arista.{Colors.ENDC}")
                    valido = False
        
    if vertices_duplicados:
        print(f"{Colors.WARNING}ADVERTENCIA: La solución tiene vértices solapados en múltiples cliques: {vertices_duplicados}{Colors.ENDC}")
        print(f"{Colors.WARNING}Para el problema estricto de 'Clique Cover', cada vértice debe pertenecer a un ÚNICO clique (debe ser una partición).{Colors.ENDC}")
        valido = False

    if len(vertices_vistos) != total_vertices:
        faltantes = set(range(total_vertices)) - vertices_vistos
        if faltantes:
            print(f"{Colors.FAIL}ERROR: Faltaron vértices por cubrir. Vértices sin clique: {faltantes}{Colors.ENDC}")
            valido = False
            
    print("-" * 30)
    if valido:
        print(f"{Colors.OKGREEN}{Colors.BOLD}¡SOLUCIÓN VÁLIDA!{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Se cubrieron los {total_vertices} vértices usando {len(cliques)} cliques perfectamente.{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}{Colors.BOLD}SOLUCIÓN INVÁLIDA.{Colors.ENDC} Revisa los errores listados arriba.")
        
    return valido

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"{Colors.WARNING}Uso: python validator.py <ruta_instancia.txt> <ruta_solucion.txt>{Colors.ENDC}")
    else:
        instancia = sys.argv[1]
        solucion = sys.argv[2]
        validar(instancia, solucion)