import os
import sys
import yaml
import json
import sqlite3
import hashlib
import asyncio
import logging
import google.generativeai as genai
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel

# Configuração do Google Gemini
GOOGLE_API_KEY = "AIzaSyCEagEEnX-RdkW3-jCAb0H9nrTsgcE-Qqo"
genai.configure(api_key=GOOGLE_API_KEY)

class EvolucaoFramework:
    def __init__(self):
        self.console = Console()
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('evolucao_framework.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('EvolucaoFramework')

    # Funções de Utilidade
    def gerar_hash_unico(self, input_text: str = None) -> str:
        """Gera um hash único baseado em texto ou timestamp"""
        if not input_text:
            input_text = str(datetime.now())
        hash_object = hashlib.sha256(input_text.encode())
        return hash_object.hexdigest()[:8]

    # Funções de Banco de Dados
    def criar_conexao_db(self, db_path: str) -> sqlite3.Connection:
        """Cria uma conexão com banco de dados SQLite"""
        try:
            return sqlite3.connect(db_path)
        except Exception as e:
            self.logger.error(f"Erro ao conectar ao banco de dados: {e}")
            raise

    # Funções de Embeddings e IA
    async def gerar_embeddings(self, texto: str, modelo: str = "gemini-1.0-pro") -> Dict:
        """Gera embeddings usando o Google Gemini"""
        try:
            response = await self.model.generate_content_async(texto)
            return {
                "texto": texto,
                "embedding": response.text,
                "timestamp": datetime.now().isoformat(),
                "modelo": modelo
            }
        except Exception as e:
            self.logger.error(f"Erro ao gerar embeddings: {e}")
            return None

    # Templates de Prompts
    PROMPT_TEMPLATES = {
        "documentacao": """
        Analise o seguinte código e gere uma documentação técnica detalhada:
        
        Código: {codigo}
        
        Por favor, inclua:
        - Visão geral
        - Funcionalidades principais
        - Parâmetros e retornos
        - Exemplos de uso
        - Considerações de performance
        """,
        
        "analise_codigo": """
        Faça uma análise profunda do seguinte código:
        
        {codigo}
        
        Considere:
        - Qualidade do código
        - Possíveis melhorias
        - Pontos de atenção
        - Boas práticas
        """
    }

    async def gerar_documentacao_ia(self, codigo: str) -> str:
        """Gera documentação usando IA"""
        prompt = self.PROMPT_TEMPLATES["documentacao"].format(codigo=codigo)
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            self.logger.error(f"Erro ao gerar documentação: {e}")
            return None

    # Funções de Arquivo
    def salvar_yaml(self, dados: Dict, caminho: str) -> bool:
        """Salva dados em formato YAML"""
        try:
            with open(caminho, 'w', encoding='utf-8') as f:
                yaml.dump(dados, f, allow_unicode=True)
            return True
        except Exception as e:
            self.logger.error(f"Erro ao salvar YAML: {e}")
            return False

    # Funções de Backup
    def criar_backup(self, origem: str, destino: str) -> bool:
        """Cria backup de arquivos e diretórios"""
        try:
            if os.path.isfile(origem):
                import shutil
                shutil.copy2(origem, destino)
            else:
                shutil.copytree(origem, destino)
            return True
        except Exception as e:
            self.logger.error(f"Erro ao criar backup: {e}")
            return False

    # Funções de Processamento
    async def processar_arquivo(self, caminho: str) -> Dict:
        """Processa um arquivo e retorna suas informações"""
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            info = {
                "caminho": caminho,
                "hash": self.gerar_hash_unico(conteudo),
                "tamanho": os.path.getsize(caminho),
                "ultima_modificacao": datetime.fromtimestamp(os.path.getmtime(caminho)).isoformat(),
                "conteudo": conteudo
            }
            return info
        except Exception as e:
            self.logger.error(f"Erro ao processar arquivo: {e}")
            return None

    # Interface CLI
    def exibir_progresso(self, total: int):
        """Cria uma barra de progresso rica"""
        return Progress()

    def exibir_painel(self, titulo: str, conteudo: str):
        """Exibe um painel rico com informações"""
        self.console.print(Panel(conteudo, title=titulo))

    # Funções de Vetorização
    async def vetorizar_texto(self, texto: str) -> Dict:
        """Vetoriza texto usando embeddings"""
        try:
            embedding = await self.gerar_embeddings(texto)
            return {
                "texto_original": texto,
                "vetor": embedding,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Erro ao vetorizar texto: {e}")
            return None

# Exemplo de uso
if __name__ == "__main__":
    framework = EvolucaoFramework()
    
    # Exemplo de uso do framework
    async def exemplo():
        texto = "Exemplo de texto para processamento"
        embedding = await framework.vetorizar_texto(texto)
        framework.exibir_painel("Resultado", str(embedding))

    asyncio.run(exemplo()) 