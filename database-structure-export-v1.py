import sqlite3
import os
from datetime import datetime
import glob

def get_next_version():
    # Verifica a pasta estrutura_banco
    if not os.path.exists('estrutura_banco'):
        os.makedirs('estrutura_banco')
    
    # Lista todos os arquivos existentes
    files = glob.glob('estrutura_banco/estrutura_*.txt')
    if not files:
        return "v0001"
    
    # Pega o último número de versão e incrementa
    versions = [int(f.split('_v')[1][:4]) for f in files]
    next_version = max(versions) + 1
    return f"v{next_version:04d}"

def analisar_banco_dados():
    # Pega a próxima versão
    versao = get_next_version()
    
    # Data e hora atual
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Encontra todos os arquivos .db na pasta atual
    arquivos_db = glob.glob('*.db')
    
    # Cria o arquivo de saída
    nome_arquivo = f'estrutura_banco/estrutura_{versao}.txt'
    
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write(f"=== ANÁLISE DE ESTRUTURA DE BANCOS DE DADOS ===\n")
        f.write(f"Data/Hora: {data_hora}\n")
        f.write(f"Versão: {versao}\n\n")
        
        for db_file in arquivos_db:
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                f.write(f"\n{'='*50}\n")
                f.write(f"BANCO DE DADOS: {db_file}\n")
                f.write(f"{'='*50}\n\n")
                
                # Lista todas as tabelas
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tabelas = cursor.fetchall()
                
                for tabela in tabelas:
                    nome_tabela = tabela[0]
                    f.write(f"\nTABELA: {nome_tabela}\n")
                    f.write("-" * 30 + "\n")
                    
                    # Obtém informações das colunas
                    cursor.execute(f"PRAGMA table_info('{nome_tabela}')")
                    colunas = cursor.fetchall()
                    
                    # Cabeçalho das colunas
                    f.write(f"{'Nome':<20} {'Tipo':<15} {'Nulo':<8} {'PK':<5}\n")
                    f.write("-" * 50 + "\n")
                    
                    for coluna in colunas:
                        nome = coluna[1]
                        tipo = coluna[2]
                        nulo = "Não" if coluna[3] else "Sim"
                        pk = "Sim" if coluna[5] else "Não"
                        
                        f.write(f"{nome:<20} {tipo:<15} {nulo:<8} {pk:<5}\n")
                    
                    # Conta número de registros
                    cursor.execute(f"SELECT COUNT(*) FROM '{nome_tabela}'")
                    count = cursor.fetchone()[0]
                    f.write(f"\nTotal de registros: {count}\n")
                    
                conn.close()
                
            except sqlite3.Error as e:
                f.write(f"\nERRO ao analisar {db_file}: {str(e)}\n")
    
    print(f"Análise concluída! Arquivo gerado: {nome_arquivo}")

if __name__ == "__main__":
    analisar_banco_dados()