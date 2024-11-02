import requests
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import numpy as np

console = Console()

def test_vector_endpoint():
    # Configurações
    BASE_URL = "http://localhost:9777"
    TEST_ID = 1
    
    console.print(Panel.fit("🧪 Iniciando teste da API de vetores", 
                          title="Teste API", 
                          subtitle="APOLLO"))

    try:
        # Fazendo a requisição
        console.print("[yellow]Fazendo requisição para o endpoint...[/]")
        response = requests.get(f"{BASE_URL}/vector/{TEST_ID}")
        
        # Verificando status code
        console.print(f"Status Code: [cyan]{response.status_code}[/]")
        
        if response.status_code == 200:
            data = response.json()
            
            # Criando tabela de resultados
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Campo")
            table.add_column("Valor")
            
            # Adicionando dados básicos
            table.add_row("ID", str(data['data']['id']))
            table.add_row("Palavra", data['data']['word'])
            table.add_row("Palavra Origem", str(data['data']['palavra_origem']))
            table.add_row("Timestamp", str(data['data']['timestamp']))
            
            # Informações sobre o vetor
            vector = np.array(data['data']['vector'])
            table.add_row("Dimensão do Vetor", str(vector.shape))
            table.add_row("Média do Vetor", f"{vector.mean():.6f}")
            table.add_row("Desvio Padrão", f"{vector.std():.6f}")
            
            console.print("\n[green]✅ Teste concluído com sucesso![/]")
            console.print(table)
            
            # Salvando resultado em arquivo
            with open('ultimo_teste_api.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            console.print("\n[blue]Resultado completo salvo em 'ultimo_teste_api.json'[/]")
            
        else:
            console.print(f"[red]❌ Erro na requisição: {response.text}[/]")
            
    except requests.exceptions.ConnectionError:
        console.print("[red]❌ Erro: Não foi possível conectar à API. Verifique se ela está rodando.[/]")
    except Exception as e:
        console.print(f"[red]❌ Erro inesperado: {str(e)}[/]")

if __name__ == "__main__":
    test_vector_endpoint()
