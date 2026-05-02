#ifndef GRAFO_H
#define GRAFO_H

#include <vector>
#include <string>
using namespace std;


vector<vector<int>> generarGrafo(int n, double prob);
std::vector<std::vector<int>> leerGrafoArchivo(const std::string& ruta);

#endif