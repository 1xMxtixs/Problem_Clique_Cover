#include <iostream>
#include <string>
#include "experimento.h"

using namespace std;

int main() {
    string ruta;

    cout << "Ingrese la ruta del grafo: ";
    getline(cin, ruta);

    if (!ruta.empty() && ruta.front() == '"' && ruta.back() == '"') {
        ruta = ruta.substr(1, ruta.size() - 2);
    }

    ejecutarExperimentoArchivo(ruta);

    return 0;
}