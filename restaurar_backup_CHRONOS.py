import os
import zipfile
from datetime import datetime
import shutil
from pathlib import Path
import logging

class RestauradorBackup:
    def __init__(self):
        self.pasta_backup = Path("backup")
        self.pasta_restauracao = Path("backup_restaurado")
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('restauracao_backup.log'),
                logging.StreamHandler()
            ]
        )

    def obter_data_modificacao(self, arquivo):
        return os.path.getmtime(arquivo)

    def listar_zips_recentes(self):
        try:
            # Lista todos os arquivos .zip na pasta backup
            arquivos_zip = []
            for root, _, files in os.walk(self.pasta_backup):
                for file in files:
                    if file.endswith('.zip'):
                        caminho_completo = Path(root) / file
                        arquivos_zip.append(caminho_completo)

            # Ordena por data de modificação e pega os 10 mais recentes
            arquivos_zip.sort(key=self.obter_data_modificacao, reverse=True)
            return arquivos_zip[:50]

        except Exception as e:
            logging.error(f"Erro ao listar arquivos ZIP: {e}")
            return []

    def extrair_zip(self, arquivo_zip):
        try:
            # Cria nome da pasta baseado no nome do zip
            nome_pasta = arquivo_zip.stem
            pasta_destino = self.pasta_restauracao / nome_pasta
            
            # Cria pasta de destino
            pasta_destino.mkdir(parents=True, exist_ok=True)

            logging.info(f"Extraindo {arquivo_zip} para {pasta_destino}")

            with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
                zip_ref.extractall(pasta_destino)

            return True

        except Exception as e:
            logging.error(f"Erro ao extrair {arquivo_zip}: {e}")
            return False

    def restaurar_backups(self):
        try:
            # Cria pasta de restauração se não existir
            self.pasta_restauracao.mkdir(parents=True, exist_ok=True)

            # Obtém os 10 zips mais recentes
            zips_recentes = self.listar_zips_recentes()

            if not zips_recentes:
                logging.warning("Nenhum arquivo ZIP encontrado na pasta backup")
                return

            # Conta arquivos processados com sucesso
            sucessos = 0

            # Processa cada zip
            for zip_file in zips_recentes:
                if self.extrair_zip(zip_file):
                    sucessos += 1
                    logging.info(f"Backup restaurado com sucesso: {zip_file.name}")
                else:
                    logging.error(f"Falha ao restaurar backup: {zip_file.name}")

            # Relatório final
            logging.info(f"\nResumo da restauração:")
            logging.info(f"Total de arquivos processados: {len(zips_recentes)}")
            logging.info(f"Restaurações bem-sucedidas: {sucessos}")
            logging.info(f"Falhas: {len(zips_recentes) - sucessos}")

        except Exception as e:
            logging.error(f"Erro durante o processo de restauração: {e}")

def main():
    restaurador = RestauradorBackup()
    restaurador.restaurar_backups()

if __name__ == "__main__":
    main()

# ----CHRONOS----
