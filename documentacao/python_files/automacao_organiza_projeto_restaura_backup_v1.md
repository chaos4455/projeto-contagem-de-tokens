# automacao_organiza_projeto_restaura_backup_v1.py

## Descrição

Este script automatiza o processo de backup, restauração e organização de arquivos de um projeto. Ele utiliza a biblioteca `rich` para exibir mensagens formatadas no console e `logging` para registrar eventos em um arquivo de log.

## Funcionalidades

- **`setup_pastas()`**: Cria as pastas necessárias (`logs`, `txt`, `json`, `zip`) se não existirem.
- **`gerar_hash_unico(arquivo: Path) -> str`**: Gera um hash único baseado no nome do arquivo e timestamp para evitar colisões de nomes ao mover arquivos.
- **`mover_arquivo_com_verificacao(arquivo: Path, pasta_destino: Path) -> bool`**: Move um arquivo para a pasta de destino, tratando duplicatas com hash único. Retorna `True` se o arquivo foi movido com sucesso, `False` caso contrário.
- **`organizar_arquivos()`**: Organiza os arquivos por extensão, movendo-os para as pastas correspondentes (`logs`, `txt`, `json`, `zip`). Utiliza a biblioteca `rich.progress` para exibir uma barra de progresso.
- **`mostrar_estatisticas_organizacao()`**: Exibe as estatísticas de organização (arquivos movidos, renomeados e zips organizados) em uma tabela usando `rich.table`.
- **`executar_script(nome_script, descricao)`**: Executa um script Python e monitora sua execução, exibindo mensagens de sucesso ou erro.
- **`mostrar_sumario_final(sucessos, total)`**: Exibe um sumário final da execução da automação, incluindo o número de scripts executados, sucessos, falhas, taxa de sucesso, arquivos organizados e zips processados.
- **`executar_automacao()`**: Executa a automação completa, incluindo a organização de arquivos e a execução de outros scripts (backup, restauração e remoção de duplicados).

## Dependências

- `os`
- `shutil`
- `pathlib`
- `subprocess`
- `time`
- `rich`
- `hashlib`
- `datetime`
- `logging`

## Uso

Para executar o script, basta rodar o comando `python automacao_organiza_projeto_restaura_backup_v1.py` no terminal.

## Logs

Os logs da execução são salvos na pasta `logs`.

## Melhorias Possíveis

- Implementar tratamento de erros mais robusto.
- Adicionar opções de configuração para personalizar o comportamento do script.
- Integrar com um sistema de versionamento de backups.
