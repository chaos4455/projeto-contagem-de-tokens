import yaml
import pandas as pd
import google.generativeai as genai
import hashlib
from datetime import datetime
from pathlib import Path
import numpy as np
from rich.console import Console
from rich.panel import Panel

# Inicialização do console rich
console = Console()

# Configuração da API Gemini - Certifique-se de ter uma chave válida!
GOOGLE_API_KEY = "AIzaSyCEagEEnX-RdkW3-jCAb0H9nrTsgcE-Qqo" # Substitua pela sua chave
genai.configure(api_key=GOOGLE_API_KEY)
NOME_MODELO = "gemini-1.5-flash"

def get_latest_yaml():
    """Obtém o arquivo YAML mais recente da pasta vector-exported-data"""
    vector_path = Path("vector-exported-data")
    yaml_files = list(vector_path.glob("*.yaml"))
    if not yaml_files:
        raise FileNotFoundError("Nenhum arquivo YAML encontrado na pasta vector-exported-data")
    return max(yaml_files, key=lambda x: x.stat().st_mtime)

def load_yaml_to_df(yaml_path):
    """Carrega o YAML como DataFrame e texto puro"""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        yaml_content = f.read()
        try:
            yaml_data = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            console.print(f"[red]Erro ao carregar YAML: {e}[/red]")
            return None, None

    # Extraindo apenas a lista de palavras
    if isinstance(yaml_data, dict) and 'palavras' in yaml_data and isinstance(yaml_data['palavras'], list):
        df = pd.DataFrame(yaml_data['palavras'], columns=['palavra'])
    else:
        console.print("[red]Formato YAML inválido ou chave 'palavras' não encontrada.[/red]")
        return None, None

    return df, yaml_content

def generate_hash():
    """Gera hash única baseada no timestamp"""
    return hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:10]

def get_gemini_response(prompt):
    """Obtém resposta do modelo Gemini"""
    try:
        model = genai.GenerativeModel(NOME_MODELO)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        console.print(f"[red]Erro na API Gemini: {str(e)}[/red]")
        return None

def save_response(content, hash_id):
    """Salva a resposta em arquivo markdown"""
    output_dir = Path("data-engineering-testing-responses")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"cube_matrix_response_{hash_id}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_file

def main():
    try:
        # Obtém e carrega o YAML mais recente
        yaml_path = get_latest_yaml()
        df, yaml_text = load_yaml_to_df(yaml_path)
        
        if df is None or yaml_text is None:
            raise ValueError("Falha ao carregar ou processar o arquivo YAML.")
        
        console.print(Panel(f"[green]Arquivo YAML carregado: {yaml_path}[/green]"))
        console.print(f"[cyan]Total de palavras: {len(df)}[/cyan]")
        
        # Prepara o prompt para o Gemini
        prompt = f"""
        responda rico, completo, detalhado
        apenas plote visualmente na sua memoria
        use ele pra gerar a resposta 
        crie essa matriz na sua memoria no seu llm mesmo que seja como df, nao simule nem invente
        
        sem mentir ou inventar, plote na sua memoria no contexto do llm, uma matriz vetorial 3d com peso altura profundiade e implemente um elemento q que é verossimilhança e relevancia
        implemente uma gravitação e repulsão para que seja possivel gerar uma nuvem de palavras mais relevante e com mais significado de inferência
        pegue os dados que foram enviados e crie uma matriz cúbica 777x777x777 dimensional onde cada ponto 
        unico é um neuron e cada neuron é uma palavra, entenda o cluster e a densidade vetorial e as relações 
        implemente logica de processamento de dados para criar uma matriz 3D com as palavras mais relevantes e 
        expanda em pipelines de verossimilhança e relevancia para que seja possivel gerar uma nuvem de palavras 
        Com base no seguinte conjunto de palavras, crie uma matriz cúbica 777x777x777  dimensional.
        Preencha cada cubo único com uma palavra e forme uma nuvem vetorial cúbica de palavras.
        
        Palavras disponíveis:
        {yaml_text}
        apresente relatórios completos, avançados, expandidos, detalhados, com analises de relevancia e verossimilhança
        use icones e emojis para ilustrar o contexto
        Por favor, descreva a matriz resultante em formato markdown, incluindo:
        1. Visualização conceitual da matriz
        2. Distribuição das palavras no espaço
        3. Padrões e clusters formados
        4. Análise da densidade vetorial
        5. Relações semânticas espaciais
        
        Mantenha o foco na estrutura tridimensional e nas relações espaciais entre as palavras.
        """
        
        # Obtém resposta do Gemini
        response = get_gemini_response(prompt)
        
        if response:
            # Gera hash única
            hash_id = generate_hash()
            
            # Salva a resposta
            output_file = save_response(response, hash_id)
            
            console.print(Panel(
                f"[green]Resposta gerada com sucesso![/green]\n"
                f"Arquivo: {output_file}\n"
                f"Hash: {hash_id}",
                title="✨ Processo Concluído"
            ))
        
    except Exception as e:
        console.print(f"[red]Erro durante a execução: {str(e)}[/red]")

if __name__ == "__main__":
    main()
