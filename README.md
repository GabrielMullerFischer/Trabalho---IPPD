## Membros do Grupo

| Nome Completo | Matrícula | Responsabilidades |
| :--- | :--- | :--- |
| **Gabriel Muller Fischer** | [20105040] | Relatório - Compilar/rodar |
| **Pedro Ivo Kuhn** | [20103604] | Implementação - Automação (Makefile) |

## Estrutura do Projeto

* **`src/`**: Código fonte em C (`main.c`).
* **`scripts/`**: Scripts auxiliares para execução (`run.sh`) e plotagem (`plot.py`).
* **`bin/`**: Diretório onde os executáveis são gerados.
* **`Makefile`**: Arquivo de automação de compilação.
* **`results.csv`**: (Gerado) Dados brutos das execuções.
* **`*.png`**: (Gerado) Gráficos de análise de desempenho.

## Objetivos do Experimento

### 1. Tarefa A: Escalonamento (Load Balancing)
Analisar como diferentes estratégias (`static`, `dynamic`, `guided`) e tamanhos de *chunk* lidam com uma carga de trabalho extremamente irregular, simulada através do cálculo de Fibonacci recursivo `fib(i % 28)`.

### 2. Tarefa D: Overhead de Paralelismo
Quantificar o custo computacional de criação e destruição de threads (*fork/join*), comparando uma abordagem ingênua (múltiplas regiões paralelas) com uma otimizada (região única) na soma de vetores.

## Como Compilar e Executar

Este projeto foi configurado para ambiente Linux (ou WSL2 no Windows). Certifique-se de ter instalado: `gcc`, `make` e `python3`.

1. Execução dos Testes
```
make run
```
Este comando executa o script scripts/run.sh e salva os tempos no arquivo results.csv.

2. Geração dos Gráficos
Para processar os dados e gerar as imagens PNG automaticamente:
```
make plot
```
Os gráficos serão salvos na raiz do projeto

