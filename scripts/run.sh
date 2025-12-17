#!/bin/bash

# Configurações
EXEC="./bin/main_omp"
OUTPUT="results.csv"
TRIALS=5

# Parâmetros do enunciado
NS=(100000 500000 1000000)
KS=(20 24 28)
THREADS=(1 2 4 8 16)
CHUNKS=(1 4 16 64)

# Cabeçalho do CSV
echo "task,n,k,threads,schedule,chunk,trial,time" > $OUTPUT

echo "Iniciando benchmarks..."

# --- TAREFA A ---
for n in "${NS[@]}"; do
  for k in "${KS[@]}"; do
    for t in "${THREADS[@]}"; do
        
        # 1. Schedule Static (Chunk padrão/auto)
        export OMP_SCHEDULE="static"
        for i in $(seq 1 $TRIALS); do
            res=$($EXEC $n $k A $t)
            # Extrai apenas o tempo da saída
            time=$(echo $res | cut -d',' -f5)
            echo "A,$n,$k,$t,static,auto,$i,$time" >> $OUTPUT
        done

        # 2. Dynamic e Guided com Chunks variados
        for sched in "dynamic" "guided"; do
            for chunk in "${CHUNKS[@]}"; do
                export OMP_SCHEDULE="$sched,$chunk"
                for i in $(seq 1 $TRIALS); do
                    res=$($EXEC $n $k A $t)
                    time=$(echo $res | cut -d',' -f5)
                    echo "A,$n,$k,$t,$sched,$chunk,$i,$time" >> $OUTPUT
                done
            done
        done
    done
  done
done

# --- TAREFA D (Overhead) ---
# Usamos um N fixo intermediário e K baixo para focar no overhead de criação, não no cálculo
N_D=500000
K_D=20
for t in "${THREADS[@]}"; do
    for type in "D_naive" "D_opt"; do
        # Schedule default para Task D
        export OMP_SCHEDULE="static"
        for i in $(seq 1 $TRIALS); do
            res=$($EXEC $N_D $K_D $type $t)
            time=$(echo $res | cut -d',' -f5)
            echo "$type,$N_D,$K_D,$t,static,auto,$i,$time" >> $OUTPUT
        done
    done
done

echo "Concluído. Resultados em $OUTPUT"