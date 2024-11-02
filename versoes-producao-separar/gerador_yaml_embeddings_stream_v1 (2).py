import yaml
import hashlib
from datetime import datetime
import google.generativeai as genai
import os
from pathlib import Path
import time
from colorama import init, Fore, Style, Back
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.columns import Columns
from rich.align import Align
from collections import Counter, deque
from rich.style import Style
from rich.text import Text
from rich.padding import Padding
import nltk
from nltk.tokenize import word_tokenize
import statistics
import asyncio
from transformers import BertTokenizer, BertModel
import torch
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Dict, List
import psutil
import GPUtil

# Download necessário do NLTK
nltk.download('punkt', quiet=True)

# Inicialização
init(autoreset=True)
console = Console()

# Emojis e ícones
EMOJI = {
    "stream": "🌊",
    "token": "🎯",
    "palavra": "📝",
    "letra": "📊",
    "tempo": "⏱️",
    "arquivo": "📄",
    "stats": "📈",
    "max": "⬆️",
    "min": "⬇️",
    "media": "➡️",
    "total": "💯",
    "velocidade": "🚀",
    "memoria": "💾",
    "processando": "⚡"
}

# 🔑 Configuração da API
API_KEY = "AIzaSyCEagEEnX-RdkW3-jCAb0H9nrTsgcE-Qqo"
genai.configure(api_key=API_KEY)

# 🎯 Configurações do modelo
NOME_MODELO = "gemini-1.5-flash"
CONFIG_GERACAO = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8096,
}

class AdvancedMetrics:
    def __init__(self):
        self.bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = 384  # dimensão do modelo MiniLM
        self.embedding_cache = {}
        self.token_frequency: Dict[str, int] = {}
        self.sentence_lengths: List[int] = []
        self.embedding_magnitudes: List[float] = []
        self.token_diversity = 0
        self.semantic_density = 0
        self.cpu_usage = 0
        self.memory_usage = 0
        self.gpu_usage = 0 if len(GPUtil.getGPUs()) > 0 else None

class StreamStats:
    def __init__(self):
        self.metrics = AdvancedMetrics()
        self.caracteres = 0
        self.palavras = 0
        self.tokens_bert = 0
        self.tokens_gemini = 0
        self.palavras_unicas = set()
        self.ultimas_palavras = deque(maxlen=10)
        self.maiores_palavras = []
        self.inicio = time.time()
        self.ultima_atualizacao = time.time()
        self.chars_por_segundo = 0
        self.palavras_por_segundo = 0
        self.buffer = ""
        self.sentences = []
        self.embedding_stats = {
            'min_magnitude': float('inf'),
            'max_magnitude': 0,
            'avg_magnitude': 0
        }
        self.token_stats = {
            'unique_ratio': 0,
            'avg_length': 0,
            'complexity_score': 0
        }

    def calcular_metricas_avancadas(self, texto: str):
        # Tokenização BERT
        tokens_bert = self.metrics.bert_tokenizer.tokenize(texto)
        self.tokens_bert += len(tokens_bert)

        # Análise de sentenças
        sentences = nltk.sent_tokenize(texto)
        self.sentences.extend(sentences)

        # Cálculo de embeddings
        if texto.strip():
            embedding = self.metrics.sentence_model.encode(texto)
            magnitude = np.linalg.norm(embedding)
            self.metrics.embedding_magnitudes.append(magnitude)
            
            # Atualizar estatísticas de embedding
            self.embedding_stats['min_magnitude'] = min(self.embedding_stats['min_magnitude'], magnitude)
            self.embedding_stats['max_magnitude'] = max(self.embedding_stats['max_magnitude'], magnitude)
            self.embedding_stats['avg_magnitude'] = np.mean(self.metrics.embedding_magnitudes)

        # Métricas de sistema
        self.metrics.cpu_usage = psutil.cpu_percent()
        self.metrics.memory_usage = psutil.virtual_memory().percent
        if self.metrics.gpu_usage is not None:
            gpus = GPUtil.getGPUs()
            self.metrics.gpu_usage = gpus[0].load * 100 if gpus else 0

        # Métricas de tokens
        for token in tokens_bert:
            self.metrics.token_frequency[token] = self.metrics.token_frequency.get(token, 0) + 1
        
        self.token_stats['unique_ratio'] = len(self.metrics.token_frequency) / sum(self.metrics.token_frequency.values())
        self.token_stats['avg_length'] = np.mean([len(token) for token in self.metrics.token_frequency.keys()])
        self.token_stats['complexity_score'] = self.calcular_complexidade()

    def calcular_complexidade(self) -> float:
        if not self.metrics.token_frequency:
            return 0
        
        # Baseado em entropia e distribuição de frequência
        total_tokens = sum(self.metrics.token_frequency.values())
        probabilities = [count/total_tokens for count in self.metrics.token_frequency.values()]
        entropy = -sum(p * np.log2(p) for p in probabilities)
        return entropy

    def criar_grid_layout(self):
        layout = Layout()
        
        # Estrutura principal
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", size=30),
            Layout(name="footer", size=3)
        )
        
        # Dividir área principal em três colunas
        layout["main"].split_row(
            Layout(name="left"),
            Layout(name="center"),
            Layout(name="right")
        )
        
        # Header com métricas em tempo real
        header = Panel(
            Align.center(
                Text.assemble(
                    (f"{EMOJI['stream']} Streaming Analytics ", "bold cyan"),
                    (f"| CPU: {self.metrics.cpu_usage:.1f}% ", "green"),
                    (f"| RAM: {self.metrics.memory_usage:.1f}% ", "yellow"),
                    (f"| GPU: {self.metrics.gpu_usage:.1f}% " if self.metrics.gpu_usage is not None else "", "red")
                )
            ),
            style="blue"
        )
        layout["header"].update(header)
        
        # Painel esquerdo - Métricas básicas e de tokens
        stats_table = Table(box=None, show_header=False)
        stats_table.add_column("Métrica", style="cyan")
        stats_table.add_column("Valor", style="green")
        
        stats_table.add_row(f"{EMOJI['letra']} Caracteres", f"{self.caracteres:,}")
        stats_table.add_row(f"{EMOJI['palavra']} Palavras", f"{self.palavras:,}")
        stats_table.add_row(f"{EMOJI['token']} Tokens BERT", f"{self.tokens_bert:,}")
        stats_table.add_row("🔄 Tokens/s", f"{self.tokens_bert/(time.time()-self.inicio):.1f}")
        stats_table.add_row("🎯 Token Uniqueness", f"{self.token_stats['unique_ratio']:.2%}")
        stats_table.add_row("📊 Complexity Score", f"{self.token_stats['complexity_score']:.2f}")
        stats_table.add_row("📏 Avg Token Length", f"{self.token_stats['avg_length']:.1f}")
        
        layout["left"].update(Panel(
            stats_table,
            title=f"{EMOJI['stats']} Token Metrics",
            border_style="blue"
        ))
        
        # Painel central - Métricas de embedding
        embedding_table = Table(box=None, show_header=False)
        embedding_table.add_column("Métrica", style="magenta")
        embedding_table.add_column("Valor", style="yellow")
        
        embedding_table.add_row("📉 Min Magnitude", f"{self.embedding_stats['min_magnitude']:.2f}")
        embedding_table.add_row("📈 Max Magnitude", f"{self.embedding_stats['max_magnitude']:.2f}")
        embedding_table.add_row("📊 Avg Magnitude", f"{self.embedding_stats['avg_magnitude']:.2f}")
        embedding_table.add_row("🔢 Embedding Dim", f"{self.metrics.embedding_dim}")
        embedding_table.add_row("📚 Sentences", f"{len(self.sentences)}")
        
        layout["center"].update(Panel(
            embedding_table,
            title=f"{EMOJI['stats']} Embedding Analytics",
            border_style="magenta"
        ))
        
        # Painel direito - Métricas avançadas
        advanced_table = Table(box=None, show_header=False)
        advanced_table.add_column("Métrica", style="blue")
        advanced_table.add_column("Valor", style="cyan")
        
        advanced_table.add_row("🧮 Semantic Density", f"{self.metrics.semantic_density:.2f}")
        advanced_table.add_row("🔄 Token Diversity", f"{self.metrics.token_diversity:.2f}")
        advanced_table.add_row("⚡ Processing Rate", f"{self.chars_por_segundo:.1f} c/s")
        advanced_table.add_row("📊 Vocab Coverage", f"{len(self.palavras_unicas)/self.palavras:.1%}")
        
        layout["right"].update(Panel(
            advanced_table,
            title=f"{EMOJI['stats']} Advanced Metrics",
            border_style="red"
        ))
        
        # Footer com progresso e status
        tempo_decorrido = time.time() - self.inicio
        layout["footer"].update(Panel(
            Align.center(
                Text.assemble(
                    (f"⏱️ Tempo: {tempo_decorrido:.1f}s ", "yellow"),
                    (f"| 💾 Buffer: {len(self.buffer)} chars ", "cyan"),
                    (f"| 🔄 Taxa: {self.palavras_por_segundo:.1f} w/s", "green")
                )
            ),
            style="blue"
        ))
        
        return layout

    def atualizar(self, novo_texto: str):
        self.buffer += novo_texto
        self.caracteres += len(novo_texto)
        
        palavras = word_tokenize(novo_texto)
        self.palavras += len(palavras)
        
        # Atualizar métricas avançadas
        self.calcular_metricas_avancadas(novo_texto)
        
        for palavra in palavras:
            self.ultimas_palavras.append(palavra)
            self.palavras_unicas.add(palavra)
            
            if not palavra in [p[1] for p in self.maiores_palavras]:
                self.maiores_palavras.append((len(palavra), palavra))
                self.maiores_palavras.sort(reverse=True)
                self.maiores_palavras = self.maiores_palavras[:10]
        
        tempo_atual = time.time()
        delta_tempo = tempo_atual - self.ultima_atualizacao
        if delta_tempo >= 1:
            self.chars_por_segundo = self.caracteres / (tempo_atual - self.inicio)
            self.palavras_por_segundo = self.palavras / (tempo_atual - self.inicio)
            self.ultima_atualizacao = tempo_atual

async def get_gemini_response_stream(prompt, stats: StreamStats, arquivo_yaml, iteracao, total):
    try:
        model = genai.GenerativeModel(
            model_name=NOME_MODELO,
            generation_config=CONFIG_GERACAO
        )
        
        response = await model.generate_content_async(
            prompt,
            stream=True,
            generation_config=CONFIG_GERACAO
        )
        
        with Live(
            stats.criar_grid_layout(),
            refresh_per_second=4,
            vertical_overflow="visible"
        ) as live:
            async for chunk in response:
                texto = chunk.text
                stats.atualizar(texto)
                
                with open(arquivo_yaml, 'a', encoding='utf-8') as f:
                    f.write(texto)
                
                live.update(stats.criar_grid_layout())
                
        return True
    except Exception as e:
        console.print(f"[red]Erro no streaming: {str(e)}[/red]")
        return False

async def processar_iteracoes(palavra_inicial):
    total_iteracoes = 20
    
    console.print(Panel.fit(
        f"{EMOJI['stream']} [bold cyan]Gerando {total_iteracoes} YAMLs a partir de: '{palavra_inicial}'[/bold cyan]",
        border_style="cyan"
    ))
    
    for i in range(total_iteracoes):
        # Inicializar estatísticas para cada iteração
        stats = StreamStats()
        
        # Criar arquivo YAML
        output_dir = Path("generated-yaml-text-to-embedding")
        output_dir.mkdir(exist_ok=True)
        
        hash_id = hashlib.md5(f"{datetime.now().timestamp()}_{i}".encode()).hexdigest()[:10]
        arquivo_yaml = output_dir / f"embedding_stream_v1_{hash_id}.yaml"
        
        # Template do prompt
        prompt = f"""
        responda bem longo altamente completo a lista e abrangente o maximo de palavras possivel para a palavra chave '{palavra_inicial}'
        Baseado na palavra-chave '{palavra_inicial}', gere um YAML técnico e detalhado para embeddings.
        O YAML deve incluir:
        - Palavras-chave relacionadas
        - Sinônimos e variações
        - Contextos de uso
        - Métricas e parâmetros
        - Configurações técnicas
        
        Formate o YAML de forma estruturada e hierárquica.
        Iteração atual: {i+1} de {total_iteracoes}
        """
        
        console.print(f"\n{EMOJI['processando']} [cyan]Iniciando iteração {i+1}/{total_iteracoes}...[/cyan]")
        
        await get_gemini_response_stream(prompt, stats, arquivo_yaml, i+1, total_iteracoes)
        
        # Estatísticas da iteração
        tempo_total = time.time() - stats.inicio
        console.print(Panel(
            f"[green]✨ Iteração {i+1} concluída![/green]\n"
            f"Tempo: {tempo_total:.2f}s\n"
            f"Arquivo: {arquivo_yaml}",
            border_style="green"
        ))
        
        # Pequena pausa entre iterações
        await asyncio.sleep(2)

async def main():
    try:
        # Solicitar palavra inicial
        console.print(f"\n{EMOJI['palavra']} [cyan]Digite a palavra inicial para gerar os YAMLs:[/cyan]")
        palavra_inicial = input().strip()
        
        if not palavra_inicial:
            console.print("[red]Palavra inicial não pode estar vazia![/red]")
            return
        
        await processar_iteracoes(palavra_inicial)
        
        console.print(Panel(
            f"[green]🎉 Processo completo![/green]\n"
            f"20 YAMLs foram gerados com sucesso!",
            border_style="green"
        ))
        
    except Exception as e:
        console.print(f"[red]Erro durante o processamento: {str(e)}[/red]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Operação cancelada pelo usuário.[/yellow]")
    except Exception as e:
        console.print(f"[red]Erro inesperado: {str(e)}[/red]")
