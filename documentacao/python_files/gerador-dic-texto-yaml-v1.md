# gerador-dic-texto-yaml-v1.py

## Descrição

Este script gera um arquivo de texto contendo um e-book estruturado em capítulos, utilizando a API do Google Generative AI (Gemini). O usuário fornece o nome do e-book e o tema, e o script gera os tópicos e o conteúdo de cada capítulo, salvando o resultado em um único arquivo de texto.

## Funcionalidades

- **`configurar_geracao()`**: Configura os parâmetros de geração de texto para a API do Gemini.
- **`enviar_mensagem(sessao, mensagem)`**: Envia uma mensagem para o modelo Gemini e retorna a resposta, com tratamento de erros.
- **`gerar_topicos(sessao_chat, nome_ebook, tema)`**: Gera uma lista de tópicos em formato YAML para o e-book, utilizando a API do Gemini.  Inclui tratamento de erros e validação da resposta YAML.
- **`criar_ebook(nome_ebook, tema)`**: Função principal que cria o e-book, gerando os tópicos e o conteúdo de cada capítulo.  Escreve o conteúdo em um arquivo de texto, com tratamento de erros e pausas controladas entre as gerações.

## Dependências

- `os`
- `time`
- `yaml`
- `google.generativeai`
- `datetime`

## Uso

Para executar o script, execute `python gerador-dic-texto-yaml-v1.py`. O script solicitará o nome do e-book e o tema.  Após a execução, o e-book será salvo em um arquivo de texto com um nome baseado no nome do e-book, tema e timestamp.

## Considerações

- **Chave de API:** O script requer uma chave de API válida para o Google Generative AI (Gemini). Substitua `"YOUR_API_KEY"` pela sua chave.
- **Modelo Gemini:** Certifique-se de que o modelo Gemini esteja disponível e configurado corretamente na sua conta do Google Cloud.
- **Tratamento de Erros:** O script inclui tratamento de erros para lidar com falhas na API do Gemini e erros de processamento do YAML.
- **Tempo de Execução:** A geração do e-book pode levar um tempo considerável, dependendo do tamanho e complexidade do conteúdo.

## Melhorias Possíveis

- Implementar um sistema de logging para registrar as atividades do script e facilitar a depuração.
- Adicionar um indicador de progresso para mostrar o andamento da geração do e-book.
- Implementar um mecanismo para salvar o e-book em diferentes formatos (por exemplo, Markdown ou HTML).
- Adicionar opções de configuração para personalizar o comportamento do script, como o número de tópicos a serem gerados ou o comprimento de cada capítulo.
