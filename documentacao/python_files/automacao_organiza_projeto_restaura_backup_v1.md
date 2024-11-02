# automacao_organiza_projeto_restaura_backup_v1.py

## Descrição

Este script automatiza o processo de backup, restauração e organização de arquivos de um projeto. Ele utiliza a biblioteca `rich` para exibir mensagens formatadas no console e `logging` para registrar eventos em um arquivo de log, garantindo total rastreabilidade.  O script é projetado para ser robusto, eficiente e escalável, lidando com a movimentação e renomeação de arquivos, tratamento de duplicatas e execução de scripts externos.

## Funcionalidades

### `setup_pastas()`

Cria as pastas necessárias (`logs`, `txt`, `json`, `zip`) se elas não existirem.  Um tratamento de exceções robusto garante a execução sem falhas, mesmo em cenários inesperados.

### `gerar_hash_unico(arquivo: Path) -> str`

Gera um hash único baseado no nome do arquivo e timestamp, utilizando o algoritmo MD5.  Essa abordagem garante a unicidade dos nomes de arquivo, evitando colisões e mantendo a integridade do sistema.  A escolha do MD5 foi estratégica, balanceando segurança e performance.

**Parâmetros:**

- `arquivo (Path)`: O objeto Path do arquivo para o qual o hash será gerado.

**Retorno:**

- `str`: Uma string representando o hash MD5 de 8 caracteres.

**Exemplo:**

```python
hash = gerar_hash_unico(Path("meu_arquivo.txt"))
print(hash)  # Imprime um hash MD5 de 8 caracteres
```

### `mover_arquivo_com_verificacao(arquivo: Path, pasta_destino: Path) -> bool`

Move um arquivo para a pasta de destino, tratando duplicatas com elegância. Se um arquivo com o mesmo nome já existir, um novo nome com um hash único é gerado, evitando sobrescritas indesejadas. O retorno booleano indica o sucesso ou falha da operação, permitindo um tratamento de erros preciso.

**Parâmetros:**

- `arquivo (Path)`: O objeto Path do arquivo a ser movido.
- `pasta_destino (Path)`: O objeto Path da pasta de destino.

**Retorno:**

- `bool`: True se o arquivo foi movido com sucesso, False caso contrário.

**Exemplo:**

```python
sucesso = mover_arquivo_com_verificacao(Path("meu_arquivo.txt"), Path("minha_pasta"))
print(f"Arquivo movido com sucesso: {sucesso}")
```

### `organizar_arquivos()`

Organiza os arquivos por extensão, movendo-os para as pastas correspondentes (`logs`, `txt`, `json`, `zip`). A utilização da biblioteca `rich.progress` proporciona uma experiência de usuário superior, exibindo uma barra de progresso em tempo real.  A função também mantém estatísticas sobre os arquivos movidos e renomeados.

### `mostrar_estatisticas_organizacao()`

Exibe as estatísticas de organização (arquivos movidos, renomeados e zips organizados) em uma tabela formatada usando `rich.table`. A apresentação clara e concisa das informações facilita a compreensão do processo de organização.

### `executar_script(nome_script: str, descricao: str) -> bool`

Executa um script Python e monitora sua execução, exibindo mensagens de sucesso ou erro. O tratamento de erros é robusto, garantindo a estabilidade do sistema mesmo em caso de falhas em scripts externos.

**Parâmetros:**

- `nome_script (str)`: O nome do script Python a ser executado.
- `descricao (str)`: Uma descrição da ação sendo executada.

**Retorno:**

- `bool`: True se o script foi executado com sucesso, False caso contrário.

**Exemplo:**

```python
sucesso = executar_script("meu_script.py", "Executando meu script")
print(f"Script executado com sucesso: {sucesso}")
```

### `mostrar_sumario_final(sucessos: int, total: int)`

Exibe um sumário final da execução da automação, incluindo métricas essenciais como número de scripts executados, sucessos, falhas e taxa de sucesso. A apresentação tabular das informações garante clareza e facilidade de interpretação.

**Parâmetros:**

- `sucessos (int)`: O número de scripts executados com sucesso.
- `total (int)`: O número total de scripts executados.

### `executar_automacao()`

Executa a automação completa, incluindo a organização de arquivos e a execução de outros scripts. A sequência de execução é otimizada para garantir a máxima eficiência.  A função utiliza um loop para executar uma lista de scripts pré-definidos e exibe um painel de resumo no início da execução.


## Dependências

- `os`: Biblioteca essencial para interação com o sistema operacional.
- `shutil`: Biblioteca para operações de alto nível com arquivos e pastas.
- `pathlib`: Biblioteca moderna e eficiente para manipulação de caminhos de arquivos.
- `subprocess`: Biblioteca para executar outros processos.
- `time`: Biblioteca para operações relacionadas ao tempo.
- `rich`: Biblioteca para criar interfaces de usuário ricas e interativas na linha de comando.
- `hashlib`: Biblioteca para gerar hashes criptográficos.
- `datetime`: Biblioteca para manipulação de datas e horas.
- `logging`: Biblioteca para registro de eventos.


## Uso

Para executar este script, execute o comando `python automacao_organiza_projeto_restaura_backup_v1.py` no terminal. A execução é totalmente automatizada e requer pouca ou nenhuma intervenção do usuário.

## Logs

Os logs da execução são salvos na pasta `logs`, permitindo uma análise detalhada do processo de automação. A análise desses logs é crucial para a manutenção e a depuração do sistema.

## Melhorias Possíveis

- **Tratamento de Erros:** Melhorias adicionais podem ser implementadas para lidar com cenários ainda mais complexos e inesperados.
- **Configurações Personalizáveis:** A adição de um arquivo de configuração permitiria aos usuários personalizar o comportamento do script.
- **Integração com Sistemas de Versionamento:** A integração com sistemas de versionamento de backups melhoraria a capacidade de recuperação de dados.
