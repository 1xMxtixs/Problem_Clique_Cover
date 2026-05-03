import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

# Configuración
RESULTS_CSV = "results/benchmark_results.csv"
PLOTS_DIR = "results/plots"

def extract_nodes(instance_str):
    match = re.search(r"_v(\d+)_", instance_str)
    return int(match.group(1)) if match else None

def extract_edges(instance_str):
    match = re.search(r"_e(\d+)_", instance_str)
    return int(match.group(1)) if match else None

def main():
    if not os.path.exists(RESULTS_CSV):
        print(f"Error: No se encontró el archivo {RESULTS_CSV}")
        return

    os.makedirs(PLOTS_DIR, exist_ok=True)
    
    # Cargar datos
    df = pd.read_csv(RESULTS_CSV)
    
    df["Nodes"] = df["Instance"].apply(extract_nodes)
    df["Edges"] = df["Instance"].apply(extract_edges)
    
    numeric_cols = ["Backtracking_Cliques", "Backtracking_Time_ms", "Greedy_Cliques", "Greedy_Time_ms"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    sns.set_theme(style="whitegrid")
    
    print("Generando gráficos (usando comparaciones justas)...")

    # Instancias válidas para Greedy
    greedy_counts = df.dropna(subset=["Greedy_Time_ms"]).groupby("Instance")["Language"].nunique()
    valid_greedy_instances = greedy_counts[greedy_counts == 3].index
    df_greedy_fair = df[df["Instance"].isin(valid_greedy_instances)]

    # Instancias válidas para Backtracking
    bt_counts = df.dropna(subset=["Backtracking_Time_ms"]).groupby("Instance")["Language"].nunique()
    valid_bt_instances = bt_counts[bt_counts == 3].index
    df_bt_fair = df[df["Instance"].isin(valid_bt_instances)]

    # Instancias válidas para Calidad 
    quality_counts = df.dropna(subset=["Backtracking_Cliques", "Greedy_Cliques"]).groupby("Instance")["Language"].nunique()
    valid_quality_instances = quality_counts[quality_counts == 3].index
    df_quality_fair = df[df["Instance"].isin(valid_quality_instances)].copy()

    # Tiempo de Ejecución Promedio (Greedy) por Lenguaje 
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df_greedy_fair, x="Language", y="Greedy_Time_ms", errorbar=None, hue="Language", palette="viridis", legend=False)
    plt.title(f"Tiempo de Ejecución Promedio (Greedy)\nComparación justa: {len(valid_greedy_instances)} instancias")
    plt.ylabel("Tiempo Promedio (ms)")
    plt.xlabel("Lenguaje")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "greedy_time_bar.png"))
    plt.close()

    # Tiempo de Ejecución Promedio (Backtracking) por Lenguaje 
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df_bt_fair, x="Language", y="Backtracking_Time_ms", errorbar=None, hue="Language", palette="magma", legend=False)
    plt.title(f"Tiempo de Ejecución Promedio (Backtracking)\nComparación justa: {len(valid_bt_instances)} instancias")
    plt.ylabel("Tiempo Promedio (ms)")
    plt.xlabel("Lenguaje")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "backtracking_time_bar.png"))
    plt.close()

    # Distribución del tiempo Greedy 
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df_greedy_fair, x="Language", y="Greedy_Time_ms", hue="Language", palette="viridis", legend=False)
    plt.title(f"Distribución de Tiempo (Greedy)\nComparación justa: {len(valid_greedy_instances)} instancias")
    plt.ylabel("Tiempo (ms)")
    plt.xlabel("Lenguaje")
    plt.yscale("log") 
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "greedy_time_boxplot.png"))
    plt.close()

    # Calidad de la solución: Backtracking vs Greedy (Cliques Encontrados)
    df_quality_fair["Extra_Cliques_Greedy"] = df_quality_fair["Greedy_Cliques"] - df_quality_fair["Backtracking_Cliques"]
    
    if not df_quality_fair.empty:
        plt.figure(figsize=(8, 5))
        sns.barplot(data=df_quality_fair, x="Language", y="Extra_Cliques_Greedy", errorbar=None, hue="Language", palette="coolwarm", legend=False)
        plt.title(f"Diferencia de Cliques (Greedy vs Backtracking Óptimo)\nComparación justa: {len(valid_quality_instances)} instancias")
        plt.ylabel("Cliques Adicionales (Promedio)")
        plt.xlabel("Lenguaje")
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, "quality_greedy_vs_bt.png"))
        plt.close()

    # Scatterplot de Tiempo Greedy según Cantidad de Nodos
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=df_greedy_fair, x="Nodes", y="Greedy_Time_ms", hue="Language", marker="o")
    plt.title("Tiempo Greedy vs Cantidad de Nodos\nSolo instancias resueltas por los 3 lenguajes")
    plt.ylabel("Tiempo (ms)")
    plt.xlabel("Cantidad de Nodos")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "greedy_time_vs_nodes.png"))
    plt.close()

    print(f"¡Gráficos generados con éxito en la carpeta '{PLOTS_DIR}'!")

if __name__ == "__main__":
    main()
