import yaml
import hashlib
from datetime import datetime
import google.generativeai as genai
import os
from pathlib import Path
import time
from colorama import init, Fore, Style
import inquirer
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
from rich.panel import Panel

# Inicializar colorama e rich
init()
console = Console()

# Configurar API do Gemini com sua chave
GOOGLE_API_KEY = "AIzaSyCEagEEnX-RdkW3-jCAb0H9nrTsgcE-Qqo"
genai.configure(api_key=GOOGLE_API_KEY)

def generate_hash():
    return hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:10]

def get_user_inputs():
    questions = [
        inquirer.Text('tema',
                     message="Digite o tema/conceito base para gerar os YAMLs",
                     validate=lambda _, x: len(x) > 0),
        inquirer.List('num_iterations',
                     message="Quantas variações você quer gerar?",
                     choices=['1', '3', '5', '10', '15', '20'],
                     default='3'),
        inquirer.Confirm('confirmar',
                        message="Confirma a geração dos YAMLs?",
                        default=True)
    ]
    
    answers = inquirer.prompt(questions)
    return answers

def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        system_prompt = """Gere um YAML técnico e detalhado para embeddings com:
        1. Vocabulário específico do domínio
        2. Parâmetros de vetorização
        3. Configurações de modelo
        4. Métricas de avaliação
        5. Hiperparâmetros recomendados
        6. Dimensões do embedding
        7. Técnicas de pré-processamento
        Seja extremamente técnico e específico."""
        
        full_prompt = f"{system_prompt}\n\nContexto: {prompt}"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        console.print(f"[red]Erro na API Gemini: {str(e)}[/red]")
        return None

def save_yaml(data, prompt):
    output_dir = Path("generated-yaml-text-to-embedding")
    output_dir.mkdir(exist_ok=True)
    
    hash_id = generate_hash()
    filename = output_dir / f"embedding_config_{hash_id}.yaml"
    
    data_with_metadata = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt,
            'hash_id': hash_id
        },
        'embedding_config': data
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(data_with_metadata, f, allow_unicode=True, sort_keys=False)
    
    return filename

def main():
    console.print(Panel.fit(
        "[bold green]Gerador de YAMLs para Embeddings[/bold green]",
        border_style="green"
    ))
    
    # Obter inputs do usuário
    answers = get_user_inputs()
    
    if not answers or not answers['confirmar']:
        console.print("[yellow]Operação cancelada pelo usuário.[/yellow]")
        return
    
    num_iterations = int(answers['num_iterations'])
    tema = answers['tema']
    
    # Iniciar processo com barra de progresso rica
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Gerando YAMLs...", total=num_iterations)
        
        for i in range(num_iterations):
            try:
                iteration_prompt = f"""
                Tema: {tema}
                Iteração: {i+1}
                Objetivo: Gerar configurações de embedding e vocabulário relacionado para machine learning
                """
                
                yaml_content = get_gemini_response(iteration_prompt)
                if not yaml_content:
                    continue
                
                try:
                    yaml_dict = yaml.safe_load(yaml_content)
                except yaml.YAMLError:
                    yaml_dict = {"raw_content": yaml_content}
                
                filename = save_yaml(yaml_dict, tema)
                if filename:
                    console.print(f"[green]✓ YAML {i+1} salvo em: {filename}[/green]")
                
                # Pausa controlada
                time.sleep(0.5)
                
                progress.update(task, advance=1)
                
            except Exception as e:
                console.print(f"[red]Erro na iteração {i+1}: {str(e)}[/red]")
                continue
        
        console.print(f"[bold green]✨ Processo concluído! Todos os YAMLs foram gerados.[/bold green]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(f"[yellow]Operação cancelada pelo usuário.[/yellow]")
    except Exception as e:
        console.print(f"[red]Erro inesperado: {str(e)}[/red]")
    finally:
        sys.exit(0)
