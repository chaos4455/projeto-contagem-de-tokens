import os
import hashlib
from pathlib import Path
from datetime import datetime
import logging
from collections import defaultdict
import shutil

class LimpadorAvancado:
    def __init__(self):
        self.pasta_backup = Path("backup_restaurado")
        self.pasta_raiz = Path(".")
        self.hashes_raiz = defaultdict(list)
        self.hashes_backup = defaultdict(list)
        self.total_removido = 0
        self.espaco_liberado = 0
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('limpeza_avancada.log'),
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

    def mapear_arquivos_raiz(self):
        """Mapeia todos os arquivos da raiz, exceto backup_restaurado"""
        logging.info("Mapeando arquivos da raiz...")
        
        pastas_ignorar = {
            self.pasta_backup,
            Path("venv"),
            Path("__pycache__"),
            Path(".git")
        }

        for caminho_arquivo in self.pasta_raiz.rglob("*"):
            # Verifica se o arquivo está em alguma pasta que deve ser ignorada
            if any(pasta in caminho_arquivo.parents for pasta in pastas_ignorar):
                continue
                
            if caminho_arquivo.is_file():
                hash_arquivo = self.calcular_hash_arquivo(caminho_arquivo)
                if hash_arquivo:
                    self.hashes_raiz[hash_arquivo].append({
                        'caminho': caminho_arquivo,
                        'data_mod': os.path.getmtime(caminho_arquivo),
                        'tamanho': caminho_arquivo.stat().st_size
                    })

        logging.info(f"Total de arquivos mapeados na raiz: {len(self.hashes_raiz)}")

    def mapear_arquivos_backup(self):
        """Mapeia todos os arquivos do backup_restaurado"""
        logging.info("Mapeando arquivos do backup_restaurado...")
        
        for caminho_arquivo in self.pasta_backup.rglob("*"):
            if caminho_arquivo.is_file():
                hash_arquivo = self.calcular_hash_arquivo(caminho_arquivo)
                if hash_arquivo:
                    self.hashes_backup[hash_arquivo].append({
                        'caminho': caminho_arquivo,
                        'data_mod': os.path.getmtime(caminho_arquivo),
                        'tamanho': caminho_arquivo.stat().st_size
                    })

        logging.info(f"Total de arquivos mapeados no backup: {len(self.hashes_backup)}")

    def remover_duplicados_internos(self):
        """Remove duplicados dentro do backup_restaurado"""
        logging.info("Removendo duplicados internos do backup_restaurado...")
        
        for hash_arquivo, arquivos in self.hashes_backup.items():
            if len(arquivos) > 1:
                # Ordena por data de modificação (mais recente primeiro)
                arquivos_ordenados = sorted(
                    arquivos, 
                    key=lambda x: x['data_mod'], 
                    reverse=True
                )
                
                # Mantém o primeiro (mais recente) e remove os outros
                for arquivo in arquivos_ordenados[1:]:
                    self._remover_arquivo(arquivo)

    def remover_duplicados_da_raiz(self):
        """Remove arquivos do backup que já existem na raiz"""
        logging.info("Removendo arquivos do backup que existem na raiz...")
        
        for hash_arquivo, arquivos_backup in self.hashes_backup.items():
            if hash_arquivo in self.hashes_raiz:
                # Se existe na raiz, remove todos do backup
                for arquivo in arquivos_backup:
                    self._remover_arquivo(arquivo)

    def _remover_arquivo(self, arquivo):
        """Função auxiliar para remover um arquivo e registrar"""
        try:
            caminho = arquivo['caminho']
            tamanho = arquivo['tamanho']
            data_mod = datetime.fromtimestamp(arquivo['data_mod'])
            
            logging.info(f"Removendo: {caminho}")
            logging.info(f"Data modificação: {data_mod}")
            logging.info(f"Tamanho: {tamanho/1024/1024:.2f} MB")
            
            caminho.unlink()
            
            self.total_removido += 1
            self.espaco_liberado += tamanho
            
        except Exception as e:
            logging.error(f"Erro ao remover {caminho}: {e}")

    def remover_pastas_vazias_geral(self):
        """Remove todas as pastas vazias do sistema"""
        logging.info("Removendo pastas vazias de todo o sistema...")
        
        # Primeiro remove pastas vazias do backup
        for pasta in sorted(self.pasta_backup.rglob("*"), reverse=True):
            if pasta.is_dir():
                try:
                    pasta.rmdir()
                    logging.info(f"Pasta vazia removida do backup: {pasta}")
                except OSError:
                    pass

        # Depois remove pastas vazias da raiz
        for pasta in sorted(self.pasta_raiz.rglob("*"), reverse=True):
            if pasta.is_dir() and not any(ignorar in str(pasta) for ignorar in ['venv', '__pycache__', '.git', 'backup_restaurado']):
                try:
                    pasta.rmdir()
                    logging.info(f"Pasta vazia removida da raiz: {pasta}")
                except OSError:
                    pass

    def gerar_relatorio(self):
        """Gera relatório final da limpeza"""
        logging.info("\nRelatório Final de Limpeza:")
        logging.info(f"Arquivos removidos: {self.total_removido}")
        logging.info(f"Espaço liberado: {self.espaco_liberado/1024/1024:.2f} MB")

    def executar_limpeza(self):
        """Executa todo o processo de limpeza"""
        try:
            logging.info("Iniciando processo de limpeza avançada...")
            
            if not self.pasta_backup.exists():
                logging.error(f"Pasta {self.pasta_backup} não encontrada!")
                return
            
            self.mapear_arquivos_raiz()
            self.mapear_arquivos_backup()
            self.remover_duplicados_internos()
            self.remover_duplicados_da_raiz()
            self.remover_pastas_vazias_geral()
            self.gerar_relatorio()
            
            logging.info("Processo de limpeza concluído com sucesso!")
            
        except Exception as e:
            logging.error(f"Erro durante o processo de limpeza: {e}")

def main():
    limpador = LimpadorAvancado()
    limpador.executar_limpeza()

if __name__ == "__main__":
    main() 