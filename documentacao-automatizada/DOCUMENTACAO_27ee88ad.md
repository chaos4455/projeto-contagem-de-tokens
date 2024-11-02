# 📚 Documentação Automatizada do Projeto

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Documentação](https://img.shields.io/badge/docs-auto%20generated-green)

## 🏗️ Estrutura do Projeto

### 📝 Arquivos Python

#### 🐍 `automacao_organiza_projeto_restaura_backup_v1.py`
- 📍 Caminho: `automacao_organiza_projeto_restaura_backup_v1.py`

#### 🐍 `backup_projeto.py`
- 📍 Caminho: `backup_projeto.py`

#### 🐍 `banco_tokens.py`
- 📍 Caminho: `banco_tokens.py`

#### 🐍 `contador_tokens_menu.py`
- 📍 Caminho: `contador_tokens_menu.py`

#### 🐍 `documentacao-projeto-automation-v1.py`
- 📍 Caminho: `documentacao-projeto-automation-v1.py`

#### 🐍 `gerador-dic-texto-yaml-v1.py`
- 📍 Caminho: `gerador-dic-texto-yaml-v1.py`

#### 🐍 `gerador_vetorizador_continuo.py`
- 📍 Caminho: `gerador_vetorizador_continuo.py`

#### 🐍 `gerador_yaml_embeddings-prompt-v2.py`
- 📍 Caminho: `gerador_yaml_embeddings-prompt-v2.py`

#### 🐍 `gerador_yaml_embeddings.py`
- 📍 Caminho: `gerador_yaml_embeddings.py`

#### 🐍 `gerador_yaml_embeddings_stream_v1-cria-contexto.py`
- 📍 Caminho: `gerador_yaml_embeddings_stream_v1-cria-contexto.py`

#### 🐍 `gerador_yaml_embeddings_stream_v1-cria-lista-palavras.py`
- 📍 Caminho: `gerador_yaml_embeddings_stream_v1-cria-lista-palavras.py`

#### 🐍 `limpar_duplicados_avancado.py`
- 📍 Caminho: `limpar_duplicados_avancado.py`

#### 🐍 `remover_duplicados.py`
- 📍 Caminho: `remover_duplicados.py`

#### 🐍 `restaurar_backup.py`
- 📍 Caminho: `restaurar_backup.py`

#### 🐍 `restaura_backup_versionado.py`
- 📍 Caminho: `restaura_backup_versionado.py`

#### 🐍 `testa-banco-vetor-ele.py`
- 📍 Caminho: `testa-banco-vetor-ele.py`

#### 🐍 `yaml-parser-vector-database-increment-v1.py`
- 📍 Caminho: `yaml-parser-vector-database-increment-v1.py`

#### 🐍 `yaml_to_vectors.py`
- 📍 Caminho: `yaml_to_vectors.py`

#### 🐍 `zipar_yamls.py`
- 📍 Caminho: `zipar_yamls.py`

### 🗄️ Bancos de Dados SQLite

#### 💾 `tokens_database.db`
- 📍 Caminho: `tokens_database.db`

**Tabelas:**

- 📋 `tokens`
  - id (INTEGER)
  - timestamp (TEXT)
  - unique_hash (TEXT)
  - input_text (TEXT)
  - tokens (TEXT)
  - embeddings (BLOB)

- 📋 `sqlite_sequence`
  - name ()
  - seq ()

#### 💾 `vectors.db`
- 📍 Caminho: `vectors.db`

**Tabelas:**

- 📋 `word_vectors`
  - id (INTEGER)
  - word (TEXT)
  - vector (BLOB)

#### 💾 `vectors_continuo.db`
- 📍 Caminho: `vectors_continuo.db`

**Tabelas:**

- 📋 `word_vectors`
  - id (INTEGER)
  - word (TEXT)
  - vector (BLOB)
  - palavra_origem (TEXT)
  - timestamp (DATETIME)
