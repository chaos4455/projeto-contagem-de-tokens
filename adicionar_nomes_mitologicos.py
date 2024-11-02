from pathlib import Path
import logging
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

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
            "automacao_organiza_projeto_restaura_backup_v1.py": "----ATLAS----",  # Titã que carrega o mundo
            "backup_projeto.py": "----JANUS----",  # Deus das transições
            "banco_tokens.py": "----HERMES----",  # Mensageiro dos deuses
            "contador_tokens_menu.py": "----THOTH----",  # Deus da escrita
            "documentacao-projeto-automation-v1.py": "----CLIO----",  # Musa da história
            "documentacao-projeto-automation-v2-gemini-powered.py": "----MINERVA----",  # Deusa da sabedoria
            "gerador-dic-texto-yaml-v1.py": "----CALLIOPE----",  # Musa da poesia
            "gerador_vetorizador_continuo.py": "----PROMETHEUS----",  # Titã do conhecimento
            "gerador_yaml_embeddings-prompt-v2.py": "----ORPHEUS----",  # Poeta mítico
            "gerador_yaml_embeddings.py": "----APOLLO----",  # Deus das artes
            "gerador_yaml_embeddings_stream_v1-cria-contexto.py": "----ATHENA----",  # Deusa da estratégia
            "gerador_yaml_embeddings_stream_v1-cria-lista-palavras.py": "----ISIS----",  # Deusa da magia
            "limpar_duplicados_avancado.py": "----PERSEUS----",  # Herói que derrotou Medusa
            "remover_duplicados.py": "----HERCULES----",  # Herói da força
            "restaurar_backup.py": "----CHRONOS----",  # Deus do tempo
            "restaura_backup_versionado.py": "----MNEMOSYNE----",  # Titã da memória
            "testa-banco-vetor-ele.py": "----HEPHAESTUS----",  # Deus dos artesãos
            "yaml-parser-vector-database-increment-v1.py": "----THESEUS----",  # Herói do labirinto
            "yaml_to_vectors.py": "----DAEDALUS----",  # Inventor mítico
            "zipar_yamls.py": "----VULCAN----"  # Deus do fogo
        }
        
    def adicionar_nomes(self):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            task = progress.add_task("[cyan]Adicionando nomes mitológicos...", total=len(self.mapeamento_nomes))
            
            for arquivo_nome, nome_mitologico in self.mapeamento_nomes.items():
                arquivo = self.pasta_raiz / arquivo_nome
                if arquivo.exists():
                    try:
                        # Ler conteúdo atual
                        conteudo = arquivo.read_text(encoding='utf-8')
                        
                        # Verificar se o nome já está presente
                        if nome_mitologico not in conteudo:
                            # Adicionar nome ao final do arquivo
                            novo_conteudo = f"{conteudo.rstrip()}\n\n# {nome_mitologico}\n"
                            
                            # Salvar arquivo
                            arquivo.write_text(novo_conteudo, encoding='utf-8')
                            
                            console.print(f"[green]✓[/green] Adicionado {nome_mitologico} ao arquivo {arquivo_nome}")
                            logging.info(f"Nome adicionado com sucesso: {arquivo_nome} -> {nome_mitologico}")
                        else:
                            console.print(f"[yellow]![/yellow] Nome já presente em {arquivo_nome}")
                            logging.info(f"Nome já presente: {arquivo_nome}")
                    
                    except Exception as e:
                        console.print(f"[red]✗[/red] Erro ao processar {arquivo_nome}: {str(e)}")
                        logging.error(f"Erro ao processar {arquivo_nome}: {str(e)}")
                else:
                    console.print(f"[yellow]![/yellow] Arquivo não encontrado: {arquivo_nome}")
                    logging.warning(f"Arquivo não encontrado: {arquivo_nome}")
                
                progress.update(task, advance=1)

    def executar(self):
        console.print("\n[bold cyan]Iniciando adição de nomes mitológicos aos arquivos Python...[/bold cyan]\n")
        self.adicionar_nomes()
        console.print("\n[bold green]Processo concluído![/bold green]")
        console.print("Verifique o arquivo 'adicionar_nomes_mitologicos.log' para mais detalhes.")

if __name__ == "__main__":
    adicionador = AdicionadorNomesMitologicos()
    adicionador.executar()
