#include "experimento.h"
#include "grafo.h"
#include "algoritmos.h"
#include "medicion.h"
#include <iostream>
#include <iomanip>

using namespace std;

void ejecutarExperimentoArchivo(const string& ruta) {
    auto grafo = leerGrafoArchivo(ruta);
    int n = grafo.size();

    cout << "=============================\n";
    cout << "Archivo: " << ruta << "\n";
    cout << "n = " << n << "\n";
    cout << fixed << setprecision(4);

    int rep_bt = (n <= 6) ? 10000 :
                 (n <= 8) ? 1000 :
                            100;

    int rep_fast = 500000;

    if (n <= 1000) {
        int res_bt = 0;

        double t_bt = medirTiempo([&]() {
            res_bt = resolverBacktracking(grafo, n);
        }, rep_bt);

        cout << "Backtracking -> cliques: " << res_bt
             << " | tiempo: " << t_bt << " ms\n";
    } else {
        cout << "Backtracking -> OMITIDO (n muy grande)\n";
    }

    int res_gr = 0;

    double t_gr = medirTiempo([&]() {
        res_gr = greedyCliqueCover(grafo, n);
    }, rep_fast);

    cout << "Greedy       -> cliques: " << res_gr
         << " | tiempo: " << t_gr << " ms\n";
}