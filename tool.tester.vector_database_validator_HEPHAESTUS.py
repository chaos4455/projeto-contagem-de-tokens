import sqlite3
import numpy as np
import torch
from transformers import BertTokenizer, BertModel
from rich.console import Console
from rich.progress import track
from rich.panel import Panel
import yaml
from pathlib import Path
from datetime import datetime
import logging
from sklearn.metrics.pairwise import cosine_similarity
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from hashlib import sha256
from queue import Queue
import json
import aiofiles

# Configuração de logging
logging.basicConfig(filename='blob_decoder.log', level=logging.ERROR,
                   format='%(asctime)s - %(levelname)s - %(message)s')

console = Console()

# Configuração do banco de dados
DATABASE_PATH = 'vectors_continuo.db'

class BlobDecoder:
    def __init__(self):
        # Inicializa BERT
        try:
            self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            self.model = BertModel.from_pretrained('bert-base-uncased')
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.model.to(self.device)
            self.model.eval()
            console.print(f"[green]Usando dispositivo: {self.device}")
        except Exception as e:
            logging.error(f"Erro ao inicializar BERT: {e}")
            raise RuntimeError("Falha na inicialização do modelo BERT")

        self.processed_queue = Queue()
        self.metrics = {
            'total_processed': 0,
            'successful_decodes': 0,
            'failed_decodes': 0,
            'avg_processing_time': 0,
            'max_similarity_score': 0,
            'min_similarity_score': 1,
            'current_batch_size': 0,
            'memory_usage': 0,
            'vectors_per_second': 0,
            'error_rate': 0
        }
        self.lock = threading.Lock()

    def create_grid_layout(self):
        """Cria layout com 4 grids de métricas"""
        layout = Layout()
        layout.split_column(
            Layout(name="upper"),
            Layout(name="lower")
        )
        layout["upper"].split_row(
            Layout(name="metrics1"),
            Layout(name="metrics2")
        )
        layout["lower"].split_row(
            Layout(name="metrics3"),
            Layout(name="metrics4")
        )
        return layout

    def create_metrics_table(self, title, metrics_dict):
        table = Table(title=title)
        table.add_column("Métrica")
        table.add_column("Valor")
        for k, v in metrics_dict.items():
            table.add_row(k, str(v))
        return table

    def blob_to_vector(self, blob):
        """Converte BLOB para vetor numpy"""
        try:
            return np.frombuffer(blob, dtype=np.float32)
        except Exception as e:
            logging.error(f"Erro ao converter blob para vetor: {e}")
            return None

    def vector_to_text(self, vector):
        """Converte vetor para texto usando BERT"""
        try:
            # Redimensiona o vetor se necessário
            if vector.shape[0] == 512:
                vector = np.pad(vector, (0, 256), 'constant')
            
            with torch.no_grad():
                # Frases de referência para comparação
                frases_referencia = [
                    "Este é um texto de exemplo em português",
                    "Outro texto para comparação",
                    "Mais uma frase de teste",
                    "Exemplo de conteúdo textual",
                    "Frase para análise vetorial",
                    "Conteúdo do documento",
                    "Informação processada",
                    "Dados convertidos",
                    "Texto extraído",
                    "Resultado da análise"
                ]
                
                # Codifica as frases de referência
                inputs = self.tokenizer(frases_referencia, padding=True, truncation=True, return_tensors="pt")
                outputs = self.model(**inputs)
                embeddings = outputs.last_hidden_state.mean(dim=1)
                
                # Calcula similaridade
                vector_tensor = torch.tensor(vector).unsqueeze(0)
                similarities = cosine_similarity(vector_tensor, embeddings.numpy())[0]
                
                return frases_referencia[np.argmax(similarities)]
        except Exception as e:
            logging.error(f"Erro na conversão do vetor para texto: {e}")
            return "Erro na conversão"

    async def process_vector(self, vector_blob, cursor_id):
        try:
            vector = self.blob_to_vector(vector_blob[0])
            if vector is not None:
                text = self.vector_to_text(vector)
                vector_preview = str(vector[:5]) + "..."
                
                with self.lock:
                    self.metrics['total_processed'] += 1
                    self.metrics['successful_decodes'] += 1
                
                return {
                    'text': text,
                    'vector_preview': vector_preview,
                    'cursor_id': cursor_id,
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            logging.error(f"Erro no processamento do vetor {cursor_id}: {e}")
            with self.lock:
                self.metrics['failed_decodes'] += 1
            return None

    async def stream_to_yaml(self, data, output_file):
        """Grava dados incrementalmente no YAML"""
        async with aiofiles.open(output_file, 'a') as f:
            await f.write(yaml.dump([data], allow_unicode=True))

    async def process_database(self):
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            # Verifica se o banco existe e tem a estrutura correta
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='word_vectors'")
            if not cursor.fetchone():
                raise Exception("Tabela word_vectors não encontrada no banco de dados")
            
            # Obtém total de registros
            cursor.execute("SELECT COUNT(*) FROM word_vectors")
            total_registros = cursor.fetchone()[0]
            console.print(f"[blue]Total de registros encontrados: {total_registros}")
            
            # Obtém todos os vetores
            cursor.execute("SELECT vector FROM word_vectors")
            
            process_hash = sha256(str(datetime.now()).encode()).hexdigest()[:8]
            output_file = f"decoded_vectors_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{process_hash}.yaml"

            layout = self.create_grid_layout()

            with Live(layout, refresh_per_second=4) as live:
                with ThreadPoolExecutor(max_workers=4) as executor:
                    futures = []
                    for cursor_id, vector_blob in enumerate(cursor.fetchall()):
                        future = asyncio.create_task(self.process_vector(vector_blob, cursor_id))
                        futures.append(future)

                        if len(futures) >= 10:  # Processa em lotes de 10
                            completed = await asyncio.gather(*futures)
                            for result in completed:
                                if result:
                                    await self.stream_to_yaml(result, output_file)
                            
                            # Atualiza displays
                            layout["metrics1"].update(self.create_metrics_table("Métricas Gerais", 
                                dict(list(self.metrics.items())[:3])))
                            layout["metrics2"].update(self.create_metrics_table("Performance", 
                                dict(list(self.metrics.items())[3:6])))
                            layout["metrics3"].update(self.create_metrics_table("Recursos", 
                                dict(list(self.metrics.items())[6:8])))
                            layout["metrics4"].update(self.create_metrics_table("Status", 
                                dict(list(self.metrics.items())[8:])))
                            
                            futures = []

            console.print(Panel(f"""[green]Processamento concluído com sucesso!
            - Arquivo YAML: {output_file}
            - Total de vetores processados: {self.metrics['total_processed']}/{total_registros}
            - Timestamp: {datetime.now().strftime('%Y%m%d_%H%M%S')}_{process_hash}"""))
            
        except Exception as e:
            logging.error(f"Erro no processamento: {e}")
            console.print(f"[red]Erro: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

if __name__ == "__main__":
    console.print(Panel("[yellow]Iniciando decodificação de vetores do banco de dados"))
    decoder = BlobDecoder()
    asyncio.run(decoder.process_database())