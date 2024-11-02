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
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
import time
import psutil
import os
from rich.style import Style
from rich.text import Text
import multiprocessing

console = Console()

class YAMLVectorizer:
    """
    Classe para vetorizar arquivos YAML usando o modelo BERT.
    """
    def __init__(self):
        """
        Inicializa o vetorizador YAML.
        """
        # Inicializa BERT
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        self.model.eval()
        
        # Inicializa banco de dados
        self.setup_database()
        self.num_processes = min(multiprocessing.cpu_count(), os.cpu_count()) # Define o número de processos com base nos núcleos da CPU, evitando exceder a capacidade

    def setup_database(self):
        """
        Configura o banco de dados SQLite.
        """
        self.conn = sqlite3.connect('vectors.db')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS word_vectors (
                id INTEGER PRIMARY KEY,
                word TEXT UNIQUE,
                vector BLOB
            )
        ''')
        self.conn.commit()
    
    def clean_text(self, text: str) -> str:
        """
        Limpa e normaliza o texto.
        """
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)  # Remove blocos de código
        text = re.sub(r'http\S+', '', text)  # Remove URLs
        text = re.sub(r'[^\w\s]', ' ', text)  # Remove caracteres especiais
        return ' '.join(text.lower().split())
    
    def extract_words(self, yaml_content: dict) -> set:
        """
        Extrai palavras únicas do conteúdo YAML.
        """
        words = set()
        for item in yaml_content.values():
            if isinstance(item, str):
                text = self.clean_text(item)
                words.update(word for word in text.split() if len(word) >= 2 and not word.isnumeric())
            elif isinstance(item, (dict, list)):
                words.update(self.extract_words(item)) # Recursividade otimizada para dicionários e listas
        return words
    
    def count_tokens(self, text: str) -> int:
        """
        Conta os tokens usando o BERT tokenizer.
        """
        return len(self.tokenizer.tokenize(text))

    def count_words(self, text: str) -> int:
        """
        Conta as palavras no texto.
        """
        return len(self.clean_text(text).split())

    def generate_embedding(self, word: str) -> np.ndarray:
        """
        Gera o embedding para uma palavra usando o modelo BERT.
        """
        try:
            with torch.no_grad():
                inputs = self.tokenizer(word, return_tensors='pt', padding=True).to(self.device)
                outputs = self.model(**inputs)
                embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy()[0]
                return embedding
        except Exception as e:
            print(f"[bold red]Erro ao gerar embedding para '{word}': {e}[/]")
            return np.zeros(768) # Retorna um vetor zero se houver erro

    def process_word(self, word):
        """
        Processa uma única palavra, gerando e salvando o embedding no banco de dados.
        """
        cursor = self.conn.cursor()
        try:
            exists = cursor.execute('SELECT 1 FROM word_vectors WHERE word = ?', (word,)).fetchone()
            if exists is None:
                vector = self.generate_embedding(word)
                cursor.execute(
                    'INSERT INTO word_vectors (word, vector) VALUES (?, ?)',
                    (word, vector.tobytes())
                )
                self.conn.commit()
                return vector
            return None
        except sqlite3.Error as e:
            print(f"[bold red]Erro de banco de dados ao processar '{word}': {e}[/]")
            return None
        except Exception as e:
            print(f"[bold red]Erro ao processar '{word}': {e}[/]")
            return None

    def process_file(self, yaml_path: Path):
        """
        Processa um arquivo YAML, extraindo palavras e gerando embeddings.
        """
        try:
            # Carrega e extrai palavras do YAML
            with open(yaml_path) as f:
                content = yaml.safe_load(f)
            words = self.extract_words(content)
            text_content = yaml.safe_dump(content) # Pega o texto do YAML para contagem
            print(f"[bold green]Processando arquivo: {yaml_path}, Palavras únicas encontradas: {len(words)}[/]")

            # Gera e salva embeddings em paralelo
            with multiprocessing.Pool(processes=self.num_processes) as pool:
                embeddings = pool.map(self.process_word, words)
            
            embeddings = [emb for emb in embeddings if emb is not None] # Remove embeddings None (palavras existentes)
            return len(words), self.count_tokens(text_content), self.count_words(text_content), np.array(embeddings) # Retorna embeddings como array numpy
            
        except yaml.YAMLError as e:
            print(f"[bold red]Erro YAML ao processar {yaml_path}: {e}[/]")
            return 0,0,0,np.array([]) # Retorna array numpy vazio em caso de erro
        except FileNotFoundError:
            print(f"[bold red]Arquivo não encontrado: {yaml_path}[/]")
            return 0,0,0,np.array([])
        except Exception as e:
            print(f"[bold red]Erro ao processar {yaml_path}: {e}[/]")
            return 0,0,0,np.array([]) # Retorna array numpy vazio em caso de erro

    def get_system_info(self):
        """
        Coleta informações do sistema.
        """
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_total = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        return cpu_percent, cpu_total, mem

    def get_bert_info(self):
        """
        Coleta informações do modelo BERT.
        """
        return self.model.config.name_or_path, self.model.config.hidden_size, 0.8 # Temperatura arbitrária

    def calculate_embedding_density(self, embeddings):
        """
        Calcula a densidade média dos embeddings.
        """
        if embeddings.size == 0: # Verifica se o array está vazio
            return 0.0
        return np.mean(np.linalg.norm(embeddings, axis=1))

    def calculate_embedding_stats(self, embeddings):
        """
        Calcula estatísticas dos embeddings (média e desvio padrão).
        """
        if embeddings.size == 0: # Verifica se o array está vazio
            return {}, 0, 0
        embeddings_np = np.array(embeddings)
        mean = np.mean(embeddings_np, axis=0)
        std = np.std(embeddings_np, axis=0)
        min_norm = np.min(np.linalg.norm(embeddings_np, axis=1))
        max_norm = np.max(np.linalg.norm(embeddings_np, axis=1))
        return {"mean": mean.tolist(), "std": std.tolist()}, min_norm, max_norm


    def process_directory(self, yaml_dir: str):
        """
        Processa um diretório de arquivos YAML.
        """
        yaml_files = list(Path(yaml_dir).glob('*.yaml'))
        total_words = 0
        total_tokens = 0
        total_unique_words = 0
        start_time = time.time()
        all_embeddings = []
        
        print(f"[bold green]Processando {len(yaml_files)} arquivos YAML...[/]")
        for yaml_file in track(yaml_files, description="Processando arquivos..."):
            unique_words, tokens, words, embeddings = self.process_file(yaml_file)
            total_words += words
            total_tokens += tokens
            total_unique_words += unique_words
            all_embeddings.extend(embeddings)

        end_time = time.time()
        elapsed_time = end_time - start_time
        cpu_percent, cpu_total, mem = self.get_system_info()
        model_name, model_dim, temperature = self.get_bert_info()
        print(f"[bold green]Embeddings shape: {np.array(all_embeddings).shape}[/]")
        embedding_density = self.calculate_embedding_density(np.array(all_embeddings))
        embedding_stats, min_norm, max_norm = self.calculate_embedding_stats(np.array(all_embeddings))
        self.display_kpis(total_unique_words, total_tokens, total_words, len(yaml_files), elapsed_time, cpu_percent, cpu_total, mem, model_name, model_dim, temperature, embedding_density, embedding_stats, min_norm, max_norm)

    def display_kpis(self, unique_words, tokens, words, files_processed, elapsed_time, cpu_percent, cpu_total, mem, model_name, model_dim, temperature, embedding_density, embedding_stats, min_norm, max_norm):
        """
        Exibe as métricas de desempenho em um grid.
        """
        def create_grid(title, data):
            table = Table(show_header=True, header_style="bold magenta", box=None)
            table.add_column("📊 Métrica", style="cyan", no_wrap=True)
            table.add_column("📈 Valor", style="green")
            
            for key, value in data.items():
                try:
                    formatted_value = f"{value:.2f}" if isinstance(value, (int, float)) else str(value)
                    table.add_row(key, formatted_value)
                except Exception as e:
                    table.add_row(key, f"[bold red]Erro: {e}[/]")
            return table

        # Criando os dados com emojis
        text_metrics = {
            "📝 Palavras Únicas": unique_words,
            "🔤 Tokens Totais": tokens,
            "📚 Palavras Totais": words,
            "⚖️ Razão Token/Palavra": tokens/words if words > 0 else 0,
            "📊 Densidade Léxica": unique_words/words if words > 0 else 0
        }

        embedding_metrics = {
            "🧮 Dimensionalidade": model_dim,
            "🎯 Densidade Média": embedding_density,
            "⬇️ Norma Mínima": min_norm,
            "⬆️ Norma Máxima": max_norm,
            "📏 Amplitude": max_norm - min_norm
        }

        performance_metrics = {
            "⏱️ Tempo Total (s)": elapsed_time,
            "🚀 Tokens/Segundo": tokens/elapsed_time if elapsed_time > 0 else 0,
            "💻 CPU Total (%)": cpu_total,
            "🧠 RAM Usada (GB)": mem.used/1e9,
            "💪 Eficiência CPU": (tokens/elapsed_time)/(cpu_total + 1) if elapsed_time > 0 else 0
        }

        bert_metrics = {
            "🤖 Modelo": model_name,
            "🌡️ Temperatura": temperature,
            "🧩 Camadas Atenção": self.model.config.num_attention_heads,
            "🔢 Vocab Size": self.tokenizer.vocab_size,
            "📏 Max Seq Length": self.model.config.max_position_embeddings
        }

        advanced_metrics = {
            "🎯 Densidade Semântica": embedding_density * (unique_words/words if words > 0 else 0),
            "🧬 Complexidade": tokens/(unique_words + 1) if unique_words > 0 else 0,
            "📊 Índice Coesão": min_norm/max_norm if max_norm > 0 else 0,
            "🎓 Score Qualidade": embedding_density * unique_words/(tokens + 1) if tokens > 0 else 0,
            "⭐ Score Global": (embedding_density * unique_words)/(elapsed_time + 1) if elapsed_time > 0 else 0
        }

        # Criando os grids
        grid1 = create_grid("Análise Textual", text_metrics)
        grid2 = create_grid("Análise Embeddings", embedding_metrics)
        grid3 = create_grid("Performance", performance_metrics)
        grid4 = create_grid("BERT", bert_metrics)
        grid5 = create_grid("Métricas Avançadas", advanced_metrics)

        # Layout principal
        main_grid = Table.grid(padding=1)
        main_grid.add_column()
        main_grid.add_column()
        main_grid.add_column()

        # Adicionando os painéis ao grid
        main_grid.add_row(
            Panel(grid1, title="📊 Análise Textual", border_style="green"),
            Panel(grid2, title="🔢 Embeddings", border_style="blue"),
            Panel(grid3, title="⚡ Performance", border_style="yellow")
        )
        
        main_grid.add_row(
            Panel(grid4, title="🤖 BERT", border_style="magenta"),
            Panel(grid5, title="🔬 Avançado", border_style="cyan"),
            Panel.fit("") # Painel vazio para manter o grid balanceado
        )

        # Imprimindo o resultado
        console.print(main_grid)

if __name__ == "__main__":
    vectorizer = YAMLVectorizer()
    try:
        vectorizer.process_directory('generated-yaml-text-to-embedding')
    except Exception as e:
        print(f"[bold red]Erro crítico: {e}[/]")

# ----DAEDALUS----
