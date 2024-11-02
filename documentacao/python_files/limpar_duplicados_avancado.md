# limpar_duplicados_avancado.py

## Descrição

Este script realiza uma limpeza avançada de duplicados em um projeto, comparando arquivos com base em seus hashes SHA256. Ele remove duplicados internos em uma pasta de backup e também remove arquivos do backup que já existem na pasta raiz do projeto.  O script também remove pastas vazias após a remoção de arquivos.

## Funcionalidades

- **`setup_logging()`**: Configura o logging para registrar as ações do script em um arquivo (`limpeza_avancada.log`) e no console.
- **`calcular_hash_arquivo(caminho_arquivo)`**: Calcula o hash SHA256 de um arquivo. Inclui tratamento de erros.
- **`mapear_arquivos_raiz()`**: Mapeia todos os arquivos na pasta raiz do projeto, excluindo pastas especificadas, calculando seus hashes e armazenando as informações em um dicionário.
- **`mapear_arquivos_backup()`**: Mapeia todos os arquivos na pasta de backup, calculando seus hashes e armazenando as informações em um dicionário.
- **`remover_duplicados_internos()`**: Remove duplicados dentro da pasta de backup, mantendo apenas a versão mais recente de cada arquivo.
- **`remover_duplicados_da_raiz()`**: Remove arquivos da pasta de backup que já existem na pasta raiz do projeto.
- **`_remover_arquivo(arquivo)`**: Função auxiliar para remover um arquivo, registrando informações como caminho, data de modificação e tamanho.
- **`remover_pastas_vazias_geral()`**: Remove todas as pastas vazias na pasta raiz e na pasta de backup.
- **`gerar_relatorio()`**: Gera um relatório final com o número de arquivos removidos e o espaço liberado.
- **`executar_limpeza()`**: Executa todo o processo de limpeza, coordenando as outras funções.
- **`main()`**: Função principal que instancia a classe `LimpadorAvancado` e executa a limpeza.

## Dependências

- `os`
- `hashlib`
- `pathlib`
- `datetime`
- `logging`
- `collections`
- `shutil`

## Uso

Para executar o script, execute `python limpar_duplicados_avancado.py`. O script criará um arquivo de log chamado `limpeza_avancada.log` e imprimirá informações no console.  A pasta de backup é assumida como `backup_restaurado`.

## Considerações

- O script assume que a pasta de backup existe e está localizada na mesma pasta do script.
- O script ignora algumas pastas padrão (como `venv`, `__pycache__`, `.git`).
- O script remove arquivos com base na data de modificação, mantendo a versão mais recente.
- O script remove pastas vazias após a remoção de arquivos.

## Melhorias Possíveis

- Adicionar opções de configuração para personalizar o comportamento do script (por exemplo, quais pastas ignorar, o tipo de hash a ser usado, etc.).
- Implementar um sistema de confirmação antes de remover arquivos.
- Adicionar um indicador de progresso para mostrar o andamento da limpeza.
- Implementar um mecanismo para comparar arquivos com base em outros critérios além do hash (por exemplo, tamanho do arquivo).
