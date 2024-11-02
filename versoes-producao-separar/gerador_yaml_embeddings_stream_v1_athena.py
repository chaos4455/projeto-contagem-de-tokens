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

    def atualizar(self, novo_texto: str, iteracao: int = 0, arquivo: str = ""):
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
            
            # Processa tokens BERT
            if self.metrics.bert_tokenizer:
                tokens = self.metrics.bert_tokenizer.tokenize(novo_texto)
                self.tokens_bert += len(tokens)
                self.token_unicos.update(tokens)
            
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
            self.tokens_por_segundo = self.tokens_bert / tempo_total if self.tokens_bert > 0 else 0
            
            # Calcula token ratio
            self.token_ratio = len(self.token_unicos) / max(1, self.tokens_bert)
            
            # Atualiza métricas avançadas
            self.calcular_metricas_avancadas(novo_texto)
            
        except Exception as e:
            console.print(f"[yellow]Erro ao atualizar estatísticas: {e}[/yellow]")

    def calcular_metricas_avancadas(self, texto: str):
        try:
            if not texto.strip():
                return
                
            # Tokenização BERT
            if self.metrics.bert_tokenizer:
                tokens = self.metrics.bert_tokenizer.tokenize(texto)
                for token in tokens:
                    self.metrics.token_frequency[token] = self.metrics.token_frequency.get(token, 0) + 1
            
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
            
            # Divisão principal: header, main (6 colunas) e footer
            layout.split_column(
                Layout(name="header", size=3),
                Layout(name="main", size=30),
                Layout(name="footer", size=3)
            )
            
            # Dividir main em 6 colunas
            layout["main"].split_row(
                Layout(name="system", ratio=1),      # Sistema
                Layout(name="process", ratio=1),     # Processamento
                Layout(name="tokens", ratio=1),      # Tokens
                Layout(name="words", ratio=1),       # Análise de Palavras
                Layout(name="stats", ratio=1),       # Estatísticas
                Layout(name="tops", ratio=1)         # Tops e Rankings
            )

            # Header com informações da iteração atual
            header = Panel(
                Align.center(
                    Text.assemble(
                        (f"🔄 Iteração: {self.iteracao_atual}/{self.total_iteracoes} ", "bold cyan"),
                        (f"| ⏱️ {tempo_formatado} ", "yellow"),
                        (f"| 📝 Último YAML: {self.ultimo_arquivo} ", "green"),
                        (f"| 💾 Total: {self.caracteres:,} chars", "blue")
                    )
                ),
                border_style="blue",
                box=ROUNDED
            )
            layout["header"].update(header)

            # 1. Coluna Sistema
            system_table = Table(box=ROUNDED, expand=True)
            system_table.add_column("💻 Sistema", style="cyan")
            system_table.add_column("Valor", justify="right", style="green")
            
            system_table.add_row("🖥️ CPU Total", f"{self.cpu_total}%")
            for i, cpu in enumerate(self.cpu_cores):
                system_table.add_row(f"Core {i+1}", f"{cpu}%")
            system_table.add_row("🧠 RAM", f"{self.ram.percent}%")
            system_table.add_row("💾 Disco", f"{self.disk.percent}%")
            
            layout["system"].update(Panel(system_table, title="Sistema", border_style="blue"))

            # 2. Coluna Processamento
            process_table = Table(box=ROUNDED, expand=True)
            process_table.add_column("⚡ Processo", style="magenta")
            process_table.add_column("Valor", justify="right", style="yellow")
            
            process_table.add_row("📊 Chars/s", f"{self.chars_por_segundo:.1f}")
            process_table.add_row("📈 Words/s", f"{self.palavras_por_segundo:.1f}")
            process_table.add_row("💾 KB/s", f"{(self.chars_por_segundo/1024):.1f}")
            process_table.add_row("🚀 MB Total", f"{(self.caracteres/1024/1024):.2f}")
            
            layout["process"].update(Panel(process_table, title="Processamento", border_style="magenta"))

            # 3. Coluna Tokens
            tokens_table = Table(box=ROUNDED, expand=True)
            tokens_table.add_column("🎯 Tokens", style="blue")
            tokens_table.add_column("Valor", justify="right", style="cyan")
            
            tokens_table.add_row("📊 Total BERT", f"{self.tokens_bert:,}")
            tokens_table.add_row("🔄 Tokens/s", f"{self.tokens_por_segundo:.1f}")
            tokens_table.add_row("📈 Únicos", f"{len(self.token_unicos):,}")
            tokens_table.add_row("💫 Token Ratio", f"{self.token_ratio:.2%}")
            
            layout["tokens"].update(Panel(tokens_table, title="Tokens BERT", border_style="cyan"))

            # 4. Coluna Análise de Palavras
            words_table = Table(box=ROUNDED, expand=True)
            words_table.add_column("📝 Palavras", style="yellow")
            words_table.add_column("Valor", justify="right", style="green")
            
            words_table.add_row("📚 Total", f"{self.palavras:,}")
            words_table.add_row("🎯 Únicas", f"{len(self.palavras_unicas):,}")
            words_table.add_row("📊 Média Len", f"{self.media_tamanho_palavras:.1f}")
            words_table.add_row("💫 Diversidade", f"{self.diversidade_lexica:.1%}")
            
            layout["words"].update(Panel(words_table, title="Análise", border_style="yellow"))

            # 5. Coluna Estatísticas
            stats_table = Table(box=ROUNDED, expand=True)
            stats_table.add_column("📊 Stats", style="red")
            stats_table.add_column("Valor", justify="right", style="blue")
            
            # Últimas 10 palavras únicas
            ultimas_unicas = list(self.palavras_unicas)[-10:] if self.palavras_unicas else []
            for palavra in ultimas_unicas:
                stats_table.add_row("📝", palavra)
            
            layout["stats"].update(Panel(stats_table, title="Últimas Únicas", border_style="red"))

            # 6. Coluna Tops
            tops_table = Table(box=ROUNDED, expand=True)
            tops_table.add_column("🏆 Tops", style="green")
            tops_table.add_column("Valor", justify="right", style="magenta")
            
            # Top 10 maiores palavras
            for tamanho, palavra in sorted(self.maiores_palavras, reverse=True)[:10]:
                tops_table.add_row("📏", f"{palavra} ({tamanho})")
            
            layout["tops"].update(Panel(tops_table, title="Maiores Palavras", border_style="green"))

            # Footer com totalizadores
            footer = Panel(
                Align.center(
                    Text.assemble(
                        (f"📊 Palavras: {self.palavras:,} ", "cyan"),
                        (f"| 🎯 Únicas: {len(self.palavras_unicas):,} ", "yellow"),
                        (f"| 📈 Tokens: {self.tokens_bert:,} ", "green"),
                        (f"| ⚡ Chars/s: {self.chars_por_segundo:.1f}", "blue")
                    )
                ),
                border_style="blue",
                box=SIMPLE
            )
            layout["footer"].update(footer)

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
            auto_refresh=False,
            screen=True,
            # Reduzir a frequência de atualização
            refresh_per_second=2,
            transient=True,  # Alterado para True
            vertical_overflow="visible"
        )

    async def processar_iteracoes(self, palavra_inicial):
        total_iteracoes = 20
        
        with self.live:
            # Removido o console.clear() aqui
            for i in range(total_iteracoes):
                try:
                    # Removido o console.clear() e console.print do cabeçalho
                    self.stats = StreamStats()
                    
                    # Configuração do arquivo
                    output_dir = Path("generated-yaml-text-to-embedding")
                    output_dir.mkdir(exist_ok=True)
                    
                    hash_id = hashlib.md5(f"{datetime.now().timestamp()}_{i}".encode()).hexdigest()[:10]
                    arquivo_yaml = output_dir / f"embedding_stream_v1_{hash_id}.yaml"
                    
                    # Template do prompt
                    prompt = f"""
                    Baseado na palavra-chave '{palavra_inicial}', gere um YAML técnico e detalhado.
                    
        inicia a listra de palavra depois do topico lista_palavras no yaml
        crie o mais longo completo e detalhado possivel, com o maximo de palavras possivel, referentes ao tema.
        
        Gere um YAML técnico e detalhado para embeddings com:
1 palavra por linha, 1 palavra chave por linha, o maximo de palavras possivel, referentes a palavra chave.
        use tecnicas de semanticas e verossimilhança para gerar o vocabulario.
        use as tecnicas de maximo verossimilhança para gerar o vocabulario.
        use a linguagem mais tecnica possivel.
        use a tecnica de tokenizacao wordpiece.
        use a tecnica de stemming.
        use a tecnica de lematizacao.
        use a tecnica de remocao de stopwords.
        use a tecnica de normalizacao de texto.
        Seja extremamente técnico e específico.

crie o mais longo completo e detalhado possivel, com o maximo de palavras possivel, referentes ao tema.
                 inicia a listra de palavra depois do topico lista_palavras no yaml
        
                Objetivo: Gerar yaml com listra de palavras que depois serão usadas em tecnicas de embedding e vocabulário relacionado para machine learning para criar vetores de embeedings
                
                    Iteração: {i+1}/{total_iteracoes}
                    """
                    
                    # Processa resposta do Gemini
                    await self.get_gemini_response_stream(prompt, arquivo_yaml)
                    
                    # Atualiza display com menor frequência
                    if i % 2 == 0:  # Atualiza a cada 2 iterações
                        self.live.update(self.stats.criar_grid_layout(), refresh=True)
                    
                    # Aumentado o intervalo entre iterações
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    self.console.print(f"[red]Erro na iteração {i+1}: {str(e)}[/red]")

    async def get_gemini_response_stream(self, prompt, arquivo_yaml):
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
            
            async for chunk in response:
                texto = chunk.text
                self.stats.atualizar(texto)
                
                with open(arquivo_yaml, 'a', encoding='utf-8') as f:
                    f.write(texto)
                
                # Atualiza o display com menos frequência
                if len(texto) > 100:  # Só atualiza quando tiver conteúdo substancial
                    self.live.update(self.stats.criar_grid_layout(), refresh=True)
                
            return True
            
        except Exception as e:
            self.console.print(f"[red]Erro no streaming: {str(e)}[/red]")
            return False

async def main():
    try:
        processor = StreamProcessor()
        
        # Solicita palavra inicial
        console.print(f"\n{EMOJI['palavra']} [cyan]Digite a palavra inicial:[/cyan]")
        palavra_inicial = input().strip()
        
        if not palavra_inicial:
            console.print("[red]Palavra inicial não pode estar vazia![/red]")
            return
            
        # Limpa a tela antes de começar
        console.clear()
        
        # Inicia processamento
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
