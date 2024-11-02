from pathlib import Path
import logging
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import shutil

# Configurar logging
logging.basicConfig(
    filename='adicionar_nomes_mitologicos.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

console = Console()

class AdicionadorNomesMitologicos:
    def __init__(self):
        self.pasta_raiz = Path('.')
        self.mapeamento_nomes = {
            "automacao_organiza_projeto_restaura_backup_v1.py": "ATLAS",
            "backup_projeto.py": "JANUS",
            "banco_tokens.py": "HERMES",
            "contador_tokens_menu.py": "THOTH",
            "documentacao-projeto-automation-v1.py": "CLIO",
            "documentacao-projeto-automation-v2-gemini-powered.py": "MINERVA",
            "gerador-dic-texto-yaml-v1.py": "CALLIOPE",
            "gerador_vetorizador_continuo.py": "PROMETHEUS",
            "gerador_yaml_embeddings-prompt-v2.py": "ORPHEUS",
            "gerador_yaml_embeddings.py": "APOLLO",
            "gerador_yaml_embeddings_stream_v1-cria-contexto.py": "ATHENA",
            "gerador_yaml_embeddings_stream_v1-cria-lista-palavras.py": "ISIS",
            "limpar_duplicados_avancado.py": "PERSEUS",
            "remover_duplicados.py": "HERCULES",
            "restaurar_backup.py": "CHRONOS",
            "restaura_backup_versionado.py": "MNEMOSYNE",
            "testa-banco-vetor-ele.py": "HEPHAESTUS",
            "yaml-parser-vector-database-increment-v1.py": "THESEUS",
            "yaml_to_vectors.py": "DAEDALUS",
            "zipar_yamls.py": "VULCAN"
        }
        
    def processar_arquivo(self, arquivo_nome, nome_mitologico):
        arquivo = self.pasta_raiz / arquivo_nome
        if not arquivo.exists():
            console.print(f"[yellow]![/yellow] Arquivo não encontrado: {arquivo_nome}")
            logging.warning(f"Arquivo não encontrado: {arquivo_nome}")
            return

        try:
            # 1. Adicionar comentário ao conteúdo
            conteudo = arquivo.read_text(encoding='utf-8')
            nome_comentario = f"----{nome_mitologico}----"
            if nome_comentario not in conteudo:
                novo_conteudo = f"{conteudo.rstrip()}\n\n# {nome_comentario}\n"
                arquivo.write_text(novo_conteudo, encoding='utf-8')
                console.print(f"[green]✓[/green] Adicionado comentário em {arquivo_nome}")
                logging.info(f"Comentário adicionado: {arquivo_nome}")

            # 2. Renomear o arquivo
            nome_base = arquivo_nome[:-3]  # Remove .py
            nova_extensao = f"_{nome_mitologico}.py"
            novo_nome = nome_base + nova_extensao
            
            # Verifica se o novo nome é diferente do atual
            if not arquivo_nome.endswith(nova_extensao):
                novo_arquivo = self.pasta_raiz / novo_nome
                if novo_arquivo.exists():
                    console.print(f"[yellow]![/yellow] Arquivo {novo_nome} já existe")
                    logging.warning(f"Arquivo já existe: {novo_nome}")
                else:
                    shutil.move(arquivo, novo_arquivo)
                    console.print(f"[green]✓[/green] Arquivo renomeado: {arquivo_nome} -> {novo_nome}")
                    logging.info(f"Arquivo renomeado: {arquivo_nome} -> {novo_nome}")

        except Exception as e:
            console.print(f"[red]✗[/red] Erro ao processar {arquivo_nome}: {str(e)}")
            logging.error(f"Erro ao processar {arquivo_nome}: {str(e)}")

    def executar(self):
        console.print("\n[bold cyan]Iniciando processamento dos arquivos Python...[/bold cyan]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            task = progress.add_task("[cyan]Processando arquivos...", total=len(self.mapeamento_nomes))
            
            for arquivo_nome, nome_mitologico in self.mapeamento_nomes.items():
                self.processar_arquivo(arquivo_nome, nome_mitologico)
                progress.update(task, advance=1)

        console.print("\n[bold green]Processo concluído![/bold green]")
        console.print("Verifique o arquivo 'adicionar_nomes_mitologicos.log' para mais detalhes.")

if __name__ == "__main__":
    adicionador = AdicionadorNomesMitologicos()
    adicionador.executar()