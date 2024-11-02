from transformers import BertTokenizer, BertModel
import torch
import numpy as np
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.progress import track
from rich.live import Live
import numpy as np
from colorama import init, Fore, Back, Style
from sklearn.preprocessing import MinMaxScaler
import math
from datetime import datetime

# Inicialização
init()  # Colorama
console = Console()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Carregar modelo BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
model = BertModel.from_pretrained('bert-base-multilingual-cased').to(device)

def analyze_vector(vector_values):
    """Analisa um vetor e retorna estatísticas detalhadas"""
    console.print(Panel.fit("🔍 Iniciando análise vetorial", 
                          title="[bold cyan]Análise de Vetores BERT[/]",
                          subtitle="🤖 Powered by Transformers"))

    # Normalização do vetor
    scaler = MinMaxScaler()
    normalized_vector = scaler.fit_transform(np.array(vector_values).reshape(-1, 1)).flatten()

    # Converter para tensor LongTensor e processar com BERT
    # Check for values outside the range of a LongTensor
    if np.any(normalized_vector < -2**31) or np.any(normalized_vector > 2**31 -1):
        console.print(f"[bold red]Error: Normalized vector contains values outside the range of a LongTensor. Please adjust the normalization method.[/]")
        return

    with torch.no_grad():
        inputs = torch.tensor(normalized_vector, dtype=torch.long).unsqueeze(0).to(device)
        outputs = model(inputs)
        hidden_states = outputs[0]

    # Criar layout
    layout = Layout()
    layout.split_column(
        Layout(name="header"),
        Layout(name="main"),
        Layout(name="footer")
    )
    layout["main"].split_row(Layout(name="grid1"), Layout(name="grid2"))
    layout["grid1"].split_row(Layout(name="grid1_1"), Layout(name="grid1_2"))
    layout["grid2"].split_row(Layout(name="grid2_1"), Layout(name="grid2_2"))


    # Grid 1: Estatísticas Básicas
    stats_basic = Table(title="📊 Estatísticas Básicas", box=None)
    stats_basic.add_column("Métrica", style="cyan")
    stats_basic.add_column("Valor", style="green")
    
    basic_stats = {
        "🔢 Dimensão": len(vector_values),
        "📈 Média": np.mean(vector_values),
        "📉 Desvio Padrão": np.std(vector_values),
        "⬆️ Máximo": np.max(vector_values),
        "⬇️ Mínimo": np.min(vector_values),
        "↔️ Amplitude": np.ptp(vector_values),
        "📊 Mediana": np.median(vector_values),
        "🎯 Variância": np.var(vector_values),
        "📐 Norma L2": np.linalg.norm(vector_values),
        "🔄 Entropia": -np.sum(normalized_vector * np.log2(normalized_vector + 1e-10))
    }
    
    for metric, value in basic_stats.items():
        stats_basic.add_row(metric, f"{value:.6f}")

    # Grid 2: Análise BERT
    stats_bert = Table(title="🤖 Análise BERT", box=None)
    stats_bert.add_column("Métrica", style="magenta")
    stats_bert.add_column("Valor", style="yellow")
    
    # Tokenização e análise BERT
    tokens = tokenizer.encode(str(vector_values), add_special_tokens=True)
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
        "🔢 Camadas": len(model.encoder.layer)
    }
    
    for metric, value in bert_stats.items():
        if isinstance(value, float):
            stats_bert.add_row(metric, f"{value:.6f}")
        else:
            stats_bert.add_row(metric, str(value))

    # Grid 3: Análise Temporal
    stats_temporal = Table(title="⏱️ Análise Temporal", box=None)
    stats_temporal.add_column("Métrica", style="blue")
    stats_temporal.add_column("Valor", style="red")
    
    # Análise de séries temporais
    temporal_stats = {
        "📈 Tendência": np.polyfit(range(len(vector_values)), vector_values, 1)[0],
        "🔄 Autocorrelação": np.correlate(vector_values, vector_values)[0],
        "📊 Cruzamentos Zero": len(np.where(np.diff(np.signbit(vector_values)))[0]),
        "📉 Volatilidade": np.std(np.diff(vector_values)),
        "🎯 Momentum": sum(np.diff(vector_values)),
        "🔍 Periodicidade": len(np.fft.fft(vector_values)),
        "📈 Pico FFT": np.max(np.abs(np.fft.fft(vector_values))),
        "⚡ Energia": np.sum(np.square(vector_values)),
        "🔄 Ciclos": len(np.where(np.diff(np.signbit(np.diff(vector_values))))[0]),
        "📊 Complexidade": np.sum(np.abs(np.diff(vector_values)))
    }
    
    for metric, value in temporal_stats.items():
        stats_temporal.add_row(metric, f"{value:.6f}")

    # Grid 4: Métricas Avançadas
    stats_advanced = Table(title="🎓 Métricas Avançadas", box=None)
    stats_advanced.add_column("Métrica", style="yellow")
    stats_advanced.add_column("Valor", style="cyan")
    
    # Cálculos avançados
    vector_tensor = torch.tensor(vector_values, dtype=torch.float)
    advanced_stats = {
        "🔍 Kurtosis": float(((vector_tensor - vector_tensor.mean())**4).mean() / (vector_tensor.std()**4)),
        "📊 Skewness": float(((vector_tensor - vector_tensor.mean())**3).mean() / (vector_tensor.std()**3)),
        "📈 Densidade": len(np.nonzero(vector_values)[0]) / len(vector_values),
        "🎯 Coef. Variação": np.std(vector_values) / np.mean(vector_values),
        "🔄 Shannon Entropy": -np.sum(normalized_vector * np.log2(normalized_vector + 1e-10)),
        "⚡ Signal Power": np.mean(np.square(vector_values)),
        "📉 Dynamic Range": 20 * np.log10(np.max(np.abs(vector_values)) / (np.min(np.abs(vector_values)) + 1e-10)),
        "🔍 Sparsity": np.sum(np.abs(vector_values) < 1e-10) / len(vector_values),
        "📊 Gini Index": np.sum(np.abs(vector_values)) / (len(vector_values) * np.mean(np.abs(vector_values))),
        "🎯 Hurst Exponent": 0.5  # Placeholder - implementação completa requer mais dados
    }
    
    for metric, value in advanced_stats.items():
        if isinstance(value, float) and not math.isnan(value):
            stats_advanced.add_row(metric, f"{value:.6f}")
        else:
            stats_advanced.add_row(metric, "N/A")

    # Exibir resultados
    with Live(layout, refresh_per_second=4):
        layout["header"].update(Panel("🔬 Análise Detalhada de Vetores"))
        layout["grid1_1"].update(Panel(stats_basic))
        layout["grid1_2"].update(Panel(stats_bert))
        layout["grid2_1"].update(Panel(stats_temporal))
        layout["grid2_2"].update(Panel(stats_advanced))
        layout["footer"].update(Panel(f"⏰ Análise concluída em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))

    # Barra de progresso colorida
    console.print("\n[bold green]Análise concluída com sucesso![/]")
    for i in track(range(10), description="[red]Finalizando análise..."):
        pass

if __name__ == "__main__":
    # Vetor de exemplo
    vector_values = [1.1924057130531671e-14, 7.15351953791486e-09, -1.6417647817581213e-13, 
                    2.406579822684353e-18, -6.152062841065303e-09]
    
    analyze_vector(vector_values)
