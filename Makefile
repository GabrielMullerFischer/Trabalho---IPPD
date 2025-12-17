CC = gcc
CFLAGS = -O3 -Wall
OMP_FLAGS = -fopenmp
SRC = src/main.c
BIN_DIR = bin

all: seq omp

# Cria diretório bin se não existir
$(BIN_DIR):
	mkdir -p $(BIN_DIR)

# Compilação Sequencial
seq: $(BIN_DIR)
	$(CC) $(CFLAGS) $(SRC) -o $(BIN_DIR)/main_seq

# Compilação Paralela
omp: $(BIN_DIR)
	$(CC) $(CFLAGS) $(OMP_FLAGS) $(SRC) -o $(BIN_DIR)/main_omp

# Executa bateria de testes
run: omp
	bash scripts/run.sh

# Gera gráficos
plot:
	python3 scripts/plot.py

clean:
	rm -rf $(BIN_DIR) results.csv *.png