#include "algoritmos.h"
#include <algorithm>
#include <bitset>
#include <numeric>

using namespace std;

const int MAXN = 100;

static int mejor;
static vector<bitset<MAXN>> adj;

void backtrackingBB(int idx,
                    vector<bitset<MAXN>>& cliques,
                    const vector<int>& orden,
                    int n) {

    if ((int)cliques.size() >= mejor) return;

    if (idx == n) {
        mejor = min(mejor, (int)cliques.size());
        return;
    }

    int nodo = orden[idx];

    int limite = cliques.size();

    for (int i = 0; i < limite; i++) {

        if ((cliques[i] & adj[nodo]) == cliques[i]) {

            cliques[i].set(nodo);

            backtrackingBB(idx + 1, cliques, orden, n);

            cliques[i].reset(nodo);
        }
    }

    if ((int)cliques.size() + 1 < mejor) {

        bitset<MAXN> nuevo;
        nuevo.set(nodo);

        cliques.push_back(nuevo);

        backtrackingBB(idx + 1, cliques, orden, n);

        cliques.pop_back();
    }
}

int resolverBacktracking(const vector<vector<int>>& grafo, int n) {

    adj.assign(n, bitset<MAXN>());

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (grafo[i][j]) {
                adj[i].set(j);
            }
        }
    }

    vector<int> orden(n);
    iota(orden.begin(), orden.end(), 0);

    sort(orden.begin(), orden.end(), [&](int a, int b) {
        return adj[a].count() > adj[b].count();
    });

    mejor = n;

    vector<bitset<MAXN>> cliques;

    backtrackingBB(0, cliques, orden, n);

    return mejor;
}

int greedyCliqueCover(const vector<vector<int>>& grafo, int n) {
    vector<bool> usado(n, false);
    int cantidad = 0;

    for (int i = 0; i < n; i++) {
        if (usado[i]) continue;

        vector<int> clique = {i};
        usado[i] = true;

        for (int j = i + 1; j < n; j++) {
            if (usado[j]) continue;

            bool puede = true;
            for (int v : clique) {
                if (grafo[v][j] == 0) {
                    puede = false;
                    break;
                }
            }

            if (puede) {
                clique.push_back(j);
                usado[j] = true;
            }
        }

        cantidad++;
    }

    return cantidad;
}
