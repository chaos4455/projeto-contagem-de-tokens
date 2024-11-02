# backup_projeto.py

## Descrição

Este script cria um backup completo do projeto em um arquivo ZIP. Ele utiliza a biblioteca `rich` para exibir mensagens formatadas no console, incluindo um dashboard com estatísticas do backup, e `logging` para registrar eventos em um arquivo de log. O script é projetado para ser robusto, eficiente e fácil de usar, lidando com a criação de arquivos ZIP, tratamento de erros e exibição de informações relevantes para o usuário.

## Funcionalidades

### `gerar_hash() -> str`

Gera um hash MD5 único baseado no timestamp para garantir a unicidade do nome do arquivo de backup.

**Retorno:**

- `str`: Uma string representando o hash MD5.

### `calcular_tamanho_pasta(pasta: Path) -> int`

Calcula o tamanho total (em bytes) de todos os arquivos dentro de uma pasta e suas subpastas.

**Parâmetros:**

- `pasta (Path)`: O objeto Path da pasta a ser analisada.

**Retorno:**

- `int`: O tamanho total da pasta em bytes.

### `obter_ultima_versao(pasta_backup: Path) -> int`

Obtém o número da próxima versão de backup a ser criada, analisando os nomes dos arquivos ZIP existentes na pasta de backups.

**Parâmetros:**

- `pasta_backup (Path)`: O objeto Path da pasta de backups.

**Retorno:**

- `int`: O número da próxima versão de backup.

### `criar_dashboard(stats: dict) -> Layout`

Cria um dashboard rico usando a biblioteca `rich` para exibir as estatísticas do backup de forma organizada e visualmente atraente.  O dashboard inclui um cabeçalho, uma tabela com as estatísticas e um rodapé indicando o sucesso da operação.

**Parâmetros:**

- `stats (dict)`: Um dicionário contendo as estatísticas do backup.

**Retorno:**

- `Layout`: Um objeto Layout da biblioteca `rich` contendo o dashboard.

### `criar_backup_projeto() -> bool`

Função principal que realiza o backup do projeto. Ela inclui um tratamento para ignorar pastas e arquivos específicos, utiliza a biblioteca `zipfile` para criar o arquivo ZIP e exibe um dashboard com as estatísticas do backup.

**Retorno:**

- `bool`: True se o backup foi criado com sucesso, False caso contrário.


## Dependências

- `zipfile`
- `datetime`
- `hashlib`
- `pathlib`
- `shutil`
- `re`
- `os`
- `humanize`
- `rich`
- `logging`

## Uso

Para executar o script, basta rodar o comando `python backup_projeto.py` no terminal. O backup será salvo na pasta `backup` no mesmo diretório do script.

## Logs

Os logs da execução são salvos no arquivo `backup_projeto.log`.

## Melhorias Possíveis

- Implementar a possibilidade de configurar quais pastas e arquivos devem ser incluídos ou excluídos do backup.
- Adicionar suporte para diferentes métodos de compressão.
- Integrar com um sistema de versionamento de backups mais robusto.
- Implementar verificação de integridade do backup após a criação.
