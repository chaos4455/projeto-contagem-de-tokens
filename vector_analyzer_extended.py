from transformers import BertTokenizer, BertModel
import torch
import numpy as np
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.progress import track
from rich.live import Live
from rich import box
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.align import Align
import numpy as np
from colorama import init, Fore, Back, Style
from sklearn.preprocessing import MinMaxScaler
import math
from datetime import datetime
import psutil
import platform
import requests
import json
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
import socket
import sys
import time
import random
import sqlite3

# Inicialização
init()  # Colorama
console = Console()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Configurações da API
API_CONFIG = {
    "host": "localhost",
    "port": 8000,
    "base_url": "http://localhost:8000",
    "endpoint": "/vectors/"
}

# Carregar modelo BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
model = BertModel.from_pretrained('bert-base-multilingual-cased').to(device)

def get_system_info():
    """Obtém informações do sistema"""
    return {
        "os": platform.system(),
        "python_version": platform.python_version(),
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "hostname": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname())
    }

def get_api_health():
    """Verifica a saúde da API"""
    try:
        response = requests.get(f"{API_CONFIG['base_url']}/docs")
        return response.status_code == 200
    except:
        return False

def decode_vector_to_words(vector_values):
    """Converte vetor em palavras usando BERT"""
    try:
        # Normalização do vetor
        scaler = MinMaxScaler()
        normalized_vector = scaler.fit_transform(np.array(vector_values).reshape(-1, 1)).flatten()
        
        # Converte para tensor e processa com BERT
        with torch.no_grad():
            inputs = torch.tensor(normalized_vector).unsqueeze(0).to(device)
            outputs = model(inputs)
            predictions = outputs[0]
        
        # Pega os tokens mais prováveis
        token_ids = torch.argmax(predictions, dim=-1)
        tokens = tokenizer.convert_ids_to_tokens(token_ids[0])
        
        # Remove tokens especiais e junta as palavras
        words = []
        for token in tokens:
            if token not in ['[PAD]', '[CLS]', '[SEP]', '[UNK]']:
                # Remove ## dos subtokens do BERT
                if token.startswith('##'):
                    if words:
                        words[-1] = words[-1] + token[2:]
                else:
                    words.append(token)
        
        return ' '.join(words)
    except Exception as e:
        console.print(f"[red]Erro ao decodificar vetor: {str(e)}[/]")
        return "N/A"

def analyze_vector(vector_id, vector_values, word=None, palavra_origem=None):
    """Analisa um vetor e retorna estatísticas detalhadas"""
    
    # Header com informações do sistema
    sys_info = get_system_info()
    console.print(Panel.fit(
        f"🖥️ Sistema: {sys_info['os']} | 🐍 Python: {sys_info['python_version']} | "
        f"📊 CPU: {sys_info['cpu_usage']}% | 💾 RAM: {sys_info['memory_usage']}%",
        title="[bold cyan]Status do Sistema[/]",
        subtitle="🔧 Informações Técnicas"
    ))

    # Informações da Palavra
    decoded_word = decode_vector_to_words(vector_values)
    console.print(Panel.fit(
        f"📝 Palavra Original: [bold green]{word}[/]\n"
        f"🔄 Palavra Decodificada: [bold yellow]{decoded_word}[/]\n"
        f"🌍 Origem: [bold blue]{palavra_origem or 'N/A'}[/]\n"
        f"🔢 ID: [bold cyan]{vector_id}[/]",
        title="[bold magenta]Informações da Palavra[/]",
        subtitle="🔤 Análise Textual"
    ))

    # API Status
    api_status = "[green]Online[/]" if get_api_health() else "[red]Offline[/]"
    console.print(Panel.fit(
        f"🌐 API: {api_status} | 🏠 Host: {API_CONFIG['host']} | "
        f"🔌 Porta: {API_CONFIG['port']} | 🔍 ID: {vector_id}",
        title="[bold magenta]Informações da API[/]",
        subtitle="🚀 Endpoint Status"
    ))

    # Normalização do vetor
    scaler = MinMaxScaler()
    normalized_vector = scaler.fit_transform(np.array(vector_values).reshape(-1, 1)).flatten()

    # Processamento BERT - Conversão de tipo adicionada
    try:
        inputs = torch.tensor(np.round(normalized_vector).astype(np.int64)).unsqueeze(0).to(device)
        with torch.no_grad():
            outputs = model(inputs)
            hidden_states = outputs[0]
    except RuntimeError as e:
        console.print(f"[bold red]Erro durante o processamento BERT: {e}[/]")
        return

    # Layout principal
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", size=30),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="left"),
        Layout(name="right")
    )
    layout["left"].split_column(Layout(name="left_top"), Layout(name="left_bottom"))
    layout["right"].split_column(Layout(name="right_top"), Layout(name="right_bottom"))

    # Grid 1: Informações do Vetor
    vector_info = Table(title="📝 Informações do Vetor", box=box.ROUNDED)
    vector_info.add_column("Campo", style="cyan")
    vector_info.add_column("Valor", style="green")
    
    vector_info.add_row("🔑 ID", str(vector_id))
    vector_info.add_row("📏 Dimensão", str(len(vector_values)))
    vector_info.add_row("💾 Tamanho em Memória", f"{sys.getsizeof(vector_values)} bytes")
    vector_info.add_row("🔢 Tipo de Dados", str(type(vector_values[0])))
    vector_info.add_row("📊 Shape", str(np.array(vector_values).shape))
    vector_info.add_row("🎯 Device", str(device))
    vector_info.add_row("🤖 Modelo BERT", "bert-base-multilingual-cased")
    vector_info.add_row("⚡ GPU Disponível", str(torch.cuda.is_available()))
    if torch.cuda.is_available():
        vector_info.add_row("🎮 GPU Nome", torch.cuda.get_device_name(0))
        vector_info.add_row("💾 GPU Memória", f"{torch.cuda.get_device_properties(0).total_memory/1e9:.2f} GB")

    # Grid 2: Análise BERT Detalhada
    bert_analysis = Table(title="🤖 Análise BERT Detalhada", box=box.ROUNDED)
    bert_analysis.add_column("Métrica", style="magenta")
    bert_analysis.add_column("Valor", style="yellow")
    
    tokens = tokenizer.encode(str(vector_values), add_special_tokens=True)
    token_words = tokenizer.convert_ids_to_tokens(tokens)
    
    bert_stats = {
        "🔤 Total Tokens": len(tokens),
        "📝 Tokens Únicos": len(set(tokens)),
        "📊 Densidade Token": len(set(tokens)) / len(tokens),
        "🔍 Atenção Média": float(hidden_states.mean()),
        "📈 Atenção Máxima": float(hidden_states.max()),
        "📉 Atenção Mínima": float(hidden_states.min()),
        "🎯 Atenção Std": float(hidden_states.std()),
        "🔄 Entropia Atenção": float(-torch.sum(hidden_states * torch.log2(hidden_states + 1e-10))),
        "📊 Dimensão Hidden": hidden_states.shape[-1],
        "🔢 Camadas BERT": len(model.encoder.layer)
    }
    
    for metric, value in bert_stats.items():
        if isinstance(value, float):
            bert_analysis.add_row(metric, f"{value:.6f}")
        else:
            bert_analysis.add_row(metric, str(value))

    # Grid 3: Tokens e Palavras
    token_table = Table(title="🔤 Análise de Tokens", box=box.ROUNDED)
    token_table.add_column("Token", style="cyan")
    token_table.add_column("ID", style="green")
    token_table.add_column("Palavra", style="yellow")
    
    for token, token_id, word in zip(tokens[:10], range(len(tokens[:10])), token_words[:10]):
        token_table.add_row(str(token), str(token_id), word)

    # Grid 4: Métricas de Performance
    performance = Table(title="⚡ Métricas de Performance", box=box.ROUNDED)
    performance.add_column("Métrica", style="blue")
    performance.add_column("Valor", style="red")
    
    perf_stats = {
        "🖥️ CPU Usage": f"{psutil.cpu_percent()}%",
        "💾 Memory Usage": f"{psutil.virtual_memory().percent}%",
        "🔄 Swap Usage": "N/A", # Valor padrão se houver erro
        "💽 Disk Usage": f"{psutil.disk_usage('/').percent}%",
        "🌡️ CPU Temp": f"{psutil.sensors_temperatures().get('coretemp', [{'current': 0}])[0]['current']}°C" if hasattr(psutil, 'sensors_temperatures') else "N/A",
        "⚡ Power Supply": "AC" if hasattr(psutil, 'sensors_battery') and psutil.sensors_battery() is None else "Battery",
        "🔌 Network IO": f"{psutil.net_io_counters().bytes_sent/1e6:.2f}MB sent / {psutil.net_io_counters().bytes_recv/1e6:.2f}MB recv",
        "⏱️ Boot Time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        "👥 Users": len(psutil.users()),
        "🔄 Processes": len(psutil.pids())
    }
    
    try:
        perf_stats["🔄 Swap Usage"] = f"{psutil.swap_memory().percent}%"
    except RuntimeError:
        pass # Ignora o erro

    for metric, value in perf_stats.items():
        performance.add_row(metric, str(value))

    # Exibir resultados
    with Live(layout, refresh_per_second=4):
        layout["header"].update(
            Panel("🔬 Análise Detalhada de Vetores e Sistema", 
                  style="bold magenta")
        )
        layout["left_top"].update(Panel(vector_info))
        layout["left_bottom"].update(Panel(bert_analysis))
        layout["right_top"].update(Panel(token_table))
        layout["right_bottom"].update(Panel(performance))
        layout["footer"].update(
            Panel(f"⏰ Análise concluída em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
                  f"🖥️ {sys_info['hostname']} | 🌐 {sys_info['ip']}")
        )

    # Progress bar com estatísticas
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task1 = progress.add_task("[red]Processando vetores...", total=100)
        task2 = progress.add_task("[green]Analisando tokens...", total=100)
        task3 = progress.add_task("[blue]Calculando estatísticas...", total=100)
        
        while not progress.finished:
            progress.update(task1, advance=0.9)
            progress.update(task2, advance=0.7)
            progress.update(task3, advance=0.5)

    # Salvar resultados
    results = {
        "timestamp": datetime.now().isoformat(),
        "system_info": sys_info,
        "api_info": {
            "status": api_status,
            "config": API_CONFIG
        },
        "vector_info": {
            "id": vector_id,
            "dimension": len(vector_values),
            "bert_stats": bert_stats,
            "performance": perf_stats
        }
    }
    
    with open(f'vector_analysis_{vector_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
        json.dump(results, f, indent=4)

def get_random_valid_id():
    """Obtém um ID aleatório válido do banco de dados"""
    try:
        conn = sqlite3.connect('vectors_continuo.db')
        cursor = conn.cursor()
        cursor.execute("SELECT MIN(id), MAX(id) FROM word_vectors")
        min_id, max_id = cursor.fetchone()
        conn.close()
        return random.randint(min_id, max_id)
    except Exception as e:
        console.print(f"[red]Erro ao obter ID aleatório: {str(e)}[/]")
        return 1

def clear_console():
    """Limpa o console mantendo o histórico"""
    console.clear()

def run_continuous_analysis():
    """Executa a análise em loop infinito"""
    iteration = 1
    
    try:
        while True:
            console.rule(f"[bold cyan]Iteração #{iteration}")
            
            # Obtém ID aleatório
            vector_id = get_random_valid_id()
            
            try:
                # Tenta obter o vetor da API
                response = requests.get(f"{API_CONFIG['base_url']}/vectors/{vector_id}")
                response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                data = response.json()
                vector_values = data['vector']
                word = data['word']
                palavra_origem = data.get('palavra_origem', 'N/A')
                    
                # Painel de informações da palavra atual
                console.print(Panel.fit(
                    f"[bold green]🎯 Analisando:[/]\n"
                    f"📝 Palavra: [bold yellow]{word}[/]\n"
                    f"🌍 Origem: [bold blue]{palavra_origem}[/]\n"
                    f"🔢 ID: [bold cyan]{vector_id}[/]",
                    title="[bold red]Palavra Atual[/]"
                ))
                    
                # Executa a análise
                analyze_vector(vector_id, vector_values, word, palavra_origem)
                    
            except requests.exceptions.RequestException as e:
                console.print(f"[red]Erro de conexão com a API: {str(e)}")
                vector_values = [0] * 5
            except KeyError as e:
                console.print(f"[red]Erro na estrutura JSON da API: {str(e)}")
                vector_values = [0] * 5
            except Exception as e:
                console.print(f"[red]Erro inesperado ao processar a resposta da API: {str(e)}")
                vector_values = [0] * 5
            
            # Aguarda antes da próxima iteração
            console.print("\n[cyan]Aguardando próxima análise...[/]")
            
            # Barra de progresso para o intervalo com informações
            with Progress() as progress:
                task = progress.add_task(
                    f"[green]Próxima análise em... (Última palavra: {word})", 
                    total=100
                )
                for _ in range(100):
                    time.sleep(0.1)  # 10 segundos total
                    progress.update(task, advance=1)
            
            # Limpa console mantendo histórico
            clear_console()
            
            iteration += 1
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Análise interrompida pelo usuário[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Erro inesperado: {str(e)}[/]")
        import traceback
        console.print("[red]" + traceback.format_exc() + "[/]")

if __name__ == "__main__":
    console.print(Panel.fit(
        "🔄 Iniciando análise contínua de vetores\n"
        "Pressione Ctrl+C para interromper\n\n"
        "[bold yellow]Informações adicionais:[/]\n"
        "- Conversão de vetores para palavras ativada\n"
        "- Comparação palavra original vs. decodificada\n"
        "- Monitoramento de origem das palavras",
        title="[bold green]Análise Contínua[/]",
        subtitle="[bold red]Auto-refresh com Decodificação[/]"
    ))
    
    try:
        run_continuous_analysis()
    except KeyboardInterrupt:
        console.print("\n[yellow]Programa finalizado pelo usuário[/]")
    except Exception as e:
        console.print(f"\n[red]Erro fatal: {str(e)}[/]")
        raise
