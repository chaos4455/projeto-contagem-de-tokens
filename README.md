# 🤖 Projeto de Geração de Embeddings com IA para RAG

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
- [Notas de Versão](#notas-de-versão)


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

O projeto segue uma arquitetura modular, organizada em diferentes módulos para facilitar a manutenção e a extensão. Os principais componentes são:

- **Módulo de Pré-processamento:** Responsável pela leitura dos arquivos YAML, limpeza de dados e tokenização do texto.
- **Módulo de Geração de Embeddings:** Gera os embeddings vetoriais utilizando os modelos BERT e Sentence Transformers.
- **Módulo de Cache:** Armazena os embeddings gerados em cache para otimizar o desempenho.
- **Módulo de Monitoramento:** Monitora o uso de recursos e coleta métricas de desempenho.
- **Módulo de Visualização:** Exibe as métricas e os resultados através da interface CLI com a biblioteca Rich.
- **Banco de Dados SQLite:** Armazena os tokens e embeddings gerados.

A comunicação entre os módulos é feita através de uma interface bem definida, permitindo a substituição de componentes sem afetar o funcionamento do sistema como um todo.  O design segue os princípios SOLID para garantir a manutenibilidade e a escalabilidade do código.

![Cursor_mvmaoYHBLG](https://github.com/user-attachments/assets/737aa609-f539-49dd-8135-4b0c60f74481)

![Cursor_Df7tQrj21A](https://github.com/user-attachments/assets/245b3ff5-902b-47fa-84d3-be4f4200c7e9)

![Cursor_YgJPNCky0X](https://github.com/user-attachments/assets/45dfe03e-bd7b-4669-aaa8-12cba53edd6b)

![Cursor_yE7siYz8tb](https://github.com/user-attachments/assets/2879f4db-c98b-4af1-8f01-ce5ad7f48890)

![Cursor_J37Yg5HPpS](https://github.com/user-attachments/assets/4bf36e23-a87f-403c-a0a6-87fb964d8ecd)

![Cursor_tbGFu8YfAX](https://github.com/user-attachments/assets/1465df9c-cc8d-4dfe-9cb1-73179ea90f7e)

![Cursor_EDfjSB1EXx](https://github.com/user-attachments/assets/2385bea4-8b7a-4ef6-b694-60265c51774d)

![Cursor_AJORiyMeec](https://github.com/user-attachments/assets/672c7fdd-368e-471e-ba0e-9ca3f20e6777)

![Cursor_bPdAl3i8a1](https://github.com/user-attachments/assets/47e92718-8f99-418c-af99-c888e17207c2)

![Cursor_0zTjXWxVMF](https://github.com/user-attachments/assets/47d10a7c-b53d-4a9b-9cbf-47f80d915ee4)

![Cursor_NrFpgAv6vu](https://github.com/user-attachments/assets/50d8bf54-0d3d-487c-a992-0812abbc3a53)

![Cursor_x2nTwEHCAn](https://github.com/user-attachments/assets/c79f4cd7-c8af-49b2-9ae8-e9e2aa3df688)

![Cursor_iSzOSpcTHu](https://github.com/user-attachments/assets/a50b220a-0768-44af-b2a0-81b7d9b392a6)

![Cursor_Dhv29Ht5K5](https://github.com/user-attachments/assets/5833b98f-0eb0-4198-be0d-863fa7750be0)

![Cursor_ZIyXfk8i9g](https://github.com/user-attachments/assets/2b1e136c-ae6e-4b0e-805f-ca0b8c3d2fc4)

![Cursor_VLyZvswGOw](https://github.com/user-attachments/assets/9074d452-06fb-44a2-a595-888008ed23e6)

![Cursor_fxzXRcfiOV](https://github.com/user-attachments/assets/32152b15-1e8b-4a63-b001-b864ef2195e3)

![Cursor_EgiVmqIsSz](https://github.com/user-attachments/assets/961f8c2f-7b8d-49d7-9d43-e25736764356)

![Cursor_OjBywR8RJ3](https://github.com/user-attachments/assets/a22a2caa-8a29-4dfe-a378-b109273eb0f0)

![Cursor_1PDjZOHXM9](https://github.com/user-attachments/assets/ff99b80a-d0d1-4207-82ba-7a59a75864ac)

![Cursor_He8dFagem3](https://github.com/user-attachments/assets/9eba389a-bd47-4834-83c4-3964110f682a)

![Cursor_baHA9OCOSE](https://github.com/user-attachments/assets/f2943b38-2fbb-474d-9e67-489ae241e6bb)

![Cursor_euDOSJgsSN](https://github.com/user-attachments/assets/830f0499-0013-4dab-9db2-dfbe1b1c0241)

![Cursor_y4ykB5cXRH](https://github.com/user-attachments/assets/ccd860fd-b1ef-4856-b119-3888ab71f8c8)

![Cursor_57e2JgBSKT](https://github.com/user-attachments/assets/6dfbf009-7fc9-4769-81a6-4ebdcfb46d73)

![Cursor_s84ZZ1zWM0](https://github.com/user-attachments/assets/108146c6-d0bd-45f8-9548-a21a94f85391)

![Cursor_qpgN6rRJ0l](https://github.com/user-attachments/assets/b3ba0834-f650-4ab6-9616-644788fad911)

![Cursor_a3FUNFT526](https://github.com/user-attachments/assets/7e760811-58e7-4944-a2b7-5ea885c450a1)

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

## 📝 Notas de Versão

### Versão 0.0.0.2 (01/01/2024 07:33)

- **Atualizações:**  Esta versão inclui todas as alterações realizadas desde o início do projeto até a data de 01/01/2024 07:33.  Uma análise completa do código-fonte é necessária para detalhar as mudanças específicas.  [Inserir aqui um detalhamento das mudanças, se possível].
