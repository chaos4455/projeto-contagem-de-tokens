from pathlib import Path
import sqlite3
import hashlib
from datetime import datetime
import logging
from rich.console import Console
from rich.panel import Panel
import yaml

console = Console()

class DocumentacaoAutomatizada:
    def __init__(self):
        self.pasta_raiz = Path(".")
        self.pasta_docs = Path("documentacao-automatizada")
        self.pasta_docs.mkdir(exist_ok=True)
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('documentacao_auto.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
    def gerar_hash_unico(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return hashlib.md5(timestamp.encode()).hexdigest()[:8]
        
    def ler_arquivo_python(self, arquivo):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                return {
                    'nome': arquivo.name,
                    'caminho': str(arquivo),
                    'conteudo': f.read(),
                    'tipo': 'python'
                }
        except Exception as e:
            logging.error(f"Erro ao ler arquivo Python {arquivo}: {e}")
            return None
            
    def analisar_estrutura_db(self, arquivo):
        try:
            conn = sqlite3.connect(arquivo)
            cursor = conn.cursor()
            
            # Obtém todas as tabelas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tabelas = cursor.fetchall()
            
            estrutura = {
                'nome': arquivo.name,
                'caminho': str(arquivo),
                'tipo': 'sqlite',
                'tabelas': {}
            }
            
            # Para cada tabela, obtém sua estrutura
            for tabela in tabelas:
                nome_tabela = tabela[0]
                cursor.execute(f"PRAGMA table_info({nome_tabela})")
                colunas = cursor.fetchall()
                estrutura['tabelas'][nome_tabela] = [
                    {'nome': col[1], 'tipo': col[2]} for col in colunas
                ]
                
            conn.close()
            return estrutura
            
        except Exception as e:
            logging.error(f"Erro ao analisar banco {arquivo}: {e}")
            return None
            
    def gerar_documentacao(self, arquivos_py, estruturas_db):
        hash_doc = self.gerar_hash_unico()
        nome_arquivo = f"DOCUMENTACAO_{hash_doc}.md"
        caminho_doc = self.pasta_docs / nome_arquivo
        
        conteudo = f"""# 📚 Documentação Automatizada do Projeto

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Documentação](https://img.shields.io/badge/docs-auto%20generated-green)

## 🏗️ Estrutura do Projeto

### 📝 Arquivos Python
"""
        
        # Documenta arquivos Python
        for arq in arquivos_py:
            if arq:
                conteudo += f"\n#### 🐍 `{arq['nome']}`\n"
                conteudo += f"- 📍 Caminho: `{arq['caminho']}`\n"
                
        # Documenta bancos SQLite
        conteudo += "\n### 🗄️ Bancos de Dados SQLite\n"
        for db in estruturas_db:
            if db:
                conteudo += f"\n#### 💾 `{db['nome']}`\n"
                conteudo += f"- 📍 Caminho: `{db['caminho']}`\n\n"
                conteudo += "**Tabelas:**\n"
                for tabela, colunas in db['tabelas'].items():
                    conteudo += f"\n- 📋 `{tabela}`\n"
                    for coluna in colunas:
                        conteudo += f"  - {coluna['nome']} ({coluna['tipo']})\n"
                        
        try:
            with open(caminho_doc, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            console.print(Panel(f"[green]✅ Documentação gerada com sucesso: {nome_arquivo}"))
            
        except Exception as e:
            logging.error(f"Erro ao gerar documentação: {e}")
            
    def executar(self):
        console.print("[bold blue]🚀 Iniciando geração de documentação automatizada...[/]")
        
        # Coleta arquivos Python
        arquivos_py = []
        for arquivo in self.pasta_raiz.glob('*.py'):
            resultado = self.ler_arquivo_python(arquivo)
            if resultado:
                arquivos_py.append(resultado)
                
        # Coleta bancos SQLite
        estruturas_db = []
        for arquivo in self.pasta_raiz.glob('*.db'):
            resultado = self.analisar_estrutura_db(arquivo)
            if resultado:
                estruturas_db.append(resultado)
                
        # Gera documentação
        self.gerar_documentacao(arquivos_py, estruturas_db)
        
if __name__ == "__main__":
    doc = DocumentacaoAutomatizada()
    doc.executar()