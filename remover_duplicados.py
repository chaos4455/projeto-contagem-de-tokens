import os
import hashlib
from pathlib import Path
from datetime import datetime
import logging
from collections import defaultdict
import shutil

class LimpadorDuplicados:
    def __init__(self):
        self.pasta_base = Path("backup_restaurado")
        self.arquivos_por_hash = defaultdict(list)
        self.total_original = 0
        self.total_removido = 0
        self.espaco_liberado = 0
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('limpeza_duplicados.log'),
                logging.StreamHandler()
            ]
        )

    def calcular_hash_arquivo(self, caminho_arquivo):
        """Calcula o hash SHA256 do arquivo"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(caminho_arquivo, "rb") as f:
                for bloco in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(bloco)
            return hash_sha256.hexdigest()
        except Exception as e:
            logging.error(f"Erro ao calcular hash de {caminho_arquivo}: {e}")
            return None

    def mapear_arquivos(self):
        """Mapeia todos os arquivos e seus hashes"""
        logging.info("Iniciando mapeamento de arquivos...")
        
        for caminho_arquivo in self.pasta_base.rglob("*"):
            if caminho_arquivo.is_file():
                self.total_original += 1
                hash_arquivo = self.calcular_hash_arquivo(caminho_arquivo)
                if hash_arquivo:
                    # Guarda o caminho e a data de modificação
                    data_mod = os.path.getmtime(caminho_arquivo)
                    self.arquivos_por_hash[hash_arquivo].append({
                        'caminho': caminho_arquivo,
                        'data_mod': data_mod,
                        'tamanho': caminho_arquivo.stat().st_size
                    })

        logging.info(f"Total de arquivos encontrados: {self.total_original}")

    def remover_duplicados(self):
        """Remove arquivos duplicados mantendo o mais recente"""
        logging.info("Iniciando remoção de duplicados...")
        
        for hash_arquivo, arquivos in self.arquivos_por_hash.items():
            if len(arquivos) > 1:
                # Ordena por data de modificação (mais recente primeiro)
                arquivos_ordenados = sorted(
                    arquivos, 
                    key=lambda x: x['data_mod'], 
                    reverse=True
                )
                
                # Mantém o primeiro (mais recente) e remove os outros
                for arquivo in arquivos_ordenados[1:]:
                    try:
                        caminho = arquivo['caminho']
                        tamanho = arquivo['tamanho']
                        data_mod = datetime.fromtimestamp(arquivo['data_mod'])
                        
                        logging.info(f"Removendo duplicado: {caminho}")
                        logging.info(f"Data modificação: {data_mod}")
                        logging.info(f"Tamanho: {tamanho/1024/1024:.2f} MB")
                        
                        caminho.unlink()
                        
                        self.total_removido += 1
                        self.espaco_liberado += tamanho
                        
                    except Exception as e:
                        logging.error(f"Erro ao remover {caminho}: {e}")

    def remover_pastas_vazias(self):
        """Remove pastas que ficaram vazias após a remoção dos duplicados"""
        logging.info("Removendo pastas vazias...")
        
        for pasta in sorted(self.pasta_base.rglob("*"), reverse=True):
            if pasta.is_dir():
                try:
                    pasta.rmdir()  # Só remove se estiver vazia
                    logging.info(f"Pasta vazia removida: {pasta}")
                except OSError:
                    pass  # Ignora pastas não vazias

    def gerar_relatorio(self):
        """Gera relatório final da limpeza"""
        logging.info("\nRelatório Final de Limpeza:")
        logging.info(f"Total de arquivos originais: {self.total_original}")
        logging.info(f"Arquivos removidos: {self.total_removido}")
        logging.info(f"Espaço liberado: {self.espaco_liberado/1024/1024:.2f} MB")
        logging.info(f"Arquivos únicos restantes: {self.total_original - self.total_removido}")

    def executar_limpeza(self):
        """Executa todo o processo de limpeza"""
        try:
            logging.info("Iniciando processo de limpeza de duplicados...")
            
            if not self.pasta_base.exists():
                logging.error(f"Pasta {self.pasta_base} não encontrada!")
                return
            
            self.mapear_arquivos()
            self.remover_duplicados()
            self.remover_pastas_vazias()
            self.gerar_relatorio()
            
            logging.info("Processo de limpeza concluído com sucesso!")
            
        except Exception as e:
            logging.error(f"Erro durante o processo de limpeza: {e}")

def main():
    limpador = LimpadorDuplicados()
    limpador.executar_limpeza()

if __name__ == "__main__":
    main()

