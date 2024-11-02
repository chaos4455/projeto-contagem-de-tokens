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

console = Console()

class YAMLVectorizer:
    def __init__(self):
        # Inicializa BERT
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        self.model.eval()
        
        # Inicializa banco
        self.setup_database()
    
    def setup_database(self):
        """Configura banco SQLite"""
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
        """Limpa e normaliza texto"""
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)  # Remove blocos código
        text = re.sub(r'http\S+', '', text)  # Remove URLs
        text = re.sub(r'[^\w\s]', ' ', text)  # Remove caracteres especiais
        return ' '.join(text.lower().split())
    
    def extract_words(self, yaml_content: dict) -> set:
        """Extrai palavras únicas do YAML"""
        words = set()
        
        def process_item(item):
            if isinstance(item, str):
                text = self.clean_text(item)
                words.update(word for word in text.split() 
                           if len(word) >= 2 and not word.isnumeric())
            elif isinstance(item, dict):
                for value in item.values():
                    process_item(value)
            elif isinstance(item, list):
                for value in item:
                    process_item(value)
        
        process_item(yaml_content)
        return words
    
    def count_tokens(self, text: str) -> int:
        """Conta tokens usando BERT tokenizer"""
        return len(self.tokenizer.tokenize(text))

    def count_words(self, text: str) -> int:
        """Conta palavras no texto"""
        return len(self.clean_text(text).split())

    def generate_embedding(self, word: str) -> np.ndarray:
        """Gera embedding para uma palavra"""
        try:
            with torch.no_grad():
                inputs = self.tokenizer(word, return_tensors='pt', padding=True).to(self.device)
                outputs = self.model(**inputs)
                embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy()[0]
                return embedding
        except Exception as e:
            print(f"Erro ao gerar embedding para '{word}': {e}")
            return np.zeros(768) # Retorna um vetor zero se houver erro

    
    def process_file(self, yaml_path: Path):
        """Processa um arquivo YAML"""
        try:
            # Carrega e extrai palavras do YAML
            with open(yaml_path) as f:
                content = yaml.safe_load(f)
            words = self.extract_words(content)
            text_content = yaml.safe_dump(content) # Pega o texto do YAML para contagem
            print(f"Processando arquivo: {yaml_path}, Palavras únicas encontradas: {len(words)}")

            # Gera e salva embeddings
            cursor = self.conn.cursor()
            embeddings = []
            for word in tqdm(words, desc=f"Gerando embeddings para {yaml_path}"):
                # Verifica se palavra já existe
                exists = cursor.execute('SELECT 1 FROM word_vectors WHERE word = ?', (word,)).fetchone()
                print(f"Palavra '{word}' já existe no banco de dados: {exists is not None}") # Corrigido: verifica explicitamente se exists é None
                if exists is None: # Corrigido: verifica explicitamente se exists é None
                    # Gera e salva embedding
                    vector = self.generate_embedding(word)
                    embeddings.append(vector)
                    cursor.execute(
                        'INSERT INTO word_vectors (word, vector) VALUES (?, ?)',
                        (word, vector.tobytes())
                    )
            
            self.conn.commit()
            return len(words), self.count_tokens(text_content), self.count_words(text_content), np.array(embeddings) # Retorna embeddings como array numpy
            
        except Exception as e:
            print(f"Erro ao processar {yaml_path}: {e}")
            return 0,0,0,np.array([]) # Retorna array numpy vazio em caso de erro

    def get_system_info(self):
        """Coleta informações do sistema"""
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_total = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        return cpu_percent, cpu_total, mem

    def get_bert_info(self):
        """Coleta informações do modelo BERT"""
        return self.model.config.name_or_path, self.model.config.hidden_size, 0.8 # Temperatura arbitrária

    def calculate_embedding_density(self, embeddings):
        if embeddings.size == 0: # Verifica se o array está vazio
            return 0.0
        return np.mean(np.linalg.norm(embeddings, axis=1))

    def calculate_embedding_stats(self, embeddings):
        if embeddings.size == 0: # Verifica se o array está vazio
            return {}, 0, 0
        embeddings_np = np.array(embeddings)
        mean = np.mean(embeddings_np, axis=0)
        std = np.std(embeddings_np, axis=0)
        min_norm = np.min(np.linalg.norm(embeddings_np, axis=1))
        max_norm = np.max(np.linalg.norm(embeddings_np, axis=1))
        return {"mean": mean.tolist(), "std": std.tolist()}, min_norm, max_norm


    def process_directory(self, yaml_dir: str):
        """Processa diretório de YAMLs"""
        yaml_files = list(Path(yaml_dir).glob('*.yaml'))
        total_words = 0
        total_tokens = 0
        total_unique_words = 0
        start_time = time.time()
        all_embeddings = []
        
        print(f"Processando {len(yaml_files)} arquivos YAML...")
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
        print(f"Embeddings shape: {np.array(all_embeddings).shape}")
        embedding_density = self.calculate_embedding_density(np.array(all_embeddings))
        embedding_stats, min_norm, max_norm = self.calculate_embedding_stats(np.array(all_embeddings))
        self.display_kpis(total_unique_words, total_tokens, total_words, len(yaml_files), elapsed_time, cpu_percent, cpu_total, mem, model_name, model_dim, temperature, embedding_density, embedding_stats, min_norm, max_norm)

    def display_kpis(self, unique_words, tokens, words, files_processed, elapsed_time, cpu_percent, cpu_total, mem, model_name, model_dim, temperature, embedding_density, embedding_stats, min_norm, max_norm):
        def create_grid(title, data, style):
            table = Table(title=title, style=style)
            table.add_column("Métrica", style="bold cyan")
            table.add_column("Valor", style="bold cyan") # Adiciona coluna para o valor
            for key, value in data.items():
                try:
                    formatted_value = round(value, 2) if isinstance(value, (int, float)) else value
                    table.add_row(Text(key, style="bold cyan"), Text(str(formatted_value), style=f"italic {style}"))
                except Exception as e:
                    print(f"Erro ao formatar valor {value}: {e}")
                    table.add_row(Text(key, style="bold cyan"), Text(str(value), style=f"italic red")) # Valor em vermelho se houver erro
            return table

        style1 = "bold green on black"
        style2 = "bold blue on black"
        style3 = "bold yellow on black"
        style4 = "bold magenta on black"
        style5 = "bold cyan on black"

        # Grid 1: Métricas de Texto
        grid1 = create_grid("Análise Textual 📝", {
            "Palavras Únicas": unique_words,
            "Tokens Totais": tokens,
            "Palavras Totais": words,
            "Razão Token/Palavra": tokens/words if words > 0 else 0,
            "Densidade Léxica": unique_words/words if words > 0 else 0,
            "Arquivos Processados": files_processed,
            "Média Tokens/Arquivo": tokens/files_processed if files_processed > 0 else 0,
            "Média Palavras/Arquivo": words/files_processed if files_processed > 0 else 0,
            "Complexidade Vocabular": unique_words/files_processed if files_processed > 0 else 0,
            "Taxa Compressão": unique_words/(tokens + 1)
        }, style1)

        # Grid 2: Métricas de Embedding
        grid2 = create_grid("Análise de Embeddings 📊", {
            "Dimensionalidade": model_dim,
            "Densidade Média": embedding_density,
            "Norma Mínima": min_norm,
            "Norma Máxima": max_norm,
            "Amplitude Norma": max_norm - min_norm,
            "Desvio Padrão Médio": np.mean(embedding_stats.get("std", [0])) if embedding_stats else 0,
            "Média Global": np.mean(embedding_stats.get("mean", [0])) if embedding_stats else 0,
            "Dispersão Vetorial": np.std(embedding_stats.get("std", [0])) if embedding_stats else 0,
            "Coeficiente Variação": np.std(embedding_stats.get("std", [0]))/np.mean(embedding_stats.get("mean", [1])) if embedding_stats and np.mean(embedding_stats.get("mean", [1])) != 0 else 0,
            "Entropia Embedding": -np.sum(np.square(embedding_stats.get("mean", [0]))) if embedding_stats else 0
        }, style2)

        # Grid 3: Métricas de Performance
        grid3 = create_grid("Performance do Sistema ⚙️", {
            "Tempo Total (s)": elapsed_time,
            "Tokens/Segundo": tokens/elapsed_time if elapsed_time > 0 else 0,
            "CPU Total (%)": cpu_total,
            "Média CPU/Core (%)": np.mean(cpu_percent),
            "RAM Utilizada (GB)": mem.used/1e9,
            "RAM Total (GB)": mem.total/1e9,
            "Uso RAM (%)": mem.percent,
            "Throughput (palavras/s)": words/elapsed_time if elapsed_time > 0 else 0,
            "Eficiência CPU": (tokens/elapsed_time)/(cpu_total + 1),
            "Eficiência Memória": (tokens * model_dim)/(mem.used + 1)
        }, style3)

        # Grid 4: Métricas BERT
        grid4 = create_grid("Análise BERT 🤖", {
            "Modelo": model_name,
            "Temperatura": temperature,
            "Camadas Atenção": self.model.config.num_attention_heads,
            "Camadas Hidden": self.model.config.num_hidden_layers,
            "Tamanho Vocabulário": self.tokenizer.vocab_size,
            "Max Seq Length": self.model.config.max_position_embeddings,
            "Dropout Rate": self.model.config.hidden_dropout_prob,
            "Attention Dropout": self.model.config.attention_probs_dropout_prob,
            "Parâmetros (M)": sum(p.numel() for p in self.model.parameters())/1e6,
            "Tipo Arquitetura": self.model.config.model_type
        }, style4)

        # Grid 5: Métricas Avançadas
        grid5 = create_grid("Métricas Avançadas 🔬", {
            "Densidade Semântica": embedding_density * (unique_words/words if words > 0 else 0),
            "Complexidade Contextual": tokens/(unique_words + 1) * np.mean(embedding_stats.get("std", [0])) if embedding_stats else 0,
            "Índice Coesão": min_norm/max_norm if max_norm > 0 else 0,
            "Saturação Embedding": np.mean(np.abs(embedding_stats.get("mean", [0]))) if embedding_stats else 0,
            "Eficiência Vetorial": unique_words/(model_dim * tokens) if tokens > 0 else 0,
            "Score Qualidade": (embedding_density * unique_words)/(tokens * np.std(embedding_stats.get("std", [0])) + 1) if embedding_stats else 0,
            "Índice Dispersão": np.max(embedding_stats.get("std", [0]))/np.min(embedding_stats.get("std", [0])) if embedding_stats and np.min(embedding_stats.get("std", [0])) > 0 else 0,
            "Cobertura Semântica": unique_words/self.tokenizer.vocab_size,
            "Eficiência Tokenização": tokens/(words * model_dim) if words > 0 else 0,
            "Score Global": (embedding_density * unique_words)/(elapsed_time * np.mean(embedding_stats.get("std", [0])) + 1) if embedding_stats else 0
        }, style5)

        console.print(grid1)
        console.print(grid2)
        console.print(grid3)
        console.print(grid4)
        console.print(grid5)


if __name__ == "__main__":
    vectorizer = YAMLVectorizer()
    try:
        vectorizer.process_directory('generated-yaml-text-to-embedding')
    except Exception as e:
        print(f"Erro crítico: {e}")

# ----DAEDALUS----
