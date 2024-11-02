import os
import shutil
import hashlib
from datetime import datetime
import pandas as pd

def calcula_hash_arquivo(caminho_arquivo):
    """Calcula o hash SHA-256 do arquivo"""
    hash_sha256 = hashlib.sha256()
    with open(caminho_arquivo, 'rb') as f:
        for bloco in iter(lambda: f.read(4096), b''):
            hash_sha256.update(bloco)
    return hash_sha256.hexdigest()

def coleta_info_arquivos(pasta_origem):
    """Coleta informações dos arquivos .py em todas as subpastas"""
    info_arquivos = []
    
    for raiz, _, arquivos in os.walk(pasta_origem):
        for arquivo in arquivos:
            if arquivo.endswith('.py'):
                caminho_completo = os.path.join(raiz, arquivo)
                stats = os.stat(caminho_completo)
                
                info = {
                    'nome_original': arquivo,
                    'caminho_completo': caminho_completo,
                    'data_criacao': datetime.fromtimestamp(stats.st_ctime),
                    'data_modificacao': datetime.fromtimestamp(stats.st_mtime),
                    'hash': calcula_hash_arquivo(caminho_completo)
                }
                info_arquivos.append(info)
    
    return pd.DataFrame(info_arquivos)

def cria_pasta_destino():
    """Cria a pasta de destino se não existir"""
    pasta_destino = 'backup-versionado-restaurado'
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    return pasta_destino

def processa_arquivos_versionados(df, pasta_destino):
    """Processa e copia os arquivos para a pasta de destino com versionamento"""
    # Ordena por nome e data de modificação
    df_ordenado = df.sort_values(['nome_original', 'data_modificacao'])
    
    # Dicionário para controlar arquivos já processados
    arquivos_processados = {}
    
    for _, row in df_ordenado.iterrows():
        nome_base, extensao = os.path.splitext(row['nome_original'])
        hash_atual = row['hash']
        
        # Verifica se já existe um arquivo com mesmo nome
        if nome_base in arquivos_processados:
            arquivo_anterior = arquivos_processados[nome_base]
            
            # Se o hash for diferente, adiciona revision ao mais recente
            if hash_atual != arquivo_anterior['hash']:
                # Encontra próxima revision disponível
                revision = 1
                while True:
                    novo_nome = f"{nome_base}--revision--{revision:05d}{extensao}"
                    if not os.path.exists(os.path.join(pasta_destino, novo_nome)):
                        break
                    revision += 1
                
                nome_final = novo_nome
                
                # Atualiza o registro do arquivo mais recente
                arquivos_processados[nome_base] = {
                    'nome': nome_final,
                    'hash': hash_atual,
                    'caminho': row['caminho_completo']
                }
            else:
                # Hash igual, ignora o arquivo
                continue
        else:
            # Primeiro arquivo com este nome
            nome_final = f"{nome_base}{extensao}"
            arquivos_processados[nome_base] = {
                'nome': nome_final,
                'hash': hash_atual,
                'caminho': row['caminho_completo']
            }
        
        # Copia o arquivo para o destino
        caminho_destino = os.path.join(pasta_destino, nome_final)
        shutil.copy2(row['caminho_completo'], caminho_destino)
    
    return arquivos_processados

def main():
    pasta_origem = 'backup_restaurado'
    
    if not os.path.exists(pasta_origem):
        print(f"Pasta {pasta_origem} não encontrada!")
        return
    
    print("Coletando informações dos arquivos...")
    df_arquivos = coleta_info_arquivos(pasta_origem)
    
    if df_arquivos.empty:
        print("Nenhum arquivo .py encontrado na pasta de origem!")
        return
    
    pasta_destino = cria_pasta_destino()
    
    print("Processando e copiando arquivos...")
    arquivos_processados = processa_arquivos_versionados(df_arquivos, pasta_destino)
    
    # Prepara relatório
    relatorio = []
    for nome_base, info in arquivos_processados.items():
        relatorio.append({
            'Nome Original': nome_base,
            'Nome Final': info['nome'],
            'Hash': info['hash']
        })
    
    df_relatorio = pd.DataFrame(relatorio)
    
    # Salva e exibe o relatório
    relatorio_path = os.path.join(pasta_destino, 'relatorio_arquivos.csv')
    df_relatorio.to_csv(relatorio_path, index=False)
    
    print("\nResumo das operações:")
    print(f"Total de arquivos processados: {len(arquivos_processados)}")
    print("\nDetalhes dos arquivos:")
    print(df_relatorio.to_string())
    print(f"\nRelatório detalhado salvo em: {relatorio_path}")

if __name__ == "__main__":
    main()

# ----MNEMOSYNE----
