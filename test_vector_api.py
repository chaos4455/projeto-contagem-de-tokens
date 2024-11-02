import requests
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import random
import json
import sqlite3

# Inicialização
console = Console()
BASE_URL = "http://localhost:8000"
DATABASE_PATH = 'vectors_continuo.db'

def get_random_id():
    """Obtém um ID aleatório válido do banco de dados"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT MIN(id), MAX(id) FROM word_vectors")
        min_id, max_id = cursor.fetchone()
        conn.close()
        return random.randint(min_id, max_id)
    except Exception as e:
        console.print(f"[red]Erro ao obter ID aleatório: {str(e)}[/]")
        return 1

def test_vector_endpoint():
    """Testa o endpoint de vetores com um ID aleatório"""
    console.print(Panel.fit("🧪 Iniciando teste da API de vetores", 
                          title="Teste API FastAPI", 
                          subtitle="Consulta Aleatória"))

    try:
        # Obtém ID aleatório
        test_id = get_random_id()
        console.print(f"[yellow]ID selecionado para teste: [cyan]{test_id}[/][/]")
        
        # Fazendo a requisição
        console.print("[yellow]Fazendo requisição para o endpoint...[/]")
        response = requests.get(f"{BASE_URL}/vectors/{test_id}")
        
        # Verificando status code
        console.print(f"Status Code: [cyan]{response.status_code}[/]")
        
        if response.status_code == 200:
            data = response.json()
            
            # Criando tabela de resultados
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Campo")
            table.add_column("Valor")
            
            # Adicionando dados básicos
            table.add_row("ID", str(data['id']))
            table.add_row("Palavra", data['word'])
            table.add_row("Palavra Origem", str(data['palavra_origem']))
            table.add_row("Timestamp", str(data['timestamp']))
            
            # Informações sobre o vetor
            vector = np.array(data['vector'])
            table.add_row("Dimensão do Vetor", str(vector.shape))
            table.add_row("Média do Vetor", f"{vector.mean():.6f}")
            table.add_row("Desvio Padrão", f"{vector.std():.6f}")
            table.add_row("Valor Mínimo", f"{vector.min():.6f}")
            table.add_row("Valor Máximo", f"{vector.max():.6f}")
            
            # Adiciona os primeiros 5 valores do vetor como exemplo
            table.add_row("Primeiros 5 valores", str(vector[:5].tolist()))
            
            console.print("\n[green]✅ Teste concluído com sucesso![/]")
            console.print(table)
            
            # Salvando resultado em arquivo
            resultado = {
                "id": data['id'],
                "word": data['word'],
                "palavra_origem": data['palavra_origem'],
                "timestamp": data['timestamp'],
                "vector_stats": {
                    "dimensao": vector.shape[0],
                    "media": float(vector.mean()),
                    "desvio_padrao": float(vector.std()),
                    "minimo": float(vector.min()),
                    "maximo": float(vector.max()),
                    "primeiros_5_valores": vector[:5].tolist()
                }
            }
            
            with open('ultimo_teste_api_fastapi.json', 'w', encoding='utf-8') as f:
                json.dump(resultado, f, ensure_ascii=False, indent=4)
            console.print("\n[blue]Resultado completo salvo em 'ultimo_teste_api_fastapi.json'[/]")
            
        else:
            console.print(f"[red]❌ Erro na requisição: {response.text}[/]")
            
    except requests.exceptions.ConnectionError:
        console.print("[red]❌ Erro: Não foi possível conectar à API. Verifique se ela está rodando.[/]")
    except Exception as e:
        console.print(f"[red]❌ Erro inesperado: {str(e)}[/]")
        import traceback
        console.print("[red]" + traceback.format_exc() + "[/]")

if __name__ == "__main__":
    test_vector_endpoint()
