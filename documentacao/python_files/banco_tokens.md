# banco_tokens.py

## Descrição

Este script interage com um banco de dados SQLite para armazenar tokens e embeddings gerados a partir de um texto de entrada. Ele utiliza a biblioteca `transformers` para realizar a análise com o modelo BERT e o `sqlite3` para a manipulação do banco de dados. O script é projetado para ser modular e reutilizável, permitindo a fácil integração com outros componentes de um sistema de processamento de linguagem natural.

## Funcionalidades

### `create_database(db_name="tokens_database.db")`

Cria um banco de dados SQLite chamado `tokens_database.db` (ou o nome especificado) com uma tabela `tokens` para armazenar os dados. A tabela inclui colunas para timestamp, hash único, texto de entrada, tokens e embeddings.

**Parâmetros:**

- `db_name (str, opcional)`: O nome do arquivo do banco de dados.  O padrão é "tokens_database.db".

**Exemplo:**

```python
create_database("meu_banco.db")
```

### `generate_unique_hash(input_text: str) -> str`

Gera um hash SHA256 único para o texto de entrada, garantindo a unicidade das entradas no banco de dados.

**Parâmetros:**

- `input_text (str)`: O texto para o qual o hash será gerado.

**Retorno:**

- `str`: Uma string representando o hash SHA256.

**Exemplo:**

```python
hash = generate_unique_hash("Este é um texto de exemplo.")
print(hash)
```

### `analyze_bert(text: str, model_name: str = "bert-base-uncased") -> Tuple[List[str], np.ndarray]`

Utiliza o modelo BERT (ou outro modelo especificado) para tokenizar o texto de entrada e gerar os embeddings. Requer a instalação da biblioteca `transformers`.

**Parâmetros:**

- `text (str)`: O texto a ser analisado.
- `model_name (str, opcional)`: O nome do modelo BERT a ser utilizado. O padrão é "bert-base-uncased".

**Retorno:**

- `Tuple[List[str], np.ndarray]`: Uma tupla contendo uma lista de tokens e uma matriz NumPy com os embeddings.

**Exemplo:**

```python
tokens, embeddings = analyze_bert("Este é outro exemplo.")
print(tokens)
print(embeddings)
```

### `insert_data(input_text: str, tokens: List[str], embeddings: np.ndarray, db_name: str = "tokens_database.db")`

Insere os dados (timestamp, hash único, texto de entrada, tokens e embeddings) no banco de dados. Trata o erro `sqlite3.IntegrityError` caso uma entrada com o mesmo hash já exista.

**Parâmetros:**

- `input_text (str)`: O texto de entrada.
- `tokens (List[str])`: A lista de tokens.
- `embeddings (np.ndarray)`: A matriz NumPy com os embeddings.
- `db_name (str, opcional)`: O nome do arquivo do banco de dados. O padrão é "tokens_database.db".

**Exemplo:**

```python
insert_data("Exemplo", ["Este", "é", "um", "exemplo"], np.array([0.1, 0.2, 0.3]))
```

### `main()`

Função principal que solicita o texto de entrada ao usuário, realiza a análise com o BERT, cria o banco de dados (se necessário) e insere os dados.


## Dependências

- `sqlite3`
- `hashlib`
- `datetime`
- `json`
- `numpy`
- `transformers`
- `torch`

## Uso

Para executar o script, execute `python banco_tokens.py`. O script solicitará um texto de entrada e, em seguida, armazenará os tokens e embeddings gerados no banco de dados `tokens_database.db`.

## Considerações

- O script assume que o modelo BERT especificado está disponível. Você pode precisar baixá-lo antes de executar o script.
- O tamanho dos embeddings pode ser significativo, dependendo do modelo BERT utilizado. Considere o espaço de armazenamento disponível ao usar este script com grandes quantidades de dados.
- A função `main` atualmente solicita a entrada do usuário diretamente. Para uso em um ambiente de produção, você precisará modificar esta função para receber a entrada de outra fonte.

## Melhorias Possíveis

- Adicionar tratamento de erros mais robusto.
- Implementar uma interface mais amigável para interagir com o banco de dados.
- Adicionar funcionalidade para consultar e recuperar dados do banco de dados.
- Implementar um sistema de cache para evitar a análise repetida do mesmo texto.
