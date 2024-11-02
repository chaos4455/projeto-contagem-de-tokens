# gerador_yaml_embeddings.py

## Descrição

Este script gera arquivos YAML contendo configurações para embeddings de texto, utilizando a API do Google Generative AI (Gemini). Ele permite ao usuário especificar um tema e o número de variações desejadas, gerando arquivos YAML com diferentes configurações para embeddings.

## Funcionalidades

- **`generate_hash()`**: Gera um hash MD5 único para cada arquivo YAML gerado, garantindo a unicidade dos nomes de arquivo.
- **`get_user_inputs()`**: Utiliza a biblioteca `inquirer` para obter as entradas do usuário (tema e número de iterações) de forma interativa.
- **`get_gemini_response(prompt)`**: Envia um prompt para a API do Gemini e retorna a resposta contendo as configurações de embedding. O prompt inclui instruções específicas para gerar um YAML com informações técnicas detalhadas.
- **`save_yaml(data, prompt)`**: Salva os dados gerados pela API do Gemini em um arquivo YAML, incluindo metadados como timestamp e o prompt utilizado.
- **`main()`**: Função principal que coordena o fluxo do programa, desde a obtenção das entradas do usuário até a geração e salvamento dos arquivos YAML. Utiliza a biblioteca `rich` para exibir uma barra de progresso durante o processo de geração.

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

Para executar o script, execute o comando `python gerador_yaml_embeddings.py` no terminal. O script solicitará ao usuário que insira um tema e o número de variações desejadas.  Após a confirmação, o script gerará os arquivos YAML na pasta `generated-yaml-text-to-embedding`.

## Considerações

- **Chave de API:** O script requer uma chave de API válida para o Google Generative AI (Gemini).  Substitua `"YOUR_API_KEY"` pela sua chave.
- **Modelo Gemini:** Certifique-se de que o modelo Gemini esteja disponível e configurado corretamente na sua conta do Google Cloud.
- **Tratamento de Erros:** O script inclui tratamento básico de erros, mas pode ser aprimorado para lidar com diferentes tipos de falhas na API do Gemini.
- **Personalização:** O prompt enviado para a API do Gemini pode ser personalizado para gerar configurações de embedding mais específicas.

## Melhorias Possíveis

- Implementar um sistema de logging para registrar as atividades do script e facilitar a depuração.
- Adicionar tratamento de erros mais robusto para lidar com diferentes cenários de falha.
- Implementar um mecanismo para verificar a validade e a consistência dos dados gerados pela API do Gemini.
- Adicionar opções de configuração para personalizar o comportamento do script, como o número máximo de tokens na resposta da API ou o formato do arquivo YAML.
