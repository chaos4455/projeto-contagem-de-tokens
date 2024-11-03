import yaml
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
import numpy as np
from collections import Counter
import re
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table
from rich.layout import Layout
from rich import box
from colorama import Fore, Back, Style
import statistics

# Inicialização
console = Console()
plt.style.use('default')

class WordVectorHeatmapAnalyzer:
    def __init__(self):
        self.output_dir = Path("vector-data-heatmaps")
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def get_latest_yaml(self):
        """Obtém o arquivo YAML mais recente"""
        vector_path = Path("vector-exported-data")
        yaml_files = list(vector_path.glob("*.yaml"))
        if not yaml_files:
            raise FileNotFoundError("Nenhum arquivo YAML encontrado")
        return max(yaml_files, key=lambda x: x.stat().st_mtime)

    def load_yaml_data(self, yaml_path):
        """Carrega e processa dados do YAML"""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict) and 'palavras' in data:
                return pd.DataFrame(data['palavras'], columns=['palavra'])
            return pd.DataFrame(data, columns=['palavra'])

    def generate_word_metrics(self, df):
        """Gera métricas detalhadas para cada palavra"""
        # Métricas básicas
        df['tamanho'] = df['palavra'].str.len()
        df['vogais'] = df['palavra'].str.count(r'[aeiouAEIOU]')
        df['consoantes'] = df['palavra'].str.count(r'[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]')
        df['especiais'] = df['palavra'].str.count(r'[^a-zA-Z]')
        
        # Métricas avançadas
        df['prop_vogais'] = df['vogais'] / df['tamanho']
        df['prop_consoantes'] = df['consoantes'] / df['tamanho']
        df['complexidade'] = df['tamanho'] * (df['especiais'] + 1)
        df['razao_vc'] = df['vogais'] / (df['consoantes'] + 1)
        
        # Padrões
        df['inicio'] = df['palavra'].str[0]
        df['fim'] = df['palavra'].str[-1]
        df['seq_vogais'] = df['palavra'].apply(lambda x: len(max(re.findall(r'[aeiouAEIOU]+', x), key=len, default='')))
        df['seq_consoantes'] = df['palavra'].apply(lambda x: len(max(re.findall(r'[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]+', x), key=len, default='')))
        
        return df

    def plot_and_save(self, fig, nome):
        """Salva o heatmap com timestamp"""
        plt.tight_layout()
        caminho = self.output_dir / f"{nome}_{self.timestamp}.png"
        fig.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close(fig)
        return caminho

    def generate_heatmaps(self, df):
        """Gera 22 heatmaps detalhados para análise linguística"""
        heatmaps = []
        
        # 1. Correlação entre métricas numéricas básicas
        numeric_cols = ['tamanho', 'vogais', 'consoantes', 'especiais', 'complexidade']
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='RdYlBu_r', center=0)
        plt.title('Correlação entre Métricas Básicas')
        heatmaps.append(self.plot_and_save(fig, '01_correlacao_basica'))

        # 2. Distribuição de vogais por posição
        pos_matrix = np.zeros((10, 10))
        for i in range(10):
            for j in range(10):
                palavras_tam = df[df['tamanho'] > i]['palavra']
                if len(palavras_tam) > 0:
                    letras = palavras_tam.str[i].fillna('')
                    pos_matrix[i, j] = sum(letra.lower() in 'aeiou' for letra in letras)
        
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(pos_matrix, annot=True, fmt='.0f', cmap='YlOrRd')
        plt.title('Distribuição de Vogais por Posição na Palavra')
        plt.xlabel('Quantidade de Vogais')
        plt.ylabel('Posição na Palavra')
        heatmaps.append(self.plot_and_save(fig, '02_vogais_posicao'))

        # 3. Padrões de início/fim
        inicio_fim = pd.crosstab(
            df['palavra'].str[0].fillna(''),
            df['palavra'].str[-1].fillna('')
        )
        fig, ax = plt.subplots(figsize=(15, 12))
        sns.heatmap(inicio_fim, cmap='viridis', annot=True, fmt='.0f')
        plt.title('Padrões de Início e Fim de Palavras')
        plt.xlabel('Letra Final')
        plt.ylabel('Letra Inicial')
        heatmaps.append(self.plot_and_save(fig, '03_inicio_fim'))

        # 4. Complexidade por tamanho e vogais
        complex_matrix = pd.crosstab(
            df['tamanho'],
            df['vogais'],
            values=df['complexidade'],
            aggfunc='mean'
        ).fillna(0)
        
        fig, ax = plt.subplots(figsize=(15, 10))
        sns.heatmap(complex_matrix, cmap='magma', annot=True, fmt='.2f')
        plt.title('Complexidade Média por Tamanho e Número de Vogais')
        plt.xlabel('Número de Vogais')
        plt.ylabel('Tamanho da Palavra')
        heatmaps.append(self.plot_and_save(fig, '04_complexidade_tamanho_vogais'))

        # 5. Distribuição de Sequências
        seq_matrix = pd.crosstab(
            df['seq_vogais'],
            df['seq_consoantes']
        ).fillna(0)
        
        fig, ax = plt.subplots(figsize=(15, 12))
        sns.heatmap(seq_matrix, cmap='coolwarm', annot=True, fmt='.0f')
        plt.title('Distribuição de Sequências de Vogais vs Consoantes')
        plt.xlabel('Sequência Máxima de Consoantes')
        plt.ylabel('Sequência Máxima de Vogais')
        heatmaps.append(self.plot_and_save(fig, '05_sequencias_distribuicao'))

        # 6. Análise de Posição Relativa
        pos_rel_matrix = np.zeros((10, 10))
        for i in range(10):
            palavras_tam = df[df['tamanho'] > i]['palavra']
            if len(palavras_tam) > 0:
                for j in range(10):
                    letras = palavras_tam.str[i:i+1].fillna('')
                    pos_rel_matrix[i,j] = sum(letra.lower() in 'aeiou' for letra in letras)
        
        fig, ax = plt.subplots(figsize=(15, 12))
        sns.heatmap(pos_rel_matrix, cmap='viridis', annot=True, fmt='.0f')
        plt.title('Mapa de Calor de Posição Relativa das Vogais')
        plt.xlabel('Posição na Palavra')
        plt.ylabel('Índice de Ocorrência')
        heatmaps.append(self.plot_and_save(fig, '06_posicao_relativa'))

        # 7. Padrões de Transição
        def get_transitions(word):
            return [f"{word[i]}{word[i+1]}" for i in range(len(word)-1)]
        
        transitions = []
        for word in df['palavra']:
            transitions.extend(get_transitions(word))
        
        trans_counts = pd.Series(transitions).value_counts()
        trans_matrix = pd.DataFrame(index=set(t[0] for t in transitions),
                                  columns=set(t[1] for t in transitions),
                                  data=0.0)
        
        for trans, count in trans_counts.items():
            if len(trans) == 2:
                trans_matrix.loc[trans[0], trans[1]] = count
        
        fig, ax = plt.subplots(figsize=(20, 15))
        sns.heatmap(trans_matrix, cmap='magma', annot=True, fmt='.0f')
        plt.title('Padrões de Transição entre Letras')
        plt.xlabel('Segunda Letra')
        plt.ylabel('Primeira Letra')
        heatmaps.append(self.plot_and_save(fig, '07_padroes_transicao'))

        return heatmaps

    def run_analysis(self):
        try:
            yaml_path = self.get_latest_yaml()
            console.print(Panel(f"[green]Analisando arquivo: {yaml_path}[/green]"))
            
            df = self.load_yaml_data(yaml_path)
            df = self.generate_word_metrics(df)
            
            # Exibir indicadores estatísticos
            self.display_statistical_indicators(df)
            
            console.print("[yellow]Gerando heatmaps...[/yellow]")
            heatmaps = self.generate_heatmaps(df)
            
            console.print(Panel(
                f"[green]Análise concluída![/green]\n"
                f"Gerados {len(heatmaps)} heatmaps em {self.output_dir}",
                title="✨ Processo Concluído"
            ))
            
        except Exception as e:
            console.print(f"[red]Erro durante a análise: {str(e)}[/red]")

    def display_statistical_indicators(self, df):
        """Exibe 44 indicadores estatísticos em 4 grids coloridos"""
        console = Console()
        
        # Definir o padrão regex fora da f-string
        padrao_vogais_repetidas = r'([aeiou])\1'
        
        # Cálculo dos indicadores
        indicators = {
            "📊 Análise Básica": {
                "Total de Palavras": len(df),
                "Média de Comprimento": f"{df['tamanho'].mean().item():.2f}",
                "Palavras Únicas": len(df['palavra'].unique()),
                "Maior Palavra": df['tamanho'].max().item(),
                "Menor Palavra": df['tamanho'].min().item(),
                "Moda de Comprimento": df['tamanho'].mode().iloc[0].item(),
                "Desvio Padrão": f"{df['tamanho'].std().item():.2f}",
                "Mediana": df['tamanho'].median().item(),
                "Variância": f"{df['tamanho'].var().item():.2f}",
                "Amplitude": (df['tamanho'].max() - df['tamanho'].min()).item(),
                "Quartil Superior": df['tamanho'].quantile(0.75).item(),
            },
            "🔤 Análise Fonética": {
                "Média de Vogais": f"{df['vogais'].mean().item():.2f}",
                "Média de Consoantes": f"{df['consoantes'].mean().item():.2f}",
                "Razão V/C Média": f"{df['razao_vc'].mean().item():.2f}",
                "Máx. Seq. Vogais": df['seq_vogais'].max().item(),
                "Máx. Seq. Consoantes": df['seq_consoantes'].max().item(),
                "% Palavras com Ditongo": f"{(df['seq_vogais'] >= 2).mean().item() * 100:.1f}%",
                "Vogais Iniciais": f"{df['inicio'].str.match('[aeiouAEIOU]').mean().item() * 100:.1f}%",
                "Consoantes Finais": f"{df['fim'].str.match('[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]').mean().item() * 100:.1f}%",
                "Média Complexidade": f"{df['complexidade'].mean().item():.2f}",
                "Índice Harmônico": f"{(df['vogais'] / df['tamanho']).mean().item():.2f}",
                "Padrão Silábico": f"{(df['consoantes'] / df['vogais']).mean().item():.2f}",
            },
            "📈 Métricas Avançadas": {
                "Entropia Média": f"{df['palavra'].apply(lambda x: len(set(x))/len(x)).mean().item():.2f}",
                "Diversidade Lexical": f"{len(df['palavra'].unique())/len(df):.2f}",
                "Índice de Repetição": f"{df['palavra'].value_counts().mean().item():.2f}",
                "Complexidade Estrutural": f"{(df['especiais'] * df['tamanho']).mean().item():.2f}",
                "Densidade Fonética": f"{((df['vogais'] + df['consoantes'])/df['tamanho']).mean().item():.2f}",
                "Variabilidade": f"{(df['tamanho'].std()/df['tamanho'].mean()).item():.2f}",
                "Índice de Regularidade": f"{(df['palavra'].str.count(padrao_vogais_repetidas)/df['tamanho']).mean().item():.2f}",
                "Score de Complexidade": f"{(df['complexidade'] * df['especiais']).mean().item():.2f}",
                "Índice de Variação": f"{df['palavra'].apply(lambda x: len(set(x))).std().item():.2f}",
                "Métrica de Coesão": f"{(df['seq_vogais'] / df['seq_consoantes']).mean().item():.2f}",
                "Fator de Equilíbrio": f"{abs(df['vogais'].mean() - df['consoantes'].mean()).item():.2f}",
            },
            "🎯 Indicadores Especiais": {
                "Padrão de Início": df['inicio'].mode().iloc[0],
                "Padrão de Fim": df['fim'].mode().iloc[0],
                "Letras Mais Comuns": ''.join(df['palavra'].str.split('').explode().value_counts().head(3).index),
                "Sequência Típica": f"{df['seq_vogais'].mode().iloc[0]}-{df['seq_consoantes'].mode().iloc[0]}",
                "Perfil Estrutural": f"V{df['vogais'].mode().iloc[0]}C{df['consoantes'].mode().iloc[0]}",
                "Índice de Pureza": f"{(df['especiais'] == 0).mean().item() * 100:.1f}%",
                "Padrão Dominante": "VC" if df['vogais'].mean().item() < df['consoantes'].mean().item() else "CV",
                "Tendência Central": f"{df['tamanho'].mode().iloc[0]}±{df['tamanho'].std().item():.1f}",
                "Marca Estrutural": "Simple" if df['complexidade'].mean().item() < 10 else "Complex",
                "Perfil Fonético": "Vocálico" if df['vogais'].mean().item() > df['consoantes'].mean().item() else "Consonantal",
                "Assinatura Lexical": f"{df['tamanho'].quantile(0.25).item():.0f}-{df['tamanho'].quantile(0.75).item():.0f}"
            }
        }

        # Criando o layout
        layout = Layout()
        layout.split_column(
            Layout(name="upper", ratio=1),
            Layout(name="lower", ratio=1)
        )
        layout["upper"].split_row(
            Layout(name="top_left"),
            Layout(name="top_right")
        )
        layout["lower"].split_row(
            Layout(name="bottom_left"),
            Layout(name="bottom_right")
        )

        # Função auxiliar para criar tabelas
        def create_table(title, data):
            table = Table(title=title, box=box.ROUNDED, show_header=True, header_style="bold magenta")
            table.add_column("Indicador", style="cyan", width=30)
            table.add_column("Valor", style="green", width=20)
            for key, value in data.items():
                table.add_row(key, str(value))
            return table

        # Criando as tabelas
        layout["top_left"].update(Panel(create_table("📊 Análise Básica", indicators["📊 Análise Básica"]), 
                                      border_style="blue"))
        layout["top_right"].update(Panel(create_table("🔤 Análise Fonética", indicators["🔤 Análise Fonética"]), 
                                     border_style="green"))
        layout["bottom_left"].update(Panel(create_table("📈 Métricas Avançadas", indicators["📈 Métricas Avançadas"]), 
                                         border_style="yellow"))
        layout["bottom_right"].update(Panel(create_table("🎯 Indicadores Especiais", indicators["🎯 Indicadores Especiais"]), 
                                          border_style="red"))

        # Exibindo o layout
        console.print("\n=== 📊 ANÁLISE ESTATÍSTICA DETALHADA ===\n")
        console.print(layout)
        console.print("\n=== 🎯 ANÁLISE CONCLUÍDA ===\n")

if __name__ == "__main__":
    analyzer = WordVectorHeatmapAnalyzer()
    analyzer.run_analysis()
