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
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        self.model.eval()

class ProcessingStats:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.total_palavras = 0
        self.palavras_unicas = 0
        self.palavras_processadas = 0
        self.palavras_novas = 0
        self.tempo_processamento = timedelta()
        self.falhas = 0
        self.inicio = time.time()
        
    def update_tempo(self):
        self.tempo_processamento = timedelta(seconds=int(time.time() - self.inicio))

# Variáveis globais para estatísticas
global_stats = ProcessingStats()

class GeradorVetorizadorContinuo:
    def __init__(self):
        # Inicializa BERT
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        self.model.eval()
        
        # Inicializa banco
        self.setup_database()
        
        self.stats = ProcessingStats()
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
        layout = Layout()
        layout.split_column(
            Layout(name="header"),
            Layout(name="main"),
            Layout(name="footer")
        )
        layout["main"].split_row(
            Layout(name="stats"),
            Layout(name="progress"),
            Layout(name="metrics"),
            Layout(name="status")
        )
        return layout
        
    def create_stats_panel(self):
        table = Table.grid()
        table.add_row(
            emoji.emojize(":hourglass_flowing_sand:"),
            f"Tempo: {self.stats.tempo_processamento}"
        )
        table.add_row(
            emoji.emojize(":input_numbers:"),
            f"Total Palavras: {self.stats.total_palavras}"
        )
        return Panel(table, title="Estatísticas", border_style="blue")

    def create_progress_panel(self):
        table = Table.grid()
        table.add_row(
            emoji.emojize(":check_mark_button:"),
            f"Processadas: {self.stats.palavras_processadas}"
        )
        table.add_row(
            emoji.emojize(":new_button:"),
            f"Novas: {self.stats.palavras_novas}"
        )
        return Panel(table, title="Progresso", border_style="green")

    def create_metrics_panel(self):
        table = Table.grid()
        taxa_sucesso = ((self.stats.palavras_processadas - self.stats.falhas) / 
                       max(self.stats.palavras_processadas, 1)) * 100
        table.add_row(
            emoji.emojize(":chart_increasing:"),
            f"Taxa Sucesso: {taxa_sucesso:.1f}%"
        )
        table.add_row(
            emoji.emojize(":cross_mark:"),
            f"Falhas: {self.stats.falhas}"
        )
        return Panel(table, title="Métricas", border_style="yellow")

    def create_status_panel(self, status: str):
        # Adiciona timestamp ao status
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_with_time = f"[{timestamp}]\n{status}"
        return Panel(status_with_time, title="Status Atual", border_style="purple")

    def update_display(self, status: str, live: Live):
        self.stats.update_tempo()
        self.layout["header"].update(
            Panel("Gerador e Vetorizador Contínuo de Palavras", style="bold cyan")
        )
        self.layout["main"]["stats"].update(self.create_stats_panel())
        self.layout["main"]["progress"].update(self.create_progress_panel())
        self.layout["main"]["metrics"].update(self.create_metrics_panel())
        self.layout["main"]["status"].update(self.create_status_panel(status))
        live.update(self.layout)

    def process_yaml_to_df(self, yaml_content: str) -> pd.DataFrame:
        palavras = self.extract_words(yaml_content)
        self.stats.total_palavras = len(palavras)
        self.stats.palavras_unicas = len(set(palavras))
        
        df = pd.DataFrame(list(palavras), columns=['word'])
        df['vector'] = df['word'].apply(self.generate_embedding)
        return df

    async def processar_palavra(self, palavra_inicial: str):
        df = None  # Initialize df outside the try block
        with Live(self.layout, refresh_per_second=4) as live:
            try:
                # 1. Preparação
                self.stats.reset()
                self.update_display("Iniciando novo processamento...", live)
                await asyncio.sleep(1)

                # 2. Gerando prompt
                self.update_display("Preparando prompt para IA...", live)
                prompt = f"""
                Gere uma lista de palavras relacionadas a '{palavra_inicial}' no seguinte formato YAML exato:

                lista_palavras:
                - palavra1
                - palavra2
                - palavra3

                Importante:
                - Use apenas o formato acima
                - Cada palavra deve estar em uma nova linha
                - Cada linha deve começar com hífen e espaço
                - Não inclua outros elementos ou formatação
                - Não use caracteres especiais
                - Use apenas palavras simples
                """
                await asyncio.sleep(1)

                # 3. Obtendo resposta da IA
                self.update_display("Aguardando resposta da IA...", live)
                yaml_content = self.get_gemini_response(prompt)
                if not yaml_content:
                    self.update_display("Erro: IA não retornou conteúdo válido", live)
                    self.stats.falhas += 1
                    await asyncio.sleep(2)
                    return

                await asyncio.sleep(1)

                # 4. Extraindo palavras do YAML
                self.update_display("Extraindo palavras do YAML...", live)
                palavras = self.extract_words(yaml_content)
                if not palavras:
                    self.stats.falhas += 1
                    self.update_display("Erro ao extrair palavras do YAML", live)
                    await asyncio.sleep(2)
                    return

                self.stats.total_palavras = len(palavras)
                self.stats.palavras_unicas = len(set(palavras))
                await asyncio.sleep(1)

                # 5. Criando DataFrame
                self.update_display("Criando DataFrame com palavras...", live)
                df = pd.DataFrame(list(palavras), columns=['word'])
                await asyncio.sleep(1)

                # 6. Gerando embeddings
                self.update_display("Gerando embeddings para cada palavra...", live)
                for idx, row in df.iterrows():
                    self.stats.palavras_processadas += 1
                    self.update_display(f"Gerando embedding para: {row['word']}", live)
                    df.at[idx, 'vector'] = self.generate_embedding(row['word'])
                    await asyncio.sleep(0.1)

                # 7. Salvando no banco
                self.update_display("Salvando vetores no banco de dados...", live)
                cursor = self.conn.cursor()
                
                for _, row in df.iterrows():
                    try:
                        exists = cursor.execute(
                            'SELECT 1 FROM word_vectors WHERE word = ?', 
                            (row['word'],)
                        ).fetchone()
                        
                        if exists is None:
                            self.stats.palavras_novas += 1
                            cursor.execute(
                                'INSERT INTO word_vectors (word, vector, palavra_origem) VALUES (?, ?, ?)',
                                (row['word'], row['vector'].tobytes(), palavra_inicial)
                            )
                            self.update_display(f"Salvando: {row['word']}", live)
                    except Exception as e:
                        self.stats.falhas += 1
                        self.update_display(f"Erro ao salvar: {row['word']}: {e}", live)
                    await asyncio.sleep(0.1)

                # 8. Finalizando
                self.conn.commit()
                self.update_display("Processamento concluído com sucesso!", live)
                await asyncio.sleep(2)

            except Exception as e:
                self.stats.falhas += 1
                self.update_display(f"Erro no processamento: {str(e)}", live)
                await asyncio.sleep(2)

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
    
    processador = GeradorVetorizadorContinuo()
    
    while True:
        palavras = input("\nDigite as palavras separadas por vírgula para processar (ou 'sair'): ").strip().lower().split(',')
        if palavras == ['sair']:
            break
        
        if palavras:
            tasks = [processador.processar_palavra(palavra.strip()) for palavra in palavras]
            await asyncio.gather(*tasks) # Aguardando as corrotinas
        else:
            console.print("[red]Entrada inválida![/red]")

    # Imprime estatísticas globais ao final
    global_stats.update_tempo()
    console.print(f"\nEstatísticas Globais:")
    console.print(f"Tempo total: {global_stats.tempo_processamento}")
    console.print(f"Total de palavras: {global_stats.total_palavras}")
    console.print(f"Palavras únicas: {global_stats.palavras_unicas}")
    console.print(f"Palavras processadas: {global_stats.palavras_processadas}")
    console.print(f"Novas palavras: {global_stats.palavras_novas}")
    console.print(f"Falhas: {global_stats.falhas}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Programa encerrado pelo usuário[/yellow]")
    except Exception as e:
        console.print(f"[red]Erro crítico: {e}[/red]")
