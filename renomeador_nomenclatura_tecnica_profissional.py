from pathlib import Path
import logging
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import shutil

# Configurar logging
logging.basicConfig(
    filename='renomeador_tecnico.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

console = Console()

class RenomeadorTecnicoProfissional:
    def __init__(self):
        self.pasta_raiz = Path('.')
        self.mapeamento_nomes = {
            "automacao_organiza_projeto_restaura_backup_v1_ATLAS.py": 
                "automation_file_organization_backup_manager_ATLAS.py",
            
            "backup_projeto_JANUS.py": 
                "project_backup_version_control_system_JANUS.py",
            
            "banco_tokens_HERMES.py": 
                "token_database_management_system_HERMES.py",
            
            "contador_tokens_menu_THOTH.py": 
                "token_counter_interface_manager_THOTH.py",
            
            "documentacao-projeto-automation-v1_CLIO.py": 
                "project_documentation_generator_v1_CLIO.py",
            
            "documentacao-projeto-automation-v2-gemini-powered_MINERVA.py": 
                "ai_powered_documentation_generator_v2_MINERVA.py",
            
            "gerador-dic-texto-yaml-v1_CALLIOPE.py": 
                "yaml_text_dictionary_generator_CALLIOPE.py",
            
            "gerador_vetorizador_continuo_PROMETHEUS.py": 
                "continuous_vector_embedding_generator_PROMETHEUS.py",
            
            "gerador_yaml_embeddings-prompt-v2_ORPHEUS.py": 
                "yaml_prompt_embedding_processor_v2_ORPHEUS.py",
            
            "gerador_yaml_embeddings_APOLLO.py": 
                "yaml_embedding_generation_system_APOLLO.py",
            
            "gerador_yaml_embeddings_stream_v1-cria-contexto_ATHENA.py": 
                "yaml_context_stream_processor_v1_ATHENA.py",
            
            "gerador_yaml_embeddings_stream_v1-cria-lista-palavras_ISIS.py": 
                "yaml_wordlist_stream_generator_v1_ISIS.py",
            
            "limpar_duplicados_avancado_PERSEUS.py": 
                "advanced_duplicate_cleaner_system_PERSEUS.py",
            
            "remover_duplicados_HERCULES.py": 
                "duplicate_file_removal_manager_HERCULES.py",
            
            "restaurar_backup_CHRONOS.py": 
                "backup_restoration_controller_CHRONOS.py",
            
            "restaura_backup_versionado_MNEMOSYNE.py": 
                "versioned_backup_recovery_system_MNEMOSYNE.py",
            
            "testa-banco-vetor-ele_HEPHAESTUS.py": 
                "vector_database_testing_framework_HEPHAESTUS.py",
            
            "yaml-parser-vector-database-increment-v1_THESEUS.py": 
                "incremental_yaml_vector_db_parser_THESEUS.py",
            
            "yaml_to_vectors_DAEDALUS.py": 
                "yaml_vector_conversion_engine_DAEDALUS.py",
            
            "zipar_yamls_VULCAN.py": 
                "yaml_compression_utility_VULCAN.py"
        }

    def renomear_arquivos(self):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            task = progress.add_task("[cyan]Renomeando arquivos...", total=len(self.mapeamento_nomes))
            
            for nome_antigo, nome_novo in self.mapeamento_nomes.items():
                arquivo_antigo = self.pasta_raiz / nome_antigo
                arquivo_novo = self.pasta_raiz / nome_novo
                
                if arquivo_antigo.exists():
                    try:
                        arquivo_antigo.rename(arquivo_novo)
                        console.print(f"[green]✓[/green] Renomeado: {nome_antigo} -> {nome_novo}")
                        logging.info(f"Arquivo renomeado com sucesso: {nome_antigo} -> {nome_novo}")
                    except Exception as e:
                        console.print(f"[red]✗[/red] Erro ao renomear {nome_antigo}: {str(e)}")
                        logging.error(f"Erro ao renomear {nome_antigo}: {str(e)}")
                else:
                    console.print(f"[yellow]![/yellow] Arquivo não encontrado: {nome_antigo}")
                    logging.warning(f"Arquivo não encontrado: {nome_antigo}")
                
                progress.update(task, advance=1)

    def executar(self):
        console.print("\n[bold cyan]Iniciando renomeação técnica dos arquivos Python...[/bold cyan]\n")
        self.renomear_arquivos()
        console.print("\n[bold green]Processo de renomeação concluído![/bold green]")
        console.print("Verifique o arquivo 'renomeador_tecnico.log' para mais detalhes.")

if __name__ == "__main__":
    renomeador = RenomeadorTecnicoProfissional()
    renomeador.executar()
