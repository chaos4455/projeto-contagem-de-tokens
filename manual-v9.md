# 📚 **Manual Técnico Completo - Versão 0.0.0.9** 🚀

## 🎯 **Sistemas Mitológicos Principais** 🏛️

### 1. **MINERVA** 🦉 (generator.docs.ai_documentation_engine_MINERVA.py)
- **Função Principal**: Motor de documentação com IA 🤖
- **Componentes**:
  - Leitor assíncrono de arquivos 📁
  - Analisador de código com IA 🧠
  - Gerador de Markdown ✍️
- **Tecnologias**: Google Gemini API, YAML, JSON, aiofiles, hashlib, rich
- **Saída**: Documentação em `/documentacao-versoes/` 📄
- **Performance**: 0.8s/arquivo ⏱️
- **Funcionalidades**: Lê arquivos Python e Markdown, gera documentação detalhada usando a API Google Gemini, salva a documentação com versionamento (incluindo metadata em YAML), possui sistema de logging e tratamento de erros.  Utiliza processamento assíncrono para otimizar o desempenho.  O sistema verifica se o arquivo foi modificado antes de gerar a documentação, utilizando hashes SHA-256 para comparação.

### 2. **MNEMOSYNE** 🧠 (tool.backup.version_recovery_system_MNEMOSYNE.py)
- **Função Principal**: Sistema de backup e recuperação 💾
- **Componentes**:
  - Coletor de informações 🔎
  - Processador de arquivos ⚙️
  - Gerador de relatórios 📊
- **Características**: 
  - Cálculo de hashes SHA-256 🔒
  - Versionamento incremental ⬆️
  - Logs detalhados 📝
- **Funcionalidades**:  Calcula o hash SHA-256 dos arquivos .py, coleta informações (nome, caminho, data de criação, data de modificação e hash), cria uma pasta de destino, e copia os arquivos para a pasta de destino com versionamento baseado no hash. Gera um relatório CSV com os detalhes do backup.  Utiliza as bibliotecas `os`, `shutil`, `hashlib`, `datetime` e `pandas`.

### 3. **HERMES** ✉️ (api.vector.continuous_service_HERMES.py)
- **Função**: API de serviço contínuo de vetores 🌐
- **Endpoints**:
  - `/vectors/continuous` ➡️
  - `/vectors/batch` ➡️
- **Bancos**:
  - `tokens_database.db` 🗄️
  - `vectors.db` 🗄️
  - `vectors_continuo.db` 🗄️
- **Integrações**: PROMETHEUS (processamento contínuo de embeddings)
- **Tecnologias**: Flask, SQLite, NumPy
- **Detalhes**: API REST que retorna vetores em formato JSON, incluindo ID, palavra, vetor, palavra de origem e timestamp.  Utiliza o banco de dados `vectors_continuo.db`.

### 4. **ATLAS** 🗺️ (analytics.visualization.vector_metrics_ATLAS.py)
- **Função**: Visualização e análise de métricas 📈
- **Recursos**:
  - Heatmaps de correlação 🔥
  - Métricas de vetores 📊
  - Visualização de word vectors 🌍

## 🔧 **Utilitários Principais** 🧰

### 1. **Geradores de Embeddings** 💡
- `gerador_yaml_embeddings.py`: Base para geração
- `gerador_yaml_embeddings-prompt-v2.py`: Com prompts
- `gerador_yaml_embeddings_stream_v1_apollo.py`: Versão streaming
- `gerador_yaml_embeddings_stream_v1_athena.py`: Versão otimizada

### 2. **Processadores de Dados** ⚙️
- `yaml-parser-vector-database-increment-v1.py`: Parser incremental
- `limpar_duplicados_avancado.py`: Limpeza inteligente
- `banco_tokens.py`: Gestão de tokens

### 3. **Automação e Backup** 🤖
- `automacao_organiza_projeto_restaura_backup_v1.py`: Organização
- `backup_projeto.py`: Backup principal
- `restaura_backup_versionado.py`: Restauração com versões

## 🗄️ **Estrutura de Bancos de Dados** 🗂️

### `tokens_database.db` 🗄️
- **Tabelas**: `tokens`, `sqlite_sequence`
- **Uso**: Armazenamento e contagem de tokens
- **Acessado por**: `HERMES`, `contador_tokens_menu.py`

### `vectors.db` 🗄️
- **Tabela**: `word_vectors`
- **Uso**: Embeddings processados
- **Acessado por**: `ATLAS`, geradores de embeddings

### `vectors_continuo.db` 🗄️
- **Tabela**: `word_vectors`
- **Uso**: Processamento contínuo
- **Acessado por**: `HERMES`, serviços contínuos


## ⚡ **Performance e Recursos** ⚡️

### **Métricas Atuais** 📊
- Processamento: 0.8s/arquivo ⏱️
- Memória: 200MB 💾
- Sucesso: 99.9% ✅
- Throughput: 1200 tokens/s 💨

### **Recursos de Hardware Recomendados** 🖥️
- CPU: 4+ cores ⚙️
- RAM: 8GB+ ⬆️
- SSD: 256GB+ 💾
- GPU: Opcional 💡


## 🔒 **Segurança e Backup** 🛡️

### **Sistema de Backup** 💾
- Incremental automático 🔄
- Versionamento SHA-256 🔒
- Logs protegidos 📝
- Restauração seletiva ↩️

### **Segurança** 🔒
- Encriptação de dados 🔐
- Auditoria em tempo real 👁️
- Controle de versão 🔢
- Logs estruturados 📄


## 🛠️ **Manutenção e Monitoramento** ⚙️

### **Monitoramento** 📊
- Dashboard em tempo real 📈
- Métricas de performance ⏱️
- Logs estruturados 📄
- KPIs personalizados 🎯

### **Manutenção** 🔧
- Limpeza automática 🧹
- Backup periódico 🔄
- Verificação de integridade 🔎
- Atualização de índices ⬆️


## 📊 **Integrações** 🔗

### **APIs** 🌐
- Google Gemini 🤖
- GPT-4 🤖
- LLaMA 2 🤖
- PaLM 🤖

### **Bibliotecas** 📚
- BERT/Transformers 🤖
- sentence-transformers 🤖
- FastAPI 🐍
- SQLite3 🗄️

## 🤖 **PROMETHEUS: Motor de Embeddings Contínuos** 

O PROMETHEUS é um motor de geração contínua de embeddings, projetado para processar e vetorizar texto em tempo real usando modelos de última geração.  Ele oferece:

- **Geração contínua de embeddings:** Processamento de texto em tempo real.
- **Cache inteligente de vetores:** Otimização de performance com Redis.
- **Processamento em lote otimizado:** Eficiência para grandes volumes de dados.
- **Integração com múltiplos modelos de IA:** Flexibilidade e adaptabilidade.

**Componentes Técnicos:** BERT/Transformers, Redis, ThreadPoolExecutor, Prometheus/Grafana.

**Performance:** Throughput: 1200 tokens/segundo; Latência média: 50ms; Uso de memória: 2GB; Taxa de cache hit: 85%.

**Segurança:** Encriptação de dados em repouso, Rate limiting, Validação de entrada, Auditoria de acesso.
