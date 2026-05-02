#include "grafo.h"
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <iostream>

vector<vector<int>> generarGrafo(int n, double prob) {
    vector<vector<int>> g(n, vector<int>(n, 0));

    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if ((double)rand() / RAND_MAX < prob) {
                g[i][j] = g[j][i] = 1;
            }
        }
    }
    return g;
}

vector<vector<int>> leerGrafoArchivo(const string& ruta) {
    ifstream file(ruta);

    if (!file.is_open()) {
        cout << "ERROR: no se pudo abrir el archivo\n";
        return {};
    }

    string linea;

    // 🔹 Ignorar comentarios
    while (getline(file, linea)) {
        if (linea.empty() || linea[0] == '#') continue;
        else break;
    }

    // 🔹 Leer n y m
    int n = 0, m = 0;
    stringstream ss(linea);
    ss >> n >> m;

    if (n <= 0) {
        cout << "ERROR: n invalido\n";
        return {};
    }

    cout << "DEBUG: n = " << n << ", m = " << m << endl;

    vector<vector<int>> g(n, vector<int>(n, 0));

    int u, v;
    int leidas = 0;
    int ignoradas = 0;

    while (file >> u >> v) {

        // 🔥 VALIDAR RANGO (0-index)
        if (u < 0 || v < 0 || u >= n || v >= n) {
            cout << "WARNING: fuera de rango: " << u << " " << v << endl;
            ignoradas++;
            continue;
        }

        // 🔥 IGNORAR LOOPS
        if (u == v) {
            ignoradas++;
            continue;
        }

        // 🔥 EVITAR DUPLICADOS
        if (g[u][v] == 0) {
            g[u][v] = 1;
            g[v][u] = 1;
            leidas++;
        }
    }

    cout << "DEBUG: aristas validas = " << leidas << endl;
    cout << "DEBUG: aristas ignoradas = " << ignoradas << endl;

    return g;
}