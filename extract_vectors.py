import sqlite3
import numpy as np
from transformers import BertTokenizer, BertModel
import torch
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich import box
from rich.table import Table
from threading import Thread, Lock
from queue import Queue
import time
from dataclasses import dataclass
from typing import Dict
import psutil
import GPUtil

@dataclass
class ProcessingStats:
    # Estatísticas de Processamento
    words_processed: int = 0
    words_per_second: float = 0.0
    current_word: str = ""
    last_words: list = None
    total_words: int = 0
    progress_percentage: float = 0.0
    
    # Métricas de Tempo
    bert_time: float = 0.0
    total_time: float = 0.0
    avg_processing_time: float = 0.0
    time_remaining: float = 0.0
    start_time: float = 0.0
    estimated_completion: str = ""
    
    # Métricas de Performance
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    gpu_usage: float = 0.0
    gpu_memory: float = 0.0
    queue_size: int = 0
    threads_active: int = 0
    
    # Métricas de Qualidade
    vector_similarity: float = 0.0
    error_count: int = 0
    success_rate: float = 100.0
    vector_dimension: int = 0
    bert_dimension: int = 0
    batch_accuracy: float = 0.0
    
    # Métricas de Sistema
    ram_available: float = 0.0
    swap_usage: float = 0.0
    disk_usage: float = 0.0
    network_usage: float = 0.0
    gpu_temperature: float = 0.0
    cpu_temperature: float = 0.0
    
    # Métricas de Batch
    batch_size: int = 0
    batch_count: int = 0
    current_batch: int = 0
    failed_batches: int = 0
    retry_count: int = 0
    batch_duration: float = 0.0
    
    # Cache e Buffer
    cache_hits: int = 0
    cache_misses: int = 0
    buffer_usage: float = 0.0
    memory_peaks: float = 0.0
    gc_collections: int = 0
    memory_leaks: int = 0
    
    def __post_init__(self):
        self.last_words = []
        self.start_time = time.time()

class VectorProcessor:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.stats = ProcessingStats()
        self.stats_lock = Lock()
        self.word_queue = Queue()
        self.stop_threads = False
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        self.model = BertModel.from_pretrained('bert-base-multilingual-cased')
        
    def create_layout(self) -> Layout:
        """Cria o layout correto com 4 painéis"""
        layout = Layout()
        
        # Divisão principal em superior e inferior
        layout.split_column(
            Layout(name="upper", ratio=1),
            Layout(name="lower", ratio=1)
        )
        
        # Divisão superior em dois painéis
        layout["upper"].split_row(
            Layout(name="processing"),
            Layout(name="system")
        )
        
        # Divisão inferior em dois painéis
        layout["lower"].split_row(
            Layout(name="metrics"),
            Layout(name="words")  # Corrigido: nome do painel alterado de 'word' para 'words'
        )
        
        return layout

    def generate_processing_panel(self) -> Panel:
        """Painel de processamento com emojis e cores"""
        table = Table.grid()
        table.add_row("🔄 Processadas:", f"[green]{self.stats.words_processed:,}[/]")
        table.add_row("⚡ Velocidade:", f"[yellow]{self.stats.words_per_second:.2f} palavras/s[/]")
        table.add_row("📊 Progresso:", f"[cyan]{self.stats.progress_percentage:.1f}%[/]")
        table.add_row("📚 Total:", f"[blue]{self.stats.total_words:,}[/]")
        table.add_row("📦 Batch:", f"[magenta]{self.stats.current_batch}/{self.stats.batch_count}[/]")
        table.add_row("🎯 Cache Hits:", f"[green]{self.stats.cache_hits:,}[/]")
        table.add_row("❌ Erros:", f"[red]{self.stats.error_count}[/]")
        table.add_row("✅ Sucesso:", f"[green]{self.stats.success_rate:.1f}%[/]")
        table.add_row("🔁 Retentativas:", f"[yellow]{self.stats.retry_count}[/]")
        table.add_row("♻️ GC Coletas:", f"[blue]{self.stats.gc_collections}[/]")
        table.add_row("📈 Buffer:", f"[cyan]{self.stats.buffer_usage:.1f}%[/]")
        table.add_row("🚨 Vazamentos:", f"[red]{self.stats.memory_leaks}[/]")
        return Panel(table, title="🎮 Processamento", border_style="blue", box=box.ROUNDED)

    def generate_performance_panel(self) -> Panel:
        """Painel de performance do sistema"""
        table = Table.grid()
        table.add_row("🔲 CPU:", self._get_usage_bar(self.stats.cpu_usage))
        table.add_row("💾 RAM:", self._get_usage_bar(self.stats.memory_usage))
        table.add_row("🎮 GPU:", self._get_usage_bar(self.stats.gpu_usage))
        table.add_row("📊 GPU Mem:", self._get_usage_bar(self.stats.gpu_memory))
        table.add_row("💿 Disco:", self._get_usage_bar(self.stats.disk_usage))
        table.add_row("📡 Rede:", f"[blue]{self.stats.network_usage:.1f} MB/s[/]")
        table.add_row("🌡️ CPU Temp:", self._get_temp_indicator(self.stats.cpu_temperature))
        table.add_row("🌡️ GPU Temp:", self._get_temp_indicator(self.stats.gpu_temperature))
        table.add_row("💫 Swap:", self._get_usage_bar(self.stats.swap_usage))
        table.add_row("🆓 RAM Livre:", f"[green]{self.stats.ram_available:.1f} GB[/]")
        table.add_row("🧵 Threads:", f"[cyan]{self.stats.threads_active}[/]")
        table.add_row("📥 Fila:", f"[magenta]{self.stats.queue_size}[/]")
        return Panel(table, title="⚙️ Sistema", border_style="green", box=box.ROUNDED)

    def generate_metrics_panel(self) -> Panel:
        """Painel de métricas de processamento"""
        table = Table.grid()
        table.add_row("⚡ BERT:", f"[cyan]{self.stats.bert_time:.3f}s[/]")
        table.add_row("⏱️ Total:", f"[yellow]{self.format_time(self.stats.total_time)}[/]")
        table.add_row("⌛ Média:", f"[green]{self.stats.avg_processing_time:.3f}s[/]")
        table.add_row("🕒 Restante:", f"[blue]{self.format_time(self.stats.time_remaining)}[/]")
        table.add_row("📊 Batch:", f"[magenta]{self.stats.batch_duration:.2f}s[/]")
        table.add_row("🎯 Similar:", self._get_similarity_indicator(self.stats.vector_similarity))
        table.add_row("📏 Vec Dim:", f"[yellow]{self.stats.vector_dimension}[/]")
        table.add_row("📐 BERT Dim:", f"[yellow]{self.stats.bert_dimension}[/]")
        table.add_row("📈 Precisão:", self._get_accuracy_indicator(self.stats.batch_accuracy))
        table.add_row("🏁 Término:", f"[blue]{self.stats.estimated_completion}[/]")
        table.add_row("📊 Pico Mem:", f"[red]{self.stats.memory_peaks:.1f} MB[/]")
        table.add_row("💔 Cache Miss:", f"[red]{self.stats.cache_misses}[/]")
        return Panel(table, title="📊 Métricas", border_style="yellow", box=box.ROUNDED)

    def generate_word_panel(self) -> Panel:
        """Painel de palavras processadas"""
        words_table = Table.grid()
        for i, word in enumerate(reversed(self.stats.last_words[-12:])):
            emoji = "🔄" if i == 0 else "✅"
            words_table.add_row(f"{emoji} {word}")
        return Panel(words_table, title="📝 Últimas Palavras", border_style="red", box=box.ROUNDED)

    def _get_usage_bar(self, percentage: float) -> str:
        """Gera barra de progresso colorida"""
        blocks = "█" * int(percentage / 10) + "░" * (10 - int(percentage / 10))
        color = "green" if percentage < 70 else "yellow" if percentage < 90 else "red"
        return f"[{color}]{blocks}[/] {percentage:.1f}%"

    def _get_temp_indicator(self, temp: float) -> str:
        """Gera indicador de temperatura colorido"""
        if temp < 60:
            return f"[green]🌡️ {temp:.1f}°C[/]"
        elif temp < 80:
            return f"[yellow]🌡️ {temp:.1f}°C[/]"
        else:
            return f"[red]🌡️ {temp:.1f}°C[/]"

    def _get_similarity_indicator(self, similarity: float) -> str:
        """Gera indicador de similaridade colorido"""
        if similarity > 0.8:
            return f"[green]🎯 {similarity:.3f}[/]"
        elif similarity > 0.5:
            return f"[yellow]🎯 {similarity:.3f}[/]"
        else:
            return f"[red]🎯 {similarity:.3f}[/]"

    def _get_accuracy_indicator(self, accuracy: float) -> str:
        """Gera indicador de precisão colorido"""
        if accuracy > 90:
            return f"[green]💯 {accuracy:.1f}%[/]"
        elif accuracy > 70:
            return f"[yellow]📈 {accuracy:.1f}%[/]"
        else:
            return f"[red]📉 {accuracy:.1f}%[/]"

    def format_time(self, seconds: float) -> str:
        """Formata tempo em formato legível"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = seconds % 60
            return f"{minutes}m {secs:.0f}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m"

    def update_system_stats(self):
        """Atualiza estatísticas do sistema com tratamento de erros"""
        while not self.stop_threads:
            try:
                with self.stats_lock:
                    # CPU e Memória
                    self.stats.cpu_usage = psutil.cpu_percent(interval=1)
                    mem = psutil.virtual_memory()
                    self.stats.memory_usage = mem.percent
                    self.stats.ram_available = mem.available / (1024**3)
                    
                    # Disco
                    disk = psutil.disk_usage('/')
                    self.stats.disk_usage = disk.percent
                    
                    # GPU (com tratamento de erro)
                    try:
                        gpus = GPUtil.getGPUs()
                        if gpus:
                            gpu = gpus[0]
                            self.stats.gpu_usage = gpu.load * 100
                            self.stats.gpu_memory = gpu.memoryUtil * 100
                            self.stats.gpu_temperature = gpu.temperature
                    except Exception:
                        self.stats.gpu_usage = 0
                        self.stats.gpu_memory = 0
                        self.stats.gpu_temperature = 0
                    
                    # Cálculos de performance
                    current_time = time.time()
                    self.stats.total_time = current_time - self.stats.start_time
                    
                    if self.stats.words_processed > 0:
                        self.stats.words_per_second = self.stats.words_processed / self.stats.total_time
                        self.stats.progress_percentage = (self.stats.words_processed / self.stats.total_words) * 100 if self.stats.total_words > 0 else 0
                        
                        if self.stats.words_per_second > 0:
                            remaining_words = self.stats.total_words - self.stats.words_processed
                            self.stats.time_remaining = remaining_words / self.stats.words_per_second
                            self.stats.estimated_completion = time.strftime(
                                '%H:%M:%S', 
                                time.localtime(current_time + self.stats.time_remaining)
                            )
                    
                    # Atualiza tamanho da fila
                    self.stats.queue_size = self.word_queue.qsize()
                    
            except Exception as e:
                print(f"Erro ao atualizar estatísticas: {e}")
            
            time.sleep(1)

    def process_vectors(self):
        """Processa os vetores da fila usando BERT"""
        while not self.stop_threads or not self.word_queue.empty():
            try:
                # Pega palavra da fila com timeout
                word, vector_blob = self.word_queue.get(timeout=1)
                start_time = time.time()
                
                # Atualiza palavra atual nas estatísticas
                with self.stats_lock:
                    self.stats.current_word = word
                    if len(self.stats.last_words) >= 12:
                        self.stats.last_words.pop(0)
                    self.stats.last_words.append(word)

                # Converte BLOB para numpy array
                vector = np.frombuffer(vector_blob, dtype=np.float32)
                self.stats.vector_dimension = vector.shape[0]

                # Processa com BERT
                inputs = self.tokenizer(word, return_tensors="pt", padding=True, truncation=True)
                
                with torch.no_grad():
                    outputs = self.model(**inputs)
                
                bert_embedding = outputs.last_hidden_state[:, 0, :].numpy()
                self.stats.bert_dimension = bert_embedding.shape[1]

                # Calcula similaridade se as dimensões forem compatíveis
                if vector.shape[0] == bert_embedding.shape[1]:
                    similarity = np.dot(vector, bert_embedding[0]) / (
                        np.linalg.norm(vector) * np.linalg.norm(bert_embedding[0]))
                    
                    with self.stats_lock:
                        self.stats.vector_similarity = similarity
                        self.stats.bert_time = time.time() - start_time
                        self.stats.words_processed += 1
                        self.stats.batch_accuracy = (similarity + 1) / 2 * 100  # Converte similaridade para porcentagem
                        self.stats.success_rate = ((self.stats.words_processed - self.stats.error_count) 
                                                 / self.stats.words_processed * 100)
                        
                        # Atualiza métricas de batch
                        self.stats.batch_duration = time.time() - start_time
                        self.stats.current_batch += 1
                        
                        # Atualiza métricas de cache
                        self.stats.cache_hits += 1
                else:
                    with self.stats_lock:
                        self.stats.error_count += 1
                        self.stats.cache_misses += 1

                self.word_queue.task_done()

            except Queue.Empty:
                continue
            except Exception as e:
                print(f"Erro no processamento: {e}")
                with self.stats_lock:
                    self.stats.error_count += 1
                    self.stats.failed_batches += 1

    def run(self):
        """Executa o processamento principal com melhor controle de fluxo"""
        try:
            # Inicializa conexão com banco
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Obtém total de palavras
            cursor.execute("SELECT COUNT(*) FROM word_vectors")
            self.stats.total_words = cursor.fetchone()[0]
            self.stats.batch_count = (self.stats.total_words + 99) // 100  # Calcula número de batches
            
            # Inicia threads
            stats_thread = Thread(target=self.update_system_stats)
            processing_threads = [Thread(target=self.process_vectors) for _ in range(4)]
            
            stats_thread.start()
            for thread in processing_threads:
                thread.start()
                with self.stats_lock:
                    self.stats.threads_active += 1
            
            # Cria layout
            layout = self.create_layout()
            
            # Processa palavras com feedback visual
            with Live(layout, refresh_per_second=4) as live:
                batch_size = 100
                current_batch = []
                
                cursor.execute("SELECT word, vector FROM word_vectors")
                
                for word, vector_blob in cursor:
                    current_batch.append((word, vector_blob))
                    
                    # Processa batch quando atingir tamanho máximo
                    if len(current_batch) >= batch_size:
                        for item in current_batch:
                            self.word_queue.put(item)
                        
                        with self.stats_lock:
                            self.stats.batch_size = len(current_batch)
                        
                        current_batch = []
                    
                    # Atualiza interface
                    layout["processing"].update(self.generate_processing_panel())
                    layout["system"].update(self.generate_performance_panel())
                    layout["metrics"].update(self.generate_metrics_panel())
                    layout["words"].update(self.generate_word_panel())
                
                # Processa último batch se houver
                if current_batch:
                    for item in current_batch:
                        self.word_queue.put(item)
                
                # Espera processamento terminar
                self.word_queue.join()
            
            # Finaliza threads
            self.stop_threads = True
            stats_thread.join()
            for thread in processing_threads:
                thread.join()
                with self.stats_lock:
                    self.stats.threads_active -= 1
            
            conn.close()
            
        except Exception as e:
            print(f"Erro durante execução: {e}")
            raise

if __name__ == "__main__":
    processor = VectorProcessor("vectors_continuo.db")
    processor.run()
