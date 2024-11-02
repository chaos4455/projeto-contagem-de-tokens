import yaml
import torch
from transformers import BertTokenizer, BertModel
import sqlite3
import numpy as np
from pathlib import Path
from tqdm import tqdm
import re
from rich import print
from rich.console import Console
from rich.progress import track
import google.generativeai as genai
import time
from datetime import datetime
import hashlib
import pandas as pd
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import emoji
from datetime import timedelta
import asyncio
import logging
import psutil
from collections import Counter, defaultdict
from rich.align import Align

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

console = Console()

# Configuração do Gemini
GOOGLE_API_KEY = "AIzaSyCEagEEnX-RdkW3-jCAb0H9nrTsgcE-Qqo" #Substitua pela sua chave
genai.configure(api_key=GOOGLE_API_KEY)
NOME_MODELO = "gemini-1.5-flash"

class YAMLVectorizer:
    def __init__(self):
        # Inicializa BERT
        try:
            self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            self.model = BertModel.from_pretrained('bert-base-uncased')
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.model.to(self.device)
            self.model.eval()
        except Exception as e:
            logging.error(f"Erro ao inicializar BERT: {e}")
            raise RuntimeError("Falha na inicialização do modelo BERT.")

class ProcessingStats:
    def __init__(self):
        self.reset()
        
    def reset(self):
        # Métricas de Palavras
        self.total_palavras = 0
        self.palavras_processadas = 0
        self.palavras_unicas = 0
        self.palavras_repetidas = 0
        self.palavras_novas = 0
        self.palavras_existentes = 0
        self.palavras_por_segundo = 0
        self.historico_palavras = []
        
        # Métricas de Tokens
        self.total_tokens = 0
        self.tokens_unicos = 0
        self.tokens_por_palavra = 0
        self.tokens_por_segundo = 0
        self.historico_tokens = []
        self.distribuicao_tokens = defaultdict(int)
        
        # Métricas de Tempo
        self.tempo_inicio = time.time()
        self.tempo_processamento = 0
        self.tempo_ia = 0
        self.tempo_vetorizacao = 0
        self.tempo_banco = 0
        self.tempo_tokenizacao = 0
        
        # Métricas de Pipeline
        self.etapa_atual = ""
        self.sub_etapa = ""
        self.progresso_etapa = 0
        self.historico_etapas = []
        
        # Métricas de Qualidade
        self.taxa_sucesso = 0
        self.taxa_erro = 0
        self.falhas = 0
        self.erros_por_tipo = defaultdict(int)
        
        # Métricas de Vetores
        self.dimensoes_vetor = 768  # BERT default
        self.media_magnitude = 0
        self.max_magnitude = 0
        self.min_magnitude = 0
        self.densidade_vetores = 0
        
        # Estatísticas Linguísticas
        self.tamanho_medio_palavra = 0
        self.palavras_por_categoria = defaultdict(int)
        self.prefixos_comuns = Counter()
        self.sufixos_comuns = Counter()
        
        # Cache e Performance
        self.cache_hits = 0
        self.cache_misses = 0
        self.latencia_media = 0
        
        # Métricas de Sistema
        self.uso_cpu = 0
        self.uso_ram = 0
        self.threads_ativos = 0
        self.tamanho_db_mb = 0
        self.em_processamento = 0
        self.palavras_na_fila = 0
        self.precisao = 0
        
        # Novos atributos para métricas IA
        self.temperatura = 0.8
        self.top_p = 0.95
        self.tokens_por_requisicao = 0
        
        # Métricas de tempo estimado
        self.tempo_estimado_restante = 0
        
        # Cache e performance expandidos
        self.cache_hits = 0
        self.cache_misses = 0
        self.precisao = 0
        self.taxa_sucesso = 0
        
    def update_tempo(self):
        """Atualiza métricas relacionadas ao tempo"""
        tempo_atual = time.time()
        self.tempo_processamento = tempo_atual - self.tempo_inicio
        if self.palavras_processadas > 0:
            self.palavras_por_segundo = self.palavras_processadas / max(1, self.tempo_processamento)
            self.tokens_por_segundo = self.total_tokens / max(1, self.tempo_processamento)
    
    def update_system_metrics(self):
        """Atualiza métricas do sistema"""
        self.uso_cpu = psutil.cpu_percent()
        self.uso_ram = psutil.virtual_memory().percent
        self.threads_ativos = len(psutil.Process().threads())
        try:
            self.tamanho_db_mb = Path('vectors_continuo.db').stat().st_size / (1024 * 1024)
        except:
            self.tamanho_db_mb = 0
            
    def update_vector_metrics(self, vector):
        """Atualiza métricas relacionadas aos vetores"""
        if vector is not None:
            magnitude = np.linalg.norm(vector)
            self.media_magnitude = (self.media_magnitude * self.palavras_processadas + magnitude) / (self.palavras_processadas + 1)
            self.max_magnitude = max(self.max_magnitude, magnitude)
            self.min_magnitude = min(self.min_magnitude, magnitude) if self.min_magnitude > 0 else magnitude
            
    def update_bert_metrics(self, palavra):
        """Atualiza métricas relacionadas ao BERT"""
        self.tamanho_medio_palavra = ((self.tamanho_medio_palavra * (self.palavras_processadas - 1)) + len(palavra)) / self.palavras_processadas
        
        # Atualiza prefixos e sufixos comuns
        if len(palavra) > 2:
            self.prefixos_comuns[palavra[:2]] += 1
            self.sufixos_comuns[palavra[-2:]] += 1

    def registrar_etapa(self, etapa: str, sub_etapa: str = ""):
        self.etapa_atual = etapa
        self.sub_etapa = sub_etapa
        self.historico_etapas.append({
            'etapa': etapa,
            'sub_etapa': sub_etapa,
            'timestamp': datetime.now(),
            'metricas': self.get_snapshot()
        })
        
    def get_snapshot(self):
        return {
            'palavras_processadas': self.palavras_processadas,
            'tokens_processados': self.total_tokens,
            'tempo_decorrido': time.time() - self.tempo_inicio,
            'taxa_processamento': self.palavras_por_segundo
        }

class GeradorVetorizadorContinuo:
    def __init__(self, stats: ProcessingStats):
        try:
            # Inicializa BERT com tratamento de erro
            self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            self.model = BertModel.from_pretrained('bert-base-uncased')
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.model.to(self.device)
            self.model.eval()
        except Exception as e:
            logging.error(f"Erro ao inicializar BERT: {e}")
            raise RuntimeError("Falha na inicialização do modelo BERT.")

        # Inicializa banco com retry
        retry_count = 3
        while retry_count > 0:
            try:
                self.setup_database()
                break
            except sqlite3.Error as e:
                retry_count -= 1
                logging.error(f"Tentativa {3-retry_count} de conectar ao banco falhou: {e}")
                if retry_count == 0:
                    raise RuntimeError("Falha na conexão com o banco de dados após múltiplas tentativas.")

        self.stats = stats
        self.stats.reset()
        self.layout = self.setup_layout()

    def setup_database(self):
        self.conn = sqlite3.connect('vectors_continuo.db')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS word_vectors (
                id INTEGER PRIMARY KEY,
                word TEXT UNIQUE,
                vector BLOB,
                palavra_origem TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def generate_embedding(self, word: str) -> np.ndarray:
        try:
            with torch.no_grad():
                inputs = self.tokenizer(word, return_tensors='pt', padding=True).to(self.device)
                outputs = self.model(**inputs)
                embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy()[0]
                return embedding
        except Exception as e:
            print(f"Erro ao gerar embedding para '{word}': {e}")
            return np.zeros(768)

    def get_gemini_response(self, prompt: str) -> str:
        try:
            model = genai.GenerativeModel(NOME_MODELO)
            response = model.generate_content(prompt)
            
            # Limpa e valida a resposta
            content = response.text.strip()
            
            # Verifica se o conteúdo começa com lista_palavras:
            if not content.startswith('lista_palavras:'):
                content = 'lista_palavras:\n' + content
                
            # Garante que cada linha tenha o formato correto
            lines = []
            for line in content.splitlines():
                line = line.strip()
                if line and line != 'lista_palavras:':
                    if not line.startswith('-'):
                        line = f'- {line}'
                    lines.append(line)
                elif line == 'lista_palavras:':
                    lines.append(line)
                    
            return '\n'.join(['lista_palavras:'] + [line for line in lines if line != 'lista_palavras:'])
            
        except Exception as e:
            logging.error(f"Erro ao obter resposta do Gemini: {e}")
            return ""

    def extract_words(self, yaml_content: str) -> set:
        try:
            # Primeira tentativa: parsing direto
            try:
                data = yaml.safe_load(yaml_content)
                if isinstance(data, dict) and 'lista_palavras' in data:
                    words = data['lista_palavras']
                    if isinstance(words, list):
                        return set(word.strip().lower() for word in words 
                                 if isinstance(word, str) and word.strip())
            except yaml.YAMLError:
                logging.warning("Falha no parsing YAML padrão, tentando método alternativo")
            
            # Segunda tentativa: parsing linha por linha
            palavras = set()
            for linha in yaml_content.splitlines():
                linha = linha.strip()
                if not linha or linha == 'lista_palavras:' or linha.startswith('#'):
                    continue
                    
                # Remove o hífen e espaços
                palavra = linha.lstrip('- ').strip()
                
                # Remove caracteres especiais mantendo letras e números
                palavra = re.sub(r'[^\w\s-]', '', palavra)
                
                if palavra:
                    palavras.add(palavra.lower())
                    
            return palavras
            
        except Exception as e:
            logging.error(f"Erro ao extrair palavras: {e}\nConteúdo YAML:\n{yaml_content}")
            return set()

    def clean_yaml_content(self, content: str) -> str:
        # Remove caracteres Unicode problemáticos
        content = content.encode('ascii', 'ignore').decode()
        
        # Remove espaços extras e quebras de linha desnecessárias
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        
        # Garante formato correto para lista YAML
        if not any('lista_palavras:' in line for line in lines):
            lines.insert(0, 'lista_palavras:')
            
        # Adiciona hífen para itens sem ele
        formatted_lines = []
        for line in lines:
            if line == 'lista_palavras:':
                formatted_lines.append(line)
            elif not line.startswith('-'):
                formatted_lines.append(f'- {line}')
            else:
                formatted_lines.append(line)
                
        return '\n'.join(formatted_lines)

    def setup_layout(self):
        """Configura o layout com 5 colunas de métricas e estatísticas no fundo"""
        layout = Layout()
        
        # Divide em duas seções principais
        layout.split_column(
            Layout(name="metrics_area", size=15),  # Área para métricas
            Layout(name="spacer", size=0),         # Espaço flexível
            Layout(name="stats_row", size=8)       # Estatísticas no fundo
        )
        
        # Divide a área de métricas em 5 colunas
        layout["metrics_area"].split_row(
            Layout(name="ia_metrics", ratio=1),
            Layout(name="queue_metrics", ratio=1),
            Layout(name="token_metrics", ratio=1),
            Layout(name="response_metrics", ratio=1),
            Layout(name="time_metrics", ratio=1)
        )
        
        # Mantém a divisão original das estatísticas
        layout["stats_row"].split_row(
            Layout(name="processamento", ratio=1),
            Layout(name="performance", ratio=1),
            Layout(name="recursos", ratio=1),
            Layout(name="metricas", ratio=1)
        )
        
        return layout

    def create_processamento_panel(self):
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="right", style="cyan")
        table.add_column(justify="left", style="white")
        
        rows = [
            ("🔢 Total", f"{self.stats.total_palavras:,}"),
            ("✅ Processadas", f"{self.stats.palavras_processadas:,}"),
            ("⏳ Em Processo", f"{self.stats.em_processamento:,}"),
            ("📤 Na Fila", f"{self.stats.palavras_na_fila:,}"),
            ("🆕 Novas", f"{self.stats.palavras_novas:,}"),
            ("🔄 Repetidas", f"{self.stats.palavras_repetidas:,}")
        ]
        
        for label, value in rows:
            table.add_row(label, value)
        
        return Panel(
            Align.center(table),
            title="[bold blue]Processamento[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        )

    def create_performance_panel(self):
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="right", style="green")
        table.add_column(justify="left", style="white")
        
        tempo_str = str(timedelta(seconds=int(self.stats.tempo_processamento)))
        rows = [
            ("⏱️ Tempo", tempo_str),
            ("🚀 Palavras/s", f"{self.stats.palavras_por_segundo:.1f}"),
            ("🔤 Tokens/s", f"{self.stats.tokens_por_segundo:.1f}"),
            ("📈 Sucesso", f"{self.stats.taxa_sucesso:.1f}%"),
            ("⚡ Velocidade", f"{self.stats.palavras_por_segundo * 60:.0f}/min"),
            ("🎯 Precisão", f"{self.stats.precisao:.1f}%")
        ]
        
        for label, value in rows:
            table.add_row(label, value)
        
        return Panel(
            Align.center(table),
            title="[bold green]Performance[/bold green]",
            border_style="green",
            padding=(1, 2)
        )

    def create_recursos_panel(self):
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="right", style="yellow")
        table.add_column(justify="left", style="white")
        
        rows = [
            ("💻 CPU", f"{self.stats.uso_cpu:.1f}%"),
            ("🧠 RAM", f"{self.stats.uso_ram:.1f}%"),
            ("⚙️ Threads", f"{self.stats.threads_ativos}"),
            ("💾 DB", f"{self.stats.tamanho_db_mb:.1f}MB"),
            ("📊 Cache", f"{self.stats.cache_hits}/{self.stats.cache_misses}"),
            ("⚡ Latência", f"{self.stats.latencia_media:.2f}ms")
        ]
        
        for label, value in rows:
            table.add_row(label, value)
        
        return Panel(
            Align.center(table),
            title="[bold yellow]Recursos[/bold yellow]",
            border_style="yellow",
            padding=(1, 2)
        )

    def create_metricas_panel(self):
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="right", style="magenta")
        table.add_column(justify="left", style="white")
        
        rows = [
            ("📊 Tokens", f"{self.stats.total_tokens:,}"),
            ("🔤 Únicos", f"{self.stats.tokens_unicos:,}"),
            ("⚠️ Erros", f"{self.stats.falhas}"),
            ("📏 Média", f"{self.stats.tamanho_medio_palavra:.1f}"),
            ("📈 Magnitude", f"{self.stats.media_magnitude:.2f}"),
            ("🔍 Densidade", f"{self.stats.densidade_vetores:.2f}")
        ]
        
        for label, value in rows:
            table.add_row(label, value)
        
        return Panel(
            Align.center(table),
            title="[bold magenta]Métricas[/bold magenta]",
            border_style="magenta",
            padding=(1, 2)
        )

    def create_status_panel(self, status: str):
        table = Table.grid()
        table.add_row(emoji.emojize(":clock:"), f"Timestamp: {datetime.now().strftime('%H:%M:%S')}")
        table.add_row(emoji.emojize(":memo:"), f"Status: {status}")
        table.add_row(emoji.emojize(":brain:"), f"Modelo: {NOME_MODELO}")
        table.add_row(emoji.emojize(":high_voltage:"), f"Device: {self.device}")
        table.add_row(emoji.emojize(":input_numbers:"), f"Tokens Total: {self.stats.total_tokens}")
        table.add_row(emoji.emojize(":card_index_dividers:"), f"Tokens Únicos: {self.stats.tokens_unicos}")
        table.add_row(emoji.emojize(":chart_increasing:"), f"Tokens/Palavra: {self.stats.tokens_por_palavra:.2f}")
        table.add_row(emoji.emojize(":bar_chart:"), f"Token Max/Min: {self.stats.tokens_max}/{self.stats.tokens_min}")
        table.add_row(emoji.emojize(":chart_with_upwards_trend:"), f"Token Média: {self.stats.tokens_media:.2f}")
        table.add_row(emoji.emojize(":stopwatch:"), f"Tempo/Token: {self.stats.tempo_tokenizacao/max(self.stats.total_tokens, 1):.3f}s")
        table.add_row(emoji.emojize(":rocket:"), f"Tokens/s: {self.stats.tokens_por_segundo:.1f}")
        table.add_row(emoji.emojize(":gear:"), f"Batch Size: {self.stats.batch_size}")
        return Panel(table, title="Status Atual", border_style="purple")

    def create_ia_metrics_panel(self):
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="right", style="cyan")
        table.add_column(justify="left", style="white")
        
        rows = [
            ("🤖 Modelo", NOME_MODELO),
            ("🌡️ Temperatura", f"{self.stats.temperatura:.2f}"),
            ("📊 Top-P", f"{self.stats.top_p:.2f}"),
            ("⚡ Latência IA", f"{self.stats.tempo_ia*1000:.0f}ms"),
            ("💭 Tokens/Req", f"{self.stats.tokens_por_requisicao:.1f}")
        ]
        
        for label, value in rows:
            table.add_row(label, value)
        
        return Panel(
            Align.center(table),
            title="[bold cyan]Métricas IA[/bold cyan]",
            border_style="cyan"
        )

    def create_queue_metrics_panel(self):
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="right", style="green")
        table.add_column(justify="left", style="white")
        
        rows = [
            ("📥 Na Fila", f"{self.stats.palavras_na_fila:,}"),
            ("⏳ Processando", f"{self.stats.em_processamento:,}"),
            ("✅ Concluídas", f"{self.stats.palavras_processadas:,}"),
            ("⚠️ Pendentes", f"{self.stats.total_palavras - self.stats.palavras_processadas:,}"),
            ("📈 Progresso", f"{(self.stats.palavras_processadas/max(1, self.stats.total_palavras))*100:.1f}%")
        ]
        
        for label, value in rows:
            table.add_row(label, value)
        
        return Panel(
            Align.center(table),
            title="[bold green]Fila de Processamento[/bold green]",
            border_style="green"
        )

    def create_token_metrics_panel(self):
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="right", style="yellow")
        table.add_column(justify="left", style="white")
        
        rows = [
            ("🔤 Total Tokens", f"{self.stats.total_tokens:,}"),
            ("🆕 Únicos", f"{self.stats.tokens_unicos:,}"),
            ("📊 Média/Palavra", f"{self.stats.tokens_por_palavra:.1f}"),
            ("📈 Taxa", f"{self.stats.tokens_por_segundo:.1f}/s"),
            ("💫 Densidade", f"{self.stats.densidade_vetores:.2f}")
        ]
        
        for label, value in rows:
            table.add_row(label, value)
        
        return Panel(
            Align.center(table),
            title="[bold yellow]Métricas de Tokens[/bold yellow]",
            border_style="yellow"
        )

    def create_response_metrics_panel(self):
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="right", style="magenta")
        table.add_column(justify="left", style="white")
        
        rows = [
            ("✅ Sucesso", f"{self.stats.taxa_sucesso:.1f}%"),
            ("❌ Erros", f"{self.stats.falhas}"),
            ("🎯 Precisão", f"{self.stats.precisao:.1f}%"),
            ("💾 Cache Hits", f"{self.stats.cache_hits:,}"),
            ("🔄 Cache Miss", f"{self.stats.cache_misses:,}")
        ]
        
        for label, value in rows:
            table.add_row(label, value)
        
        return Panel(
            Align.center(table),
            title="[bold magenta]Respostas[/bold magenta]",
            border_style="magenta"
        )

    def create_time_metrics_panel(self):
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="right", style="blue")
        table.add_column(justify="left", style="white")
        
        rows = [
            ("⚡ Palavras/s", f"{self.stats.palavras_por_segundo:.1f}"),
            ("🚀 Tokens/s", f"{self.stats.tokens_por_segundo:.1f}"),
            ("⏱️ Tempo Total", str(timedelta(seconds=int(self.stats.tempo_processamento)))),
            ("💨 Velocidade", f"{self.stats.palavras_por_segundo * 60:.0f}/min"),
            ("📊 ETA", str(timedelta(seconds=int(self.stats.tempo_estimado_restante))))
        ]
        
        for label, value in rows:
            table.add_row(label, value)
        
        return Panel(
            Align.center(table),
            title="[bold blue]Métricas de Tempo[/bold blue]",
            border_style="blue"
        )

    def update_display(self, status: str, live: Live):
        try:
            self.stats.update_tempo()
            self.stats.update_system_metrics()
            
            # Atualiza os painéis de métricas
            self.layout["metrics_area"]["ia_metrics"].update(self.create_ia_metrics_panel())
            self.layout["metrics_area"]["queue_metrics"].update(self.create_queue_metrics_panel())
            self.layout["metrics_area"]["token_metrics"].update(self.create_token_metrics_panel())
            self.layout["metrics_area"]["response_metrics"].update(self.create_response_metrics_panel())
            self.layout["metrics_area"]["time_metrics"].update(self.create_time_metrics_panel())
            
            # Atualiza os painéis de estatísticas no fundo
            self.layout["stats_row"]["processamento"].update(self.create_processamento_panel())
            self.layout["stats_row"]["performance"].update(self.create_performance_panel())
            self.layout["stats_row"]["recursos"].update(self.create_recursos_panel())
            self.layout["stats_row"]["metricas"].update(self.create_metricas_panel())
            
            live.update(self.layout)
            
        except Exception as e:
            logging.error(f"Erro ao atualizar display: {e}")
            raise

    def process_yaml_to_df(self, yaml_content: str) -> pd.DataFrame:
        palavras = self.extract_words(yaml_content)
        self.stats.total_palavras = len(palavras)
        self.stats.palavras_unicas = len(set(palavras))
        df = pd.DataFrame(list(palavras), columns=['word'])
        df['vector'] = ''
        df['vector'] = df['word'].apply(self.generate_embedding)
        return df

    async def processar_palavra(self, palavra_inicial: str):
        with Live(self.layout, refresh_per_second=4) as live:
            try:
                # 1. Inicialização
                self.stats.registrar_etapa("Inicialização")
                inicio = time.time()
                self.stats.tempo_inicio = inicio
                
                # 2. Geração IA
                self.stats.registrar_etapa("IA", "Gerando prompt")
                prompt = f"""
                Gere uma lista YAML técnica de palavras relacionadas a '{palavra_inicial}'.
                
                Requisitos:
                - Gere exatamente 500 palavras técnicas relacionadas
                - Inclua sinônimos e termos técnicos
                - Evite repetições
                - Use apenas palavras únicas
                
                Formato:
                lista_palavras:
                - palavra1
                - palavra2
                ...
                """
                
                self.stats.registrar_etapa("IA", "Obtendo resposta")
                tempo_ia_inicio = time.time()
                yaml_content = self.get_gemini_response(prompt)
                self.stats.tempo_ia = time.time() - tempo_ia_inicio
                
                # 3. Processamento de Palavras
                self.stats.registrar_etapa("Processamento", "Extração de palavras")
                palavras_relacionadas = self.extract_words(yaml_content)
                todas_palavras = {palavra_inicial} | palavras_relacionadas
                
                self.stats.total_palavras = len(todas_palavras)
                self.stats.palavras_unicas = len(set(todas_palavras))
                self.stats.palavras_repetidas = len(todas_palavras) - self.stats.palavras_unicas
                
                # 4. Processamento Individual
                for palavra in todas_palavras:
                    self.stats.registrar_etapa("Processamento", f"Palavra: {palavra}")
                    
                    # 4.1 Tokenização
                    tempo_token_inicio = time.time()
                    tokens = self.tokenizer.tokenize(palavra)
                    self.stats.tempo_tokenizacao += time.time() - tempo_token_inicio
                    
                    # Atualiza métricas de tokens
                    self.stats.total_tokens += len(tokens)
                    self.stats.tokens_unicos = len(set(tokens))
                    self.stats.tokens_por_palavra = len(tokens)
                    self.stats.distribuicao_tokens[len(tokens)] += 1
                    
                    # 4.2 Vetorização
                    tempo_vetor_inicio = time.time()
                    vector = self.generate_embedding(palavra)
                    self.stats.tempo_vetorizacao += time.time() - tempo_vetor_inicio
                    
                    if vector is not None:
                        # Atualiza métricas de vetores
                        magnitude = np.linalg.norm(vector)
                        self.stats.media_magnitude = (self.stats.media_magnitude * self.stats.palavras_processadas + magnitude) / (self.stats.palavras_processadas + 1)
                        self.stats.max_magnitude = max(self.stats.max_magnitude, magnitude)
                        self.stats.min_magnitude = min(self.stats.min_magnitude, magnitude) if self.stats.min_magnitude > 0 else magnitude
                        
                        # 4.3 Salvamento
                        tempo_banco_inicio = time.time()
                        vector_bytes = vector.tobytes()
                        self.conn.execute(
                            'INSERT OR REPLACE INTO word_vectors (word, vector, palavra_origem) VALUES (?, ?, ?)',
                            (palavra, vector_bytes, palavra_inicial)
                        )
                        self.conn.commit()
                        self.stats.tempo_banco += time.time() - tempo_banco_inicio
                    
                    # Atualiza estatísticas
                    self.stats.palavras_processadas += 1
                    self.stats.palavras_por_segundo = self.stats.palavras_processadas / (time.time() - inicio)
                    self.stats.tokens_por_segundo = self.stats.total_tokens / (time.time() - inicio)
                    
                    # Atualiza display
                    self.update_display(f"Processando: {palavra}", live)
                    await asyncio.sleep(0.1)
                
                # 5. Finalização e Relatório
                self.stats.registrar_etapa("Finalização", "Gerando relatório")
                self.gerar_relatorio_final()
                
            except Exception as e:
                self.stats.falhas += 1
                self.stats.erros_por_tipo[type(e).__name__] += 1
                logging.error(f"Erro no processamento:\nTipo: {type(e).__name__}\nMensagem: {str(e)}\nPalavra: {palavra_inicial}")
                self.update_display(f"Erro: {str(e)}", live)

    def gerar_relatorio_final(self):
        console = Console()
        console.print("\n[bold cyan]Relatório Final de Processamento[/bold cyan]")
        
        # Métricas de Palavras
        console.print("\n[yellow]Métricas de Palavras:[/yellow]")
        console.print(f"Total de palavras: {self.stats.total_palavras}")
        console.print(f"Palavras únicas: {self.stats.palavras_unicas}")
        console.print(f"Palavras repetidas: {self.stats.palavras_repetidas}")
        console.print(f"Taxa de processamento: {self.stats.palavras_por_segundo:.2f} palavras/s")
        
        # Métricas de Tokens
        console.print("\n[yellow]Métricas de Tokens:[/yellow]")
        console.print(f"Total de tokens: {self.stats.total_tokens}")
        console.print(f"Tokens únicos: {self.stats.tokens_unicos}")
        console.print(f"Média de tokens por palavra: {self.stats.tokens_por_palavra:.2f}")
        console.print(f"Taxa de tokenização: {self.stats.tokens_por_segundo:.2f} tokens/s")
        
        # Métricas de Tempo
        console.print("\n[yellow]Métricas de Tempo:[/yellow]")
        console.print(f"Tempo total: {timedelta(seconds=int(self.stats.tempo_processamento))}")
        console.print(f"Tempo IA: {timedelta(seconds=int(self.stats.tempo_ia))}")
        console.print(f"Tempo vetorização: {timedelta(seconds=int(self.stats.tempo_vetorizacao))}")
        console.print(f"Tempo banco: {timedelta(seconds=int(self.stats.tempo_banco))}")
        
        # Histórico de Etapas
        console.print("\n[yellow]Histórico de Processamento:[/yellow]")
        for etapa in self.stats.historico_etapas:
            console.print(f"{etapa['timestamp'].strftime('%H:%M:%S')} - {etapa['etapa']} - {etapa['sub_etapa']}")

def configurar_geracao(temperatura=0.8, top_p=0.95, top_k=64, max_tokens=8096):
    return {
        "temperature": temperatura,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": max_tokens,
        "response_mime_type": "text/plain",
    }

async def main():
    console.print("[bold cyan]Gerador e Vetorizador Contínuo de Palavras[/bold cyan]")
    console.print("[yellow]Digite 'sair' para encerrar o programa[/yellow]")
    stats = ProcessingStats()
    processador = GeradorVetorizadorContinuo(stats)
    
    while True:
        palavra = input("\nDigite uma palavra para processar (ou 'sair'): ").strip().lower()
        if palavra == 'sair':
            break
        if palavra:
            # Processa uma palavra por vez
            await processador.processar_palavra(palavra)
        else:
            console.print("[red]Entrada inválida![/red]")
    
    stats.update_tempo()
    console.print(f"\nEstatísticas Globais:")
    console.print(f"Tempo total: {timedelta(seconds=int(stats.tempo_processamento))}")
    console.print(f"Total de palavras: {stats.total_palavras}")
    console.print(f"Palavras processadas: {stats.palavras_processadas}")
    console.print(f"Novas palavras: {stats.palavras_novas}")
    console.print(f"Falhas: {stats.falhas}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Programa encerrado pelo usuário[/yellow]")
    except Exception as e:
        console.print(f"[red]Erro crítico: {e}[/red]")
