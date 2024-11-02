# Gerador Vetorizador Contínuo - Documentação 📝

## Visão Geral 🤔

Olá! Sou Elias Andrade e criei este gerador vetorizador contínuo.  Este documento descreve como ele funciona, passo a passo.  🚀 É um sistema que gera embeddings de palavras usando o modelo BERT 🤖 e armazena esses vetores em um banco de dados SQLite 🗄️.  Além disso, ele usa a API do Google Gemini 🧠 para expandir a lista de palavras a serem processadas, tornando o processo mais completo e eficiente.  ✨

## Arquitetura 🏗️

O sistema é composto por três módulos principais, que trabalham juntos em perfeita harmonia: 🤝

1. **Módulo de Aquisição de Palavras 🎣:** Este módulo é responsável por obter a lista de palavras que serão processadas.  Inicialmente, o usuário fornece uma palavra-chave.  Em seguida, a API do Google Gemini é consultada para obter uma lista de palavras relacionadas a essa palavra-chave.  A resposta da API é processada para extrair as palavras relevantes, que são então limpas e preparadas para o próximo estágio.  Este módulo inclui um tratamento de erros robusto para lidar com possíveis falhas na API do Gemini, garantindo a estabilidade do sistema.  A limpeza de dados inclui a remoção de caracteres especiais, conversão para minúsculas e a remoção de palavras duplicadas.

2. **Módulo de Vetorização ⚡:** Este módulo utiliza o modelo BERT para gerar os embeddings vetoriais para cada palavra na lista.  O modelo BERT é carregado na memória e usado para gerar representações vetoriais de 768 dimensões para cada palavra.  Cada vetor representa a semântica da palavra, permitindo que sejam usadas em tarefas de processamento de linguagem natural.  Este módulo é otimizado para velocidade e eficiência, utilizando a GPU se disponível.  Um mecanismo de cache é implementado para armazenar os embeddings já gerados, evitando cálculos redundantes e melhorando o desempenho.

3. **Módulo de Persistência 💾:** Este módulo é responsável por armazenar os embeddings gerados em um banco de dados SQLite.  Cada entrada no banco de dados contém a palavra, seu vetor (armazenado como um objeto BLOB), e um carimbo de data/hora.  Um mecanismo de `INSERT OR REPLACE` garante que apenas palavras únicas sejam armazenadas, atualizando o vetor se a palavra já existir.  Isso garante a integridade dos dados e evita redundâncias.  O banco de dados é otimizado para acesso rápido e eficiente aos embeddings.


## Fluxo de Dados ➡️

1. Você fornece uma palavra inicial.  🔤
2. O **Módulo de Aquisição de Palavras** consulta a API do Google Gemini para obter uma lista de palavras relacionadas.  🌐
3. As palavras são extraídas da resposta do Gemini e limpas pelo **Módulo de Aquisição de Palavras**.  🧽
4. Para cada palavra, o **Módulo de Vetorização** gera um embedding usando o modelo BERT.  🤖
5. O embedding e a palavra são armazenados no banco de dados SQLite pelo **Módulo de Persistência**.  🗄️
6. O sistema fornece um relatório com métricas de desempenho e processamento.  📊

## Funcionalidades 🎉

* **Geração de Embeddings:**  Geração de embeddings vetoriais de alta dimensionalidade para palavras usando o modelo BERT.  📈
* **Persistência de Dados:**  Armazenamento eficiente dos embeddings em um banco de dados SQLite.  🗄️
* **Integração com Gemini:**  Utilização da API do Google Gemini para expandir a lista de palavras.  🌐
* **Monitoramento de Desempenho:**  Coleta e exibição de métricas de desempenho em tempo real, incluindo tempo de processamento, uso de recursos do sistema, e estatísticas sobre as palavras e tokens processados.  ⏱️
* **Tratamento de Erros:**  Mecanismos de tratamento de erros para lidar com falhas na API do Gemini e na geração de embeddings.  🛡️
* **Relatório Final:**  Geração de um relatório completo com todas as métricas coletadas durante o processamento.  📄

## Classes Principais 🧱

* **`GeradorVetorizadorContinuo`:**  A classe principal que coordena todo o processo, do início ao fim.  👑
* **`YAMLVectorizer`:**  Responsável pela inicialização e utilização do modelo BERT.  🤖
* **`ProcessingStats`:**  Coleta e gerencia as métricas de desempenho.  📊
* **`GeminiAPIWrapper`:** Classe auxiliar para interação com a API do Google Gemini.
* **`SQLiteDataManager`:** Classe auxiliar para interação com o banco de dados SQLite.

## Tecnologias Utilizadas 🛠️

* **Python:**  A linguagem que escolhi para este projeto.  🐍
* **BERT (Transformers):**  O modelo de linguagem que faz a mágica dos embeddings.  🧙‍♂️
* **SQLite:**  O banco de dados que armazena tudo com segurança.  🗄️
* **Google Gemini API:**  A API que me ajuda a expandir a lista de palavras.  🧠
* **Rich:**  Biblioteca Python para uma interface de usuário incrível.  ✨
* **Pandas:**  Para manipulação de dados.  🐼
* **NumPy:**  Para computação numérica.  🧮
* **Torch:**  Para processamento de tensores.  🔥

## Considerações 🤔

* A precisão dos embeddings depende da qualidade do modelo BERT e da qualidade das palavras geradas pela API do Gemini.  A escolha do modelo BERT e a parametrização da API do Gemini podem afetar significativamente a qualidade dos embeddings gerados.  Experimentação e ajuste fino são recomendados para otimizar a precisão.
* O desempenho do sistema pode ser afetado pela velocidade da API do Gemini, pela disponibilidade de recursos do sistema (CPU, memória, GPU) e pelo tamanho da lista de palavras a serem processadas.  O uso de processamento paralelo e técnicas de otimização de memória são cruciais para garantir um desempenho eficiente, especialmente com grandes conjuntos de dados.
* O tamanho do banco de dados pode crescer significativamente com o tempo, dependendo do número de palavras processadas.  Considerações sobre o gerenciamento do banco de dados, como a implementação de mecanismos de limpeza de dados antigos ou a migração para um banco de dados mais escalável, devem ser levadas em conta para sistemas de produção.  O uso de um sistema de cache eficiente também é crucial para minimizar o impacto do tamanho do banco de dados no desempenho.

## Histórico de Versões 📜

| Versão | Data       | Descrição                               | Autor     |
|--------|------------|-------------------------------------------|-----------|
| 1.0    | 2024-11-02 | Versão inicial da documentação           | Elias Andrade |
| 1.1    | 2024-11-03 | Atualização da documentação com detalhes adicionais sobre a arquitetura e considerações de desempenho. | Elias Andrade |
