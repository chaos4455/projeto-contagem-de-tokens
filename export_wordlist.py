import sqlite3
import json
import yaml
import hashlib
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from collections import Counter
from typing import Dict, List, Tuple
import statistics
from dataclasses import dataclass

class WordlistExporterV2:
    def __init__(self):
        self.console = Console()
        
    def verificar_estrutura_banco(self, cursor):
        """Verifica as colunas existentes na tabela"""
        cursor.execute("PRAGMA table_info(word_vectors)")
        colunas = {coluna[1] for coluna in cursor.fetchall()}
        return colunas
        
    def buscar_palavras_do_banco(self, cursor, colunas_existentes):
        """Busca palavras do banco adaptando-se às colunas existentes"""
        query_base = 'SELECT word, LENGTH(vector) as vector_size'
        
        if 'timestamp' in colunas_existentes:
            query = f"{query_base}, datetime(timestamp) as timestamp FROM word_vectors ORDER BY word"
        else:
            query = f"{query_base}, datetime('now') as timestamp FROM word_vectors ORDER BY word"
            
        cursor.execute(query)
        return cursor.fetchall()

    def analisar_palavras(self, palavras: List[str]) -> Dict:
        """Análise detalhada das palavras"""
        vogais = set('aeiouáéíóúâêîôûãõàèìòùäëïöü')
        
        stats = {
            'metricas_basicas': {
                'total_palavras': len(palavras),
                'palavras_unicas': len(set(palavras)),
                'comprimento_medio': round(statistics.mean(len(p) for p in palavras), 2),
                'comprimento_mediano': statistics.median(len(p) for p in palavras),
                'desvio_padrao_comprimento': round(statistics.stdev(len(p) for p in palavras), 2) if len(palavras) > 1 else 0,
            },
            'analise_caracteres': {
                'distribuicao_primeira_letra': dict(Counter(p[0].lower() for p in palavras).most_common(10)),
                'chars_especiais': dict(Counter(c for p in palavras for c in p if not c.isalnum()).most_common(10)),
                'vogais_mais_comuns': dict(Counter(c for p in palavras for c in p.lower() if c in vogais).most_common(10)),
                'consoantes_mais_comuns': dict(Counter(c for p in palavras for c in p.lower() if c.isalpha() and c not in vogais).most_common(10))
            },
            'distribuicao_tamanhos': dict(Counter(len(p) for p in palavras)),
            'padroes_linguisticos': {
                'prefixos_comuns': dict(Counter(p[:3] for p in palavras if len(p) > 3).most_common(10)),
                'sufixos_comuns': dict(Counter(p[-3:] for p in palavras if len(p) > 3).most_common(10)),
            },
            'indicadores_estatisticos': {
                'densidade_lexica': round(len(set(palavras)) / len(palavras), 4),
                'palavras_por_tamanho': self.agrupar_por_tamanho(palavras),
                'distribuicao_acentuacao': self.analisar_acentuacao(palavras),
            }
        }
        return stats

    def agrupar_por_tamanho(self, palavras: List[str]) -> Dict[int, int]:
        """Agrupa palavras por tamanho"""
        return dict(sorted(Counter(len(p) for p in palavras).items()))

    def analisar_acentuacao(self, palavras: List[str]) -> Dict[str, int]:
        """Analisa padrões de acentuação"""
        acentos = 'áéíóúâêîôûãõàèìòùäëïöü'
        return {
            'palavras_com_acento': sum(1 for p in palavras if any(c in p for c in acentos)),
            'palavras_sem_acento': sum(1 for p in palavras if not any(c in p for c in acentos))
        }

    def exportar_palavras(self):
        """Exporta palavras e análises para JSON e YAML"""
        output_dir = Path('vector-exported-data')
        output_dir.mkdir(exist_ok=True)
        
        try:
            with sqlite3.connect('vetor-words-database-index.db') as conn:
                cursor = conn.cursor()
                
                # Verifica estrutura do banco
                colunas_existentes = self.verificar_estrutura_banco(cursor)
                
                # Busca dados adaptando-se às colunas existentes
                resultados = self.buscar_palavras_do_banco(cursor, colunas_existentes)
                
                palavras = [row[0] for row in resultados]
                
                # Realizar análises
                analytics = self.analisar_palavras(palavras)
                
                # Preparar dados para exportação
                data = {
                    'metadata': {
                        'timestamp_export': datetime.now().isoformat(),
                        'total_palavras': len(palavras),
                        'versao_exportador': '2.0.1',
                        'banco_origem': 'vetor-words-database-index.db',
                        'colunas_disponiveis': list(colunas_existentes)
                    },
                    'analytics': analytics,
                    'palavras': sorted(palavras)  # Lista ordenada de palavras
                }
                
                # Gerar hash e nomes de arquivo
                hash_arquivo = hashlib.sha256(json.dumps(data, ensure_ascii=False).encode()).hexdigest()[:8]
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                base_filename = f'wordlist_v2_{timestamp}_{hash_arquivo}'
                
                # Exportar JSON
                json_path = output_dir / f'{base_filename}.json'
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                # Exportar YAML
                yaml_path = output_dir / f'{base_filename}.yaml'
                with open(yaml_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, allow_unicode=True, sort_keys=False)
                
                # Exibir relatório
                self.exibir_relatorio(data, base_filename)
                
        except Exception as e:
            self.console.print(f"[red]Erro durante a exportação: {str(e)}[/]")
            raise
    
    def exibir_relatorio(self, data: Dict, filename: str):
        """Exibe relatório detalhado com indicadores"""
        self.console.print("\n[bold green]✨ Exportação Concluída com Sucesso![/]\n")
        
        # Tabela principal
        table = Table(title="📊 Resumo da Exportação")
        table.add_column("Métrica", style="cyan", justify="right")
        table.add_column("Valor", style="magenta")
        
        # Métricas básicas
        for key, value in data['analytics']['metricas_basicas'].items():
            table.add_row(
                key.replace('_', ' ').title(),
                f"{value:.2f}" if isinstance(value, float) else str(value)
            )
        
        self.console.print(table)
        
        # Painéis de análise
        panels = []
        
        # Distribuição de tamanhos
        dist_table = Table(title="📏 Distribuição de Tamanhos")
        dist_table.add_column("Tamanho", justify="center")
        dist_table.add_column("Quantidade", justify="right")
        for size, count in sorted(data['analytics']['distribuicao_tamanhos'].items())[:10]:
            dist_table.add_row(str(size), str(count))
        panels.append(Panel(dist_table, title="Distribuição"))
        
        # Caracteres mais comuns
        chars_table = Table(title="🔤 Caracteres Mais Comuns")
        chars_table.add_column("Tipo", justify="right")
        chars_table.add_column("Top 5", justify="left")
        for char_type, chars in data['analytics']['analise_caracteres'].items():
            chars_str = ", ".join(f"{c}({n})" for c, n in list(chars.items())[:5])
            chars_table.add_row(char_type.replace('_', ' ').title(), chars_str)
        panels.append(Panel(chars_table, title="Caracteres"))
        
        # Exibir painéis
        self.console.print(Columns(panels))
        
        # Informações do arquivo
        self.console.print(f"\n[blue]📁 Arquivos gerados:[/]")
        self.console.print(f"  • JSON: {filename}.json")
        self.console.print(f"  • YAML: {filename}.yaml")
        self.console.print(f"[blue]🔑 Hash do conteúdo:[/] {filename.split('_')[-1]}")
        self.console.print(f"\n[green]✅ Total de palavras exportadas:[/] {data['metadata']['total_palavras']}")

if __name__ == '__main__':
    console = Console()
    console.print("[yellow]🚀 Iniciando exportação da lista de palavras...[/]")
    
    try:
        exporter = WordlistExporterV2()
        exporter.exportar_palavras()
    except Exception as e:
        console.print(f"[red]❌ Erro fatal: {str(e)}[/]")
