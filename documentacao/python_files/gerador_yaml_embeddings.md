# gerador_yaml_embeddings.py

## Descrição

Este script gera arquivos YAML contendo configurações para embeddings, utilizando a API do Google Gemini para gerar o conteúdo. Ele utiliza a biblioteca `inquirer` para obter informações do usuário, `yaml` para manipular arquivos YAML, `hashlib` para gerar hashes únicos, `google.generativeai` para interagir com a API do Gemini, e `rich` para exibir mensagens formatadas no console. O script é projetado para ser uma ferramenta flexível e fácil de usar para gerar configurações de embeddings para diferentes cenários.

## Funcionalidades

### `generate_hash() -> str`

Gera um hash MD5 único baseado no timestamp atual.

**Retorno:**

- `str`: Uma string representando o hash MD5.

### `get_user_inputs() -> Dict`

Coleta as entradas do usuário através de um menu interativo usando a biblioteca `inquirer`.

**Retorno:**

- `Dict`: Um dicionário contendo as entradas do usuário (tema, número de iterações e confirmação).

### `get_gemini_response(prompt: str) -> str | None`

Envia uma solicitação à API do Google Gemini com o prompt fornecido e retorna a resposta.

**Parâmetros:**

- `prompt (str)`: O prompt a ser enviado à API do Gemini.

**Retorno:**

- `str | None`: A resposta da API do Gemini, ou None se ocorrer um erro.

### `save_yaml(data: Dict, prompt: str) -> Path | None`

Salva os dados em um arquivo YAML com metadados (timestamp, prompt e hash).

**Parâmetros:**

- `data (Dict)`: Os dados a serem salvos no arquivo YAML.
- `prompt (str)`: O prompt usado para gerar os dados.

**Retorno:**

- `Path | None`: O objeto Path do arquivo YAML salvo, ou None se ocorrer um erro.

### `main()`

Função principal que executa o script.  Coleta as entradas do usuário, gera múltiplas iterações de YAMLs usando a API do Gemini, salva os arquivos e exibe mensagens de progresso e conclusão.


## Dependências

- `yaml`
- `hashlib`
- `datetime`
- `google.generativeai`
- `os`
- `pathlib`
- `time`
- `colorama`
- `inquirer`
- `rich`


## Uso

Para executar o script, execute `python gerador_yaml_embeddings.py`. O script solicitará informações do usuário (tema e número de iterações) e gerará os arquivos YAML na pasta `generated-yaml-text-to-embedding`.

## Considerações

- O script requer uma chave de API válida para o Google Gemini.  Configure a variável `GOOGLE_API_KEY` com sua chave antes de executar o script.
- O número de iterações pode afetar o tempo de execução do script.
- A qualidade da saída da API do Gemini depende da qualidade do prompt fornecido.

## Melhorias Possíveis

- Adicionar tratamento de erros mais robusto.
- Implementar um sistema de cache para evitar solicitações repetidas à API do Gemini.
- Adicionar opções para personalizar o prompt enviado à API do Gemini.
- Adicionar suporte para diferentes modelos do Google Gemini.
