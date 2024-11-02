# Gerador Vetorizador Contínuo - Documentação 📝

## Visão Geral 🤔

Olá! Sou Elias Andrade e criei este gerador vetorizador contínuo.  Este documento descreve como ele funciona, passo a passo.  🚀 É um sistema que gera embeddings de palavras usando o modelo BERT 🤖 e armazena esses vetores em um banco de dados SQLite 🗄️.  Além disso, ele usa a API do Google Gemini 🧠 para expandir a lista de palavras a serem processadas, tornando o processo mais completo e eficiente.  ✨

## Arquitetura 🏗️

O sistema é composto por três módulos principais, que trabalham juntos em perfeita harmonia: 🤝

1. **Módulo de Aquisição de Palavras 🎣:**  Aqui, eu uso a API do Google Gemini para gerar uma lista de palavras relacionadas a uma palavra inicial que você, usuário, fornece.  A resposta do Gemini é processada cuidadosamente para extrair as palavras, que são então limpas e preparadas para o próximo estágio.  🧹  Eu implementei um tratamento de erros robusto para garantir que o processo seja o mais estável possível, mesmo com respostas inesperadas da API.  🛡️

2. **Módulo de Vetorização ⚡:**  Neste módulo, eu emprego o poderoso modelo BERT para gerar embeddings vetoriais para cada palavra.  O modelo BERT é carregado e usado para gerar representações vetoriais de 768 dimensões para cada palavra.  Cada vetor representa a semântica da palavra, permitindo que sejam usadas em tarefas de processamento de linguagem natural.  🤓  Eu otimizei este processo para garantir velocidade e eficiência, usando a GPU se disponível. 💨

3. **Módulo de Persistência 💾:**  Finalmente, eu armazeno os embeddings gerados em um banco de dados SQLite.  Cada entrada no banco de dados contém a palavra, seu vetor (armazenado como um objeto BLOB), e um carimbo de data/hora.  ⏰  Um mecanismo de `INSERT OR REPLACE` garante que apenas palavras únicas sejam armazenadas, atualizando o vetor se a palavra já existir.  Isso garante a integridade dos dados e evita redundâncias.  ✅

## Fluxo de Dados ➡️

1. Você fornece uma palavra inicial.  🔤
2. Eu consulto a API do Google Gemini para obter uma lista de palavras relacionadas.  🌐
3. As palavras são extraídas da resposta do Gemini e limpas.  🧽
4. Para cada palavra, eu gero um embedding usando o modelo BERT.  🤖
5. O embedding e a palavra são armazenados no banco de dados SQLite.  🗄️
6. Eu forneço um relatório com métricas de desempenho e processamento.  📊

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

* A precisão dos embeddings depende da qualidade do modelo BERT e da qualidade das palavras geradas pela API do Gemini.  🎯
* O desempenho do sistema pode ser afetado pela velocidade da API do Gemini e pela disponibilidade de recursos do sistema.  ⚡️
* O tamanho do banco de dados pode crescer significativamente com o tempo, dependendo do número de palavras processadas.  📈

## Histórico de Versões 📜

| Versão | Data       | Descrição                               | Autor     |
|--------|------------|-------------------------------------------|-----------|
| 1.0    | 2024-11-02 | Versão inicial da documentação           | Elias Andrade |
