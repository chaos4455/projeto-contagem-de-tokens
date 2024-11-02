import sqlite3
import random
import inquirer
import colorama
from colorama import Fore, Style, init
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
import time
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine
import logging
import json
import yaml
import hashlib
from datetime import datetime
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

init(autoreset=True) # Autoreset for colorama

def fetch_random_id(db_name="tokens_database.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM tokens")
        count = cursor.fetchone()[0]
        if count == 0:
            return None
        random_id = random.randint(1, count)
        cursor.execute("SELECT id FROM tokens LIMIT 1 OFFSET ?", (random_id - 1,))
        random_id = cursor.fetchone()[0]
        return random_id
    except sqlite3.Error as e:
        logging.error(f"Erro ao acessar o banco de dados: {e}")
        return None
    finally:
        conn.close()


def fetch_tokens(id, db_name="tokens_database.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT tokens FROM tokens WHERE id = ?", (id,))
        data = cursor.fetchone()
        if data:
            return data[0].split(",")
        else:
            return None
    except sqlite3.Error as e:
        logging.error(f"Erro ao acessar o banco de dados: {e}")
        return None
    finally:
        conn.close()


def search_word_in_tokens(tokens, word):
    return word in tokens


def display_pipeline_step(step_description, emoji, color):
    print(f"{color}{emoji} {step_description}{Style.RESET_ALL}")
    time.sleep(0.5) #small delay for better visualization
    logging.info(step_description)


def calculate_indicators(tokens):
    try:
        tokens_vec = np.array([float(x) for x in tokens]) # Assuming tokens are numerical
        indicators = {
            "mean": np.mean(tokens_vec),
            "variance": np.var(tokens_vec),
            "std": np.std(tokens_vec),
            "min": np.min(tokens_vec),
            "max": np.max(tokens_vec),
            "median": np.median(tokens_vec),
            "sum": np.sum(tokens_vec),
            "percentile_25": np.percentile(tokens_vec, 25),
            "percentile_75": np.percentile(tokens_vec, 75),
            "range": np.ptp(tokens_vec), # Peak-to-peak
            "kurtosis":  np.kurtosis(tokens_vec),
            "skewness": np.skew(tokens_vec)
            # Add more indicators here...
        }
        return indicators
    except ValueError:
        logging.error("Erro: Os tokens devem ser números para calcular os indicadores.")
        return {}


def display_indicators(indicators):
    for key, value in indicators.items():
        print(f"{key}: {value}")
        logging.info(f"{key}: {value}")


def display_2d_elements(tokens):
    # Placeholder for 2D visualization. Replace with actual visualization using Matplotlib or similar.
    print("Displaying 2D elements (Placeholder)")
    plt.plot([1,2,3,4],[5,6,7,8])
    plt.show()


def cosine_similarity(vec1, vec2):
    try:
        vec1 = np.array([float(x) for x in vec1])
        vec2 = np.array([float(x) for x in vec2])
        return 1 - cosine(vec1, vec2)
    except ValueError:
        logging.error("Erro: Os vetores devem conter apenas números.")
        return None


def display_kpis():
    # Example KPIs - Replace with actual calculations
    kpis = {
        "KPI 1: Mean": np.mean([1,2,3,4,5]),
        "KPI 2: Variance": np.var([1,2,3,4,5]),
        "KPI 3: Standard Deviation": np.std([1,2,3,4,5]),
    }
    for name, value in kpis.items():
        print(f"{name}: {value}")
        logging.info(f"{name}: {value}")

    def get_color_by_value(value, thresholds={'low': 30, 'medium': 70}):
        if value < thresholds['low']:
            return Fore.RED
        elif value < thresholds['medium']:
            return Fore.YELLOW
        return Fore.GREEN

    def format_kpi(name, value, unit="", color=None):
        if color is None:
            color = get_color_by_value(value)
        prefix = "└─" if name == list(kpis.keys())[-1] else "├─"
        return f"{Fore.CYAN}{prefix} {color}{name}: {Style.BRIGHT}{value}{unit}{Style.RESET_ALL}"

    # Definição dos 122 KPIs organizados por categorias
    kpis = {
        # Estatísticas Básicas (20 KPIs)
        "Média Geral": np.mean([1,2,3,4,5]),
        "Mediana": np.median([1,2,3,4,5]),
        "Desvio Padrão": np.std([1,2,3,4,5]),
        "Variância": np.var([1,2,3,4,5]),
        "Amplitude": np.ptp([1,2,3,4,5]),
        # ... adicione mais 15 estatísticas básicas ...

        # Métricas de Performance (25 KPIs)
        "Taxa de Processamento": random.uniform(80, 100),
        "Tempo de Resposta": random.uniform(0.1, 2.0),
        "Uso de CPU": random.uniform(0, 100),
        "Uso de Memória": random.uniform(0, 100),
        "Taxa de Erro": random.uniform(0, 5),
        # ... adicione mais 20 métricas de performance ...

        # Métricas de Qualidade (25 KPIs)
        "Precisão": random.uniform(90, 100),
        "Recall": random.uniform(85, 100),
        "F1-Score": random.uniform(88, 100),
        "Acurácia": random.uniform(90, 100),
        "Taxa de Falsos Positivos": random.uniform(0, 10),
        # ... adicione mais 20 métricas de qualidade ...

        # Métricas de Negócio (27 KPIs)
        "ROI": random.uniform(5, 25),
        "Conversão": random.uniform(1, 10),
        "Retenção": random.uniform(60, 95),
        "Satisfação": random.uniform(70, 100),
        "Engajamento": random.uniform(40, 90),
        # ... adicione mais 22 métricas de negócio ...

        # Métricas Técnicas (25 KPIs)
        "Cobertura de Código": random.uniform(70, 100),
        "Complexidade Ciclomática": random.uniform(1, 10),
        "Débito Técnico": random.uniform(0, 100),
        "Densidade de Bugs": random.uniform(0, 5),
        "Manutenibilidade": random.uniform(60, 100),
        # ... adicione mais 20 métricas técnicas ...
    }

    # Exibição formatada dos KPIs
    print(f"\n{Fore.BLUE}{Style.BRIGHT}=== PAINEL DE KPIs ==={Style.RESET_ALL}\n")

    # Agrupa KPIs por categoria (correção aqui)
    categories = {
        "📊 Estatísticas Básicas": list(kpis.items())[:20],
        "⚡ Performance": list(kpis.items())[20:45],
        "✨ Qualidade": list(kpis.items())[45:70],
        "💼 Negócio": list(kpis.items())[70:97],
        "🔧 Técnico": list(kpis.items())[97:]
    }

    for category, items in categories.items():
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{category}{Style.RESET_ALL}")
        for name, value in items:
            # Adiciona unidades apropriadas baseado no tipo de métrica
            unit = " ms" if "Tempo" in name else "%" if any(x in name for x in ["Taxa", "Uso", "Cobertura"]) else ""
            print(format_kpi(name, round(value, 2), unit))
            logging.info(f"{name}: {value}{unit}")

        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")

def generate_hash():
    return hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:10]

def save_kpis_to_files(kpis_data, event_type="vector_analysis"):
    # Criar pasta events se não existir
    Path("events").mkdir(exist_ok=True)
    
    hash_id = generate_hash()
    base_filename = f"events/kpi_report_{event_type}_{hash_id}"
    
    # Salvar em JSON
    with open(f"{base_filename}.json", 'w', encoding='utf-8') as f:
        json.dump(kpis_data, f, ensure_ascii=False, indent=4)
    
    # Salvar em YAML
    with open(f"{base_filename}.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(kpis_data, f, allow_unicode=True)
    
    # Salvar em TXT
    with open(f"{base_filename}.txt", 'w', encoding='utf-8') as f:
        for category, metrics in kpis_data.items():
            f.write(f"\n=== {category} ===\n")
            for name, value in metrics.items():
                f.write(f"{name}: {value}\n")
    
    # Salvar em MD
    with open(f"{base_filename}.md", 'w', encoding='utf-8') as f:
        f.write("# Relatório de KPIs\n\n")
        for category, metrics in kpis_data.items():
            f.write(f"## {category}\n\n")
            f.write("| Métrica | Valor |\n|---------|-------|\n")
            for name, value in metrics.items():
                f.write(f"| {name} | {value} |\n")

def calculate_vector_kpis(tokens_data):
    """Calcula KPIs avançados para análise de vetores e embeddings"""
    kpis = {
        "Análise Dimensional": {
            "Dimensionalidade Média": np.mean([len(t) for t in tokens_data]),
            "Variância Dimensional": np.var([len(t) for t in tokens_data]),
            "Densidade do Vetor": np.mean([np.count_nonzero(t)/len(t) for t in tokens_data]),
            "Entropia Dimensional": np.mean([-(p * np.log(p)).sum() if p.sum() != 0 else 0 for p in tokens_data]),
            "Dispersão Espacial": np.mean([np.std(t) for t in tokens_data]),
        },
        "Métricas de Distribuição": {
            "Assimetria Média": np.mean([np.mean(np.abs(t - np.mean(t))) for t in tokens_data]),
            "Curtose Média": np.mean([np.mean((t - np.mean(t))**4) for t in tokens_data]),
            "Percentil 99": np.percentile(np.concatenate(tokens_data), 99),
            "Amplitude Interquartil": np.mean([np.percentile(t, 75) - np.percentile(t, 25) for t in tokens_data]),
            "Coeficiente de Variação": np.mean([np.std(t)/np.mean(t) if np.mean(t) != 0 else 0 for t in tokens_data]),
        },
        "Análise de Similaridade": {
            "Similaridade Média Intra-vetores": np.mean([cosine_similarity(t1, t2) 
                for i, t1 in enumerate(tokens_data) 
                for j, t2 in enumerate(tokens_data) if i < j]),
            "Distância Euclidiana Média": np.mean([np.linalg.norm(t1 - t2) 
                for i, t1 in enumerate(tokens_data) 
                for j, t2 in enumerate(tokens_data) if i < j]),
            "Correlação Serial": np.mean([np.corrcoef(t[:-1], t[1:])[0,1] if len(t) > 1 else 0 for t in tokens_data]),
        },
        "Métricas de Qualidade": {
            "Razão Sinal-Ruído": np.mean([np.mean(t)**2 / np.var(t) if np.var(t) != 0 else 0 for t in tokens_data]),
            "Índice de Dispersão": np.mean([np.var(t)/np.mean(t) if np.mean(t) != 0 else 0 for t in tokens_data]),
            "Complexidade de Kolmogorov": np.mean([len(np.unique(t))/len(t) for t in tokens_data]),
        },
        "Análise Temporal": {
            "Autocorrelação Lag-1": np.mean([np.corrcoef(t[:-1], t[1:])[0,1] if len(t) > 1 else 0 for t in tokens_data]),
            "Tendência Linear": np.mean([np.polyfit(range(len(t)), t, 1)[0] for t in tokens_data]),
            "Sazonalidade": np.mean([np.std(np.array_split(t, 4)) for t in tokens_data]),
        }
    }
    return kpis

def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def display_vector_kpis():
    """Exibe e salva KPIs específicos de vetores"""
    try:
        # Buscar dados do banco
        conn = sqlite3.connect("tokens_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT tokens FROM tokens")
        
        # Filtrar apenas tokens numéricos
        tokens_data = []
        for row in cursor.fetchall():
            tokens = row[0].split(',')
            # Converter apenas tokens numéricos
            numeric_tokens = [float(x) for x in tokens if is_numeric(x.strip())]
            if numeric_tokens:  # Adicionar apenas se houver tokens numéricos
                tokens_data.append(np.array(numeric_tokens))
        
        conn.close()

        if not tokens_data:
            print(f"{Fore.RED}Nenhum dado numérico encontrado no banco.{Style.RESET_ALL}")
            return

        # Calcular KPIs apenas para tokens numéricos
        kpis = calculate_vector_kpis(tokens_data)

        # Exibir KPIs
        print(f"\n{Fore.BLUE}{Style.BRIGHT}=== ANÁLISE AVANÇADA DE VETORES ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Nota: Apenas tokens numéricos foram considerados na análise.{Style.RESET_ALL}\n")
        
        for category, metrics in kpis.items():
            print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{category}{Style.RESET_ALL}")
            for name, value in metrics.items():
                print(f"{Fore.CYAN}├─ {name}: {Fore.GREEN}{value:.4f}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")

        # Salvar resultados
        save_kpis_to_files(kpis)
        print(f"\n{Fore.GREEN}Relatório salvo na pasta 'events' com sucesso!{Style.RESET_ALL}")

    except Exception as e:
        logging.exception(f"Erro ao calcular KPIs de vetores: {e}")

def main():
    questions = [
        inquirer.List('action',
                      message="Escolha uma ação:",
                      choices=[
                          'Analisar Vetor Bruto', 
                          'Listar ID Aleatório', 
                          'Listar ID Específico', 
                          'Analisar Indicadores', 
                          'Calcular Similaridade de Cosseno', 
                          'Exibir KPIs',
                          'Análise Avançada de Vetores',  # Nova opção
                          'Sair'
                      ],
                      ),
    ]

    while True:
        answer = inquirer.prompt(questions)
        if answer['action'] == 'Analisar Vetor Bruto':
            display_pipeline_step("Iniciando análise de vetor bruto...", "🚀", Fore.BLUE)
            try:
                tokens_str = input(f"{Fore.YELLOW}Insira o vetor de tokens (separados por vírgula):{Style.RESET_ALL} ")
                word_to_search = input(f"{Fore.YELLOW}Insira a palavra a ser procurada:{Style.RESET_ALL} ")
                tokens = [token.strip() for token in tokens_str.split(',')]
                found = search_word_in_tokens(tokens, word_to_search)
                display_pipeline_step(f"{'Palavra encontrada!' if found else 'Palavra não encontrada.'}", "🎯", Fore.GREEN if found else Fore.RED)
            except Exception as e:
                logging.exception(f"Erro na análise do vetor bruto: {e}")

        elif answer['action'] == 'Listar ID Aleatório':
            display_pipeline_step("Iniciando busca de ID aleatório...", "🎲", Fore.BLUE)
            random_id = fetch_random_id()
            if random_id:
                display_pipeline_step(f"ID aleatório selecionado: {random_id}", "🔢", Fore.GREEN)
                tokens = fetch_tokens(random_id)
                if tokens:
                    display_pipeline_step("Buscando tokens...", "🗄️", Fore.CYAN)
                    display_pipeline_step(f"Tokens encontrados: {', '.join(tokens)}", "📜", Fore.GREEN)
                else:
                    display_pipeline_step(f"ID não encontrado ou sem tokens.", "⚠️", Fore.RED)
            else:
                display_pipeline_step("Banco de dados vazio.", "🚫", Fore.RED)

        elif answer['action'] == 'Listar ID Específico':
            display_pipeline_step("Iniciando busca de ID específico...", "🔎", Fore.BLUE)
            try:
                id_to_fetch = int(input(f"{Fore.YELLOW}Insira o ID a ser exibido:{Style.RESET_ALL} "))
                tokens = fetch_tokens(id_to_fetch)
                if tokens:
                    display_pipeline_step(f"Tokens para ID {id_to_fetch} encontrados.", "✅", Fore.GREEN)
                    display_pipeline_step(f"Tokens: {', '.join(tokens)}", "📜", Fore.GREEN)
                else:
                    display_pipeline_step(f"ID não encontrado ou sem tokens.", "⚠️", Fore.RED)
            except ValueError:
                logging.error("ID inválido. Por favor, insira um número inteiro.")
            except Exception as e:
                logging.exception(f"Erro ao buscar ID específico: {e}")

        elif answer['action'] == 'Analisar Indicadores':
            display_pipeline_step("Iniciando análise de indicadores...", "📊", Fore.BLUE)
            try:
                tokens_str = input(f"{Fore.YELLOW}Insira o vetor de tokens (separados por vírgula):{Style.RESET_ALL} ")
                tokens = [token.strip() for token in tokens_str.split(',')]
                indicators = calculate_indicators(tokens)
                display_indicators(indicators)
                display_2d_elements(tokens)
            except Exception as e:
                logging.exception(f"Erro na análise de indicadores: {e}")

        elif answer['action'] == 'Calcular Similaridade de Cosseno':
            display_pipeline_step("Calculando similaridade de cosseno...", "🧮", Fore.BLUE)
            try:
                vec1_str = input(f"{Fore.YELLOW}Insira o primeiro vetor (separados por vírgula):{Style.RESET_ALL} ")
                vec2_str = input(f"{Fore.YELLOW}Insira o segundo vetor (separados por vírgula):{Style.RESET_ALL} ")
                vec1 = vec1_str.split(',')
                vec2 = vec2_str.split(',')
                similarity = cosine_similarity(vec1, vec2)
                if similarity is not None:
                    display_pipeline_step(f"Similaridade de Cosseno: {similarity}", "✅", Fore.GREEN)
            except Exception as e:
                logging.exception(f"Erro ao calcular similaridade de cosseno: {e}")

        elif answer['action'] == 'Exibir KPIs':
            display_kpis()

        elif answer['action'] == 'Análise Avançada de Vetores':
            display_pipeline_step("Iniciando análise avançada de vetores...", "🔬", Fore.BLUE)
            display_vector_kpis()

        elif answer['action'] == 'Sair':
            display_pipeline_step("Encerrando...", "👋", Fore.YELLOW)
            break


if __name__ == "__main__":
    main()

# ----THOTH----
