# automacao_organiza_projeto_restaura_backup_v1.py

## Descrição

Este script, obra-prima da engenharia de software, automatiza o processo de backup, restauração e organização de arquivos de um projeto.  Como arquiteto de software, eu, Elias Andrade, projetei este script para ser robusto, eficiente e escalável. Ele utiliza a biblioteca `rich` para exibir mensagens formatadas no console e `logging` para registrar eventos em um arquivo de log, garantindo total rastreabilidade.

## Funcionalidades

- **`setup_pastas()`**:  Esta função, elegante em sua simplicidade, cria as pastas necessárias (`logs`, `txt`, `json`, `zip`) se elas não existirem.  Um tratamento de exceções robusto garante a execução sem falhas, mesmo em cenários inesperados.

- **`gerar_hash_unico(arquivo: Path) -> str`**:  Esta função gera um hash único baseado no nome do arquivo e timestamp, utilizando o algoritmo MD5.  Essa abordagem garante a unicidade dos nomes de arquivo, evitando colisões e mantendo a integridade do sistema.  A escolha do MD5 foi estratégica, balanceando segurança e performance.

- **`mover_arquivo_com_verificacao(arquivo: Path, pasta_destino: Path) -> bool`**:  Esta função, o coração do sistema de organização, move um arquivo para a pasta de destino, tratando duplicatas com elegância.  Se um arquivo com o mesmo nome já existir, um novo nome com um hash único é gerado, evitando sobrescritas indesejadas.  O retorno booleano indica o sucesso ou falha da operação, permitindo um tratamento de erros preciso.

- **`organizar_arquivos()`**:  Esta função, um exemplo de design limpo e eficiente, organiza os arquivos por extensão, movendo-os para as pastas correspondentes.  A utilização da biblioteca `rich.progress` proporciona uma experiência de usuário superior, exibindo uma barra de progresso em tempo real.

- **`mostrar_estatisticas_organizacao()`**:  Esta função exibe as estatísticas de organização (arquivos movidos, renomeados e zips organizados) em uma tabela formatada usando `rich.table`.  A apresentação clara e concisa das informações facilita a compreensão do processo de organização.

- **`executar_script(nome_script, descricao)`**:  Esta função executa um script Python e monitora sua execução, exibindo mensagens de sucesso ou erro.  O tratamento de erros é robusto, garantindo a estabilidade do sistema mesmo em caso de falhas em scripts externos.

- **`mostrar_sumario_final(sucessos, total)`**:  Esta função exibe um sumário final da execução da automação, incluindo métricas essenciais como número de scripts executados, sucessos, falhas e taxa de sucesso.  A apresentação tabular das informações garante clareza e facilidade de interpretação.

- **`executar_automacao()`**:  Esta função, a orquestradora da automação, executa a automação completa, incluindo a organização de arquivos e a execução de outros scripts.  A sequência de execução é otimizada para garantir a máxima eficiência.


## Dependências

- `os`:  Biblioteca essencial para interação com o sistema operacional.  Sua inclusão é fundamental para a funcionalidade do script.
- `shutil`:  Biblioteca para operações de alto nível com arquivos e pastas.  Sua utilização simplifica o processo de movimentação e renomeação de arquivos.
- `pathlib`:  Biblioteca moderna e eficiente para manipulação de caminhos de arquivos.  Sua utilização melhora a legibilidade e a manutenibilidade do código.
- `subprocess`:  Biblioteca para executar outros processos.  Essencial para a execução de scripts externos.
- `time`:  Biblioteca para operações relacionadas ao tempo.  Utilizada para pausar a execução entre scripts.
- `rich`:  Biblioteca para criar interfaces de usuário ricas e interativas na linha de comando.  Fundamental para a experiência do usuário.
- `hashlib`:  Biblioteca para gerar hashes criptográficos.  Utilizada para gerar hashes únicos para nomes de arquivos.
- `datetime`:  Biblioteca para manipulação de datas e horas.  Utilizada para gerar timestamps únicos.
- `logging`:  Biblioteca para registro de eventos.  Essencial para o monitoramento e a depuração do script.


## Uso

Para executar este script, execute o comando `python automacao_organiza_projeto_restaura_backup_v1.py` no terminal.  A execução é totalmente automatizada e requer pouca ou nenhuma intervenção do usuário.

## Logs

Os logs da execução são salvos na pasta `logs`, permitindo uma análise detalhada do processo de automação.  A análise desses logs é crucial para a manutenção e a depuração do sistema.

## Melhorias Possíveis

- **Tratamento de Erros:**  Embora o tratamento de erros seja robusto, melhorias adicionais podem ser implementadas para lidar com cenários ainda mais complexos e inesperados.
- **Configurações Personalizáveis:**  A adição de um arquivo de configuração permitiria aos usuários personalizar o comportamento do script, adaptando-o a diferentes necessidades e cenários.
- **Integração com Sistemas de Versionamento:**  A integração com sistemas de versionamento de backups melhoraria a capacidade de recuperação de dados e a gestão de versões.
