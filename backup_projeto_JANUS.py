import zipfile
from datetime import datetime
import hashlib
from pathlib import Path
import shutil
import re
import os
import humanize
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich import box
from rich.text import Text
from rich.align import Align
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s', encoding='utf-8')

console = Console()

# 🎨 Emojis e ícones
EMOJI = {
    "backup": "📦",
    "pasta": "📁",
    "arquivo": "📄",
    "relógio": "⏱️",
    "hash": "🔐",
    "versão": "🔄",
    "sucesso": "✨",
    "erro": "❌",
    "alerta": "⚠️",
    "lixeira": "🗑️",
    "compressão": "🗜️",
    "disco": "💾",
    "foguete": "🚀",
    "gráfico": "📊",
    "config": "⚙️",
    "check": "✅"
}

def gerar_hash():
    """Gera um hash MD5 único baseado no timestamp."""
    timestamp = datetime.now().timestamp()
    return hashlib.md5(str(timestamp).encode()).hexdigest()[:8]

def calcular_tamanho_pasta(pasta):
    """Calcula o tamanho total (em bytes) de todos os arquivos dentro de uma pasta e suas subpastas."""
    total = 0
    try:
        for entry in pasta.rglob('*'):
            if entry.is_file():
                total += entry.stat().st_size
        return total
    except FileNotFoundError:
        logging.error(f"Pasta não encontrada: {pasta}")
        return 0
    except Exception as e:
        logging.exception(f"Erro ao calcular tamanho da pasta: {e}")
        return 0

def obter_ultima_versao(pasta_backup):
    """Obtém o número da próxima versão de backup a ser criada."""
    padrao = re.compile(r'.*-(\d{4})\.zip$')
    ultima_versao = 0
    
    if pasta_backup.exists():
        for arquivo in pasta_backup.glob('*.zip'):
            match = padrao.match(arquivo.name)
            if match:
                try:
                    versao = int(match.group(1))
                    ultima_versao = max(ultima_versao, versao)
                except (IndexError, ValueError) as e:
                    logging.warning(f"Erro ao processar nome de arquivo '{arquivo.name}': {e}")
    
    return ultima_versao + 1

def criar_dashboard(stats):
    """Cria um dashboard rico com estatísticas do backup."""
    layout = Layout()
    layout.split_column(
        Layout(name="header"),
        Layout(name="main"),
        Layout(name="footer")
    )
    
    # Header
    header = Panel(
        Align.center(
            f"{EMOJI['backup']} [bold cyan]Dashboard de Backup do Projeto[/bold cyan] {EMOJI['backup']}"
        ),
        style="blue"
    )
    layout["header"].update(header)
    
    # Main Content - Tabela de Estatísticas
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("Métrica", style="cyan")
    table.add_column("Valor", justify="right", style="green")
    
    for key, value in stats.items():
        table.add_row(key, str(value))
    
    layout["main"].update(Panel(table, title="[bold]Estatísticas do Backup[/bold]"))
    
    # Footer
    layout["footer"].update(Panel(
        f"{EMOJI['sucesso']} [green]Backup concluído com sucesso![/green] {EMOJI['sucesso']}",
        style="green"
    ))
    
    return layout

def criar_backup_projeto():
    """Cria um backup completo do projeto em um arquivo ZIP."""
    # 🛠️ Configurações iniciais
    pasta_raiz = Path.cwd()
    nome_projeto = pasta_raiz.name
    pasta_backup = pasta_raiz / "backup"
    pasta_backup.mkdir(exist_ok=True)
    
    # 📊 Estatísticas iniciais
    tamanho_inicial = calcular_tamanho_pasta(pasta_raiz)
    
    # 🏷️ Gerar nome do arquivo
    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    hash_unica = gerar_hash()
    versao = f"{obter_ultima_versao(pasta_backup):04d}"
    
    nome_zip = f"completo_backup_projeto-{nome_projeto}-{data_hora}-{hash_unica}-versao-{versao}.zip"
    caminho_zip = pasta_backup / nome_zip
    
    try:
        # 🚫 Lista de diretórios e arquivos a serem ignorados
        ignorar = {
            'backup', '__pycache__', '.git', '.pytest_cache',
            '.venv', 'venv', '.env', '.idea', '.vscode',
            'node_modules', 'dist', 'build'
        }
        
        arquivos_incluidos = 0
        tamanho_total = 0
        arquivos_ignorados = 0
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            
            task = progress.add_task(f"{EMOJI['compressão']} Compactando arquivos...", total=100)
            
            with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for item in pasta_raiz.rglob('*'):
                    if any(ignore in item.parts for ignore in ignorar):
                        arquivos_ignorados += 1
                        continue
                    
                    if item == caminho_zip:
                        continue
                    
                    if item.is_file():
                        caminho_relativo = item.relative_to(pasta_raiz)
                        zipf.write(item, caminho_relativo)
                        tamanho_total += item.stat().st_size
                        arquivos_incluidos += 1
                        try:
                            progress.update(task, advance=100/arquivos_incluidos)
                        except ZeroDivisionError:
                            logging.warning("Tentativa de divisão por zero. Ignorando.")

        # 📊 Preparar estatísticas para o dashboard
        stats = {
            f"{EMOJI['arquivo']} Arquivos Incluídos": arquivos_incluidos,
            f"{EMOJI['lixeira']} Arquivos Ignorados": arquivos_ignorados,
            f"{EMOJI['disco']} Tamanho Original": humanize.naturalsize(tamanho_inicial),
            f"{EMOJI['compressão']} Tamanho Final": humanize.naturalsize(caminho_zip.stat().st_size),
            f"{EMOJI['versão']} Versão do Backup": versao,
            f"{EMOJI['hash']} Hash": hash_unica,
            f"{EMOJI['relógio']} Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 🎨 Exibir dashboard
        console.print(criar_dashboard(stats))
        logging.info(f"Backup criado com sucesso: {caminho_zip}")
        return True
        
    except Exception as e:
        console.print(f"{EMOJI['erro']} [red]Erro ao criar backup: {str(e)}[/red]")
        logging.exception(f"Erro ao criar backup: {e}")
        return False

if __name__ == "__main__":
    try:
        console.print(Panel.fit(
            f"{EMOJI['foguete']} [bold cyan]Iniciando Backup Completo do Projeto[/bold cyan] {EMOJI['foguete']}",
            border_style="cyan"
        ))
        logging.info("Iniciando backup...")
        criar_backup_projeto()
    except KeyboardInterrupt:
        console.print(f"\n{EMOJI['alerta']} [yellow]Operação cancelada pelo usuário.[/yellow]")
        logging.warning("Operação cancelada pelo usuário.")
    except Exception as e:
        console.print(f"{EMOJI['erro']} [red]Erro inesperado: {str(e)}[/red]")
        logging.exception(f"Erro inesperado: {e}")

# ----JANUS----
