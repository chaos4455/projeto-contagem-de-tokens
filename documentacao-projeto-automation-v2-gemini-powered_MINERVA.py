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
import json
import locale


console = Console()


class DocumentacaoAutomatizadaAvancada:
    def __init__(self):
        self.pasta_raiz = Path(".")
        self.pasta_docs = Path("documentacao-automatizada")
        self.pasta_versoes = Path("documentacao-versoes")
        self.pasta_versoes.mkdir(exist_ok=True)
        self.setup_logging()
        self.configurar_ia()
        self.executor = ThreadPoolExecutor()
        self.arquivo_controle = self.pasta_versoes / "controle_hash.json"
        self.hashes_anteriores = self.carregar_hashes()
        # Configurar locale para português
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
            except:
                logging.warning("Não foi possível configurar locale para português")

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
            return {
                "nome": arquivo.name, 
                "caminho": str(arquivo), 
                "conteudo": conteudo,
                "codigo_fonte": conteudo, 
                "tipo": "python"
            }
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
        pasta_arquivo = self.pasta_versoes / nome_arquivo.stem
        pasta_arquivo.mkdir(exist_ok=True)
        
        arquivos_existentes = list(pasta_arquivo.glob(f"v*.md"))
        if not arquivos_existentes:
            return "0001"

        versoes = [int(arquivo.stem.replace('v', '')) for arquivo in arquivos_existentes]
        return f"{max(versoes) + 1:04d}"

    async def listar_arquivos_python(self):
        arquivos_py = []
        for arquivo in self.pasta_raiz.glob("*.py"):
            if arquivo.is_file():
                arquivos_py.append(arquivo.name)
        return arquivos_py

    def formatar_data_hora_extenso(self):
        agora = datetime.now()
        
        # Formatar data
        dia = agora.strftime("%d")
        mes = agora.strftime("%B").lower()
        ano = agora.strftime("%Y")
        dia_semana = agora.strftime("%A").lower()
        
        # Formatar hora
        hora = agora.strftime("%H")
        minuto = agora.strftime("%M")
        
        texto_data_hora = (
            f"Documentação gerada em {dia_semana}, {dia} de {mes} de {ano} "
            f"às {hora} horas e {minuto} minutos"
        )
        
        return texto_data_hora

    async def analisar_arquivo_com_ia(self, nome_arquivo):
        max_tentativas = 3
        tentativa = 0
        
        arquivo_path = self.pasta_raiz / nome_arquivo
        arquivo_info = await self.ler_arquivo_python(arquivo_path)
        data_hora_extenso = self.formatar_data_hora_extenso()
        
        if not arquivo_info:
            logging.error(f"Não foi possível ler o arquivo {nome_arquivo}")
            return None
        
        while tentativa < max_tentativas:
            try:
                prompt = f"""
                {data_hora_extenso}
                
                Analise o seguinte arquivo Python e gere uma documentação técnica detalhada.
                
                Nome do arquivo: {arquivo_info['nome']}
                Caminho: {arquivo_info['caminho']}
                
                CÓDIGO FONTE COMPLETO:
                ```python
                {arquivo_info['codigo_fonte']}
                ```

                Use a data e hora informada acima no início da documentação e em qualquer 
                referência temporal ao longo do documento.

                crie as documentações bem longas, detalhadas, use icones, emojis, use badges e shields 
                use muita shield e badges coloridas em tudo, estilizadas
                estilize o markdown com css e js, use tudo colorido e rico e bonito
                crie ao estado da arte
                fale de mim e fale em primeira pessoa, elias andrade - evolução it - 
                entenda o codigo fonte, documente e fale bem téncico bem arrogante
                seja detalhado e cubra o minucioso pra mostrar conhecimento


                sempre faça citações de musicas  e de filmes a ver com tecnologia, com ia, com automação, 
                sempre gere a documentação com sua perosnalidade

                sempre comente a documentação do ponto de vista de uma persona

                mas crie como sendo eu autentico e meu alter ego encapsulado pela ia

                eu gosto muito de filmes, de coisas antigas, nostalgias, sempre cite coisas assim, de contexto de coisas de filmes
                de coisas da cultura pos, pra dar contexto ao que está sendo feito e suas qualidades técnicas, as minhas qualidades em desenvolver tal projeto, etc
                sempre ressalte meu expertise, me venda profissionalmente e me ssustente, de forma sucinta, ser parecer forçado

                
                A documentação deve incluir:
                - Data e hora da geração da documentação
                - Visão geral e propósito do arquivo
                - Descrição detalhada de cada classe e método
                - Fluxo de execução principal
                - Dependências e requisitos
                - Exemplos de uso
                - Considerações técnicas importantes
                - Possíveis melhorias e recomendações
                - Análise de segurança e performance (se aplicável)


                sempre link os repos reais
                https://github.com/chaos4455
                https://github.com/evolucaoit
                https://github.com/replika-ai-solutions
                meu linkedin https://www.linkedin.com/in/itilmgf/ - 

                meus contatos oeliasandrade@gmail.com whatsapp 44 9 8859-7116

                Formato esperado:
                # Documentação Técnica: {nome_arquivo}
                
                > {data_hora_extenso}
                
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
                    await asyncio.sleep(2)
                else:
                    logging.error(f"Todas as tentativas falharam para {nome_arquivo}")
                    return None

    def carregar_hashes(self):
        try:
            if self.arquivo_controle.exists():
                with open(self.arquivo_controle, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logging.error(f"Erro ao carregar hashes: {e}")
            return {}

    def salvar_hashes(self):
        try:
            with open(self.arquivo_controle, 'w', encoding='utf-8') as f:
                json.dump(self.hashes_anteriores, f, indent=4)
        except Exception as e:
            logging.error(f"Erro ao salvar hashes: {e}")

    def calcular_hash_arquivo(self, caminho):
        try:
            with open(caminho, 'rb') as f:
                conteudo = f.read()
                return hashlib.sha256(conteudo).hexdigest()
        except Exception as e:
            logging.error(f"Erro ao calcular hash: {e}")
            return None

    async def processar_fila_documentacao(self):
        console.print("[bold blue]🚀 Iniciando processamento da fila de documentação...[/]")
        arquivos = await self.listar_arquivos_python()
        arquivos_processados = []

        for arquivo in arquivos:
            try:
                arquivo_path = Path(arquivo)
                hash_atual = self.calcular_hash_arquivo(arquivo_path)
                
                if not hash_atual:
                    continue

                # Verifica se o arquivo foi modificado
                if (arquivo not in self.hashes_anteriores or 
                    self.hashes_anteriores[arquivo] != hash_atual):
                    
                    pasta_arquivo = self.pasta_versoes / arquivo_path.stem
                    pasta_arquivo.mkdir(exist_ok=True)
                    
                    proxima_versao = self.obter_proxima_versao(arquivo_path)
                    nome_doc = f"v{proxima_versao}.md"
                    caminho_doc = pasta_arquivo / nome_doc

                    console.print(f"[yellow]📝 Processando: {arquivo} (Modificado)[/]")

                    documentacao = await self.analisar_arquivo_com_ia(arquivo)

                    if documentacao:
                        await self.escrever_arquivo(caminho_doc, documentacao)
                        metadata = {
                            "versao": proxima_versao,
                            "data_criacao": datetime.now().isoformat(),
                            "arquivo_original": str(arquivo_path),
                            "hash_arquivo": hash_atual,
                            "autor": "Elias Andrade - Evolução IT"
                        }
                        await self.escrever_metadata(
                            pasta_arquivo / f"v{proxima_versao}_metadata.yaml", 
                            metadata
                        )
                        
                        # Atualiza o hash no controle
                        self.hashes_anteriores[arquivo] = hash_atual
                        arquivos_processados.append(arquivo)
                        
                        console.print(f"[green]✅ Nova versão gerada: {pasta_arquivo}/{nome_doc}[/]")
                else:
                    console.print(f"[blue]ℹ️ Arquivo não modificado: {arquivo}[/]")

                await asyncio.sleep(1)

            except Exception as e:
                logging.error(f"Erro ao processar {arquivo}: {e}")
                continue

        if arquivos_processados:
            self.salvar_hashes()
            console.print(f"[green]✅ {len(arquivos_processados)} arquivos processados[/]")
        else:
            console.print("[yellow]ℹ️ Nenhum arquivo necessitou atualização[/]")

    async def escrever_arquivo(self, caminho, conteudo):
        try:
            async with aiofiles.open(caminho, "w", encoding="utf-8") as f:
                await f.write(conteudo)
        except Exception as e:
            logging.error(f"Erro ao escrever arquivo {caminho}: {e}")

    async def escrever_metadata(self, caminho, metadata):
        try:
            async with aiofiles.open(caminho, "w", encoding="utf-8") as f:
                await f.write(yaml.dump(metadata, allow_unicode=True))
        except Exception as e:
            logging.error(f"Erro ao escrever metadata {caminho}: {e}")

    async def executar(self):
        console.print("[bold blue]🚀 Iniciando documentação automatizada...[/]")
        await self.processar_fila_documentacao()


if __name__ == "__main__":
    import aiofiles

    doc = DocumentacaoAutomatizadaAvancada()
    asyncio.run(doc.executar())

# ----MINERVA----
