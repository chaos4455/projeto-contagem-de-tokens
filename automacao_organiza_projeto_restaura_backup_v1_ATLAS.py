import os
import shutil
from pathlib import Path
import subprocess
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
import hashlib
from datetime import datetime
import logging

# Configura o logging com suporte UTF-8
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s', encoding='utf-8')

class AutomacaoBackup:
    """
    Automatiza o processo de backup, restauração e organização de arquivos de um projeto.

    Utiliza a biblioteca `rich` para exibir mensagens formatadas no console e `logging` para registrar eventos em um arquivo de log.
    """
    def __init__(self):
        self.console = Console()
        self.pasta_raiz = Path(".")
        self.estatisticas = {
            'arquivos_movidos': 0,
            'arquivos_renomeados': 0,
            'zips_organizados': 0
        }
        self.setup_pastas()


    def setup_pastas(self):
        """Cria as pastas necessárias se não existirem."""
        pastas = ['logs', 'txt', 'json', 'zip']
        for pasta in pastas:
            Path(pasta).mkdir(exist_ok=True)
        logging.info("Pastas criadas ou verificadas.")


    def gerar_hash_unico(self, arquivo: Path) -> str:
        """Gera um hash único baseado no nome do arquivo e timestamp."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        hash_base = f"{arquivo.stem}_{timestamp}"
        return hashlib.md5(hash_base.encode()).hexdigest()[:8]

    def mover_arquivo_com_verificacao(self, arquivo: Path, pasta_destino: Path) -> bool:
        """Move arquivo para destino, tratando duplicatas com hash único."""
        try:
            nome_arquivo = arquivo.name
            caminho_destino = pasta_destino / nome_arquivo

            if caminho_destino.exists():
                # Gera novo nome com hash
                hash_unico = self.gerar_hash_unico(arquivo)
                novo_nome = f"{arquivo.stem}_{hash_unico}{arquivo.suffix}"
                caminho_destino = pasta_destino / novo_nome
                self.estatisticas['arquivos_renomeados'] += 1
                
                msg = f"Arquivo renomeado: {novo_nome} (original: {nome_arquivo})"
                self.console.print(f"[yellow]⚠️ {msg}[/]")
                logging.warning(msg)

            shutil.move(str(arquivo), str(caminho_destino))
            self.estatisticas['arquivos_movidos'] += 1
            
            msg = f"Arquivo movido: {arquivo} → {caminho_destino}"
            logging.info(msg)
            return True

        except Exception as e:
            msg = f"Erro ao mover {arquivo}: {str(e)}"
            logging.exception(msg)
            self.console.print(f"[red]❌ {msg}[/]")
            return False

    def organizar_arquivos(self):
        """Organiza os arquivos por extensão."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task("[cyan]Organizando arquivos...", total=None)
            
            extensoes = {
                '.log': 'logs',
                '.txt': 'txt',
                '.json': 'json',
                '.zip': 'zip'
            }

            arquivos_para_mover = []
            for arquivo in self.pasta_raiz.glob('*'):
                if arquivo.is_file():
                    ext = arquivo.suffix.lower()
                    if ext in extensoes:
                        arquivos_para_mover.append((arquivo, extensoes[ext]))

            for arquivo, pasta_destino in arquivos_para_mover:
                if arquivo.suffix.lower() == '.zip':
                    self.estatisticas['zips_organizados'] += 1
                self.mover_arquivo_com_verificacao(arquivo, Path(pasta_destino))

            progress.update(task, completed=True)
            self.mostrar_estatisticas_organizacao()
            logging.info("Organização de arquivos concluída.")

    def mostrar_estatisticas_organizacao(self):
        """Exibe as estatísticas de organização em uma tabela."""
        table = Table(title="📊 Estatísticas de Organização")
        table.add_column("Métrica", style="cyan")
        table.add_column("Quantidade", justify="right", style="green")

        table.add_row("Arquivos Movidos", str(self.estatisticas['arquivos_movidos']))
        table.add_row("Arquivos Renomeados", str(self.estatisticas['arquivos_renomeados']))
        table.add_row("ZIPs Organizados", str(self.estatisticas['zips_organizados']))

        self.console.print(table)
        logging.info(f"Estatísticas de organização: {self.estatisticas}")


    def executar_script(self, nome_script, descricao):
        """Executa um script Python e monitora sua execução."""
        self.console.print(f"\n[bold blue]🚀 Executando: {descricao}[/]")
        logging.info(f"Iniciando execução: {descricao} ({nome_script})")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(f"[cyan]Processando {nome_script}...", total=None)
            
            try:
                resultado = subprocess.run(
                    f'python "{nome_script}"',
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore'
                )
                
                if resultado.returncode == 0:
                    msg = f"{descricao} concluído com sucesso!"
                    self.console.print(f"[green]✅ {msg}[/]")
                    logging.info(msg)
                    
                    if resultado.stdout.strip():
                        logging.info(f"Saída do script {nome_script}:\n{resultado.stdout}")
                        self.console.print("[dim]Saída do script:[/]")
                        self.console.print(resultado.stdout)
                else:
                    msg = f"Erro ao executar {descricao}"
                    self.console.print(f"[red]❌ {msg}[/]")
                    logging.error(msg)
                    
                    if resultado.stderr.strip():
                        erro = f"Erro: {resultado.stderr}"
                        logging.error(erro)
                        self.console.print(f"[red]{erro}[/]")
                
                progress.update(task, completed=True)
                return resultado.returncode == 0
                
            except Exception as e:
                msg = f"Erro na execução de {nome_script}: {str(e)}"
                self.console.print(f"[red]❌ {msg}[/]")
                logging.exception(msg)
                progress.update(task, completed=True)
                return False

    def mostrar_sumario_final(self, sucessos, total):
        """Exibe um sumário final da execução da automação."""
        table = Table(title="📑 Sumário Final de Execução")
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", justify="right", style="green")

        table.add_row("Scripts Executados", str(total))
        table.add_row("Sucessos", str(sucessos))
        table.add_row("Falhas", str(total - sucessos))
        table.add_row("Taxa de Sucesso", f"{(sucessos/total)*100:.1f}%")
        table.add_row("Arquivos Organizados", str(self.estatisticas['arquivos_movidos']))
        table.add_row("ZIPs Processados", str(self.estatisticas['zips_organizados']))

        self.console.print(table)
        logging.info(f"Sumário final: Sucessos={sucessos}, Total={total}, Arquivos Movidos={self.estatisticas['arquivos_movidos']}, Zips Organizados={self.estatisticas['zips_organizados']}")


    def executar_automacao(self):
        """Executa a automação completa."""
        self.console.print(Panel(
            "[bold yellow]Automação de Backup e Restauração[/]\n"
            f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            "🔄 Sistema de Organização e Backup Automatizado",
            border_style="blue"
        ))
        logging.info("Iniciando automação...")
        
        scripts = [
            ("backup_projeto.py", "Backup inicial"),
            ("restaurar_backup.py", "Restauração de backup"),
            ("remover_duplicados.py", "Remoção de duplicados"),
            ("limpar_duplicados_avancado.py", "Limpeza avançada")
        ]

        self.console.print("\n[bold yellow]🗂 Iniciando organização de arquivos...[/]")
        self.organizar_arquivos()

        sucessos = 0
        for script, descricao in scripts:
            if self.executar_script(script, descricao):
                sucessos += 1
            time.sleep(1)  # Pequena pausa entre scripts

        self.mostrar_sumario_final(sucessos, len(scripts))
        logging.info("Automação concluída.")

def main():
    automacao = AutomacaoBackup()
    automacao.executar_automacao()

if __name__ == "__main__":
    main()

# ----ATLAS----
