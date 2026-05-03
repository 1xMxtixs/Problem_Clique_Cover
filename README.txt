Instructivo para ejecutar cada programa desde la consola, tomar en cuenta que los archivos grafos están en la carpeta "instances" ordenados por tamaño y estructura, también que en el momento en la terminal se encuentra en "C:\....\Problem_Clique_Cover".

//PROGRAMAS//

C++: 1. Acceder a la ubicación del programa con "cd src\cpp".

     2. Revisar si existe el "main.exe", si no existe, compilar con "g++ main.cpp algoritmos.cpp grafo.cpp experimento.cpp medicion.cpp -o 	main.exe", si el main.exe existe y no se ejecuta, recompilar nuevamente.

     3. Ejecutar el programa con "./main".

     4. Ingresar el nombre del archivo grafo con comillas a probar de manera que quede "Ingrese la ruta del grafo: "nombreDelGrafo.txt"".

     Nota: para ejecutar grafos de 60 vértices hacia arriba, hacerlo tomando en cuenta el backtracking de c++ tardara mucho tiempo en 	resolver grafos grandes.

Python: Ejecutar con "python src/python/main.py instances/"direccionArchivo"", luego de instances debe ingresar la ruta del grafo que desea 	probar ejecutarlo con python.

Java: Ejecutar con "java -cp build cl.unab.cliquecover.Main <ruta_al_grafo.txt>" <- tiene que ser la ruta completa al grafo "C:\..	\grafo.txt".

//HERRAMIENTAS//

Benchmark: Ejecutar con "python tools\benchmark.py".

Generador de grafos: Ejecutar con "python tools\generator.py".

Validador de soluciones: Ejecutar con "python tools\validator.py <ruta_al_grafo.txt> <ruta_a_la_solucion.txt>".

Generador de gráficos: Ejecutar con "python tools\graficos_obtenidos.py".