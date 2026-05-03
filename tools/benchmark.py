import os
import sys
import subprocess
import re
import csv
import concurrent.futures
import multiprocessing
from pathlib import Path

# Configuración de rutas
BASE_DIR = Path(__file__).parent.resolve()
INSTANCES_DIR = BASE_DIR / "instances"
RESULTS_DIR = BASE_DIR / "results"

CPP_EXE = BASE_DIR / "src" / "cpp" / "main.exe"
JAVA_CP = BASE_DIR / "build"
JAVA_CLASS = "cl.unab.cliquecover.Main"
PYTHON_SCRIPT = BASE_DIR / "src" / "python" / "main.py"

TIMEOUT_SECONDS = 15

def run_cpp(filepath):
    try:
        result = subprocess.run(
            [str(CPP_EXE)],
            input=(str(filepath) + "\n").encode('utf-8'),
            capture_output=True,
            timeout=TIMEOUT_SECONDS
        )
        output = result.stdout.decode('utf-8')
        
        bt_cliques, bt_time = None, None
        gr_cliques, gr_time = None, None
        
        match_bt = re.search(r"Backtracking\s*->\s*cliques:\s*(\d+)\s*\|\s*tiempo:\s*([\d\.]+)\s*ms", output)
        if match_bt:
            bt_cliques = int(match_bt.group(1))
            bt_time = float(match_bt.group(2))
            
        match_gr = re.search(r"Greedy\s*->\s*cliques:\s*(\d+)\s*\|\s*tiempo:\s*([\d\.]+)\s*ms", output)
        if match_gr:
            gr_cliques = int(match_gr.group(1))
            gr_time = float(match_gr.group(2))
            
        return {"lang": "C++", "bt_cliques": bt_cliques, "bt_time_ms": bt_time, "gr_cliques": gr_cliques, "gr_time_ms": gr_time}
    except Exception as e:
        return {"lang": "C++", "bt_cliques": None, "bt_time_ms": None, "gr_cliques": None, "gr_time_ms": None}

def run_java(filepath):
    try:
        result = subprocess.run(
            ["java", "-cp", str(JAVA_CP), JAVA_CLASS, str(filepath)],
            capture_output=True,
            timeout=TIMEOUT_SECONDS
        )
        output = result.stdout.decode('utf-8', errors='ignore')
        
        bt_cliques, bt_time = None, None
        gr_cliques, gr_time = None, None
        
        match_bt_c = re.search(r"RESULTADO BASE:\s*(\d+)\s*cliques", output)
        match_bt_t = re.search(r"TIEMPO BASE\s*:\s*([\d\.,]+)\s*ms", output)
        if match_bt_c and match_bt_t:
            bt_cliques = int(match_bt_c.group(1))
            bt_time = float(match_bt_t.group(1).replace(',', '.'))
            
        match_gr_c = re.search(r"RESULTADO GREEDY:\s*(\d+)\s*cliques", output)
        match_gr_t = re.search(r"TIEMPO GREEDY\s*:\s*([\d\.,]+)\s*ms", output)
        if match_gr_c and match_gr_t:
            gr_cliques = int(match_gr_c.group(1))
            gr_time = float(match_gr_t.group(1).replace(',', '.'))

        return {"lang": "Java", "bt_cliques": bt_cliques, "bt_time_ms": bt_time, "gr_cliques": gr_cliques, "gr_time_ms": gr_time}
    except Exception as e:
        return {"lang": "Java", "bt_cliques": None, "bt_time_ms": None, "gr_cliques": None, "gr_time_ms": None}

def run_python(filepath):
    try:
        result = subprocess.run(
            [sys.executable, str(PYTHON_SCRIPT), str(filepath)],
            input=b"\n",
            capture_output=True,
            timeout=TIMEOUT_SECONDS
        )
        output = result.stdout.decode('utf-8', errors='ignore')
        
        bt_cliques, bt_time = None, None
        gr_cliques, gr_time = None, None
        
        match_gr = re.search(r"Greedy:\s*(\d+)\s*cliques\s*\(([\d\.]+)\s*ms\)", output)
        if match_gr:
            gr_cliques = int(match_gr.group(1))
            gr_time = float(match_gr.group(2))
            
        match_bt = re.search(r"Backtracking:\s*(\d+)\s*cliques\s*\(([\d\.]+)\s*ms\)", output)
        if match_bt:
            bt_cliques = int(match_bt.group(1))
            bt_time = float(match_bt.group(2))
            
        return {"lang": "Python", "bt_cliques": bt_cliques, "bt_time_ms": bt_time, "gr_cliques": gr_cliques, "gr_time_ms": gr_time}
    except Exception as e:
        return {"lang": "Python", "bt_cliques": None, "bt_time_ms": None, "gr_cliques": None, "gr_time_ms": None}

def benchmark_instance(file_path, cpp_exists):
    rel_path = file_path.relative_to(INSTANCES_DIR)
    results = []
    
    # Run C++
    if cpp_exists:
        res_cpp = run_cpp(file_path)
        results.append([
            str(rel_path), res_cpp["lang"],
            res_cpp["bt_cliques"], res_cpp["bt_time_ms"],
            res_cpp["gr_cliques"], res_cpp["gr_time_ms"]
        ])
    else:
        pass
        
    # Run Java
    res_java = run_java(file_path)
    results.append([
        str(rel_path), res_java["lang"],
        res_java["bt_cliques"], res_java["bt_time_ms"],
        res_java["gr_cliques"], res_java["gr_time_ms"]
    ])
    
    # Run Python
    res_python = run_python(file_path)
    results.append([
        str(rel_path), res_python["lang"],
        res_python["bt_cliques"], res_python["bt_time_ms"],
        res_python["gr_cliques"], res_python["gr_time_ms"]
    ])
    
    print(f"Completado: {rel_path}")
    return results

def main():
    if not INSTANCES_DIR.exists():
        print(f"Error: No se encontró la carpeta {INSTANCES_DIR}")
        return
        
    RESULTS_DIR.mkdir(exist_ok=True)
    csv_file = RESULTS_DIR / "benchmark_results.csv"
    
    txt_files = list(INSTANCES_DIR.rglob("*.txt"))
    if not txt_files:
        print("No se encontraron archivos .txt en las subcarpetas de instancias/")
        return
        
    print(f"Se encontraron {len(txt_files)} instancias para ejecutar.")
    
    cpp_exists = CPP_EXE.exists()
    if not cpp_exists:
        print("Advertencia: No se encontró el ejecutable de C++. Se omitirá.")
        
    max_workers = multiprocessing.cpu_count()
    print(f"Iniciando ejecución en paralelo con {max_workers} workers. Timeout: {TIMEOUT_SECONDS}s por ejecución...\n")
    
    all_results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(benchmark_instance, f, cpp_exists): f for f in txt_files}
        
        for future in concurrent.futures.as_completed(futures):
            try:
                rows = future.result()
                all_results.extend(rows)
            except Exception as exc:
                print(f"Una instancia generó una excepción: {exc}")
                
    # Guardar resultados
    print(f"\nGuardando resultados en {csv_file}...")
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Instance", "Language", 
            "Backtracking_Cliques", "Backtracking_Time_ms", 
            "Greedy_Cliques", "Greedy_Time_ms"
        ])
        writer.writerows(all_results)
            
    print("¡Benchmark completado!")

if __name__ == "__main__":
    main()
