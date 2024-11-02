import yaml
import hashlib
from datetime import datetime, timedelta
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
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from rich.text import Text
from rich.box import ROUNDED, HEAVY, SIMPLE  # Importação correta dos boxes
from psutil import cpu_percent, virtual_memory, disk_usage
import platform
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Thread
import multiprocessing
from functools import partial
from dataclasses import dataclass
from collections import defaultdict
import aiofiles
from contextlib import suppress

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
    "arquivo": "🗂",
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

# Configurações Globais
TOKEN_COUNTER = True  # Define se a análise de tokens BERT será realizada (True/False)

@dataclass
class TokenBatch:
    """Estrutura para batch de tokens"""
    text: str
    timestamp: float
    batch_id: int

class BertProcessor:
    """Processador BERT Multi-threaded"""
    def __init__(self, num_threads: int = 4):
        self.num_threads = num_threads
        self.input_queue = asyncio.Queue()
        self.output_queue = asyncio.Queue()
        self.token_stats = defaultdict(int)
        self.batch_size = 32
        self.executor = ThreadPoolExecutor(max_workers=num_threads)
        self.bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.processing = True
        self.stats_lock = asyncio.Lock()
        self.batch_buffer = []
        
    async def process_batch(self, batch: List[TokenBatch]):
        """Processa um batch de textos"""
        try:
            # Tokenização paralela
            texts = [b.text for b in batch]
            
            def tokenize_text(text):
                tokens = self.bert_tokenizer.tokenize(text)
                ids = self.bert_tokenizer.convert_tokens_to_ids(tokens)
                return tokens, ids
            
            # Executa tokenização em threads
            results = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                lambda: list(map(tokenize_text, texts))
            )
            
            # Processa resultados
            async with self.stats_lock:
                for (tokens, ids), batch_item in zip(results, batch):
                    stats = {
                        'num_tokens': len(tokens),
                        'unique_tokens': len(set(tokens)),
                        'subwords': sum(1 for t in tokens if t.startswith('##')),
                        'special': sum(1 for t in tokens if t in self.bert_tokenizer.special_tokens_map.values()),
                        'max_len': max(len(t) for t in tokens) if tokens else 0,
                        'avg_len': np.mean([len(t) for t in tokens]) if tokens else 0
                    }
                    
                    # Atualiza estatísticas globais
                    for k, v in stats.items():
                        self.token_stats[k] += v
                    
                    # Atualiza frequências
                    for token in tokens:
                        self.token_stats[f'freq_{token}'] += 1
                    
                    # Coloca resultado na fila de saída
                    await self.output_queue.put((batch_item.batch_id, stats))
            
        except Exception as e:
            console.print(f"[red]Erro no processamento do batch: {e}[/red]")

    async def process_queue(self):
        """Processa a fila de entrada"""
        while self.processing:
            try:
                # Coleta batch
                self.batch_buffer = []
                while len(self.batch_buffer) < self.batch_size:
                    try:
                        item = await asyncio.wait_for(self.input_queue.get(), timeout=0.1)
                        self.batch_buffer.append(item)
                    except asyncio.TimeoutError:
                        break
                
                if self.batch_buffer:
                    await self.process_batch(self.batch_buffer)
                    
            except Exception as e:
                console.print(f"[red]Erro no processamento da fila: {e}[/red]")
                await asyncio.sleep(0.1)

class AdvancedMetrics:
    def __init__(self):
        try:
            self.bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            console.print(f"[yellow]Aviso: Usando fallback para tokenização: {str(e)}[/yellow]")
            self.bert_tokenizer = None
            self.sentence_model = None
            
        self.embedding_dim = 384
        self.embedding_cache = {}
        self.token_frequency = {}
        self.sentence_lengths = []
        self.embedding_magnitudes = []
        self.token_diversity = 0.0
        self.semantic_density = 0.0
        self.cpu_usage = 0.0
        self.memory_usage = 0.0
        self.gpu_usage = 0.0

class SystemMonitor:
    """Monitora recursos do sistema com fallbacks"""
    def __init__(self):
        self.os_type = platform.system()
        self.fallback_mode = False
        
        # Tenta inicializar contadores
        try:
            self.cpu_percent = psutil.cpu_percent(interval=0.1)
            self.cpu_per_core = psutil.cpu_percent(percpu=True)
        except Exception as e:
            console.print(f"[yellow]⚠️ Usando modo fallback para métricas de CPU[/yellow]")
            self.fallback_mode = True

    def get_cpu_stats(self):
        """Obtém estatísticas de CPU com fallback"""
        try:
            if self.fallback_mode:
                # Fallback usando /proc no Linux ou wmic no Windows
                if self.os_type == "Linux":
                    with open('/proc/stat', 'r') as f:
                        cpu_lines = f.readlines()
                    return {
                        'total': float(cpu_lines[0].split()[1]),
                        'cores': [float(line.split()[1]) for line in cpu_lines[1:] if line.startswith('cpu')]
                    }
                else:
                    # Windows fallback
                    return {
                        'total': os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0,
                        'cores': [0] * psutil.cpu_count()
                    }
            else:
                return {
                    'total': psutil.cpu_percent(interval=0.1),
                    'cores': psutil.cpu_percent(percpu=True)
                }
        except Exception:
            return {'total': 0, 'cores': [0] * psutil.cpu_count()}

    def get_memory_stats(self):
        """Obtém estatísticas de memória com fallback"""
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            return {
                'used': mem.used,
                'total': mem.total,
                'percent': mem.percent,
                'swap_percent': swap.percent
            }
        except Exception:
            return {
                'used': 0,
                'total': 0,
                'percent': 0,
                'swap_percent': 0
            }

class StreamStats:
    def __init__(self):
        self.metrics = AdvancedMetrics()
        # Contadores básicos
        self.caracteres = 0
        self.palavras = 0
        self.tokens_bert = 0
        self.palavras_unicas = set()
        self.token_unicos = set()
        self.maiores_palavras = []
        self.ultimas_palavras = deque(maxlen=10)
        self.inicio = time.time()
        self.chars_por_segundo = 0
        self.palavras_por_segundo = 0
        self.tokens_por_segundo = 0
        self.buffer = ""
        
        # Controle de iteração
        self.iteracao_atual = 0
        self.total_iteracoes = 20
        self.ultimo_arquivo = ""
        
        # Métricas calculadas
        self.media_tamanho_palavras = 0
        self.diversidade_lexica = 0
        self.token_ratio = 0
        
        # Inicializa métricas do sistema
        self.atualizar_metricas_sistema()

        # Inicialização condicional do tokenizador BERT
        self.bert_enabled = TOKEN_COUNTER
        if self.bert_enabled:
            try:
                console.print("[cyan]🎯 Token Counter: ATIVADO - Iniciando BERT...[/cyan]")
                self.bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
                self.tokens_bert = 0
                self.token_unicos = set()
                self.token_frequency = {}
                self.tokens_por_segundo = 0
                self.token_stats = {
                    'media_len': 0,
                    'max_len': 0,
                    'subwords_ratio': 0,
                    'special_tokens': 0
                }
                console.print("[green]✅ BERT inicializado com sucesso![/green]")
            except Exception as e:
                console.print(f"[yellow]⚠️ Aviso: Erro ao inicializar BERT: {e}[/yellow]")
                self.bert_tokenizer = None
        else:
            console.print("[yellow]⚠️ Token Counter: DESATIVADO - BERT não será utilizado[/yellow]")
            self.bert_tokenizer = None

        # Inicialização do processador BERT multi-thread
        if TOKEN_COUNTER:
            self.bert_processor = BertProcessor(num_threads=4)
            self.batch_id = 0
            self.pending_results = {}
            asyncio.create_task(self.bert_processor.process_queue())
            console.print("[green]🚀 BERT Multi-threaded inicializado![/green]")

        self.system_monitor = SystemMonitor()

        # Adicionar atributos faltantes
        self.sentences = []
        self.embedding_stats = {
            'min_magnitude': 0,
            'max_magnitude': 0,
            'avg_magnitude': 0
        }
        self.top_tokens = []  # Lista para os tokens mais frequentes
        self.eficiencia_tokens = 0.0
        self.cobertura_vocab = 0.0
        self.densidade_texto = 0.0
        self.performance_score = 0.0

    def safe_div(self, n, d):
        """Divisão segura com valor default 0"""
        try:
            if d == 0:
                return 0.0
            result = float(n) / float(d)
            return result if result != float('inf') else 0.0
        except:
            return 0.0

    def safe_mean(self, values):
        """Média segura com verificações"""
        try:
            cleaned_values = [float(v) for v in values if v is not None and str(v).strip()]
            return np.mean(cleaned_values) if cleaned_values else 0.0
        except:
            return 0.0

    async def atualizar(self, novo_texto: str, iteracao: int = 0, arquivo: str = ""):
        """Atualiza estatísticas com novo texto"""
        try:
            if not novo_texto:
                return
                
            # Atualiza controle de iteração
            self.iteracao_atual = iteracao
            if arquivo:
                self.ultimo_arquivo = Path(arquivo).name
            
            # Atualiza contadores básicos
            self.buffer += novo_texto
            self.caracteres += len(novo_texto)
            
            # Processa palavras
            palavras = word_tokenize(novo_texto)
            self.palavras += len(palavras)
            
            for palavra in palavras:
                if palavra.strip():
                    self.palavras_unicas.add(palavra)
                    self.ultimas_palavras.append(palavra)
                    
                    # Atualiza maiores palavras
                    if not palavra in [p[1] for p in self.maiores_palavras]:
                        self.maiores_palavras.append((len(palavra), palavra))
                        self.maiores_palavras.sort(reverse=True)
                        self.maiores_palavras = self.maiores_palavras[:10]
            
            # Atualiza métricas calculadas
            tempo_total = max(0.001, time.time() - self.inicio)
            self.chars_por_segundo = self.caracteres / tempo_total
            self.palavras_por_segundo = self.palavras / tempo_total
            self.tokens_por_segundo = self.tokens_bert / tempo_total
            
            # Calcula médias e ratios
            if self.palavras > 0:
                tamanhos = [len(p) for p in self.palavras_unicas]
                self.media_tamanho_palavras = sum(tamanhos) / len(tamanhos) if tamanhos else 0
                self.diversidade_lexica = len(self.palavras_unicas) / self.palavras
                
            if self.tokens_bert > 0:
                self.token_ratio = len(self.token_unicos) / self.tokens_bert
            
            # Atualiza métricas do sistema
            self.atualizar_metricas_sistema()
            
            # Processamento BERT assíncrono
            await self.processar_tokens_bert(novo_texto)
            
        except Exception as e:
            console.print(f"[yellow]Erro ao atualizar estatísticas: {e}[/yellow]")

    async def processar_tokens_bert(self, texto: str):
        """Processa tokens BERT de forma assíncrona"""
        if not TOKEN_COUNTER or not self.bert_processor:
            return
            
        try:
            # Cria batch
            batch = TokenBatch(
                text=texto,
                timestamp=time.time(),
                batch_id=self.batch_id
            )
            self.batch_id += 1
            
            # Adiciona à fila de processamento
            await self.bert_processor.input_queue.put(batch)
            
            # Processa resultados disponíveis
            while not self.bert_processor.output_queue.empty():
                batch_id, stats = await self.bert_processor.output_queue.get()
                self.atualizar_estatisticas_bert(stats)
                
        except Exception as e:
            console.print(f"[yellow]Erro ao processar tokens BERT: {e}[/yellow]")

    def atualizar_estatisticas_bert(self, stats: Dict):
        """Atualiza estatísticas do BERT"""
        try:
            self.tokens_bert += stats['num_tokens']
            self.token_stats['media_len'] = stats['avg_len']
            self.token_stats['max_len'] = max(self.token_stats['max_len'], stats['max_len'])
            self.token_stats['subwords_ratio'] = stats['subwords'] / max(1, stats['num_tokens'])
            self.token_stats['special_tokens'] += stats['special']
            
            # Atualiza taxa de processamento
            tempo_total = max(0.001, time.time() - self.inicio)
            self.tokens_por_segundo = self.tokens_bert / tempo_total
            
        except Exception as e:
            console.print(f"[yellow]Erro ao atualizar estatísticas BERT: {e}[/yellow]")

    def calcular_metricas_avancadas(self, texto: str):
        try:
            if not texto.strip():
                return
                
            # Tokenização segura
            if self.metrics.bert_tokenizer:
                tokens_bert = self.metrics.bert_tokenizer.tokenize(texto)
                self.tokens_bert = max(1, self.tokens_bert + len(tokens_bert))
            
            # Análise de sentenças
            sentences = nltk.sent_tokenize(texto)
            if sentences:
                self.sentences.extend(sentences)
            
            # Embeddings seguros
            if self.metrics.sentence_model and texto.strip():
                try:
                    embedding = self.metrics.sentence_model.encode(texto)
                    magnitude = float(np.linalg.norm(embedding))
                    
                    if not np.isnan(magnitude) and magnitude > 0:
                        self.metrics.embedding_magnitudes.append(magnitude)
                        
                        # Atualizar estatísticas
                        mags = [m for m in self.metrics.embedding_magnitudes if m > 0]
                        if mags:
                            self.embedding_stats['min_magnitude'] = min(mags)
                            self.embedding_stats['max_magnitude'] = max(mags)
                            self.embedding_stats['avg_magnitude'] = self.safe_mean(mags)
                except:
                    pass
            
            # Métricas de sistema
            try:
                self.metrics.cpu_usage = psutil.cpu_percent()
                self.metrics.memory_usage = psutil.virtual_memory().percent
                if len(GPUtil.getGPUs()) > 0:
                    self.metrics.gpu_usage = GPUtil.getGPUs()[0].load * 100
            except:
                pass
                
        except Exception as e:
            console.print(f"[yellow]Aviso em métricas avançadas: {str(e)}[/yellow]")

    def atualizar_metricas_sistema(self):
        """Atualiza métricas do sistema"""
        try:
            self.cpu_total = psutil.cpu_percent()
            self.cpu_cores = psutil.cpu_percent(percpu=True)
            self.ram = psutil.virtual_memory()
            self.disk = psutil.disk_usage('/')
        except Exception as e:
            console.print(f"[yellow]Erro ao atualizar métricas do sistema: {e}[/yellow]")

    def formatar_tempo(self, segundos):
        """Formata segundos em HH:MM:SS"""
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        segs = int(segundos % 60)
        return f"{horas:02d}:{minutos:02d}:{segs:02d}"

    def criar_grid_layout(self):
        try:
            tempo_atual = time.time()
            tempo_total = max(0.001, tempo_atual - self.inicio)
            tempo_formatado = str(timedelta(seconds=int(tempo_total)))

            layout = Layout()
            layout.split_column(
                Layout(name="header", size=3),
                Layout(name="main", size=30),
                Layout(name="footer", size=3)
            )

            # Header com métricas de processamento
            header = Panel(
                Align.center(
                    Text.assemble(
                        (f"🚀 Multi-Thread BERT ", "bold cyan"),
                        (f"| ⚡ Threads: {self.bert_processor.num_threads} ", "green"),
                        (f"| 📦 Batch: {len(self.bert_processor.batch_buffer)}/{self.bert_processor.batch_size} ", "yellow"),
                        (f"| 🔄 Queue: {self.bert_processor.input_queue.qsize()} ", "blue"),
                        (f"| ⏱️ {tempo_formatado}", "magenta")
                    )
                ),
                border_style="blue",
                box=ROUNDED
            )
            layout["header"].update(header)

            # 6 colunas para métricas
            layout["main"].split_row(
                Layout(name="system", ratio=1),
                Layout(name="process", ratio=1),
                Layout(name="tokens", ratio=1),
                Layout(name="words", ratio=1),
                Layout(name="stats", ratio=1),
                Layout(name="tops", ratio=1)
            )

            # 1. Sistema e Recursos
            system_stats = self.system_monitor.get_cpu_stats()
            memory_stats = self.system_monitor.get_memory_stats()
            
            system_table = Table(box=ROUNDED, expand=True)
            system_table.add_column("💻 Sistema", style="cyan")
            system_table.add_column("Valor", justify="right", style="green")
            
            # CPU com fallback
            system_table.add_row("🖥️ CPU Total", f"{system_stats['total']:.1f}%")
            for i, cpu in enumerate(system_stats['cores']):
                with suppress(Exception):
                    system_table.add_row(f"Core {i+1}", f"{cpu:.1f}%")
            
            # Memória com fallback
            system_table.add_row("🧠 RAM Uso", f"{memory_stats['percent']}%")
            system_table.add_row("💾 RAM Total", f"{memory_stats['total']/1024**3:.1f}GB")
            system_table.add_row("📊 RAM Livre", f"{(memory_stats['total']-memory_stats['used'])/1024**3:.1f}GB")
            
            if memory_stats['swap_percent'] > 0:
                system_table.add_row("💫 Swap", f"{memory_stats['swap_percent']}%")
            
            # Informações do sistema
            system_table.add_row("🔧 Sistema", platform.system())
            system_table.add_row("📌 Python", platform.python_version())
            
            if self.system_monitor.fallback_mode:
                system_table.add_row("⚠️ Modo", "Fallback", style="yellow")
            
            layout["system"].update(Panel(
                system_table,
                title="💻 Sistema" + (" (Fallback)" if self.system_monitor.fallback_mode else ""),
                border_style="blue"
            ))

            # 2. Processamento
            process_table = Table(box=ROUNDED, expand=True)
            process_table.add_column("⚡ Processo", style="magenta")
            process_table.add_column("Valor", justify="right", style="yellow")
            
            process_table.add_row("📝 Iteração", f"{self.iteracao_atual}/{self.total_iteracoes}")
            process_table.add_row("⏱️ Tempo", tempo_formatado)
            process_table.add_row("📊 Chars/s", f"{self.chars_por_segundo:.1f}")
            process_table.add_row("🚀 Words/s", f"{self.palavras_por_segundo:.1f}")
            process_table.add_row("💾 Buffer", f"{len(self.buffer):,}")
            process_table.add_row("📈 Total KB", f"{self.caracteres/1024:.1f}")
            
            layout["process"].update(Panel(process_table, title="⚡ Processamento", border_style="magenta"))

            # 3. Tokens BERT
            tokens_table = Table(box=ROUNDED, expand=True)
            tokens_table.add_column("🎯 Tokens", style="blue")
            tokens_table.add_column("Valor", justify="right", style="cyan")
            
            tokens_table.add_row("📊 Total", f"{self.tokens_bert:,}")
            tokens_table.add_row("🔄 Por Seg", f"{self.tokens_por_segundo:.1f}")
            tokens_table.add_row("📈 Únicos", f"{len(self.token_unicos):,}")
            tokens_table.add_row("🎯 Ratio", f"{self.token_stats['subwords_ratio']:.1%}")
            tokens_table.add_row("📏 Média Len", f"{self.token_stats['media_len']:.1f}")
            tokens_table.add_row("⚡ Especiais", f"{self.token_stats['special_tokens']}")
            
            # Top 5 tokens mais frequentes
            tokens_table.add_row("📈 TOP TOKENS", "", style="bold magenta")
            for token, freq in self.top_tokens[:5]:
                tokens_table.add_row("🔤", f"{token} ({freq})")
            
            layout["tokens"].update(Panel(tokens_table, title="🎯 Tokens BERT", border_style="cyan"))

            # 4. Análise de Palavras
            words_table = Table(box=ROUNDED, expand=True)
            words_table.add_column("📝 Palavras", style="yellow")
            words_table.add_column("Valor", justify="right", style="green")
            
            words_table.add_row("📚 Total", f"{self.palavras:,}")
            words_table.add_row("🎯 Únicas", f"{len(self.palavras_unicas):,}")
            words_table.add_row("📊 Média Len", f"{self.media_tamanho_palavras:.1f}")
            words_table.add_row("💫 Diversidade", f"{self.diversidade_lexica:.1%}")
            
            # Últimas 10 palavras
            words_table.add_row("📝 ÚLTIMAS", "", style="bold cyan")
            for palavra in list(self.ultimas_palavras)[-10:]:
                words_table.add_row("📖", palavra)
            
            layout["words"].update(Panel(words_table, title="📝 Análise", border_style="yellow"))

            # 5. Estatísticas
            stats_table = Table(box=ROUNDED, expand=True)
            stats_table.add_column("📊 Stats", style="red")
            stats_table.add_column("Valor", justify="right", style="blue")
            
            stats_table.add_row("🎯 Eficiência", f"{self.eficiencia_tokens:.1%}")
            stats_table.add_row("📈 Cobertura", f"{self.cobertura_vocab:.1%}")
            stats_table.add_row("💫 Densidade", f"{self.densidade_texto:.2f}")
            stats_table.add_row("⚡ Performance", f"{self.performance_score:.1f}")
            
            layout["stats"].update(Panel(stats_table, title="📊 Estatísticas", border_style="red"))

            # 6. Tops e Rankings
            tops_table = Table(box=ROUNDED, expand=True)
            tops_table.add_column("🏆 Tops", style="green")
            tops_table.add_column("Valor", justify="right", style="magenta")
            
            # Top 10 maiores palavras
            tops_table.add_row("📏 MAIORES", "", style="bold yellow")
            for tamanho, palavra in sorted(self.maiores_palavras, reverse=True)[:10]:
                tops_table.add_row("📏", f"{palavra} ({tamanho})")
            
            layout["tops"].update(Panel(tops_table, title="🏆 Rankings", border_style="green"))

            return layout

        except Exception as e:
            console.print(f"[yellow]Aviso no layout: {str(e)}[/yellow]")
            return Layout()

class StreamProcessor:
    def __init__(self):
        self.console = Console()
        self.stats = StreamStats()
        self.live = Live(
            self.stats.criar_grid_layout(),
            console=self.console,
            auto_refresh=True,
            refresh_per_second=10,
            screen=True
        )

    async def processar_yaml(self, prompt: str, arquivo_yaml: Path, iteracao: int, total: int):
        """Processa um único YAML com atualizações em tempo real"""
        try:
            self.stats.iteracao_atual = iteracao
            self.stats.total_iteracoes = total
            
            # Inicializa o modelo
            model = genai.GenerativeModel(
                model_name=NOME_MODELO,
                generation_config=CONFIG_GERACAO
            )

            # Gera o conteúdo de forma síncrona
            response = model.generate_content(prompt, stream=True)
            
            # Processa o stream
            async with aiofiles.open(arquivo_yaml, 'w', encoding='utf-8') as f:
                async for chunk in response:
                    if chunk.text:
                        texto = chunk.text
                        # Atualiza estatísticas (BERT em thread separada)
                        await self.stats.atualizar(texto, iteracao, arquivo_yaml.name)
                        # Escreve no arquivo
                        await f.write(texto)
                        # Atualiza display
                        self.live.update(self.stats.criar_grid_layout())

            return True

        except Exception as e:
            self.console.print(f"[red]Erro ao processar YAML {iteracao}: {str(e)}[/red]")
            return False

    async def processar_iteracoes(self, palavra_inicial: str):
        """Processa todas as iterações com display em tempo real"""
        total_iteracoes = 20
        
        with self.live:
            self.console.clear()
            
            for i in range(total_iteracoes):
                try:
                    # Prepara diretório e arquivo
                    output_dir = Path("generated-yaml-text-to-embedding")
                    output_dir.mkdir(exist_ok=True)
                    
                    hash_id = hashlib.md5(f"{datetime.now().timestamp()}_{i}".encode()).hexdigest()[:10]
                    arquivo_yaml = output_dir / f"embedding_stream_v1_{hash_id}.yaml"
                    
                    # Template do prompt
                    prompt = f"""
                    Baseado na palavra-chave '{palavra_inicial}', gere um YAML técnico e detalhado.
                    Iteração: {i+1}/{total_iteracoes}
                    """
                    
                    # Processa YAML
                    await self.processar_yaml(prompt, arquivo_yaml, i+1, total_iteracoes)
                    
                    # Pausa entre iterações
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    self.console.print(f"[red]Erro na iteração {i+1}: {str(e)}[/red]")

async def main():
    try:
        processor = StreamProcessor()
        
        # Solicita palavra inicial
        console.print(f"\n{EMOJI['palavra']} [cyan]Digite a palavra inicial:[/cyan]")
        palavra_inicial = input().strip()
        
        if not palavra_inicial:
            console.print("[red]Palavra inicial não pode estar vazia![/red]")
            return
        
        # Limpa console e inicia processamento
        console.clear()
        await processor.processar_iteracoes(palavra_inicial)
        
        # Mensagem final
        console.print(Panel(
            f"[green]🎉 Processo completo![/green]\n"
            f"20 YAMLs foram gerados com sucesso!",
            border_style="green"
        ))
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Operação cancelada pelo usuário.[/yellow]")
    except Exception as e:
        console.print(f"[red]Erro durante o processamento: {str(e)}[/red]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Operação cancelada pelo usuário.[/yellow]")
    except Exception as e:
        console.print(f"[red]Erro inesperado: {str(e)}[/red]")
