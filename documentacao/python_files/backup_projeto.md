# backup_projeto.py

## Descrição

Este script cria um backup completo do projeto em um arquivo ZIP. Ele utiliza a biblioteca `rich` para exibir mensagens formatadas no console, incluindo um dashboard com estatísticas do backup, e `logging` para registrar eventos em um arquivo de log.

## Funcionalidades

- **`gerar_hash()`**: Gera um hash MD5 único baseado no timestamp para garantir a unicidade do nome do arquivo de backup.
- **`calcular_tamanho_pasta(pasta)`**: Calcula o tamanho total (em bytes) de todos os arquivos dentro de uma pasta e suas subpastas.
- **`obter_ultima_versao(pasta_backup)`**: Obtém o número da próxima versão de backup a ser criada, analisando os nomes dos arquivos ZIP existentes na pasta de backups.
- **`criar_dashboard(stats)`**: Cria um dashboard rico usando a biblioteca `rich` para exibir as estatísticas do backup de forma organizada e visualmente atraente.
- **`criar_backup_projeto()`**: Função principal que realiza o backup do projeto.  Ela inclui um tratamento para ignorar pastas e arquivos específicos, utiliza a biblioteca `zipfile` para criar o arquivo ZIP e exibe um dashboard com as estatísticas do backup.
    - Inclui tratamento de erros e mensagens informativas para o usuário.
    - Utiliza `rich.progress` para exibir uma barra de progresso durante a criação do arquivo ZIP.

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
