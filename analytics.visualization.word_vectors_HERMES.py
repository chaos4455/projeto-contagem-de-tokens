import yaml
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import numpy as np
from collections import Counter
import re
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich import box
import colorama
from colorama import Fore, Back, Style

# Inicialização
colorama.init()
console = Console()
plt.style.use('default')

class WordVectorAnalyzer:
    def __init__(self):
        self.output_dir = Path("words-vectors-reports-22")
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.metrics = {}
        
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
        """Gera métricas para cada palavra"""
        df['tamanho'] = df['palavra'].str.len()
        df['vogais'] = df['palavra'].str.count(r'[aeiouAEIOU]')
        df['consoantes'] = df['palavra'].str.count(r'[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]')
        df['especiais'] = df['palavra'].str.count(r'[^a-zA-Z]')
        return df

    def plot_and_save(self, fig, nome):
        """Salva o gráfico com timestamp"""
        plt.tight_layout()
        caminho = self.output_dir / f"{nome}_{self.timestamp}.png"
        fig.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close(fig)
        return caminho

    def calculate_advanced_metrics(self, df):
        """Calcula métricas avançadas para o dashboard"""
        self.metrics = {
            'básico': {
                'Total de Palavras': len(df),
                'Palavras Únicas': df['palavra'].nunique(),
                'Tamanho Médio': df['tamanho'].mean(),
                'Maior Palavra': df['tamanho'].max(),
                'Menor Palavra': df['tamanho'].min(),
            },
            'complexidade': {
                'Média de Vogais': df['vogais'].mean(),
                'Média de Consoantes': df['consoantes'].mean(),
                'Razão Vogal/Consoante': df['vogais'].sum() / df['consoantes'].sum(),
                'Palavras com Caracteres Especiais': (df['especiais'] > 0).sum(),
                'Complexidade Média': df['tamanho'].std(),
            },
            'distribuição': {
                'Mediana Tamanho': df['tamanho'].median(),
                'Moda Tamanho': df['tamanho'].mode().iloc[0],
                'Desvio Padrão': df['tamanho'].std(),
                'Assimetria': df['tamanho'].skew(),
                'Curtose': df['tamanho'].kurtosis(),
            },
            # ... mais categorias de métricas
        }

    def display_metrics_dashboard(self):
        """Exibe dashboard com métricas no console"""
        layout = Layout()
        layout.split_column(
            Layout(name="header"),
            Layout(name="main")
        )

        # Cabeçalho
        header = Panel(
            Text("📊 Análise Detalhada do Conjunto de Palavras", style="bold magenta"),
            box=box.DOUBLE
        )
        layout["header"].update(header)

        # Criar grid principal
        main_grid = Table.grid(padding=1)
        main_grid.add_column()
        main_grid.add_column()

        # Criar tabelas para cada categoria
        table_rows = []
        for category, metrics in self.metrics.items():
            table = Table(title=f"[bold blue]{category.title()}[/bold blue]", 
                         box=box.ROUNDED,
                         show_header=True,
                         header_style="bold cyan")
            
            table.add_column("Métrica", style="cyan")
            table.add_column("Valor", style="green")
            
            for metric, value in metrics.items():
                if isinstance(value, float):
                    formatted_value = f"{value:.2f}"
                else:
                    formatted_value = str(value)
                table.add_row(metric, formatted_value)
            
            table_rows.append(Panel(table, border_style="blue"))

        # Organizar tabelas em grid 2x2
        for i in range(0, len(table_rows), 2):
            if i + 1 < len(table_rows):
                main_grid.add_row(table_rows[i], table_rows[i + 1])
            else:
                main_grid.add_row(table_rows[i], "")

        layout["main"].update(main_grid)
        console.print(layout)

    def generate_visualizations(self, df):
        """Gera visualizações detalhadas"""
        visualizations = []
        
        # 1-10. Análises básicas individuais
        # 1. Distribuição de tamanhos
        fig, ax = plt.subplots(figsize=(15, 8))
        plt.hist(df['tamanho'], bins=30, edgecolor='black')
        plt.title('Distribuição do Tamanho das Palavras')
        plt.xlabel('Tamanho da Palavra')
        plt.ylabel('Frequência')
        visualizations.append(self.plot_and_save(fig, '01_tamanho_distribuicao'))

        # 2. Distribuição de vogais
        fig, ax = plt.subplots(figsize=(15, 8))
        plt.hist(df['vogais'], bins=20, edgecolor='black')
        plt.title('Distribuição de Vogais por Palavra')
        plt.xlabel('Número de Vogais')
        plt.ylabel('Frequência')
        visualizations.append(self.plot_and_save(fig, '02_vogais_distribuicao'))

        # 3. Distribuição de consoantes
        fig, ax = plt.subplots(figsize=(15, 8))
        plt.hist(df['consoantes'], bins=20, edgecolor='black')
        plt.title('Distribuição de Consoantes por Palavra')
        plt.xlabel('Número de Consoantes')
        plt.ylabel('Frequência')
        visualizations.append(self.plot_and_save(fig, '03_consoantes_distribuicao'))

        # 11-22. Análises de correlação
        # 11. Vogais vs Consoantes
        fig, ax = plt.subplots(figsize=(15, 8))
        plt.scatter(df['vogais'], df['consoantes'], alpha=0.5)
        plt.title('Correlação entre Vogais e Consoantes')
        plt.xlabel('Número de Vogais')
        plt.ylabel('Número de Consoantes')
        z = np.polyfit(df['vogais'], df['consoantes'], 1)
        p = np.poly1d(z)
        plt.plot(df['vogais'], p(df['vogais']), "r--", alpha=0.8)
        visualizations.append(self.plot_and_save(fig, '11_correlacao_vogais_consoantes'))

        # 12. Tamanho vs Complexidade
        df['complexidade'] = df['tamanho'] * (df['especiais'] + 1)
        fig, ax = plt.subplots(figsize=(15, 8))
        plt.scatter(df['tamanho'], df['complexidade'], alpha=0.5)
        plt.title('Relação entre Tamanho e Complexidade')
        plt.xlabel('Tamanho da Palavra')
        plt.ylabel('Índice de Complexidade')
        visualizations.append(self.plot_and_save(fig, '12_tamanho_complexidade'))

        # 23-33. Análises de padrões
        # 23. Padrões de Início/Fim combinados
        fig, ax = plt.subplots(figsize=(15, 8))
        inicio_fim = df.apply(lambda x: f"{x['palavra'][0]}_{x['palavra'][-1]}", axis=1)
        inicio_fim.value_counts().head(20).plot(kind='bar')
        plt.title('Top 20 Combinações de Letras Iniciais/Finais')
        plt.xlabel('Padrão (Inicial_Final)')
        plt.ylabel('Frequência')
        plt.xticks(rotation=45)
        visualizations.append(self.plot_and_save(fig, '23_padrao_inicio_fim'))

        # 34-44. Análises avançadas e cruzamentos
        # 34. Matriz de correlação
        correlation_metrics = ['tamanho', 'vogais', 'consoantes', 'especiais', 'complexidade']
        corr_matrix = df[correlation_metrics].corr()
        fig, ax = plt.subplots(figsize=(12, 10))
        im = ax.imshow(corr_matrix)
        plt.colorbar(im)
        plt.xticks(range(len(correlation_metrics)), correlation_metrics, rotation=45)
        plt.yticks(range(len(correlation_metrics)), correlation_metrics)
        plt.title('Matriz de Correlação entre Métricas')
        for i in range(len(correlation_metrics)):
            for j in range(len(correlation_metrics)):
                text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                             ha="center", va="center", color="w")
        visualizations.append(self.plot_and_save(fig, '34_matriz_correlacao'))

        # 35. Análise de Proporções
        df['prop_vogais'] = df['vogais'] / df['tamanho']
        df['prop_consoantes'] = df['consoantes'] / df['tamanho']
        df['prop_especiais'] = df['especiais'] / df['tamanho']

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6))
        ax1.hist(df['prop_vogais'], bins=20)
        ax1.set_title('Proporção de Vogais')
        ax2.hist(df['prop_consoantes'], bins=20)
        ax2.set_title('Proporção de Consoantes')
        ax3.hist(df['prop_especiais'], bins=20)
        ax3.set_title('Proporção de Caracteres Especiais')
        plt.tight_layout()
        visualizations.append(self.plot_and_save(fig, '35_proporcoes'))

        # 36. Análise de Sequências
        df['sequencia_vogais'] = df['palavra'].apply(lambda x: len(max(re.findall(r'[aeiouAEIOU]+', x), key=len, default='')))
        df['sequencia_consoantes'] = df['palavra'].apply(lambda x: len(max(re.findall(r'[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]+', x), key=len, default='')))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
        ax1.hist(df['sequencia_vogais'], bins=range(max(df['sequencia_vogais'])+2), align='left')
        ax1.set_title('Maior Sequência de Vogais')
        ax1.set_xlabel('Tamanho da Sequência')
        ax2.hist(df['sequencia_consoantes'], bins=range(max(df['sequencia_consoantes'])+2), align='left')
        ax2.set_title('Maior Sequência de Consoantes')
        ax2.set_xlabel('Tamanho da Sequência')
        plt.tight_layout()
        visualizations.append(self.plot_and_save(fig, '36_sequencias'))

        # 37. Análise de Proporções por Tamanho
        fig, ax = plt.subplots(figsize=(15, 8))
        tamanho_grupos = pd.cut(df['tamanho'], bins=5)
        prop_por_tamanho = df.groupby(tamanho_grupos)['prop_vogais'].mean()
        prop_por_tamanho.plot(kind='bar')
        plt.title('Proporção Média de Vogais por Faixa de Tamanho')
        plt.xlabel('Faixa de Tamanho da Palavra')
        plt.ylabel('Proporção Média de Vogais')
        plt.xticks(rotation=45)
        visualizations.append(self.plot_and_save(fig, '37_proporcao_por_tamanho'))

        # 38. Top 10 Padrões de Início
        fig, ax = plt.subplots(figsize=(12, 12))
        inicio_counts = df['palavra'].str[:2].value_counts().head(10)
        plt.pie(inicio_counts, labels=inicio_counts.index, autopct='%1.1f%%')
        plt.title('Top 10 Padrões de Início de Palavras (Primeiras 2 Letras)')
        visualizations.append(self.plot_and_save(fig, '38_top_inicios_pie'))

        # 39. Distribuição de Palavras por Comprimento (Linha)
        fig, ax = plt.subplots(figsize=(15, 8))
        tamanho_counts = df['tamanho'].value_counts().sort_index()
        plt.plot(tamanho_counts.index, tamanho_counts.values, marker='o')
        plt.title('Distribuição de Palavras por Comprimento')
        plt.xlabel('Comprimento da Palavra')
        plt.ylabel('Quantidade de Palavras')
        plt.grid(True)
        visualizations.append(self.plot_and_save(fig, '39_distribuicao_tamanho_linha'))

        # 40. Análise de Terminações
        fig, ax = plt.subplots(figsize=(15, 8))
        terminacoes = df['palavra'].str[-2:].value_counts().head(15)
        terminacoes.plot(kind='bar')
        plt.title('15 Terminações Mais Comuns (Últimas 2 Letras)')
        plt.xlabel('Terminação')
        plt.ylabel('Frequência')
        plt.xticks(rotation=45)
        visualizations.append(self.plot_and_save(fig, '40_terminacoes_comuns'))

        # 41. Distribuição de Complexidade
        fig, ax = plt.subplots(figsize=(15, 8))
        df['complexidade_total'] = df['tamanho'] * df['consoantes'] / (df['vogais'] + 1)
        plt.hist(df['complexidade_total'], bins=30, edgecolor='black')
        plt.title('Distribuição do Índice de Complexidade Total')
        plt.xlabel('Índice de Complexidade')
        plt.ylabel('Frequência')
        visualizations.append(self.plot_and_save(fig, '41_complexidade_total'))

        # 42. Padrões de Sílabas
        fig, ax = plt.subplots(figsize=(12, 12))
        df['padrao_silaba'] = df['palavra'].apply(lambda x: 'CV' if len(x) >= 2 else 'O')
        padrao_counts = df['padrao_silaba'].value_counts()
        plt.pie(padrao_counts, labels=padrao_counts.index, autopct='%1.1f%%')
        plt.title('Distribuição de Padrões Silábicos')
        visualizations.append(self.plot_and_save(fig, '42_padroes_silabicos'))

        # 43. Análise Temporal de Complexidade
        fig, ax = plt.subplots(figsize=(15, 8))
        df['indice'] = range(len(df))
        plt.plot(df['indice'], df['complexidade_total'].rolling(window=50).mean())
        plt.title('Tendência de Complexidade (Média Móvel)')
        plt.xlabel('Índice da Palavra')
        plt.ylabel('Complexidade Média (Janela de 50 palavras)')
        plt.grid(True)
        visualizations.append(self.plot_and_save(fig, '43_tendencia_complexidade'))

        # 44. Distribuição de Caracteres Especiais
        fig, ax = plt.subplots(figsize=(15, 8))
        especiais_dist = df['especiais'].value_counts().sort_index()
        plt.bar(especiais_dist.index, especiais_dist.values)
        plt.title('Distribuição de Caracteres Especiais por Palavra')
        plt.xlabel('Número de Caracteres Especiais')
        plt.ylabel('Quantidade de Palavras')
        visualizations.append(self.plot_and_save(fig, '44_distribuicao_especiais'))

        # 45. Análise de Vogais vs Tamanho (Scatter com densidade)
        fig, ax = plt.subplots(figsize=(15, 8))
        plt.hexbin(df['tamanho'], df['vogais'], gridsize=20, cmap='YlOrRd')
        plt.colorbar(label='Densidade')
        plt.title('Relação entre Tamanho e Número de Vogais')
        plt.xlabel('Tamanho da Palavra')
        plt.ylabel('Número de Vogais')
        visualizations.append(self.plot_and_save(fig, '45_vogais_tamanho_densidade'))

        # 46. Proporção de Tipos de Caracteres
        fig, ax = plt.subplots(figsize=(12, 12))
        medias = [
            df['vogais'].mean(),
            df['consoantes'].mean(),
            df['especiais'].mean()
        ]
        labels = ['Vogais', 'Consoantes', 'Caracteres Especiais']
        plt.pie(medias, labels=labels, autopct='%1.1f%%')
        plt.title('Proporção Média de Tipos de Caracteres')
        visualizations.append(self.plot_and_save(fig, '46_proporcao_tipos_caracteres'))

        # 47. Análise de Sequências Repetidas
        fig, ax = plt.subplots(figsize=(15, 8))
        df['tem_repeticao'] = df['palavra'].apply(lambda x: bool(re.search(r'(.)\1', x)))
        repeticao_counts = df['tem_repeticao'].value_counts()
        plt.bar(repeticao_counts.index.map({True: 'Com Repetição', False: 'Sem Repetição'}), 
                repeticao_counts.values)
        plt.title('Palavras com Caracteres Repetidos Consecutivos')
        plt.ylabel('Quantidade de Palavras')
        visualizations.append(self.plot_and_save(fig, '47_caracteres_repetidos'))

        # 48. Distribuição de Razão Vogal/Consoante
        fig, ax = plt.subplots(figsize=(15, 8))
        df['razao_vc'] = df['vogais'] / (df['consoantes'] + 1)
        plt.hist(df['razao_vc'], bins=30, edgecolor='black')
        plt.title('Distribuição da Razão Vogal/Consoante')
        plt.xlabel('Razão Vogal/Consoante')
        plt.ylabel('Frequência')
        visualizations.append(self.plot_and_save(fig, '48_razao_vogal_consoante'))

        # 49. Padrões de Início por Tamanho
        fig, ax = plt.subplots(figsize=(15, 8))
        inicio_tamanho = df.groupby('tamanho')['palavra'].apply(lambda x: x.str[0].value_counts().head(1).index[0])
        plt.plot(inicio_tamanho.index, inicio_tamanho.values, marker='o')
        plt.title('Letra Inicial Mais Comum por Tamanho de Palavra')
        plt.xlabel('Tamanho da Palavra')
        plt.ylabel('Letra Inicial Mais Comum')
        plt.grid(True)
        visualizations.append(self.plot_and_save(fig, '49_inicio_por_tamanho'))

        # 50. Análise de Complexidade por Tamanho
        fig, ax = plt.subplots(figsize=(15, 8))
        complexidade_tamanho = df.groupby('tamanho')['complexidade_total'].mean()
        plt.plot(complexidade_tamanho.index, complexidade_tamanho.values, marker='o')
        plt.title('Complexidade Média por Tamanho de Palavra')
        plt.xlabel('Tamanho da Palavra')
        plt.ylabel('Complexidade Média')
        plt.grid(True)
        visualizations.append(self.plot_and_save(fig, '50_complexidade_por_tamanho'))

        # 51-55. Análises de subgrupos e tendências
        # 51. Análise de Complexidade por Grupos de Tamanho
        fig, ax = plt.subplots(figsize=(15, 8))
        df['grupo_tamanho'] = pd.qcut(df['tamanho'], q=5, labels=['Muito Curtas', 'Curtas', 'Médias', 'Longas', 'Muito Longas'])
        grupo_complexidade = df.groupby('grupo_tamanho')['complexidade_total'].mean().sort_values()
        plt.bar(range(len(grupo_complexidade)), grupo_complexidade.values)
        plt.xticks(range(len(grupo_complexidade)), grupo_complexidade.index, rotation=45)
        plt.title('Complexidade Média por Grupo de Tamanho')
        plt.xlabel('Grupo de Palavras')
        plt.ylabel('Complexidade Média')
        plt.grid(True, axis='y')
        visualizations.append(self.plot_and_save(fig, '51_complexidade_grupos'))

        # 52. Distribuição de Tipos de Caracteres por Tamanho
        fig, ax = plt.subplots(figsize=(15, 8))
        tamanhos_unicos = sorted(df['tamanho'].unique())
        prop_tipos = df.groupby('tamanho').agg({
            'vogais': 'mean',
            'consoantes': 'mean',
            'especiais': 'mean'
        })
        plt.plot(tamanhos_unicos, prop_tipos['vogais'], 'b-', label='Vogais', marker='o')
        plt.plot(tamanhos_unicos, prop_tipos['consoantes'], 'r-', label='Consoantes', marker='s')
        plt.plot(tamanhos_unicos, prop_tipos['especiais'], 'g-', label='Especiais', marker='^')
        plt.title('Distribuição de Tipos de Caracteres por Tamanho')
        plt.xlabel('Tamanho da Palavra')
        plt.ylabel('Média de Caracteres')
        plt.legend()
        plt.grid(True)
        visualizations.append(self.plot_and_save(fig, '52_distribuicao_tipos_tamanho'))

        # 53. Padrões de Terminação por Tamanho
        fig, ax = plt.subplots(figsize=(15, 8))
        terminacoes_por_tamanho = df.groupby('tamanho')['palavra'].apply(
            lambda x: x.str[-1].value_counts().head(1).values[0]
        )
        plt.plot(terminacoes_por_tamanho.index, terminacoes_por_tamanho.values, 'o-')
        plt.title('Frequência da Terminação Mais Comum por Tamanho')
        plt.xlabel('Tamanho da Palavra')
        plt.ylabel('Frequência da Terminação Mais Comum')
        plt.grid(True)
        visualizations.append(self.plot_and_save(fig, '53_terminacoes_tamanho'))

        # 54. Análise de Diversidade por Tamanho
        fig, ax = plt.subplots(figsize=(15, 8))
        diversidade = df.groupby('tamanho')['palavra'].agg(
            lambda x: len(set(x)) / len(x)
        ) * 100
        plt.bar(diversidade.index, diversidade.values)
        plt.title('Diversidade de Palavras por Tamanho')
        plt.xlabel('Tamanho da Palavra')
        plt.ylabel('Porcentagem de Palavras Únicas')
        plt.grid(True, axis='y')
        visualizations.append(self.plot_and_save(fig, '54_diversidade_tamanho'))

        # 55. Análise de Padrões Silábicos por Tamanho
        fig, ax = plt.subplots(figsize=(15, 8))
        df['padrao_silabico'] = df['vogais'].astype(str) + 'v' + df['consoantes'].astype(str) + 'c'
        padroes_por_tamanho = df.groupby('tamanho')['padrao_silabico'].agg(
            lambda x: x.value_counts().head(1).index[0]
        )
        plt.plot(padroes_por_tamanho.index, [float(p.split('v')[0]) for p in padroes_por_tamanho.values], 'bo-', label='Vogais')
        plt.plot(padroes_por_tamanho.index, [float(p.split('c')[0].split('v')[1]) for p in padroes_por_tamanho.values], 'ro-', label='Consoantes')
        plt.title('Padrão Silábico Mais Comum por Tamanho')
        plt.xlabel('Tamanho da Palavra')
        plt.ylabel('Quantidade de Caracteres')
        plt.legend()
        plt.grid(True)
        visualizations.append(self.plot_and_save(fig, '55_padroes_silabicos_tamanho'))

        return visualizations

    def run_analysis(self):
        try:
            yaml_path = self.get_latest_yaml()
            console.print(Panel(f"[green]Analisando arquivo: {yaml_path}[/green]"))
            
            df = self.load_yaml_data(yaml_path)
            df = self.generate_word_metrics(df)
            
            # Calcular métricas avançadas
            self.calculate_advanced_metrics(df)
            
            # Exibir dashboard
            self.display_metrics_dashboard()
            
            # Gerar visualizações
            visualizations = self.generate_visualizations(df)
            
            console.print(Panel(
                f"[green]Análise concluída![/green]\n"
                f"Gerados {len(visualizations)} gráficos em {self.output_dir}",
                title="✨ Processo Concluído"
            ))
            
        except Exception as e:
            console.print(f"[red]Erro durante a análise: {str(e)}[/red]")

if __name__ == "__main__":
    analyzer = WordVectorAnalyzer()
    analyzer.run_analysis()
