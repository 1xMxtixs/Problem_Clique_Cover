import argparse
import os
import random
from typing import List, Tuple

# Constantes de la suite por defecto
SMALL_V = [10, 20, 30]
MEDIUM_V = [40, 60, 80]
LARGE_V = [100, 200, 500]
DENSITIES = [0.2, 0.5, 0.8]
SEEDS = range(3)

def write_instance(path: str, v:int, edges: List[Tuple[int, int]], family: str, seed: int, opt: int = None):
    "Se escribe el grafo en formato V E seguido de la lista de artistas"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="\n") as f:
        f.write(f"# family={family} seed={seed}\n")
        if opt is not None:
            f.write(f"# opt_upper_bound={opt}\n")
        f.write(f"{v} {len(edges)}\n")
        for u, w in edges:
            f.write(f"{u} {w}\n")

def instance_filename(family: str, v: int, e: int, seed: int) -> str:
    return f"{family}_v{v}_e{e}_s{seed}.txt"

# Generadores por familia

def generate_random(v: int, density: float, seed: int) -> List[Tuple[int, int]]:
    rng = random.Random(seed)
    edges = []
    for i in range(v):
        for j in range(i + 1, v):
            if rng.random() < density:
                edges.append((i, j))
    return edges

def generate_structured(v: int, k_cliques: int, noise: float, seed: int) -> Tuple[List[Tuple[int, int]], int]:
    # Genera K cliques perfectos y añande aristar de ruido entre ellos
    rng = random.Random(seed)
    edges = set()

    assignments = [rng.randrange(k_cliques) for _ in range(v)]

    for i in range(v):
        for j in range(1 + 1, v):
            if assignments[i] == assignments[j]:
                edges.add((i, j))
            elif rng.random() < noise:
                edges.add((i, j))
    return list(edges), k_cliques

def generate_hard(v: int, seed: int) -> List[Tuple[int, int]]:
    # Genera un grafo tipo multipartito denso
    rng = random.Random(seed)
    edges = set()
    parts = rng.randint(3, max(4, v // 5))
    assignments = [rng.randrange(parts) for _ in range(v)]

    for i in range(v):
        for j in range(i + 1, v):
            if assignments[i] == assignments[j]:
                if rng.random() < 0.95:
                    edges.add((i, j))
            else:
                if rng.random() < 0.60:
                    edges.add((i, j))
    return list(edges)                 

#Orquestacion

def generate_family_suite(out_dir: str, v_list: list, family: str):
    os.makedirs(out_dir, exist_ok=True)
    count = 0
    for v in v_list:
        for seed in SEEDS:
            if family == "random":
                for d in DENSITIES:
                    edges = generate_random(v, d, seed)
                    fname = instance_filename(family, v, len(edges), seed)
                    write_instance(os.path.join(out_dir, fname), v, edges, family, seed)
                    count += 1
            elif family == "structured":
                k = max(2, v // 10)
                edges, opt_bound = generate_structured(v, k, 0.1, seed)
                fname = instance_filename(family, v, len(edges), seed)
                write_instance(os.path.join(out_dir, fname), v, edges, family, seed, opt=opt_bound)
                count += 1
            elif family == "hard":
                edges = generate_hard(v, seed)
                fname = instance_filename(family, v, len(edges), seed)
                write_instance(os.path.join(out_dir, fname), v, edges, family, seed)
                count += 1
    return count

def main():
    parser = argparse.ArgumentParser(description="Generador Clique Cover")
    parser.add_argument("--family", choices=["random", "structured", "hard", "all"], default="all")
    parser.add_argument("--v", type=int, help="Número de vértices")
    parser.add_argument("--density", type=float, default=0.5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default="instances")
    args = parser.parse_args()

    if args.family == "all":
        print("Generando suite completa...")
        for size_name, v_list in [("small", SMALL_V), ("medium", MEDIUM_V), ("large", LARGE_V)]:
            for fam in ["random", "structured", "hard"]:
                out_path = os.path.join(args.out, size_name, fam)
                c = generate_family_suite(out_path, v_list, fam)
                print(f"  [{size_name}/{fam}] -> {c} archivos")
        print("¡Completado!")
        return

    if not args.v:
        parser.error("--v es requerido para generaciones individuales.")
        
    os.makedirs(args.out, exist_ok=True)
    
    if args.family == "random":
        edges = generate_random(args.v, args.density, args.seed)
        fname = instance_filename("random", args.v, len(edges), args.seed)
        path = os.path.join(args.out, fname)
        write_instance(path, args.v, edges, "random", args.seed)
        print(f"✅ Generado: {path} (Densidad: {args.density})")

    elif args.family == "structured":
        k = max(2, args.v // 10) 
        edges, opt_bound = generate_structured(args.v, k, 0.1, args.seed)
        fname = instance_filename("structured", args.v, len(edges), args.seed)
        path = os.path.join(args.out, fname)
        write_instance(path, args.v, edges, "structured", args.seed, opt=opt_bound)
        print(f"Generado: {path} (K={k} cliques perfectos ocultos)")

    elif args.family == "hard":
        edges = generate_hard(args.v, args.seed)
        fname = instance_filename("hard", args.v, len(edges), args.seed)
        path = os.path.join(args.out, fname)
        write_instance(path, args.v, edges, "hard", args.seed)
        print(f"Generado: {path} (Instancia trampa generada)")

if __name__ == "__main__":
    main()