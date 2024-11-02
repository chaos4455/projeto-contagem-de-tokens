import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime
import hashlib
import os
from colorama import Fore, Style, init
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from sentence_transformers import SentenceTransformer
from transformers import BertTokenizer, BertModel
import torch
import emoji

init(autoreset=True)
console = Console()

def gerar_nome_arquivo():
    """Gera nome único para arquivo com timestamp e hash"""
    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
    hash_unica = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
    return f"{agora}_{hash_unica}"

def salvar_grafico(plt, nome_base):
    """Salva gráfico na pasta reports-graphics"""
    os.makedirs('reports-graphics', exist_ok=True)
    nome_arquivo = f"reports-graphics/{nome_base}_{gerar_nome_arquivo()}.png"
    plt.savefig(nome_arquivo)
    plt.close()

def vector_to_text(vector, model, tokenizer):
    """Converte vetor de volta para texto usando BERT"""
    try:
        # Redimensiona o vetor se necessário para corresponder à dimensão do BERT
        if vector.shape[0] == 512:
            vector = np.pad(vector, (0, 256), 'constant')
        
        # Encontra a sentença mais próxima usando BERT
        with torch.no_grad():
            # Exemplo de frases para comparação
            frases = [
                "Este é um texto de exemplo em português",
                "Outro texto para comparação",
                "Mais uma frase de teste",
                "Exemplo de conteúdo textual",
                "Frase para análise vetorial"
            ]
            
            # Codifica as frases de exemplo
            inputs = tokenizer(frases, padding=True, truncation=True, return_tensors="pt")
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)
            
            # Calcula similaridade
            vector_tensor = torch.tensor(vector).unsqueeze(0)
            similarities = cosine_similarity(vector_tensor, embeddings.numpy())[0]
            
            return frases[np.argmax(similarities)]
    except Exception as e:
        return f"Erro na conversão: {str(e)}"

def realizar_testes_avancados(df):
    """Realiza testes expandidos com BERT e análises avançadas"""
    # Inicialização dos modelos
    bert_tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
    bert_model = BertModel.from_pretrained('bert-base-multilingual-cased')
    sentence_model = SentenceTransformer('distiluse-base-multilingual-cased-v2')

    # === Bloco 1: Análise Vetorial Básica ===
    console.print(Panel(
        f"{emoji.emojize(':microscope:')} [bold]Análise Vetorial Básica[/]\n"
        f"Dimensões: {dict(df['vector'].apply(len).value_counts())}\n"
        f"Total vetores: {len(df)}\n"
        f"Média norma L2: {df['vector'].apply(np.linalg.norm).mean():.4f}\n"
        f"Densidade média: {df['vector'].apply(lambda x: np.count_nonzero(x)/len(x)).mean():.4f}"
    ))

    # === Bloco 2: Análise Estatística Avançada ===
    df['entropia'] = df['vector'].apply(lambda x: -np.sum(np.square(x) * np.log2(np.square(x) + 1e-10)))
    stats_panel = Panel(
        f"{emoji.emojize(':chart_increasing:')} [bold]Análise Estatística Avançada[/]\n"
        f"Entropia média: {df['entropia'].mean():.4f}\n"
        f"Máximo global: {df['vector'].apply(lambda x: np.max(x)).max():.4f}\n"
        f"Mínimo global: {df['vector'].apply(lambda x: np.min(x)).min():.4f}\n"
        f"Curtose média: {df['vector'].apply(lambda x: pd.Series(x).kurtosis()):.4f}"
    )
    console.print(stats_panel)

    # === Bloco 3: Análise de Tokens ===
    amostra_vetores = df['vector'].head(5).tolist()
    token_stats = []
    for vec in track(amostra_vetores, description="Analisando tokens..."):
        texto = vector_to_text(vec, bert_model, bert_tokenizer)
        tokens = bert_tokenizer.tokenize(texto)
        token_stats.append(len(tokens))
    
    console.print(Panel(
        f"{emoji.emojize(':abacus:')} [bold]Análise de Tokens[/]\n"
        f"Média de tokens: {np.mean(token_stats):.2f}\n"
        f"Máximo de tokens: {max(token_stats)}\n"
        f"Mínimo de tokens: {min(token_stats)}"
    ))

    # === Bloco 4: Análise de Similaridade ===
    similarity_matrix = cosine_similarity(amostra_vetores)
    console.print(Panel(
        f"{emoji.emojize(':dna:')} [bold]Análise de Similaridade[/]\n"
        f"Similaridade média: {np.mean(similarity_matrix):.4f}\n"
        f"Similaridade máxima: {np.max(similarity_matrix[similarity_matrix < 1]):.4f}\n"
        f"Similaridade mínima: {np.min(similarity_matrix):.4f}"
    ))

    # === Bloco 5: Visualizações Avançadas ===
    # Gráfico 1: Distribuição de Entropia
    plt.figure(figsize=(10, 6))
    sns.histplot(df['entropia'], kde=True)
    plt.title('Distribuição de Entropia dos Vetores')
    salvar_grafico(plt, 'entropia_dist')

    # Gráfico 2: Heatmap de Similaridade
    plt.figure(figsize=(10, 8))
    sns.heatmap(similarity_matrix, annot=True, cmap='viridis')
    plt.title('Matriz de Similaridade entre Vetores')
    salvar_grafico(plt, 'similarity_matrix')

    # Gráfico 3: PCA dos Vetores
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(np.vstack(df['vector'].values))
    plt.figure(figsize=(10, 8))
    plt.scatter(pca_result[:, 0], pca_result[:, 1], alpha=0.5)
    plt.title('PCA dos Vetores')
    salvar_grafico(plt, 'pca_vectors')

    # Gráfico 4: Distribuição de Valores por Dimensão
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=pd.DataFrame(np.vstack(df['vector'].values)[:, :10]))
    plt.title('Distribuição de Valores por Dimensão (10 primeiras)')
    salvar_grafico(plt, 'dim_distribution')

    # Gráfico 5: Análise de Componentes
    explained_variance = pca.explained_variance_ratio_
    plt.figure(figsize=(10, 6))
    plt.plot(np.cumsum(explained_variance))
    plt.title('Variância Explicada Acumulada')
    plt.xlabel('Número de Componentes')
    plt.ylabel('Variância Explicada Acumulada')
    salvar_grafico(plt, 'variance_explained')

    # === Bloco 6: Conversão para Texto ===
    console.print("\n[bold]🔄 Amostra de Conversões Vetor->Texto[/]")
    for i in track(range(min(5, len(df))), description="Convertendo vetores..."):
        texto = vector_to_text(df['vector'].iloc[i], bert_model, bert_tokenizer)
        tokens = bert_tokenizer.tokenize(texto)
        console.print(f"Vetor {i}:")
        console.print(f"  Texto: {texto}")
        console.print(f"  Tokens: {tokens}")
        console.print(f"  Quantidade de tokens: {len(tokens)}")

def fetch_vectors():
    """Recupera vetores do banco de dados vectors.db"""
    try:
        conn = sqlite3.connect('vectors.db')
        df = pd.read_sql_query("SELECT vector FROM word_vectors", conn)
        conn.close()
        df['vector'] = df['vector'].apply(lambda x: np.fromstring(x[1:-1], dtype=float, sep=' '))
        return df
    except sqlite3.Error as e:
        console.print(f"[bold red]Erro ao acessar o banco de dados: {e}[/]")
        return pd.DataFrame()
    except Exception as e:
        console.print(f"[bold red]Erro ao processar vetores: {e}[/]")
        return pd.DataFrame()

def main():
    console.print(f"\n{emoji.emojize(':rocket:')} [bold cyan]Iniciando análise avançada de vetores...[/]")
    df = fetch_vectors()
    realizar_testes_avancados(df)
    console.print(f"\n{emoji.emojize(':check_mark_button:')} [bold cyan]Análise concluída![/]")

if __name__ == "__main__":
    main()
