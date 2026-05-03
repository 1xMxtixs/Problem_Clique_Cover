#include "medicion.h"
#include <chrono>

double medirTiempo(function<void()> f, int repeticiones) {
    using namespace chrono;

    auto inicio = high_resolution_clock::now();

    for (int i = 0; i < repeticiones; i++) {
        f();
    }

    auto fin = high_resolution_clock::now();

    auto total_ns = duration_cast<nanoseconds>(fin - inicio).count();

    double total_ms = (double)total_ns / 1'000'000.0;

    return total_ms / repeticiones;
}