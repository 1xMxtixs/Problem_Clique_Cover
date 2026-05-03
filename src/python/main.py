import sys
import time

from instance_reader import leer_archivo
from algoritmos import GreedySolver, BacktrackingSolver

def main():
    archivo = sys.argv[1] if len(sys.argv) > 1 else "test.txt"

    print("--- INICIANDO ---")

    g = leer_archivo(archivo)

    if g:
        print(f"Grafo cargado: {g.v} vértices, {g.e} aristas\n")

        # Greedy
        t_ini = time.time()
        res_greedy = GreedySolver().resolver(g)
        t_greedy = (time.time() - t_ini) * 1000
        print(f"Greedy: {res_greedy} cliques ({t_greedy:.2f} ms)")

        # Backtracking
        t_ini = time.time()
        res_bt = BacktrackingSolver(g).resolver()
        t_bt = (time.time() - t_ini) * 1000
        print(f"Backtracking: {res_bt} cliques ({t_bt:.2f} ms)")

    input("\nPresiona ENTER para salir...")


if __name__ == "__main__":
    main()