#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <string.h>
#include <math.h>

// Fibonacci ineficiente (recursivo) para gerar carga irregular
long long fib(int n) {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        printf("Uso: %s <N> <K> <TASK_TYPE [A|D_naive|D_opt]> [NUM_THREADS]\n", argv[0]);
        return 1;
    }

    int N = atoi(argv[1]);
    int K = atoi(argv[2]);
    char *task = argv[3];
    int threads = (argc > 4) ? atoi(argv[4]) : 1;

    // Define número de threads
    omp_set_num_threads(threads);

    long long *v = malloc(N * sizeof(long long));
    double start, end;

    start = omp_get_wtime();

    // --- TAREFA A: Laço Irregular e Schedule ---
    // A política de schedule será definida via variável de ambiente OMP_SCHEDULE no run.sh
    if (strcmp(task, "A") == 0) {
        #pragma omp parallel for schedule(runtime)
        for (int i = 0; i < N; i++) {
            v[i] = fib(i % K);
        }
    }

    // --- TAREFA D: Organização de Região Paralela ---
    // Variante Ingênua (overhead de abrir/fechar região paralela 2x)
    else if (strcmp(task, "D_naive") == 0) {
        #pragma omp parallel for
        for (int i = 0; i < N; i++) {
            v[i] = fib(i % K); // Trabalho 1
        }
        
        #pragma omp parallel for
        for (int i = 0; i < N; i++) {
            v[i] += 1;         // Trabalho 2 (simples)
        }
    }
    // Variante Arrumada (uma única região paralela)
    else if (strcmp(task, "D_opt") == 0) {
        #pragma omp parallel
        {
            #pragma omp for
            for (int i = 0; i < N; i++) {
                v[i] = fib(i % K);
            }

            #pragma omp for
            for (int i = 0; i < N; i++) {
                v[i] += 1;
            }
        }
    }

    end = omp_get_wtime();

    // Saída CSV-friendly: Task, N, K, Threads, Time
    printf("%s,%d,%d,%d,%.6f\n", task, N, K, threads, end - start);

    free(v);
    return 0;
}