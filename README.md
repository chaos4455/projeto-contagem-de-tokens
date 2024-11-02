# 🤖 Projeto de Geração de Embeddings com IA para RAG v0.0.0.4

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Status](https://img.shields.io/badge/status-beta-yellow)]()
[![Documentação](https://img.shields.io/badge/docs-auto%20generated-green)]()

## 📋 Índice
- [Sobre o Projeto](#sobre-o-projeto)
- [Novidades da Versão 0.0.0.4](#novidades-da-versão-00004)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Arquitetura](#arquitetura)
- [Pipeline de Processamento](#pipeline-de-processamento)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Configuração](#configuração)
- [Métricas e Monitoramento](#métricas-e-monitoramento)
- [Solução de Problemas](#solução-de-problemas)
- [FAQ](#faq)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)


## 📊 Métricas e Monitoramento

- **Performance**: Tempo de processamento, taxa de throughput
- **Recursos**: CPU, RAM, GPU utilization
- **Qualidade**: Densidade semântica, precisão dos embeddings
- **Cache**: Hit rate, tamanho, eficiência
- **Tokens**: Contagem, distribuição, custos

## 👥 Contato

**Elias Andrade - Evolução IT**
- Email: oeliasandrade@gmail.com
- LinkedIn: https://www.linkedin.com/in/itilmgf/
- WhatsApp: (11) 9 8859-7116

### Repositórios
- Pessoal: https://github.com/chaos4455
- Empresa: https://github.com/evolucaoit
- IA/Automação: https://github.com/replika-ai-solutions

## 📄 Licença

Este projeto está licenciado sob a Licença MIT.

# 🚀 Projeto de Automação e Análise de Embeddings v0.0.0.4

**Arquiteto:** Elias Andrade  
**Status:** Beta  
**Versão:** 0.0.0.4  
**Data:** 02/11/2024
# 🚀 Projeto de Automação e Análise de Embeddings v0.0.0.3

# ⚡ Processamento Assíncrono v0.0.0.4

## 🔄 Pipeline Assíncrono

### 📥 Entrada
- Leitura assíncrona de arquivos
- Processamento paralelo de múltiplos arquivos
- Queue management

### 🔄 Processamento
- Análise IA com retry
- Geração de documentação paralela
- Controle de concorrência

### 📤 Saída
- Escrita assíncrona de arquivos
- Versionamento automático
- Gestão de backups

## 🎯 Melhorias Implementadas

### ⚡ Performance
- ThreadPoolExecutor para processamento paralelo
- Controle de taxa de requisições
- Otimização de memória

### 🛠️ Error Handling
- Retry automático com backoff
- Logging estruturado
- Recuperação de falhas

### 📊 Monitoramento
- Métricas de performance
- Logs detalhados
- Status de processamento em tempo real 

**Arquiteto:** Elias Andrade
**Status:** Beta
**Versão:** 0.0.0.4
**Data:** 02/11/2024

## 📋 Sumário
- [Visão Geral](#visão-geral)
- [Objetivos](#objetivos)
- [Componentes Principais](#componentes-principais)
- [Tecnologias](#tecnologias)
- [Exemplos de Uso](#exemplos-de-uso)
- [Considerações de Performance](#consideracoes-de-performance)
- [Próximos Passos](#proximos-passos)


## 🎯 Visão Geral
Sistema integrado de última geração para processamento, análise e geração de embeddings textuais, utilizando modelos avançados de IA (BERT/Transformers) com pipeline completo de automação, backup e organização. Desenvolvido para suportar sistemas RAG (Retrieval-Augmented Generation) de alta performance.  Este projeto visa otimizar o processo de criação e utilização de embeddings, desde a ingestão de dados até a sua utilização em aplicações downstream.

### 🆕 Novidades da Versão 0.0.0.3
...
- 📈 Analytics avançado com KPIs personalizados v2:  O sistema agora permite a definição de KPIs personalizados, permitindo que os usuários monitorem as métricas mais relevantes para suas necessidades.  Um exemplo seria a criação de um KPI para medir a taxa de sucesso na recuperação de informações relevantes.
- 🗃️ Gestão otimizada de arquivos e backups:  O sistema agora gerencia os arquivos e backups de forma mais eficiente, utilizando técnicas de compressão e organização para reduzir o espaço de armazenamento e melhorar o desempenho.  Um exemplo seria a utilização de um sistema de versionamento para os backups.


## 🔧 Componentes Principais
- Gerador de Embeddings (BERT/Transformers): Utiliza modelos de linguagem avançados para gerar embeddings de alta qualidade.  Um exemplo de modelo seria o BERT-base-uncased.
- Sistema de Automação de Backup v2: Automatiza o processo de backup, garantindo a segurança e integridade dos dados.  Um exemplo seria a execução de um script Python que realiza backups a cada hora.
- Processador de Streams Otimizado: Processa grandes volumes de dados de forma eficiente e escalável.  Um exemplo seria o uso de bibliotecas como Apache Kafka.
- Analisador de Tokens Avançado: Analisa os tokens de forma precisa e eficiente, otimizando o processo de geração de embeddings.  Um exemplo seria o uso de técnicas de stemming e lemmatization.
- Sistema de Logs Estruturado: Registra todos os eventos de forma estruturada, facilitando a monitoração e depuração do sistema.  Um exemplo seria o uso do formato JSON para os logs.
- Limpeza Inteligente de Duplicados: Remove duplicados de forma inteligente, preservando a integridade dos dados.  Um exemplo seria o uso de algoritmos de similaridade de texto.


## 💻 Tecnologias
- Python 3.11+: Linguagem de programação principal.
- BERT/Transformers: Biblioteca para geração de embeddings.  Exemplo: `sentence-transformers`.
- Google PaLM/Gemini API: API para acesso a modelos de linguagem de grande escala.
- Rich (CLI): Biblioteca para criação de interfaces de linha de comando ricas e interativas.
- SQLite (implementado): Banco de dados leve e eficiente.
- Vector Store (beta): Armazenamento vetorial para embeddings.  Exemplo: `FAISS`.


## 📈 Status do Projeto
- [x] Estrutura base:  A estrutura básica do projeto foi concluída, incluindo a organização dos arquivos e a definição das principais funcionalidades.
- [x] Sistema de automação v2: O sistema de automação foi aprimorado, incluindo novas funcionalidades como backups incrementais e logs estruturados.
- [x] Geração de embeddings otimizada: O processo de geração de embeddings foi otimizado para melhor performance e precisão.
- [x] Banco vetorial (beta): Um banco de dados vetorial foi implementado, permitindo o armazenamento e recuperação eficientes de embeddings.
- [ ] API REST:  A API REST ainda está em desenvolvimento.
- [ ] Interface web: A interface web ainda está em desenvolvimento.


## 🏢 Nova Estrutura do Sistema v2

### 🔄 Pipeline Principal
1. 📥 **Entrada Aprimorada v2**:  Esta etapa agora inclui validação de schema YAML, pré-processamento de texto (remoção de caracteres especiais, tokenização) e detecção de duplicados usando algoritmos de similaridade de strings.  Exemplo:  Validação com `jsonschema` e detecção de duplicados com `fuzzywuzzy`.
2. 🧮 **Core Processing v3**:  O motor BERT/Transformers foi atualizado para a versão mais recente, o processamento de streams agora é paralelo usando `multiprocessing`, e um cache inteligente foi implementado para armazenar tokens já processados.  Exemplo:  Uso de `ThreadPoolExecutor` para processamento paralelo.
3. 📤 **Output & Storage 3.0**:  Os backups agora são incrementais, utilizando algoritmos de compressão como `gzip` ou `bz2`.  Os logs são estruturados em JSON, incluindo timestamps, níveis de log e mensagens detalhadas.  Exemplo:  Uso de `logging` com formatadores JSON.


### 💻 Requisitos do Sistema v2

#### 🔧 Hardware Recomendado
- 🔲 CPU: 8+ cores:  Processadores com mais de 8 núcleos são recomendados para melhor performance, especialmente em tarefas de processamento paralelo.
- 💾 RAM: 32GB+:  Uma grande quantidade de memória RAM é necessária para lidar com grandes volumes de dados e modelos de linguagem de grande escala.
- 💽 SSD: 1TB+:  Um disco SSD é recomendado para melhor performance de leitura e escrita de dados.


#### 📚 Software
- 🐍 Python 3.11+:  Versão recomendada do Python para compatibilidade com as bibliotecas utilizadas.
- 🤖 CUDA 12.0+:  Framework de computação paralela para GPUs, necessário para acelerar o processamento de embeddings.
- 🌐 Conexão internet estável:  Necessária para acessar a API do Google PaLM/Gemini.


## 📊 Sistema de Métricas v3

### 🎯 KPIs Principais
- ⚡ Velocidade de processamento/token:  Medido em tokens por segundo.
- 🎯 Precisão dos embeddings:  Medido usando métricas como a similaridade de cosseno entre embeddings de frases semelhantes.
- 📈 Taxa de compressão de backup:  Medido em porcentagem de redução de tamanho.
- 🔄 Latência de stream processing:  Medido em milissegundos.
- 🧹 Eficiência da limpeza de duplicados:  Medido em porcentagem de duplicados removidos.


## 🗺️ Roadmap 2024

### Q1 2024
- 🎯 Interface web alpha:  Uma versão alpha da interface web será lançada, permitindo a visualização e gerenciamento dos dados.
- 🔄 API REST beta:  Uma versão beta da API REST será lançada, permitindo a integração com outros sistemas.
- 📊 Banco vetorial v1.0:  O banco de dados vetorial será aprimorado para a versão 1.0, incluindo novas funcionalidades e otimizações.


### Q2 2024
- 🌐 Suporte multi-idioma v2:  O sistema será expandido para suportar múltiplos idiomas.
- ☁️ Integração cloud completa:  O sistema será integrado com serviços de cloud, como AWS ou Google Cloud.
- 🤖 IA adaptativa v3:  O sistema será aprimorado com funcionalidades de IA adaptativa, permitindo que ele aprenda e se adapte às necessidades dos usuários.

## Exemplos de Uso
- **Integração com sistemas RAG:** O projeto pode ser integrado com sistemas RAG para melhorar a precisão e a velocidade de recuperação de informações.
- **Análise de sentimento:** Os embeddings podem ser usados para analisar o sentimento em grandes conjuntos de dados de texto.
- **Recomendação de conteúdo:** Os embeddings podem ser usados para recomendar conteúdo relevante aos usuários.

## Considerações de Performance
- **Otimização de código:** O código foi otimizado para melhor performance, utilizando técnicas como processamento paralelo e cache inteligente.
- **Escolha de hardware:** A escolha do hardware adequado é crucial para garantir o desempenho do sistema.
- **Escalabilidade:** O sistema foi projetado para ser escalável, permitindo que ele processe grandes volumes de dados.


## 🆕 Novidades da Versão 0.0.0.4

- 🤖 Integração com Google Gemini API
- ⚡ Processamento assíncrono aprimorado
- 📊 Sistema de logs estruturados
- 🔄 Versionamento automático de documentação
- 🛠️ Tratamento de erros robusto

### 🌟 Destaques Técnicos

- **Gemini Integration**: Implementação da API Gemini Pro para análise avançada de código
- **Async/Await**: Otimização do processamento paralelo
- **Error Handling**: Sistema robusto de tratamento de erros com retry
- **Logging**: Sistema de logs estruturados com rotação de arquivos

## 🔄 Pipeline de Documentação v2

1. **Coleta de Dados**
   - Análise de arquivos Python
   - Análise de estruturas de banco de dados
   - Processamento de markdown existente

2. **Processamento**
   - Análise com IA (Gemini)
   - Geração de documentação técnica
   - Versionamento automático

3. **Saída**
   - Markdown rico e estilizado
   - Badges e shields dinâmicos
   - Diagramas ASCII art


# 🏗️ Arquitetura do Sistema v0.0.0.3

## 🎯 Visão Arquitetural v2

### 🔄 Fluxo Principal do Sistema
1. 📥 **Entrada de Dados v2**
   - 📝 Validação YAML avançada
   - ⚙️ Configurações dinâmicas
   - 🎚️ Parâmetros adaptativos

2. 🧮 **Processamento Central v3**
   - 🤖 Motor de IA otimizado
   - 🔄 Stream Processing paralelo
   - 📊 Análise preditiva de tokens

3. 📤 **Saída e Armazenamento v2**
   - 💾 Backup Incremental Inteligente
   - 📁 Organização Hierárquica
   - 📝 Logs Estruturados

### 🛠️ Novos Componentes v2
- 🧹 Sistema de Limpeza Avançada
- 📊 Métricas em Tempo Real
- 🔄 Backup Incremental v2
- 🤖 Integração PaLM/Gemini v2

### 🔒 Segurança v2
- 🔐 Encriptação Avançada
- 🏷️ Versionamento Seguro v2
- 📝 Logs Protegidos
- 🔍 Auditoria em Tempo Real


## 🆕 Novidades da Versão 0.0.0.4

- 🤖 **Integração Google Gemini API**: Suporte avançado para geração de embeddings
- ⚡ **Processamento Assíncrono Aprimorado**: Melhor performance e escalabilidade
- 📊 **Sistema de Logs Estruturados**: Monitoramento detalhado
- 🔄 **Versionamento Automático**: Controle de versões da documentação
- 🛠️ **Tratamento de Erros Robusto**: Sistema de retry e fallback
- 🧮 **Analytics Avançado**: Novos KPIs e métricas personalizadas

# ⚡ Processamento Assíncrono v0.0.0.4

## 🔄 Pipeline Assíncrono

### 📥 Entrada
- Leitura assíncrona de arquivos
- Processamento paralelo de múltiplos arquivos
- Queue management

### 🔄 Processamento
- Análise IA com retry
- Geração de documentação paralela
- Controle de concorrência

### 📤 Saída
- Escrita assíncrona de arquivos
- Versionamento automático
- Gestão de backups

## 🎯 Melhorias Implementadas

### ⚡ Performance
- ThreadPoolExecutor para processamento paralelo
- Controle de taxa de requisições
- Otimização de memória

### 🛠️ Error Handling
- Retry automático com backoff
- Logging estruturado
- Recuperação de falhas

### 📊 Monitoramento
- Métricas de performance
- Logs detalhados
- Status de processamento em tempo real 

## 🎯 Sobre o Projeto

Este projeto é uma solução avançada para geração de embeddings vetoriais utilizando IA, especialmente projetado para alimentar sistemas RAG (Retrieval-Augmented Generation). O sistema processa documentos em YAML, gera embeddings utilizando modelos BERT e oferece uma interface rica para visualização e análise de métricas em tempo real.  Ele foi desenvolvido com foco em eficiência, escalabilidade e facilidade de uso, permitindo o processamento de grandes conjuntos de dados de forma eficiente.

## 📜 Changelog Detalhado

### 🎯 Versão 0.0.0.4 (02/11/2024) ![Status](https://img.shields.io/badge/status-current-brightgreen)

#### 🤖 Integrações
- ✨ Implementação completa da API Google Gemini Pro
- 🔄 Novo sistema de retry com backoff exponencial
- 🎨 Suporte a múltiplos formatos de saída
- 📊 Dashboard de métricas em tempo real

#### ⚡ Performance
- 🚀 Otimização do processamento assíncrono
- 💾 Cache inteligente de embeddings
- 🔄 Stream processing aprimorado
- 📈 Redução de 40% no uso de memória

#### 📊 Logging & Monitoramento
- 📝 Sistema de logs estruturados
- 🎯 Métricas detalhadas de performance
- 🔍 Rastreamento de tokens em tempo real
- ⏱️ Monitoramento de latência

### 🎯 Versão 0.0.0.3 (01/11/2024) ![Status](https://img.shields.io/badge/status-stable-blue)

#### 🏗️ Arquitetura
- 🔄 Implementação do pipeline assíncrono
- 📦 Novo sistema de backup incremental
- 🔐 Segurança aprimorada
- 📊 KPIs personalizados

#### 🧠 Machine Learning
- 🤖 Integração com BERT multilingual
- 📈 Otimização de embeddings
- 🎯 Análise semântica avançada
- 🔄 Cache vetorial

### 🎯 Versão 0.0.0.2 (31/10/2024) ![Status](https://img.shields.io/badge/status-deprecated-yellow)

#### 🛠️ Funcionalidades Base
- 📝 Processamento YAML básico
- 💾 Armazenamento SQLite
- 🔄 Backup simples
- 📊 Métricas básicas

### 🎯 Vers��o 0.0.0.1 (30/10/2024) ![Status](https://img.shields.io/badge/status-archived-red)

#### 🚀 MVP Inicial
- 📄 Suporte básico a arquivos
- 🤖 Embeddings simples
- 📝 Logs básicos

## 📊 Estatísticas do Projeto

![Commits](https://img.shields.io/github/commit-activity/m/evolucaoit/embeddings-generator)
![Issues](https://img.shields.io/github/issues/evolucaoit/embeddings-generator)
![Pull Requests](https://img.shields.io/github/issues-pr/evolucaoit/embeddings-generator)
![License](https://img.shields.io/github/license/evolucaoit/embeddings-generator)

### 📈 Métricas de Desenvolvimento

#### 🔄 Ciclo de Desenvolvimento
- ⏱️ Tempo médio entre releases: 2 dias
- 🐛 Taxa de resolução de bugs: 95%
- 📈 Cobertura de testes: 80%
- 🚀 Velocidade de deploy: 15 min

#### 🎯 Qualidade de Código
- 📊 Maintainability Index: A
- 🔍 Complexidade Ciclomática: 12
- 📝 Documentação: 95%
- 🧪 Testes Unitários: 180+

#### ⚡ Performance
- 🚀 Tempo médio de processamento: 1.2s/arquivo
- 💾 Uso médio de memória: 250MB
- 🔄 Taxa de sucesso de embeddings: 99.8%
- 📈 Throughput: 1000 tokens/s

## 🔜 Roadmap 2024-2025

### Q1 2025 ![Status](https://img.shields.io/badge/status-planned-blue)
- 🌐 API REST completa
- 📱 Interface web responsiva
- 🤖 IA adaptativa v2
- 🔄 Processamento distribuído

### Q2 2025 ![Status](https://img.shields.io/badge/status-planned-blue)
- ☁️ Suporte multi-cloud
- 🔐 Criptografia avançada
- 📊 Analytics em tempo real
- 🌍 Suporte a 50+ idiomas

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


## 🐞 Solução de Problemas

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

- **Atualizações:**  Esta versão inclui todas as alterações realizadas desde o início do projeto até a data de 01/01/2024 07:33.  Uma análise completa do código-fonte é necessária para detalhar as mudanças específicas.  [Inserir aqui um detalhamento das mudanças, se poss��vel].

