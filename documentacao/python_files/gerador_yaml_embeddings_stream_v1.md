# gerador_yaml_embeddings_stream_v1.py

## Descrição

Este script gera múltiplos arquivos YAML contendo embeddings de texto usando a API do Google Generative AI e processamento de linguagem natural com BERT. Ele utiliza um sistema multi-threaded para processar os tokens do BERT, monitora recursos do sistema e exibe um dashboard em tempo real com estatísticas detalhadas.

## Funcionalidades

- **`TokenBatch`**: Classe para agrupar tokens em batches para processamento eficiente.
- **`BertProcessor`**: Classe que realiza a tokenização usando BERT em múltiplas threads, gerenciando filas de entrada e saída.
- **`AdvancedMetrics`**: Classe para calcular métricas avançadas, incluindo embeddings e estatísticas de tokens.
- **`SystemMonitor`**: Classe para monitorar recursos do sistema (CPU, memória, GPU) com fallbacks para diferentes sistemas operacionais.
- **`StreamStats`**: Classe para coletar e gerenciar estatísticas do stream de texto, incluindo métricas básicas e avançadas.
- **`StreamProcessor`**: Classe principal que gerencia o fluxo de processamento, incluindo a geração de texto com a API do Google Generative AI, o processamento de tokens BERT e a atualização do dashboard.
- **`processar_yaml(prompt: str, arquivo_yaml: Path, iteracao: int, total: int)`**: Processa um único arquivo YAML, gerando texto, atualizando estatísticas e escrevendo no arquivo.
- **`processar_iteracoes(palavra_inicial: str)`**: Processa todas as iterações, gerando múltiplos arquivos YAML.
- **`main()`**: Função principal que inicia o processo.

## Dependências

- `yaml`
- `hashlib`
- `datetime`
- `google.generativeai`
- `os`
- `pathlib`
- `time`
- `colorama`
- `rich`
- `nltk`
- `sentence_transformers`
- `numpy`
- `torch`
- `psutil`
- `GPUtil`
- `platform`
- `concurrent.futures`
- `queue`
- `threading`
- `multiprocessing`
- `functools`
- `dataclasses`
- `collections`
- `aiofiles`
- `contextlib`

## Uso

Para executar o script, execute `python gerador_yaml_embeddings_stream_v1.py`.  O script solicitará uma palavra inicial e gerará 20 arquivos YAML na pasta `generated-yaml-text-to-embedding`.

## Considerações

- O script requer uma chave de API válida para o Google Generative AI.
- O script utiliza o modelo BERT para tokenização.  Certifique-se de que o modelo esteja instalado.
- O script monitora recursos do sistema, mas a precisão pode variar dependendo do sistema operacional e das bibliotecas disponíveis.
- O processamento de tokens BERT é realizado em threads separadas para melhorar a performance.

## Melhorias Possíveis

- Adicionar opções de configuração para personalizar o comportamento do script (por exemplo, o número de iterações, o modelo BERT a ser usado, etc.).
- Implementar um sistema de logging mais robusto.
- Adicionar tratamento de erros mais completo.
- Melhorar a interface do usuário, por exemplo, adicionando um indicador de progresso mais detalhado.
