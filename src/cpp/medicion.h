#ifndef MEDICION_H
#define MEDICION_H

#include <functional>
using namespace std;

double medirTiempo(function<void()> f, int repeticiones);

#endif