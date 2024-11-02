import yaml
import hashlib
from datetime import datetime
import google.generativeai as genai
import os
from pathlib import Path
import time
from colorama import init, Fore, Style
import inquirer
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.console import Console
from rich.panel import Panel
from collections import Counter
from transformers import BertTokenizer
import numpy as np
from rich.table import Table
from rich import box
from rich.text import Text

# Inicializar colorama e rich
init()
console = Console()

# Configurar API do Gemini com sua chave
GOOGLE_API_KEY = "AIzaSyCEagEEnX-RdkW3-jCAb0H9nrTsgcE-Qqo"
genai.configure(api_key=GOOGLE_API_KEY)

# 🧠 Nome do modelo
NOME_MODELO = "gemini-1.5-flash"

# 🚀 Função para configurar a geração de texto
def configurar_geracao(temperatura=0.8, top_p=0.95, top_k=64, max_tokens=8096):
    return {
        "temperature": temperatura,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": max_tokens,
        "response_mime_type": "text/plain",
    }

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
        model = genai.GenerativeModel(NOME_MODELO, generation_config=configurar_geracao())
        
        system_prompt = """


        inicia a listra de palavra depois do topico lista_palavras no yaml
        crie o mais longo completo e detalhado possivel, com o maximo de palavras possivel, referentes ao tema.

        Gere um YAML técnico e detalhado para embeddings com:
1 palavra por linha, 1 palavra chave por linha, o maximo de palavras possivel, referentes a palavra chave.
        use tecnicas de semanticas e verossimilhança para gerar o vocabulario.
        use as tecnicas de maximo verossimilhança para gerar o vocabulario.
        use a linguagem mais tecnica possivel.
        use a tecnica de tokenizacao wordpiece.
        use a tecnica de stemming.
        use a tecnica de lematizacao.
        use a tecnica de remocao de stopwords.
        use a tecnica de normalizacao de texto.
        Seja extremamente técnico e específico."""
        
        full_prompt = f"{system_prompt}\n\nContexto: {prompt}"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        console.print(f"[red]Erro na API Gemini: {str(e)}[/red]")
        return None

def analyze_text_metrics(text_list):
    """Analisa métricas do texto gerado"""
    if not isinstance(text_list, list):
        return {}
    
    # Contagem básica
    word_count = len(text_list)
    unique_words = len(set(text_list))
    
    # Tokenização BERT
    bert_tokens = []
    for word in text_list:
        tokens = tokenizer.tokenize(word)
        bert_tokens.extend(tokens)
    
    # Análise de frequência
    word_freq = Counter(text_list)
    top_words = word_freq.most_common(10)
    
    # Palavras mais longas
    longest_words = sorted(text_list, key=len, reverse=True)[:10]
    
    # Últimas 10 palavras
    recent_words = text_list[-10:] if len(text_list) >= 10 else text_list
    
    # Score de uniqueness (0-1)
    uniqueness_score = unique_words / word_count if word_count > 0 else 0
    
    return {
        'metricas': {
            'total_palavras': word_count,
            'palavras_unicas': unique_words,
            'tokens_bert': len(bert_tokens),
            'score_uniqueness': round(uniqueness_score, 2),
            'top_10_frequentes': top_words,
            'top_10_maiores': longest_words,
            'ultimas_10_palavras': recent_words
        }
    }

def save_yaml(data, prompt):
    output_dir = Path("generated-yaml-text-to-embedding")
    output_dir.mkdir(exist_ok=True)
    
    hash_id = generate_hash()
    filename = output_dir / f"embedding_config_{hash_id}.yaml"
    
    # Extrair lista de palavras do YAML
    palavras_list = []
    if isinstance(data, dict) and 'lista_palavras' in data:
        palavras_list = data['lista_palavras']
    
    data_with_metadata = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt,
            'hash_id': hash_id
        },
        'embedding_config': data
    }
    
    # Configuração do YAML para formato vertical e UTF-8
    yaml.add_representer(
        str,
        lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    )
    
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(
            data_with_metadata,
            f,
            allow_unicode=True,
            sort_keys=False,
            indent=2,
            default_flow_style=False,
            explicit_start=True,
            width=1000  # Evita quebras de linha automáticas
        )
    
    return filename

def create_metrics_panel(metrics):
    """Cria um painel rico com métricas"""
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("📈 Métrica", style="cyan")
    table.add_column("📊 Valor", style="green")

    table.add_row("🔤 Total de Palavras", str(metrics['total_palavras']))
    table.add_row("🎯 Palavras Únicas", str(metrics['palavras_unicas']))
    table.add_row("🔠 Tokens BERT", str(metrics['tokens_bert']))
    table.add_row("💯 Score Uniqueness", f"{metrics['score_uniqueness']*100:.1f}%")

    # Top palavras
    top_words_table = Table(title="🏆 Top 10 Palavras Mais Frequentes", box=box.SIMPLE)
    top_words_table.add_column("Palavra", style="cyan")
    top_words_table.add_column("Frequência", style="green")
    
    for word, freq in metrics['top_10_frequentes']:
        top_words_table.add_row(word, str(freq))

    console.print(table)
    console.print(top_words_table)


    # Rodapé com palavras longas e recentes
    console.print(f"[bold blue]📏 Maiores Palavras:[/bold blue] {', '.join(metrics['top_10_maiores'][:5])}")
    console.print(f"[bold green]🕒 Palavras Recentes:[/bold green] {', '.join(metrics['ultimas_10_palavras'][:5])}")


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
        BarColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Gerando YAMLs...", total=num_iterations)
        for i in range(num_iterations):
            try:
                iteration_prompt = f"""
                Tema: {tema}
                Iteração: {i+1}
                crie o mais longo completo e detalhado possivel, com o maximo de palavras possivel, referentes ao tema.
                 inicia a listra de palavra depois do topico lista_palavras no yaml

                Objetivo: Gerar yaml com listra de palavras que depois serão usadas em tecnicas de embedding e vocabulário relacionado para machine learning para criar vetores de embeedings
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
                
                # Após gerar e salvar o YAML, atualizar métricas
                if yaml_dict and 'lista_palavras' in yaml_dict:
                    metricas = analyze_text_metrics(yaml_dict['lista_palavras'])
                    create_metrics_panel(metricas['metricas'])
                
            except Exception as e:
                console.print(f"[red]Erro na iteração {i+1}: {str(e)}[/red]")
                continue
        
        console.print(f"[bold green]✨ Processo concluído! Todos os YAMLs foram gerados.[/bold green]")

if __name__ == "__main__":
    try:
        from transformers import BertTokenizer
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        main()
    except KeyboardInterrupt:
        console.print(f"[yellow]Operação cancelada pelo usuário.[/yellow]")
    except Exception as e:
        console.print(f"[red]Erro inesperado: {str(e)}[/red]")
    finally:
        import sys
        sys.exit(0)
