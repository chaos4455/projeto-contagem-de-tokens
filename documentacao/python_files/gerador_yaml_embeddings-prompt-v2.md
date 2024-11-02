# gerador_yaml_embeddings-prompt-v2.py

## Descrição

Este script gera arquivos YAML contendo listas de palavras para serem usadas em técnicas de embedding e vocabulário para machine learning. Ele utiliza a API do Google Generative AI (Gemini) para gerar o conteúdo e oferece um menu interativo para o usuário configurar o processo.

## Funcionalidades

- **`configurar_geracao()`**: Configura os parâmetros de geração de texto para a API do Gemini.
- **`generate_hash()`**: Gera um hash MD5 único para identificar cada arquivo YAML gerado.
- **`get_user_inputs()`**: Utiliza a biblioteca `inquirer` para obter as entradas do usuário (tema, número de iterações e confirmação).
- **`get_gemini_response(prompt)`**: Envia um prompt para a API do Gemini e retorna a resposta de texto. Inclui um prompt de sistema para garantir a qualidade e a diversidade do texto gerado.
- **`save_yaml(data, prompt)`**: Salva os dados em um arquivo YAML, incluindo metadados como timestamp e prompt.  Utiliza `yaml.add_representer` para formatar strings em estilo vertical.
- **`main()`**: Função principal que coordena todo o processo, desde a obtenção de entradas do usuário até a geração e salvamento dos arquivos YAML.  Utiliza `rich.progress` para exibir uma barra de progresso.

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

Para executar o script, execute `python gerador_yaml_embeddings-prompt-v2.py`. O script solicitará o tema, o número de iterações e confirmará a geração dos YAMLs. Os arquivos YAML gerados serão salvos na pasta `generated-yaml-text-to-embedding`.

## Considerações

- O script requer uma chave de API válida para o Google Generative AI (Gemini).  Substitua `"YOUR_API_KEY"` pela sua chave.
- O script utiliza o modelo Gemini.  Certifique-se de que o modelo esteja disponível e configurado corretamente na sua conta do Google Cloud.
- O prompt de sistema incluído na função `get_gemini_response` é projetado para gerar texto técnico e detalhado, mas pode ser ajustado para atender a necessidades específicas.

## Melhorias Possíveis

- Adicionar tratamento de erros mais robusto para lidar com falhas na API do Gemini.
- Implementar um sistema de logging para registrar as atividades do script.
- Adicionar opções de configuração para personalizar os parâmetros de geração de texto.
- Implementar um mecanismo para verificar a qualidade do texto gerado e descartar resultados insatisfatórios.
