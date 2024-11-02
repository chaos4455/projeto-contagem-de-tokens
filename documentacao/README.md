# 🤖 Projeto de Geração de Embeddings com IA para RAG

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Maintainability](https://api.codeclimate.com/v1/badges/github/EliasAndrade/projeto-contagem-de-tokens/maintainability)](https://codeclimate.com/github/EliasAndrade/projeto-contagem-de-tokens/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/github/EliasAndrade/projeto-contagem-de-tokens/test_coverage)](https://codeclimate.com/github/EliasAndrade/projeto-contagem-de-tokens/test_coverage)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/EliasAndrade/projeto-contagem-de-tokens/CI)](https://github.com/EliasAndrade/projeto-contagem-de-tokens/actions)
[![Downloads](https://img.shields.io/github/downloads/EliasAndrade/projeto-contagem-de-tokens/total.svg)](https://github.com/EliasAndrade/projeto-contagem-de-tokens/releases)


## 📋 Índice
- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Arquitetura](#arquitetura)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Configuração](#configuração)
- [Métricas e Monitoramento](#métricas-e-monitoramento)
- [Solução de Problemas (Troubleshooting)](#solução-de-problemas-troubleshooting)
- [Perguntas Frequentes (FAQ)](#perguntas-frequentes-faq)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Scripts do Projeto](#scripts-do-projeto)


## 🎯 Sobre o Projeto

Este projeto é uma solução avançada para geração de embeddings vetoriais utilizando Inteligência Artificial, especialmente projetado para alimentar sistemas RAG (Retrieval-Augmented Generation). O sistema processa documentos em YAML, gera embeddings utilizando modelos BERT e oferece uma interface rica para visualização e análise de métricas em tempo real.  Ele foi desenvolvido com foco em eficiência, escalabilidade e facilidade de uso, permitindo o processamento de grandes conjuntos de dados de forma eficiente.

### 🌟 Principais Características

- Geração de embeddings vetoriais de alta qualidade utilizando modelos pré-treinados de última geração.
- Processamento em stream para grandes volumes de dados, permitindo o processamento de arquivos YAML de qualquer tamanho sem sobrecarregar a memória.
- Integração com múltiplos modelos de IA (BERT, Sentence Transformers, e potencialmente outros modelos via APIs), oferecendo flexibilidade e adaptabilidade a diferentes necessidades.
- Interface rica com a biblioteca Rich, fornecendo uma experiência de usuário intuitiva e informativa com métricas em tempo real.
- Otimização de recursos computacionais através do uso de processamento paralelo (multithreading e multiprocessing), reduzindo o tempo de processamento.
- Cache inteligente de embeddings para evitar cálculos redundantes e acelerar o processamento subsequente.
- Suporte a processamento paralelo para maximizar o uso de recursos multi-core.
- Robustez e tratamento de erros para garantir a estabilidade do sistema.


## 🛠 Funcionalidades

### Processamento de Dados
- **Conversão de documentos YAML para embeddings:** O sistema lê arquivos YAML contendo texto e gera embeddings vetoriais correspondentes.  Suporta diferentes estruturas de YAML, desde listas simples até estruturas complexas aninhadas.
- **Tokenização avançada com BERT:** Utiliza o modelo BERT para tokenizar o texto, considerando o contexto e a semântica das palavras.  Isso garante uma representação vetorial mais precisa e significativa.
- **Análise semântica com Sentence Transformers:** Emprega modelos Sentence Transformers para capturar a semântica do texto, resultando em embeddings que refletem melhor o significado do conteúdo.
- **Cache de embeddings para otimização:** Armazena os embeddings gerados em cache para evitar cálculos repetidos, melhorando significativamente o desempenho, especialmente para grandes conjuntos de dados com textos repetidos ou similares.  O cache é persistido em disco para uso em sessões subsequentes.

### Métricas e Análises
- **Contagem de tokens:** Fornece a contagem precisa de tokens para cada documento processado, permitindo o monitoramento do tamanho do texto e a otimização do uso de recursos.
- **Análise de densidade semântica:** Calcula a densidade semântica dos embeddings, fornecendo insights sobre a riqueza e complexidade do conteúdo.
- **Monitoramento de recursos (CPU, GPU, Memória):** Monitora o uso de recursos do sistema em tempo real, permitindo a identificação de gargalos e a otimização do desempenho.
- **Estatísticas de processamento em tempo real:** Exibe estatísticas de processamento, como tempo de processamento, taxa de processamento e progresso geral.

### Visualização
- **Interface rica com Rich library:** Utiliza a biblioteca Rich para criar uma interface de linha de comando (CLI) interativa e visualmente atraente.
- **Painéis interativos:** Apresenta painéis interativos que permitem a navegação e a análise das métricas.
- **Gráficos de progresso:** Exibe gráficos de progresso em tempo real, mostrando o andamento do processamento.
- **Indicadores de performance:** Fornece indicadores de performance chave (KPIs) para monitorar a eficiência do sistema.


## 🔧 Tecnologias Utilizadas

- **Python 3.9+:** Linguagem de programação principal.
- **BERT (bert-base-uncased):** Modelo de linguagem pré-treinado para tokenização e geração de embeddings.
- **Sentence Transformers:** Biblioteca para gerar embeddings semânticos de alta qualidade.
- **Google Gemini API (opcional):**  Integração opcional com a API do Google Gemini para geração de embeddings ainda mais avançados. (Requer chave de API)
- **PyTorch:** Framework para processamento de dados e cálculos de embeddings.
- **NLTK:** Biblioteca para processamento de linguagem natural (NLP).
- **Rich:** Biblioteca para criar interfaces de usuário ricas e interativas na linha de comando.
- **YAML:** Formato de dados utilizado para entrada e saída de documentos.
- **Asyncio:** Biblioteca para programação assíncrona, otimizando o processamento de dados.
- **Threading e Multiprocessing:** Técnicas de processamento paralelo para acelerar o processamento.
- **SQLite:** Banco de dados para armazenamento persistente de embeddings (opcional, para cache).


## 🏗 Arquitetura

O projeto utiliza uma arquitetura modular e escalável, composta pelos seguintes componentes principais:

- **Módulo de Pré-processamento:** Responsável pela leitura e validação dos arquivos YAML, limpeza de dados e tokenização do texto utilizando modelos BERT.
- **Módulo de Geração de Embeddings:** Gera os embeddings vetoriais utilizando modelos Sentence Transformers, otimizado para processamento em stream e com cache inteligente para melhorar o desempenho.
- **Módulo de Armazenamento:**  Utiliza um banco de dados SQLite para armazenar os embeddings gerados, permitindo acesso eficiente e persistência dos dados.
- **Módulo de Análise:** Realiza análises de métricas, incluindo contagem de tokens, densidade semântica e monitoramento de recursos do sistema.
- **Módulo de Visualização:**  Fornece uma interface de usuário rica e interativa via CLI (usando a biblioteca Rich) para exibir as métricas e resultados em tempo real.

Esta arquitetura modular permite fácil manutenção, extensão e escalabilidade do sistema.  O design segue os princípios SOLID para garantir a manutenibilidade e a escalabilidade do código.  O sistema é projetado para lidar com grandes volumes de dados de forma eficiente, utilizando processamento paralelo e técnicas de otimização de memória.


## ⚙️ Instalação

1. **Clone o repositório:** `git clone https://github.com/EliasAndrade/projeto-contagem-de-tokens.git`
2. **Crie um ambiente virtual (recomendado):** `python3 -m venv .venv`
3. **Ative o ambiente virtual:** `.venv\Scripts\activate` (Windows)
4. **Instale as dependências:** `pip install -r requirements.txt`
5. **(Opcional) Configure a API Key do Google Gemini:**  Adicione sua chave de API no arquivo `config.yaml`.


## 🎬 Como Usar

1. **Prepare seus dados:** Organize seus dados em arquivos YAML, com cada arquivo contendo um ou mais documentos.
2. **Execute o script principal:** `python main.py --input_dir <caminho_para_seus_arquivos_yaml>`
3. **Monitore o progresso:** A interface Rich exibirá o progresso do processamento, as métricas e os resultados.
4. **Analise os resultados:** Os embeddings gerados serão salvos em um banco de dados SQLite (ou em memória, dependendo da configuração).  Você pode acessar os embeddings e as métricas através da interface.


## ⚙️ Configuração

O arquivo `config.yaml` permite configurar diversos aspectos do projeto, incluindo:

- `input_dir`: Caminho para a pasta contendo os arquivos YAML de entrada.
- `output_dir`: Caminho para a pasta onde os resultados serão salvos.
- `model_name`: Nome do modelo BERT a ser utilizado.
- `cache_size`: Tamanho máximo do cache de embeddings (em MB).
- `num_workers`: Número de workers para processamento paralelo.
- `use_gemini_api`:  `true` ou `false` para habilitar/desabilitar a API do Google Gemini.
- `gemini_api_key`: Chave de API do Google Gemini (se `use_gemini_api` for `true`).


## 📊 Métricas e Monitoramento

O sistema monitora e exibe as seguintes métricas:

- **Tempo de processamento:** Tempo total gasto para processar todos os documentos.
- **Taxa de processamento:** Número de documentos processados por segundo.
- **Uso de CPU:** Porcentagem de uso da CPU durante o processamento.
- **Uso de RAM:** Quantidade de memória RAM utilizada durante o processamento.
- **Tamanho do cache:** Tamanho atual do cache de embeddings.
- **Número de tokens:** Contagem total de tokens processados.
- **Densidade semântica média:** Densidade semântica média dos embeddings gerados.


## 🐞 Solução de Problemas (Troubleshooting)

- **Erro de importação de bibliotecas:** Certifique-se de ter instalado todas as dependências listadas em `requirements.txt`.
- **Erro de conexão com a API do Google Gemini:** Verifique sua chave de API e sua conexão com a internet.
- **Erro de processamento de arquivos YAML:** Certifique-se de que seus arquivos YAML estão bem formatados.
- **Uso excessivo de memória:** Aumente o tamanho do cache ou reduza o número de workers.


## ❓ Perguntas Frequentes (FAQ)

- **Qual o tamanho máximo de arquivo YAML que o sistema suporta?**  O sistema suporta arquivos YAML de qualquer tamanho, graças ao processamento em stream.
- **Posso usar outros modelos de linguagem além do BERT?**  Sim, o sistema pode ser adaptado para usar outros modelos, desde que sejam compatíveis com a biblioteca Sentence Transformers.
- **Como posso contribuir para o projeto?**  Veja a seção "Contribuição".


## 🤝 Contribuição

Contribuições são bem-vindas!  Por favor, abra um pull request com suas alterações.


## 📄 Licença

Este projeto está licenciado sob a Licença MIT.

## 📜 Scripts do Projeto

Esta seção descreve os scripts Python principais do projeto:

### `automacao_organiza_projeto_restaura_backup_v1.py`

Este script automatiza o processo de backup, restauração e organização dos arquivos do projeto. Ele utiliza a biblioteca `rich` para exibir mensagens formatadas no console e `logging` para registrar eventos.  As principais funcionalidades incluem:

- **Backup:** Cria um backup completo do projeto.
- **Restauração:** Restaura um backup anterior.
- **Organização:** Organiza os arquivos em pastas específicas por extensão (`.log`, `.txt`, `.json`, `.zip`).
- **Tratamento de Duplicatas:** Renomeia arquivos com nomes duplicados, adicionando um hash único ao nome.
- **Monitoramento:** Exibe o progresso e as estatísticas da automação.

### `backup_projeto.py`

Este script cria um backup completo do projeto em um arquivo ZIP. Ele calcula o tamanho da pasta, gera um hash único para cada backup, obtém a última versão do backup e usa a biblioteca `rich` para criar um dashboard visual com as estatísticas do backup.  Ele também inclui tratamento de erros e logging.

### `banco_tokens.py`

Este script define funções para interagir com um banco de dados SQLite que armazena tokens e embeddings gerados pelo sistema.  As funções principais são:

- `create_database()`: Cria o banco de dados SQLite se ele não existir.
- `generate_unique_hash(input_text)`: Gera um hash SHA256 único para um dado texto.
- `analyze_bert(text, model_name="bert-base-uncased")`: Usa o modelo BERT para gerar tokens e embeddings para um dado texto.
- `insert_data(input_text, tokens, embeddings, db_name="tokens_database.db")`: Insere os dados (timestamp, hash único, texto, tokens e embeddings) no banco de dados.

### `contador_tokens_menu.py`

Este script fornece um menu interativo para analisar tokens e embeddings. Ele permite ao usuário escolher entre várias ações, incluindo analisar vetores brutos, listar IDs aleatórios ou específicos, analisar indicadores estatísticos, calcular a similaridade de cosseno entre vetores, exibir KPIs e sair.  Ele usa as bibliotecas `inquirer`, `colorama`, `matplotlib` e `scipy`.

### `gerador_yaml_embeddings_stream_v1.py`

Este script gera arquivos YAML usando a API do Google Gemini em modo de streaming. Ele inclui processamento de tokens BERT em threads separadas, monitoramento de recursos do sistema e um painel de estatísticas em tempo real usando a biblioteca `rich`.  Ele também calcula métricas avançadas, como densidade semântica e diversidade lexical.  As principais características incluem:

- **Geração de YAML em Streaming:** Gera arquivos YAML usando a API do Google Gemini com streaming para lidar com grandes quantidades de texto.
- **Processamento de Tokens BERT Multi-threaded:** Utiliza o modelo BERT para tokenizar o texto em paralelo, melhorando o desempenho.
- **Monitoramento de Recursos:** Monitora o uso de CPU, memória e GPU (se disponível) em tempo real.
- **Painel de Estatísticas:** Exibe um painel interativo com estatísticas de processamento, incluindo contagem de tokens, palavras, tempo de processamento, uso de recursos e outras métricas.
- **Métricas Avançadas:** Calcula métricas como densidade semântica, diversidade lexical e outras métricas relevantes para análise de texto.

### `gerador_yaml_embeddings-prompt-v2.py`

Este script gera arquivos YAML contendo listas de palavras para embeddings, usando a API do Google Gemini. Ele permite configurar a geração (temperatura, top_p, etc.) e inclui um prompt de sistema para garantir a qualidade e diversidade do texto gerado.

### `gerador_yaml_embeddings.py`

Este script gera arquivos YAML com configurações para embeddings de texto, usando a API do Google Gemini. Ele permite ao usuário especificar um tema e o número de iterações, gerando arquivos YAML com diferentes configurações.

### `gerador-dic-texto-yaml-v1.py`

Este script gera um arquivo de texto contendo um e-book estruturado em capítulos, usando a API do Google Gemini. O usuário fornece o nome do e-book e o tema, e o script gera os tópicos e o conteúdo de cada capítulo.

### `limpar_duplicados_avancado.py`

Este script realiza uma limpeza avançada de duplicados, comparando arquivos com base em seus hashes SHA256. Ele remove duplicados internos em uma pasta de backup e arquivos do backup que já existem na pasta raiz.  Ele também remove pastas vazias.
