import asyncio
import hashlib
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import google.generativeai as genai
import logging
from pathlib import Path
import sqlite3
import time
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
import yaml


console = Console()


class DocumentacaoAutomatizadaAvancada:
    def __init__(self):
        self.pasta_raiz = Path(".")
        self.pasta_docs = Path("documentacao-automatizada")
        self.pasta_versoes = Path("documentacao-versoes")
        self.pasta_docs.mkdir(exist_ok=True)
        self.pasta_versoes.mkdir(exist_ok=True)
        self.setup_logging()
        self.configurar_ia()
        self.executor = ThreadPoolExecutor()

    def configurar_ia(self):
        try:
            API_KEY = "AIzaSyCEagEEnX-RdkW3-jCAb0H9nrTsgcE-Qqo"
            genai.configure(api_key=API_KEY)
            self.modelo = genai.GenerativeModel("gemini-1.0-pro")
        except Exception as e:
            logging.error(f"Erro ao configurar IA: {e}")

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("documentacao_auto.log", encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )

    async def ler_todos_arquivos(self):
        arquivos_py = []
        arquivos_md = []
        estruturas_db = []

        for arquivo in self.pasta_raiz.glob("*"):
            if arquivo.is_file():
                if arquivo.suffix == ".py":
                    resultado = await self.ler_arquivo_python(arquivo)
                    if resultado:
                        arquivos_py.append(resultado)
                elif arquivo.suffix == ".md":
                    resultado = await self.ler_arquivo_markdown(arquivo)
                    if resultado:
                        arquivos_md.append(resultado)
                elif arquivo.suffix == ".db":
                    resultado = await self.analisar_estrutura_db(arquivo)
                    if resultado:
                        estruturas_db.append(resultado)

        return arquivos_py, arquivos_md, estruturas_db

    async def ler_arquivo_markdown(self, arquivo):
        try:
            async with aiofiles.open(arquivo, "r", encoding="utf-8") as f:
                conteudo = await f.read()
            return {"nome": arquivo.name, "caminho": str(arquivo), "conteudo": conteudo, "tipo": "markdown"}
        except Exception as e:
            logging.error(f"Erro ao ler arquivo Markdown {arquivo}: {e}")
            return None

    async def ler_arquivo_python(self, arquivo):
        try:
            async with aiofiles.open(arquivo, "r", encoding="utf-8") as f:
                conteudo = await f.read()
            return {"nome": arquivo.name, "caminho": str(arquivo), "conteudo": conteudo, "tipo": "python"}
        except Exception as e:
            logging.error(f"Erro ao ler arquivo Python {arquivo}: {e}")
            return None

    async def analisar_com_ia(self, conteudo_projeto, documentacao_basica):
        try:
            prompt = f"""
            Analise o seguinte projeto e gere uma documentação técnica detalhada em Markdown com pelo menos 3500 linhas.

            A documentação básica do projeto é:
            {documentacao_basica}

            Analise todo o conteúdo e inclua:
            - Visão geral detalhada do projeto
            - Arquitetura e componentes (com diagramas em ASCII se possível)
            - Funcionalidades principais de cada arquivo
            - Tecnologias utilizadas e suas versões
            - Fluxo de dados entre componentes
            - Considerações técnicas e boas práticas
            - Análise de segurança e performance
            - Melhorias sugeridas e roadmap técnico
            - Documentação de APIs e interfaces
            - Guia de instalação e configuração

            Conteúdo detalhado do projeto:
            {conteudo_projeto}
            """

            resposta = await self.modelo.generate_content_async(prompt)
            return resposta.text

        except Exception as e:
            logging.error(f"Erro na análise com IA: {e}")
            return None

    async def gerar_documentacao_avancada(self, arquivos_py, arquivos_md, estruturas_db):
        hash_doc = self.gerar_hash_unico()
        nome_arquivo = f"DOCUMENTACAO_{hash_doc}.md"
        nome_arquivo_ia = f"DOCUMENTACAO_IA_{hash_doc}.md"
        caminho_doc = self.pasta_docs / nome_arquivo
        caminho_doc_ia = self.pasta_docs / nome_arquivo_ia

        conteudo_basico = self.gerar_conteudo_basico(arquivos_py, estruturas_db)
        conteudo_completo = ""
        for arq in arquivos_py + arquivos_md:
            conteudo_completo += f"\n\n### {arq['caminho']}\n```\n{arq['conteudo']}\n```\n"

        analise_ia = await self.analisar_com_ia(conteudo_completo, conteudo_basico)

        try:
            if analise_ia:
                await self.escrever_arquivo(caminho_doc_ia, analise_ia)
            console.print(Panel(f"[green]✅ Documentação gerada com sucesso:\n{nome_arquivo_ia}"))

        except Exception as e:
            logging.error(f"Erro ao gerar documentação: {e}")

    async def executar(self):
        console.print("[bold blue]🚀 Iniciando geração de documentação automatizada avançada...[/]")

        arquivos_py, arquivos_md, estruturas_db = await self.ler_todos_arquivos()
        await self.gerar_documentacao_avancada(arquivos_py, arquivos_md, estruturas_db)

    def gerar_hash_unico(self):
        timestamp = str(datetime.now())
        hash_object = hashlib.sha256(timestamp.encode())
        return hash_object.hexdigest()[:8]

    def gerar_conteudo_basico(self, arquivos_py, estruturas_db):
        conteudo = "# Documentação Básica do Projeto\n\n"

        conteudo += "## Arquivos Python:\n"
        for arquivo in arquivos_py:
            conteudo += f"- {arquivo['nome']}\n"

        conteudo += "\n## Estruturas de Banco de Dados:\n"
        for db in estruturas_db:
            if db:
                conteudo += f"\n### {db['nome']}\n"
                for tabela, colunas in db["estrutura"].items():
                    conteudo += f"\n#### Tabela: {tabela}\n"
                    conteudo += "| Coluna | Tipo |\n|--------|------|\n"
                    for coluna in colunas:
                        conteudo += f"| {coluna['nome']} | {coluna['tipo']} |\n"

        return conteudo

    async def analisar_estrutura_db(self, arquivo):
        try:
            conn = sqlite3.connect(arquivo)
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tabelas = cursor.fetchall()

            estrutura_completa = {}
            for tabela in tabelas:
                nome_tabela = tabela[0]
                cursor.execute(f"PRAGMA table_info({nome_tabela})")
                colunas = cursor.fetchall()
                estrutura_completa[nome_tabela] = [
                    {"nome": col[1], "tipo": col[2]} for col in colunas
                ]

            conn.close()
            return {"nome": arquivo.name, "estrutura": estrutura_completa}
        except Exception as e:
            logging.error(f"Erro ao analisar banco de dados {arquivo}: {e}")
            return None

    def obter_proxima_versao(self, nome_arquivo):
        arquivos_existentes = list(self.pasta_versoes.glob(f"{nome_arquivo.stem}_v*.md"))
        if not arquivos_existentes:
            return "0001"

        versoes = [int(arquivo.stem.split("_v")[-1]) for arquivo in arquivos_existentes]
        return f"{max(versoes) + 1:04d}"

    async def listar_arquivos_python(self):
        arquivos_py = []
        for arquivo in self.pasta_raiz.glob("*.py"):
            if arquivo.is_file():
                arquivos_py.append(arquivo.name)
        return arquivos_py

    async def analisar_arquivo_com_ia(self, nome_arquivo):
        max_tentativas = 3
        tentativa = 0
        
        while tentativa < max_tentativas:
            try:
                prompt = f"""
                crie as documentações bem longas, detalhadas, use icones, emojis, use badges e shields 
                use muita shield e badges coloridas em tudo, estilizadas
                estilize o markdown com css e js, use tudo colorido e rico e bonito
                crie ao estado da arte
                fale de mim e fale em primeira pessoa, elias andrade - evolução it - 
                entenda o codigo fonte, documente e fale bem téncico bem arrogante
                seja detalhado e cubra o minucioso pra mostrar conhecimento
                Gere uma documentação técnica detalhada em Markdown para o arquivo Python: {nome_arquivo}

                A documentação deve incluir:
                - Visão geral e propósito do arquivo
                - Descrição detalhada de cada classe e método
                - Fluxo de execução principal
                - Dependências e requisitos
                - Exemplos de uso
                - Considerações técnicas importantes
                - Possíveis melhorias e recomendações
                - Análise de segurança e performance (se aplicável)

                Formato esperado:
                # Documentação Técnica: {nome_arquivo}

                ## Visão Geral
                [Sua análise aqui]

                ## Estrutura e Componentes
                [Sua análise aqui]

                [Continue com as demais seções...]
                """

                resposta = await self.modelo.generate_content_async(prompt)
                return resposta.text

            except Exception as e:
                tentativa += 1
                logging.error(f"Tentativa {tentativa} falhou para {nome_arquivo}: {e}")
                if tentativa < max_tentativas:
                    await asyncio.sleep(2)  # Espera 2 segundos antes de tentar novamente
                else:
                    logging.error(f"Todas as tentativas falharam para {nome_arquivo}")
                    return None

    async def processar_fila_documentacao(self):
        console.print("[bold blue]🚀 Iniciando processamento da fila de documentação...[/]")

        arquivos = await self.listar_arquivos_python()

        for arquivo in arquivos:
            try:
                proxima_versao = self.obter_proxima_versao(Path(arquivo))
                nome_doc = f"{Path(arquivo).stem}_v{proxima_versao}.md"
                caminho_doc = self.pasta_versoes / nome_doc

                console.print(f"[yellow]📝 Processando: {arquivo}[/]")

                documentacao = await self.analisar_arquivo_com_ia(arquivo)

                if documentacao:
                    await self.escrever_arquivo(caminho_doc, documentacao)
                    console.print(f"[green]✅ Documentação gerada: {nome_doc}[/]")

                await asyncio.sleep(2)

            except Exception as e:
                logging.error(f"Erro ao processar {arquivo}: {e}")
                continue

    async def escrever_arquivo(self, caminho, conteudo):
        try:
            async with aiofiles.open(caminho, "w", encoding="utf-8") as f:
                await f.write(conteudo)
        except Exception as e:
            logging.error(f"Erro ao escrever arquivo {caminho}: {e}")

    async def executar(self):
        console.print("[bold blue]🚀 Iniciando documentação automatizada...[/]")
        await self.processar_fila_documentacao()


if __name__ == "__main__":
    import aiofiles

    doc = DocumentacaoAutomatizadaAvancada()
    asyncio.run(doc.executar())