from pathlib import Path
import logging
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
import shutil
from datetime import datetime

# Configurar logging
logging.basicConfig(
    filename='renomeador_tecnico_v2.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

console = Console()

class RenomeadorTecnicoProfissionalV2:
    def __init__(self):
        self.pasta_raiz = Path('.')
        self.estatisticas = {
            'arquivos_renomeados': 0,
            'erros': 0,
            'arquivos_nao_encontrados': 0,
            'ja_renomeados': 0
        }
        self.mapeamento_nomes = {
            # Ferramentas de Automação e Backup
            "automation_file_organization_backup_manager_ATLAS.py": 
                "tool.automation.file_organization_manager_ATLAS.py",
            
            "project_backup_version_control_system_JANUS.py": 
                "tool.backup.project_version_controller_JANUS.py",
            
            # Gerenciadores de Banco de Dados
            "token_database_management_system_HERMES.py": 
                "db.manager.token_database_controller_HERMES.py",
            
            "token_counter_interface_manager_THOTH.py": 
                "tool.analyzer.token_counter_interface_THOTH.py",
            
            # Geradores de Documentação
            "project_documentation_generator_v1_CLIO.py": 
                "generator.docs.project_documentation_builder_CLIO.py",
            
            "ai_powered_documentation_generator_v2_MINERVA.py": 
                "generator.docs.ai_documentation_engine_MINERVA.py",
            
            # Processadores YAML e Vetores
            "yaml_text_dictionary_generator_CALLIOPE.py": 
                "processor.yaml.dictionary_text_generator_CALLIOPE.py",
            
            "continuous_vector_embedding_generator_PROMETHEUS.py": 
                "processor.vector.continuous_embedding_engine_PROMETHEUS.py",
            
            "yaml_prompt_embedding_processor_v2_ORPHEUS.py": 
                "processor.yaml.prompt_embedding_generator_ORPHEUS.py",
            
            "yaml_embedding_generation_system_APOLLO.py": 
                "processor.yaml.embedding_core_system_APOLLO.py",
            
            "yaml_context_stream_processor_v1_ATHENA.py": 
                "processor.yaml.context_stream_engine_ATHENA.py",
            
            "yaml_wordlist_stream_generator_v1_ISIS.py": 
                "processor.yaml.wordlist_stream_processor_ISIS.py",
            
            # Utilitários de Limpeza
            "advanced_duplicate_cleaner_system_PERSEUS.py": 
                "util.cleaner.advanced_duplicate_remover_PERSEUS.py",
            
            "duplicate_file_removal_manager_HERCULES.py": 
                "util.cleaner.duplicate_file_handler_HERCULES.py",
            
            # Ferramentas de Backup e Restauração
            "backup_restoration_controller_CHRONOS.py": 
                "tool.backup.restoration_controller_CHRONOS.py",
            
            "versioned_backup_recovery_system_MNEMOSYNE.py": 
                "tool.backup.version_recovery_system_MNEMOSYNE.py",
            
            # Ferramentas de Teste e Análise
            "vector_database_testing_framework_HEPHAESTUS.py": 
                "tool.tester.vector_database_validator_HEPHAESTUS.py",
            
            # Processadores de Base de Dados
            "incremental_yaml_vector_db_parser_THESEUS.py": 
                "processor.db.incremental_vector_parser_THESEUS.py",
            
            "yaml_vector_conversion_engine_DAEDALUS.py": 
                "processor.vector.yaml_vectorization_engine_DAEDALUS.py",
            
            # Utilitários de Compressão
            "yaml_compression_utility_VULCAN.py": 
                "util.compression.yaml_archiver_VULCAN.py"
        }

    def criar_backup_arquivo(self, arquivo):
        """Cria um backup do arquivo antes de renomear."""
        try:
            backup_dir = self.pasta_raiz / 'backups_renomeacao'
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_nome = f"{arquivo.stem}_backup_{timestamp}{arquivo.suffix}"
            backup_path = backup_dir / backup_nome
            
            shutil.copy2(arquivo, backup_path)
            logging.info(f"Backup criado: {backup_nome}")
            return True
        except Exception as e:
            logging.error(f"Erro ao criar backup de {arquivo}: {str(e)}")
            return False

    def validar_novo_nome(self, novo_nome):
        """Valida se o novo nome segue o padrão correto."""
        partes = novo_nome.split('.')
        if len(partes) < 4:  # Deve ter pelo menos: categoria.subcategoria.nome_DEUS.py
            return False
        
        categorias_validas = {'tool', 'processor', 'generator', 'util', 'db'}
        if partes[0] not in categorias_validas:
            return False
            
        return True

    def mostrar_estatisticas(self):
        """Mostra uma tabela com as estatísticas da renomeação."""
        table = Table(title="Estatísticas de Renomeação")
        
        table.add_column("Métrica", style="cyan")
        table.add_column("Quantidade", style="green")
        
        table.add_row("Arquivos Renomeados", str(self.estatisticas['arquivos_renomeados']))
        table.add_row("Erros Encontrados", str(self.estatisticas['erros']))
        table.add_row("Arquivos Não Encontrados", str(self.estatisticas['arquivos_nao_encontrados']))
        table.add_row("Já Renomeados", str(self.estatisticas['ja_renomeados']))
        
        console.print(table)

    def processar_arquivo(self, arquivo_nome, nome_novo):
        """Processa um único arquivo para renomeação."""
        arquivo = self.pasta_raiz / arquivo_nome
        if not arquivo.exists():
            console.print(f"[yellow]![/yellow] Arquivo não encontrado: {arquivo_nome}")
            logging.warning(f"Arquivo não encontrado: {arquivo_nome}")
            self.estatisticas['arquivos_nao_encontrados'] += 1
            return

        try:
            if not self.validar_novo_nome(nome_novo):
                raise ValueError(f"Nome inválido: {nome_novo}")

            # Criar backup antes de qualquer modificação
            if not self.criar_backup_arquivo(arquivo):
                raise Exception("Falha ao criar backup")

            arquivo_novo = self.pasta_raiz / nome_novo
            
            if arquivo_novo.exists():
                console.print(f"[yellow]![/yellow] Arquivo {nome_novo} já existe")
                logging.warning(f"Arquivo já existe: {nome_novo}")
                self.estatisticas['ja_renomeados'] += 1
                return

            # Renomear o arquivo
            arquivo.rename(arquivo_novo)
            console.print(f"[green]✓[/green] Arquivo renomeado: {arquivo_nome} -> {nome_novo}")
            logging.info(f"Arquivo renomeado com sucesso: {arquivo_nome} -> {nome_novo}")
            self.estatisticas['arquivos_renomeados'] += 1

        except Exception as e:
            console.print(f"[red]✗[/red] Erro ao processar {arquivo_nome}: {str(e)}")
            logging.error(f"Erro ao processar {arquivo_nome}: {str(e)}")
            self.estatisticas['erros'] += 1

    def executar(self):
        """Executa o processo de renomeação."""
        console.print(Panel.fit(
            "[bold cyan]Iniciando Processo de Renomeação Técnica[/bold cyan]\n"
            "[dim]Este processo irá renomear os arquivos Python seguindo uma nomenclatura técnica padronizada[/dim]"
        ))

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            task = progress.add_task(
                "[cyan]Processando arquivos...", 
                total=len(self.mapeamento_nomes)
            )
            
            for arquivo_antigo, arquivo_novo in self.mapeamento_nomes.items():
                self.processar_arquivo(arquivo_antigo, arquivo_novo)
                progress.update(task, advance=1)

        console.print("\n[bold green]Processo de renomeação concluído![/bold green]")
        self.mostrar_estatisticas()
        console.print("\nVerifique o arquivo 'renomeador_tecnico_v2.log' para mais detalhes.")

def main():
    try:
        renomeador = RenomeadorTecnicoProfissionalV2()
        renomeador.executar()
    except KeyboardInterrupt:
        console.print("\n[yellow]Processo interrompido pelo usuário[/yellow]")
        logging.warning("Processo interrompido pelo usuário")
    except Exception as e:
        console.print(f"\n[red]Erro fatal: {str(e)}[/red]")
        logging.error(f"Erro fatal: {str(e)}")

if __name__ == "__main__":
    main()
