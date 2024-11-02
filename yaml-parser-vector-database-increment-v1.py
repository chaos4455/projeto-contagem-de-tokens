import asyncio
import yaml
import os
import pandas as pd
from rich.console import Console
from rich.progress import track
from colorama import init, Fore
from transformers import BertTokenizer, BertModel
import torch
import sqlite3
import numpy as np
import re
from typing import List, Dict, Set, Any # Importando Any
import time
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich import box
from datetime import datetime
import threading
import psutil
import GPUtil
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from concurrent.futures import ThreadPoolExecutor, as_completed

# Inicialização
init()  # Colorama
console = Console()  # Rich

# Configuração do banco de dados
def setup_database():
    conn = sqlite3.connect('vector-blob-database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS word_vectors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL UNIQUE,
            vector_blob BLOB NOT NULL
        )
    ''')
    conn.commit()
    return conn

# Função para limpar o conteúdo do YAML
def clean_yaml_content(content: str) -> str:
    # Remove caracteres especiais no início do arquivo
    content = re.sub(r'^[`\'"]', '', content, flags=re.MULTILINE)
    # Remove blocos de código markdown
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    # Remove caracteres especiais restantes
    content = re.sub(r'[^\w\s\-:{}[\],.]', ' ', content)
    return content.strip()

class YAMLParser:
    def __init__(self, tokenizer):
        self.errors = []
        self.stats = {
            'total_files': 0,
            'successful_files': 0,
            'failed_files': 0,
            'total_tokens': 0,
            'unique_tokens': 0
        }
        self.tokenizer = tokenizer  # BERT tokenizer

    def safe_yaml_load(self, content: str) -> Dict:
        """Parser YAML seguro com múltiplas tentativas de recuperação"""
        try:
            # Primeira tentativa: parsing direto
            return yaml.safe_load(content)
        except yaml.YAMLError:
            try:
                # Segunda tentativa: limpeza básica
                cleaned = clean_yaml_content(content)
                return yaml.safe_load(cleaned)
            except yaml.YAMLError:
                try:
                    # Terceira tentativa: parsing linha por linha
                    result = {}
                    for line in content.split('\n'):
                        try:
                            if ':' in line:
                                key, value = line.split(':', 1)
                                result[key.strip()] = value.strip()
                        except Exception:
                            continue
                    return result if result else {'text': content}
                except Exception:
                    # Última tentativa: retorna como texto puro
                    return {'text': content}

    async def process_file(self, file_path: str) -> pd.DataFrame:
        """Processa um arquivo YAML e retorna DataFrame com tokens"""
        self.stats['total_files'] += 1
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            yaml_content = self.safe_yaml_load(content)
            tokens = self.extract_tokens(yaml_content, file_path) # Passando file_path
            
            df = pd.DataFrame(tokens, columns=['token', 'source_file', 'context'])
            self.stats['successful_files'] += 1
            return df
            
        except Exception as e:
            self.errors.append(f"Erro ao processar {file_path}: {str(e)}")
            self.stats['failed_files'] += 1
            return pd.DataFrame(columns=['token', 'source_file', 'context'])

    def extract_tokens(self, content: Any, file_path: str, context: str = '') -> List[tuple]: # Adicionando file_path
        """Extrai tokens recursivamente do conteúdo YAML"""
        tokens = []
        
        if isinstance(content, dict):
            for key, value in content.items():
                new_context = f"{context}.{key}" if context else key
                tokens.extend(self.extract_tokens(value, file_path, new_context)) # Passando file_path
                
        elif isinstance(content, list):
            for i, item in enumerate(content):
                new_context = f"{context}[{i}]"
                tokens.extend(self.extract_tokens(item, file_path, new_context)) # Passando file_path
                
        elif isinstance(content, str):
            # Ignora URLs e strings muito longas
            if not re.match(r'http[s]?://', content) and len(content) < 1000:
                clean_tokens = self.tokenize_text(content)
                tokens.extend((token, file_path, context) for token in clean_tokens)
        elif content is not None:
            self.errors.append(f"Conteúdo não-string encontrado em {file_path} contexto: {context}, tipo: {type(content)}")

        return tokens

    def tokenize_text(self, text: str) -> Set[str]:
        """Tokeniza texto usando BERT"""
        # Remove URLs e limpa o texto
        text = re.sub(r'http[s]?://\S+', '', text)
        text = clean_yaml_content(text)
        
        # Usa BERT tokenizer
        tokens = self.tokenizer.tokenize(text)
        
        # Filtra tokens válidos
        valid_tokens = set()
        for token in tokens:
            # Remove tokens especiais do BERT e tokens muito curtos/longos
            if (not token.startswith('[')) and (not token.startswith('#')) and (2 <= len(token) <= 50):
                valid_tokens.add(token)
                self.stats['total_tokens'] += 1
        
        return valid_tokens

class DataProcessor:
    def __init__(self, batch_size: int = 16):  # Reduzido batch_size para melhor performance
        self.batch_size = batch_size
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.model.to(self.device)
        self.model.eval()  # Importante: coloca o modelo em modo de avaliação

    async def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processa DataFrame com tokens e gera embeddings"""
        unique_tokens = df['token'].unique()
        print(f"Unique Tokens: {unique_tokens}") # adicionando log
        print(f"Unique Tokens type: {type(unique_tokens)}") # adicionando log
        embeddings = await self.generate_embeddings(list(unique_tokens)) # Convertendo para lista
        
        # Cria DataFrame de embeddings
        embeddings_df = pd.DataFrame({
            'word': unique_tokens, # Mudança aqui
            'embedding': embeddings
        })
        
        return embeddings_df

    async def generate_embeddings(self, tokens: List[str]) -> List[np.ndarray]:
        """Gera embeddings em batches de forma otimizada"""
        embeddings = []
        
        for i in range(0, len(tokens), self.batch_size):
            batch = tokens[i:i + self.batch_size]
            
            # Prepara inputs
            inputs = self.tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            ).to(self.device)
            
            # Processa batch
            with torch.no_grad():
                outputs = self.model(**inputs)
                # Usa [CLS] token como embedding da palavra
                batch_embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
                embeddings.extend(batch_embeddings)
            
            # Libera memória CUDA
            if self.device.type == 'cuda':
                torch.cuda.empty_cache()
        
        return embeddings

    def create_single_embedding(self, token: str) -> np.ndarray:
        """Cria embedding para um único token"""
        try:
            inputs = self.tokenizer(
                token,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            return outputs.last_hidden_state.mean(dim=1).cpu().numpy()[0]
            
        except Exception as e:
            raise Exception(f"Erro ao criar embedding para '{token}': {e}")

# Função para salvar no banco
async def save_to_database(df: pd.DataFrame, conn: sqlite3.Connection, progress_callback=None):
    console.print("💾 [blue]Salvando no banco de dados...[/blue]")
    
    cursor = conn.cursor()
    
    async def empty_callback():
        await asyncio.sleep(0)

    if progress_callback is None:
        progress_callback = empty_callback

    try:
        for index, row in df.iterrows():
            word = row['word']
            embedding = row['embedding']
            
            cursor.execute(
                'INSERT OR IGNORE INTO word_vectors (word, vector_blob) VALUES (?, ?)',
                (word, embedding.tobytes())
            )
            
            await progress_callback()
            
            conn.commit()
            
        console.print("✅ [green]Dados salvos com sucesso![/green]")
    except sqlite3.Error as e:
        console.print(f"❌ [red]Erro ao salvar no banco de dados:[/red] {e}")
    finally:
        conn.close()

# Contadores globais com thread safety
class Counters:
    def __init__(self):
        self.lock = threading.Lock()
        self.processed_files = 0
        self.total_words = 0
        self.processed_embeddings = 0
        self.saved_to_db = 0
        self.errors = 0
        self.start_time = time.time()
        
counters = Counters()

def create_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="stats"),
        Layout(name="progress"),
        Layout(name="details")
    )
    return layout

def generate_stats_table() -> Table:
    table = Table(title="📊 Estatísticas", box=box.ROUNDED)
    table.add_column("Métrica", style="cyan")
    table.add_column("Valor", justify="right", style="green")
    
    elapsed = time.time() - counters.start_time
    
    with counters.lock:
        table.add_row("📁 Arquivos Processados", str(counters.processed_files))
        table.add_row("📝 Palavras Únicas", str(counters.total_words))
        table.add_row("🧮 Embeddings Gerados", str(counters.processed_embeddings))
        table.add_row("💾 Registros Salvos", str(counters.saved_to_db))
        table.add_row("⚠️ Erros", str(counters.errors))
        table.add_row("⏱️ Tempo Decorrido", f"{elapsed:.2f}s")
        
        if elapsed > 0:
            rate = counters.processed_embeddings / elapsed
            table.add_row("🚀 Taxa de Processamento", f"{rate:.2f}/s")
    
    return table

def generate_progress_table(progress_data: dict) -> Table:
    table = Table(title="📈 Progresso", box=box.ROUNDED)
    table.add_column("Etapa", style="cyan")
    table.add_column("Progresso", justify="right", style="green")
    
    for stage, (current, total) in progress_data.items():
        if total > 0:
            percentage = (current / total) * 100
            table.add_row(stage, f"{percentage:.1f}% ({current}/{total})")
    
    return table

def generate_details_table(recent_actions: list) -> Table:
    table = Table(title="📋 Detalhes Recentes", box=box.ROUNDED)
    table.add_column("Timestamp", style="cyan")
    table.add_column("Ação", style="green")
    table.add_column("Detalhes", style="yellow")
    
    for action in recent_actions[-5:]:  # Mostra últimas 5 ações
        table.add_row(*action)
    
    return table

class ProcessingManager:
    def __init__(self):
        self.layout = None
        self.progress_data = {
            "Processamento de Arquivos": [0, 0],
            "Geração de Embeddings": [0, 0],
            "Salvamento no Banco": [0, 0]
        }
        self.recent_actions = []
        self.live = None

    def add_action(self, action: str, details: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.recent_actions.append((timestamp, action, details))
        if len(self.recent_actions) > 10:
            self.recent_actions.pop(0)
        self.update_display()

    def update_display(self):
        if self.layout and self.live:
            self.layout["stats"].update(generate_stats_table())
            self.layout["progress"].update(generate_progress_table(self.progress_data))
            self.layout["details"].update(generate_details_table(self.recent_actions))
            self.live.refresh()

# Função principal
async def main():
    manager = ProcessingManager()
    data_processor = DataProcessor()
    yaml_parser = YAMLParser(data_processor.tokenizer)  # Passa o tokenizer
    
    with Live(manager.layout, refresh_per_second=4) as live:
        manager.live = live
        
        # 1. Coleta todos os arquivos YAML
        yaml_dir = 'generated-yaml-text-to-embedding'
        yaml_files = [f for f in os.listdir(yaml_dir) if f.endswith('.yaml')]
        total_files = len(yaml_files)
        
        manager.progress_data["Arquivos"] = [0, total_files]
        manager.add_action("Início", f"Encontrados {total_files} arquivos YAML")
        
        # 2. Processa todos os arquivos e coleta tokens únicos
        all_tokens_df = pd.DataFrame(columns=['token', 'source_file', 'context'])
        
        for idx, yaml_file in enumerate(yaml_files, 1):
            file_path = os.path.join(yaml_dir, yaml_file)
            df = await yaml_parser.process_file(file_path)
            all_tokens_df = pd.concat([all_tokens_df, df], ignore_index=True)
            
            manager.progress_data["Arquivos"][0] = idx
            manager.add_action("Arquivo", f"Processado {yaml_file}")
            manager.update_display()
        
        # 3. Obtém tokens únicos
        unique_tokens = all_tokens_df['token'].unique()
        total_tokens = len(unique_tokens)
        
        manager.progress_data["Tokens"] = [0, total_tokens]
        manager.add_action("Tokens", f"Encontrados {total_tokens} tokens únicos")
        
        # 4. Gera embeddings
        print(f"Unique Tokens before embedding generation: {unique_tokens}") # adicionando log
        print(f"Unique Tokens type before embedding generation: {type(unique_tokens)}") # adicionando log
        embeddings_list = await data_processor.generate_embeddings(list(unique_tokens)) # Convertendo para lista
        
        # 5. Cria DataFrame final
        embeddings_df = pd.DataFrame({
            'word': unique_tokens,
            'embedding': embeddings_list
        })
        
        # 6. Salva no banco
        conn = setup_database()
        total_to_save = len(embeddings_df)
        manager.progress_data["Banco"] = [0, total_to_save]
        
        async def update_progress():
            with counters.lock:
                counters.saved_to_db += 1
                current = counters.saved_to_db
                manager.progress_data["Banco"][0] = current
                if current % 50 == 0:
                    manager.add_action("Banco", f"Salvos {current}/{total_to_save}")
                    manager.update_display()
        
        await save_to_database(embeddings_df, conn, update_progress)
        
        # 7. Relatório final
        manager.add_action("Conclusão", f"""
        Arquivos processados: {total_files}
        Tokens únicos: {total_tokens}
        Embeddings gerados: {len(embeddings_df)}
        Salvos no banco: {counters.saved_to_db}
        """)
        manager.update_display()

if __name__ == "__main__":
    asyncio.run(main())
