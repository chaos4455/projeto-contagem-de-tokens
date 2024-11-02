# contador_tokens_menu.py

## Descrição

Este script fornece um menu interativo para realizar diferentes operações com tokens e embeddings armazenados em um banco de dados SQLite. Ele utiliza a biblioteca `inquirer` para criar o menu interativo, `colorama` para colorir a saída do console, `numpy` para cálculos numéricos, `transformers` (potencialmente) para processamento de linguagem natural, e outras bibliotecas para diversas funcionalidades. O script é projetado para ser uma ferramenta flexível e fácil de usar para análise e manipulação de dados de tokens e embeddings.

## Funcionalidades

O script oferece as seguintes funcionalidades através de um menu interativo:

### `fetch_random_id(db_name="tokens_database.db") -> int | None`

Recupera um ID aleatório de um token do banco de dados.

**Parâmetros:**

- `db_name (str, opcional)`: O nome do arquivo do banco de dados. O padrão é "tokens_database.db".

**Retorno:**

- `int | None`: Um inteiro representando o ID aleatório, ou None se o banco de dados estiver vazio ou ocorrer um erro.

### `fetch_tokens(id: int, db_name: str = "tokens_database.db") -> List[str] | None`

Recupera os tokens associados a um ID específico do banco de dados.

**Parâmetros:**

- `id (int)`: O ID do token a ser recuperado.
- `db_name (str, opcional)`: O nome do arquivo do banco de dados. O padrão é "tokens_database.db".

**Retorno:**

- `List[str] | None`: Uma lista de strings representando os tokens, ou None se o ID não for encontrado ou ocorrer um erro.

### `search_word_in_tokens(tokens: List[str], word: str) -> bool`

Verifica se uma palavra específica existe na lista de tokens.

**Parâmetros:**

- `tokens (List[str])`: A lista de tokens a serem pesquisados.
- `word (str)`: A palavra a ser pesquisada.

**Retorno:**

- `bool`: True se a palavra for encontrada, False caso contrário.

### `display_pipeline_step(step_description: str, emoji: str, color: Fore)`

Exibe uma mensagem de progresso formatada no console.

**Parâmetros:**

- `step_description (str)`: A descrição da etapa.
- `emoji (str)`: O emoji a ser exibido.
- `color (Fore)`: A cor da mensagem.

### `calculate_indicators(tokens: List[str]) -> Dict[str, float] | Dict`

Calcula indicadores estatísticos (média, variância, desvio padrão, etc.) para uma lista de tokens numéricos.

**Parâmetros:**

- `tokens (List[str])`: A lista de tokens numéricos.

**Retorno:**

- `Dict[str, float] | Dict`: Um dicionário contendo os indicadores estatísticos calculados, ou um dicionário vazio se ocorrer um erro.

### `display_indicators(indicators: Dict[str, float])`

Exibe os indicadores estatísticos calculados.

**Parâmetros:**

- `indicators (Dict[str, float])`: Um dicionário contendo os indicadores estatísticos.

### `display_2d_elements(tokens: List[str])`

(Placeholder) Função para exibir elementos em 2D (provavelmente usando Matplotlib).

**Parâmetros:**

- `tokens (List[str])`: A lista de tokens.

### `cosine_similarity(vec1: List[str], vec2: List[str]) -> float | None`

Calcula a similaridade de cosseno entre dois vetores.

**Parâmetros:**

- `vec1 (List[str])`: O primeiro vetor.
- `vec2 (List[str])`: O segundo vetor.

**Retorno:**

- `float | None`: A similaridade de cosseno, ou None se ocorrer um erro.

### `display_kpis()`

Exibe um conjunto de KPIs (Key Performance Indicators).

### `generate_hash() -> str`

Gera um hash MD5 único baseado no timestamp.

**Retorno:**

- `str`: Uma string representando o hash MD5.

### `save_kpis_to_files(kpis_data: Dict, event_type: str = "vector_analysis")`

Salva os dados dos KPIs em arquivos JSON, YAML, TXT e MD.

**Parâmetros:**

- `kpis_data (Dict)`: Os dados dos KPIs a serem salvos.
- `event_type (str, opcional)`: O tipo de evento. O padrão é "vector_analysis".

### `calculate_vector_kpis(tokens_data: List[np.ndarray]) -> Dict`

Calcula KPIs avançados para análise de vetores e embeddings.

**Parâmetros:**

- `tokens_data (List[np.ndarray])`: Uma lista de matrizes NumPy representando os vetores.

**Retorno:**

- `Dict`: Um dicionário contendo os KPIs calculados.

### `is_numeric(value: Any) -> bool`

Verifica se um valor é numérico.

**Parâmetros:**

- `value (Any)`: O valor a ser verificado.

**Retorno:**

- `bool`: True se o valor for numérico, False caso contrário.

### `display_vector_kpis()`

Exibe e salva KPIs específicos de vetores.

### `main()`

Função principal que executa o menu interativo.


## Dependências

- `sqlite3`
- `random`
- `inquirer`
- `colorama`
- `numpy`
- `transformers` (potencialmente)
- `torch` (potencialmente)
- `time`
- `matplotlib.pyplot`
- `scipy.spatial.distance`
- `logging`
- `json`
- `yaml`
- `hashlib`
- `datetime`
- `os`
- `pathlib`

## Uso

Para executar o script, execute `python contador_tokens_menu.py`. O script apresentará um menu com as opções disponíveis.

## Considerações

- O script depende de um banco de dados SQLite chamado `tokens_database.db` que deve conter dados previamente inseridos.
- A funcionalidade de visualização 2D é um placeholder e precisa ser implementada usando uma biblioteca de visualização como Matplotlib.
- O cálculo de alguns KPIs (como a similaridade de cosseno) assume que os tokens são representados numericamente.
- A análise avançada de vetores requer que os tokens sejam numéricos.

## Melhorias Possíveis

- Implementar a visualização 2D usando Matplotlib.
- Adicionar mais opções ao menu, como a possibilidade de adicionar novos tokens ao banco de dados.
- Melhorar o tratamento de erros.
- Adicionar validação de entrada para garantir que os dados inseridos pelo usuário sejam válidos.
