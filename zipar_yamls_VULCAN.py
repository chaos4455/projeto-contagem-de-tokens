import zipfile
from datetime import datetime
import hashlib
from pathlib import Path
import shutil
from rich.console import Console
from rich.panel import Panel

console = Console()

def gerar_hash():
    timestamp = datetime.now().timestamp()
    return hashlib.md5(str(timestamp).encode()).hexdigest()[:8]

def zipar_pasta_yamls():
    # Pasta fonte dos YAMLs
    pasta_origem = Path("generated-yaml-text-to-embedding")
    
    if not pasta_origem.exists():
        console.print("[red]Pasta de YAMLs não encontrada![/red]")
        return False
    
    # Gerar nome do arquivo zip
    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    hash_unica = gerar_hash()
    nome_zip = f"yamls_textembedding_bruto_backups_original_limpeza_{data_hora}_{hash_unica}.zip"
    
    try:
        # Lista para guardar os arquivos que foram zipados
        arquivos_zipados = []
        
        # Criar arquivo ZIP
        with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Adicionar todos os arquivos YAML
            for arquivo in pasta_origem.glob("*.yaml"):
                zipf.write(arquivo, arquivo.name)
                arquivos_zipados.append(arquivo)
        
        # Mover para a raiz se estiver em outro diretório
        arquivo_zip = Path(nome_zip)
        if arquivo_zip.parent != Path.cwd():
            shutil.move(str(arquivo_zip), str(Path.cwd() / nome_zip))
        
        # Apagar os arquivos YAML originais
        for arquivo in arquivos_zipados:
            arquivo.unlink()
        
        console.print(Panel.fit(
            f"[green]✓ Backup criado com sucesso:[/green]\n"
            f"[blue]{nome_zip}[/blue]\n"
            f"[green]✓ {len(arquivos_zipados)} arquivos YAML foram removidos[/green]",
            border_style="green"
        ))
        return True
        
    except Exception as e:
        console.print(f"[red]Erro ao criar backup: {str(e)}[/red]")
        return False

if __name__ == "__main__":
    try:
        console.print(Panel.fit(
            "[bold cyan]Criando backup dos arquivos YAML[/bold cyan]",
            border_style="cyan"
        ))
        zipar_pasta_yamls()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operação cancelada pelo usuário.[/yellow]")
    except Exception as e:
        console.print(f"[red]Erro inesperado: {str(e)}[/red]")

# ----VULCAN----
