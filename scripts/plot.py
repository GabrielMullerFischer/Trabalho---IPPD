import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração visual
sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.max_open_warning': 0})

try:
    df = pd.read_csv("results.csv")
except FileNotFoundError:
    print("Erro: Arquivo results.csv não encontrado.")
    exit(1)

df_avg = df.groupby(['task', 'n', 'k', 'threads', 'schedule', 'chunk'])['time'].agg(['mean', 'std']).reset_index()

# 1. Gráfico Tarefa A: Impacto do Schedule (Linhas)
subset_a = df_avg[(df_avg['task'] == 'A') & (df_avg['n'] == 1000000) & (df_avg['k'] == 28)]

if not subset_a.empty:
    plt.figure(figsize=(12, 6))
    subset_a['config'] = subset_a['schedule'] + " (chunk=" + subset_a['chunk'].astype(str) + ")"
    
    sns.lineplot(data=subset_a, x='threads', y='mean', hue='config', marker='o')
    plt.title('Tarefa A: Comparação de Schedules (N=1M, K=28 - Carga Desbalanceada)')
    plt.ylabel('Tempo Médio (s)')
    plt.xlabel('Threads')
    plt.yscale('log')
    plt.savefig('grafico_task_a_schedules.png')
    print("Gerado grafico_task_a_schedules.png")

# 2. Gráfico Tarefa A: Ranking (Barras)
subset_16 = subset_a[subset_a['threads'] == 16].copy()

if not subset_16.empty:
    plt.figure(figsize=(14, 7))
    
    # Ordena do menor tempo (mais rápido) para o maior (mais lento)
    subset_16 = subset_16.sort_values('mean')
    
    ax = sns.barplot(
        data=subset_16, 
        x='config', 
        y='mean', 
        palette='viridis', 
        zorder=3
    )
    
    plt.grid(axis='y', linestyle='--', alpha=0.7, color='gray', zorder=0)
    plt.title('Ranking de Performance: Todos os Schedules com 16 Threads (N=1M, K=28)', fontsize=14)
    plt.ylabel('Tempo de Execução (s)', fontsize=12)
    plt.xlabel('Configuração', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    for i in ax.containers:
        ax.bar_label(i, fmt='%.3f s', padding=3, fontsize=10)

    plt.ylim(0, subset_16['mean'].max() * 1.1) 
    plt.tight_layout()
    plt.savefig('grafico_task_a_barras.png')
    print("-> Gerado: grafico_task_a_barras.png")

# 3. Gráfico Tarefa D: Comparação de TEMPOS
subset_d = df_avg[df_avg['task'].str.contains('D_')]

if not subset_d.empty:
    plt.figure(figsize=(8, 6))
    sns.barplot(data=subset_d, x='threads', y='mean', hue='task')

    plt.title('Tarefa D: Comparação de Tempos (Naive vs Opt)')
    plt.ylabel('Tempo Médio (s)')
    plt.xlabel('Threads')
    plt.savefig('grafico_task_d_tempos.png')
    print("Gerado grafico_task_d_tempos.png")

# 4. Gráfico Tarefa D: Comparação de OVERHEAD 
if not subset_d.empty:
    pivot_d = subset_d.pivot_table(index='threads', columns='task', values='mean').reset_index()
    
    # Se existirem as duas colunas, calcula a diferença
    if 'D_naive' in pivot_d.columns and 'D_opt' in pivot_d.columns:
        pivot_d['overhead'] = pivot_d['D_naive'] - pivot_d['D_opt']
        
        plt.figure(figsize=(10, 6))
        plt.grid(axis='y', linestyle='-', alpha=0.3, color='#cccccc', zorder=0)

        colors = ['#e74c3c' if x > 0 else '#95a5a6' for x in pivot_d['overhead']]
        
        ax = sns.barplot(
            data=pivot_d, 
            x='threads', 
            y='overhead', 
            palette=colors,
            zorder=3
        )
        
        plt.title('Custo do Overhead (Tempo Naive - Tempo Opt)', fontsize=14)
        plt.ylabel('Diferença de Tempo (segundos)', fontsize=12)
        plt.xlabel('Threads', fontsize=12)

        plt.axhline(0, color='black', linewidth=1)

        max_val = pivot_d['overhead'].max()
        min_val = pivot_d['overhead'].min()
        limit = max(abs(max_val), abs(min_val)) * 1.2
        if min_val < 0:
            plt.ylim(-limit, limit)
        else:
            plt.ylim(0, limit)

        for i in ax.containers:
            ax.bar_label(i, fmt='%.4f s', padding=3, fontsize=10, weight='bold')

        plt.tight_layout()
        plt.savefig('grafico_task_d_overhead.png')
        print("-> Gerado: grafico_task_d_overhead.png")
    else:
        print("Aviso: Não foi possível calcular overhead (faltam dados de D_naive ou D_opt).")