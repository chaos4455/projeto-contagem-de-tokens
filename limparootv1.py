import os
import shutil
from pathlib import Path

def criar_pastas():
    Path("logs").mkdir(exist_ok=True)
    Path("zip").mkdir(exist_ok=True)

def gerar_novo_nome(caminho_destino, nome_arquivo):
    nome_base = os.path.splitext(nome_arquivo)[0]
    extensao = os.path.splitext(nome_arquivo)[1]
    contador = 0
    
    while True:
        if contador == 0:
            novo_nome = nome_arquivo
        else:
            novo_nome = f"{nome_base}_version{contador:03d}{extensao}"
            
        caminho_completo = os.path.join(caminho_destino, novo_nome)
        if not os.path.exists(caminho_completo):
            return novo_nome
        contador += 1

def mover_arquivos():
    for arquivo in os.listdir('.'):
        if os.path.isfile(arquivo):
            if arquivo.endswith('.log'):
                pasta_destino = 'logs'
            elif arquivo.endswith('.zip'):
                pasta_destino = 'zip'
            else:
                continue
            
            novo_nome = gerar_novo_nome(pasta_destino, arquivo)
            shutil.move(arquivo, os.path.join(pasta_destino, novo_nome))
            print(f"Movido: {arquivo} -> {pasta_destino}/{novo_nome}")

def main():
    criar_pastas()
    mover_arquivos()
    print("Organização concluída!")

if __name__ == "__main__":
    main()
