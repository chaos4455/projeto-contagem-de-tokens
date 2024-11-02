import requests
import numpy as np
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import track
from transformers import AutoTokenizer, AutoModel
import torch
from scipy.spatial.distance import cosine
import datetime

console = Console()

class VectorValidator:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        console.print(f"[yellow]Usando dispositivo: {self.device}[/]")
        
        # Usando modelo BERT mini que gera embeddings de 512 dimensões
        self.model_name = 'google/bert_uncased_L-4_H-512_A-8'  # BERT mini (512d)
        console.print(f"[yellow]Carregando modelo {self.model_name}...[/]")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name).to(self.device)
        self.model.eval()

    def generate_word_embedding(self, word: str) -> np.ndarray:
        """Gera embedding para uma palavra usando BERT mini"""
        with torch.no_grad():
            inputs = self.tokenizer(word, return_tensors='pt', padding=True).to(self.device)
            outputs = self.model(**inputs)
            embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy()[0]
            
            console.print(f"[blue]Dimensões do embedding gerado: {embedding.shape}[/]")
            return embedding

    def calculate_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calcula similaridade do cosseno entre dois vetores"""
        # Normaliza os vetores antes de calcular a similaridade
        vec1_norm = vec1 / np.linalg.norm(vec1)
        vec2_norm = vec2 / np.linalg.norm(vec2)
        
        console.print(f"[blue]Dimensões do vetor API: {vec1.shape}[/]")
        console.print(f"[blue]Dimensões do vetor gerado: {vec2.shape}[/]")
        
        return np.dot(vec1_norm, vec2_norm)

    def validate_vector(self, api_vector: np.ndarray, word: str) -> dict:
        """Valida o vetor da API contra um novo embedding gerado"""
        # Gera novo embedding para comparação
        new_vector = self.generate_word_embedding(word)
        
        # Calcula similaridade
        similarity = self.calculate_similarity(api_vector, new_vector)
        
        # Analisa tokens
        tokens = self.tokenizer.tokenize(word)
        
        return {
            "similarity": float(similarity),  # Converte para float para serialização JSON
            "tokens": tokens,
            "token_count": len(tokens),
            "validation_passed": similarity > 0.7,  # Threshold de 70% de similaridade
            "vector_dimensions": {
                "api_vector": api_vector.shape[0],
                "generated_vector": new_vector.shape[0]
            }
        }

def test_vector_endpoint():
    BASE_URL = "http://localhost:9777"
    TEST_ID = 1
    
    console.print(Panel.fit("🧪 Iniciando teste avançado da API de vetores", 
                          title="Teste API v2", 
                          subtitle="APOLLO"))

    try:
        # Inicializa validador
        validator = VectorValidator()
        
        # Faz requisição
        console.print("[yellow]Fazendo requisição para o endpoint...[/]")
        response = requests.get(f"{BASE_URL}/vector/{TEST_ID}")
        
        if response.status_code == 200:
            data = response.json()['data']
            
            # Extrai dados
            word = data['word']
            api_vector = np.array(data['vector'])
            
            console.print(f"[green]Palavra recuperada: {word}[/]")
            console.print(f"[green]Dimensões do vetor da API: {api_vector.shape}[/]")
            
            # Valida vetor
            console.print("[yellow]Validando vetor...[/]")
            validation_results = validator.validate_vector(api_vector, word)
            
            # Cria tabela de resultados
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Métrica")
            table.add_column("Valor")
            
            # Dados básicos
            table.add_row("ID", str(data['id']))
            table.add_row("Palavra", word)
            table.add_row("Palavra Origem", str(data['palavra_origem']))
            table.add_row("Timestamp Original", str(data['timestamp']))
            
            # Dados de validação
            table.add_row("Dimensões Vetor API", str(validation_results['vector_dimensions']['api_vector']))
            table.add_row("Dimensões Vetor Gerado", str(validation_results['vector_dimensions']['generated_vector']))
            table.add_row("Similaridade", f"{validation_results['similarity']:.4f}")
            table.add_row("Tokens", str(validation_results['tokens']))
            table.add_row("Quantidade de Tokens", str(validation_results['token_count']))
            table.add_row("Validação Passou", 
                         "[green]SIM[/]" if validation_results['validation_passed'] 
                         else "[red]NÃO[/]")
            
            # Status final
            status = "✅ SUCESSO" if validation_results['validation_passed'] else "❌ FALHA"
            console.print(f"\n[bold]Status Final: {status}[/]")
            console.print(table)
            
            # Salva relatório
            report = {
                "timestamp": datetime.datetime.now().isoformat(),
                "api_data": data,
                "validation_results": validation_results,
                "test_passed": validation_results['validation_passed']
            }
            
            with open('relatorio_validacao_v2.json', 'w', encoding='utf-8') as f:
                import json
                json.dump(report, f, indent=4, ensure_ascii=False)
            
            console.print("\n[blue]Relatório completo salvo em 'relatorio_validacao_v2.json'[/]")
            
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
