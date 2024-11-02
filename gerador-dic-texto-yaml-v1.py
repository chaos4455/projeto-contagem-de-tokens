import os
import time
import yaml
import google.generativeai as genai
from datetime import datetime

# 🔑 Configura a chave da API
API_KEY = 'AIzaSyCEagEEnX-RdkW3-jCAb0H9nrTsgcE-Qqo'
genai.configure(api_key=API_KEY)

# 🧠 Nome do modelo
NOME_MODELO = "gemini-1.5-flash"

# 🚀 Função para configurar a geração de texto
def configurar_geracao(temperatura=0.8, top_p=0.95, top_k=64, max_tokens=8096):
    return {
        "temperature": temperatura,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": max_tokens,
        "response_mime_type": "text/plain",
    }

# 💬 Função para enviar uma mensagem para o modelo com tratamento de erro
def enviar_mensagem(sessao, mensagem):
    try:
        resposta = sessao.send_message([mensagem])
        return resposta.text
    except Exception as e:
        print(f"❗Erro ao enviar mensagem para o modelo: {e}")
        return ""

# 📝 Função para criar os tópicos do e-book em formato YAML
def gerar_topicos(sessao_chat, nome_ebook, tema):
    prompt_topicos = f"""
    Crie 16 tópicos para o seguinte e-book: '{nome_ebook}', baseado no tema: '{tema}'. 
    Responda em formato de lista YAML. Aqui está o formato esperado:
    crie as respostas em cada capitulo bem longa, completa, detalhada, sempre mais de 400 linhas, muitos exemplos, do basico ao avançado para cada topico
    nunca gere em html pois o html nao renderiza no markdown nunca crie exemplo "
<h1> Capítulo 3: Configurando seu Ambiente de Desenvolvimento com Docker e Portainer 🐳 </h1>

<p style="text-align: center;">
  <img src="https://www.docker.com/wp-content/uploads/2022/03/vertical-logo-monochromatic.png" alt="Docker Logo" width="200"/>
  <img src="https://www.portainer.io/hubfs/Website-Assets/Logos/Portainer-Logo-Dark-Mode.svg" alt="Portainer Logo" width="200"/>
</p>

" nunca use tags html como essas 


    ```yaml
    tópicos:
      - nome: "Tópico 1"
        descrição: "Descrição do Tópico 1"
      - nome: "Tópico 2"
        descrição: "Descrição do Tópico 2"
      ...
    ```

    Lembre-se que a lista completa dos tópicos será usada para orientar a criação de cada capítulo do e-book.
    """
    resposta_topicos = enviar_mensagem(sessao_chat, prompt_topicos)
    
    if resposta_topicos:
        try:
            # Limpa a marcação de código YAML
            resposta_topicos = resposta_topicos.strip()
            if resposta_topicos.startswith('```yaml'):
                resposta_topicos = resposta_topicos[7:]  # Remove ```yaml
            if resposta_topicos.endswith('```'):
                resposta_topicos = resposta_topicos[:-3]  # Remove ```
            
            topicos_yaml = yaml.safe_load(resposta_topicos)
            if 'tópicos' in topicos_yaml:
                return topicos_yaml['tópicos']
            else:
                raise ValueError("❗A resposta YAML não contém a chave 'tópicos'.")
        except yaml.YAMLError as e:
            print(f"❗Erro ao processar YAML: {e}")
    return []

# 🔄 Função principal para criar o e-book
def criar_ebook(nome_ebook, tema):
    # Validação básica das entradas
    if not nome_ebook or not tema:
        print("❗Nome do e-book e tema não podem estar vazios.")
        return
    
    # Criação do nome do arquivo com timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nome_arquivo = f"{nome_ebook}_{tema}_{timestamp}.txt"
    
    # 🚀 Inicia a sessão de chat com o modelo
    try:
        sessao_chat = genai.GenerativeModel(
            model_name=NOME_MODELO,
            generation_config=configurar_geracao(),
        ).start_chat(history=[])
    except Exception as e:
        print(f"❗Erro ao iniciar sessão de chat: {e}")
        return

    # Gera os tópicos em YAML
    topicos = gerar_topicos(sessao_chat, nome_ebook, tema)
    
    if not topicos:
        print("❗Falha ao gerar tópicos. O processo será encerrado.")
        return

    # Processa cada tópico e escreve no arquivo
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        for i, topico in enumerate(topicos, start=1):
            topico_nome = topico.get('nome', f"Tópico {i}")
            topico_descricao = topico.get('descrição', '')

            print(f"🔄 Gerando capítulo {i}/16: {topico_nome}")

            # Gera conteúdo para o tópico atual
            prompt_capitulo = f"""
            Abaixo está a lista de tópicos em YAML para o e-book '{nome_ebook}' baseado no tema '{tema}':

            {yaml.dump({'tópicos': topicos}, allow_unicode=True)}

            Crie o capítulo {i}, cujo tópico é '{topico_nome}'. 
            Escreva o capítulo completo, literal e didático, incluindo todos os detalhes necessários.
            Use muitos ícones e emojis para melhorar a leitura, e estilize o conteúdo como se fosse uma página do Notion.
            """
            capitulo = enviar_mensagem(sessao_chat, prompt_capitulo)
            
            if capitulo:
                # Escreve o conteúdo no arquivo
                arquivo.write(f"{i}. {topico_nome}\n\n{capitulo}\n\n")
                arquivo.flush()  # Garante que o conteúdo seja salvo incrementalmente
            else:
                print(f"❗Erro ao gerar o capítulo {i}. Pulando para o próximo.")
            
            # Intervalos entre as gerações
            if i == 1:
                time.sleep(1)  # Espera 30 segundos após o primeiro capítulo
            else:
                time.sleep(1)   # Espera 3 segundos entre os capítulos restantes

    print(f"📚 E-book '{nome_ebook}' baseado no tema '{tema}' criado com sucesso! Arquivo salvo em: {nome_arquivo}")

# 🚀 Execução do programa
if __name__ == "__main__":
    try:
        nome_ebook = input("Digite o nome do e-book: ").strip()
        tema = input("Digite o tema do e-book: ").strip()

        criar_ebook(nome_ebook, tema)
    except KeyboardInterrupt:
        print("❗Processo interrompido pelo usuário.")
    except Exception as e:
        print(f"❗Erro inesperado: {e}")
