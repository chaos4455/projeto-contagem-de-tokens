import os
import shutil
from datetime import datetime
import getpass
from colorama import init, Fore, Back, Style
import inquirer
from glob import glob
import re
import tkinter as tk
from tkinter import ttk
import threading
import emoji

# Inicializa o colorama
init(autoreset=True)

def listar_arquivos_py():
    # Encontra todos os arquivos .py no diretório atual
    arquivos = glob("*.py")
    return arquivos

def obter_proxima_versao(arquivo_base):
    padrao = f"{arquivo_base.replace('.py', '')}-work--revision-*"
    versoes_existentes = glob(padrao)
    
    if not versoes_existentes:
        return f"{arquivo_base.replace('.py', '')}-work--revision-0001.py"
    
    # Encontra o número mais alto atual
    numeros = [int(re.findall(r'revision-(\d+)', v)[-1]) for v in versoes_existentes]
    proximo_numero = max(numeros) + 1
    
    return f"{arquivo_base.replace('.py', '')}-work--revision-{proximo_numero:04d}.py"

def print_header():
    """Imprime o cabeçalho do programa com estilo"""
    header = f"""
{Back.BLUE + Fore.WHITE}{'='*60}{Style.RESET_ALL}
{Back.BLUE + Fore.WHITE}🔄 Versionador de Arquivos Python v2.0 🐍{Style.RESET_ALL}
{Back.BLUE + Fore.WHITE}{'='*60}{Style.RESET_ALL}
"""
    print(header)

def print_status(mensagem, tipo="info"):
    """Imprime mensagens de status formatadas"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    icons = {
        "info": "ℹ️",
        "sucesso": "✅",
        "erro": "❌",
        "alerta": "⚠️",
        "processo": "⚙️",
        "arquivo": "📄",
        "versao": "🏷️",
        "tempo": "⏱️",
        "memoria": "💾",
        "sistema": "🖥️"
    }
    
    cores = {
        "info": Fore.CYAN,
        "sucesso": Fore.GREEN,
        "erro": Fore.RED,
        "alerta": Fore.YELLOW,
        "processo": Fore.BLUE,
        "arquivo": Fore.MAGENTA,
        "versao": Fore.WHITE,
        "tempo": Fore.CYAN,
        "memoria": Fore.GREEN,
        "sistema": Fore.BLUE
    }
    
    print(f"{cores[tipo]}[{timestamp}] {icons[tipo]} {mensagem}{Style.RESET_ALL}")

def mostrar_estatisticas(dados):
    """Mostra estatísticas em uma tabela colorida"""
    print(f"\n{Back.WHITE + Fore.BLACK}📊 Estatísticas do Sistema{Style.RESET_ALL}")
    
    tabela = f"""
    {Fore.CYAN}💾 Versões Criadas:{Style.RESET_ALL} {dados['Versões Criadas']}
    {Fore.MAGENTA}📁 Arquivos Versionados:{Style.RESET_ALL} {dados['Arquivos Versionados']}
    {Fore.GREEN}📦 Espaço Usado:{Style.RESET_ALL} {dados['Espaço Usado (MB)']} MB
    {Fore.YELLOW}🕒 Última Versão:{Style.RESET_ALL} {dados['Última Versão']}
    """
    print(tabela)

def registrar_log(mensagem, tipo="info"):
    """Registra mensagens no log com formatação melhorada"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    emojis = {
        "info": "ℹ️",
        "erro": "❌",
        "alerta": "⚠️",
        "sucesso": "✅"
    }
    
    with open("versionador.log", "a", encoding="utf-8") as log:
        log.write(f"[{timestamp}] {emojis.get(tipo, '•')} {mensagem}\n")

def gerar_dados_indicadores():
    """Gera dados fictícios para os indicadores."""
    # Adicionar try/except para evitar erros na contagem
    try:
        arquivos_py = glob("*.py")
        versoes = [f for f in arquivos_py if "revision" in f]
        tamanho_total = sum(os.path.getsize(f) for f in versoes) / (1024 * 1024)  # Converter para MB
        ultima_versao = max([os.path.getmtime(f) for f in versoes]) if versoes else 0
        
        return {
            "Versões Criadas": len(versoes),
            "Arquivos Versionados": len(set([f.split("-work-")[0] + ".py" for f in versoes])),
            "Espaço Usado (MB)": round(tamanho_total, 2),
            "Última Versão": datetime.datetime.fromtimestamp(ultima_versao).strftime('%Y-%m-%d %H:%M:%S') if ultima_versao else "Nenhuma"
        }
    except Exception as e:
        registrar_log(f"Erro ao gerar indicadores: {e}", tipo="erro")
        return {
            "Versões Criadas": 0,
            "Arquivos Versionados": 0,
            "Espaço Usado (MB)": 0,
            "Última Versão": "Erro ao carregar"
        }

def criar_interface_grafica():
    """Cria a interface gráfica com Tkinter."""
    root = None
    
    def atualizar_interface():
        try:
            nonlocal root
            if not root or not root.winfo_exists():
                return
                
            for widget in root.winfo_children():
                widget.destroy()
                
            dados = gerar_dados_indicadores()
            for i, (chave, valor) in enumerate(dados.items()):
                frame = ttk.Frame(root, padding=10)
                frame.grid(row=i, column=0, sticky="nsew")
                label = ttk.Label(frame, text=f"{chave}: {valor}", font=("Arial", 14))
                label.pack()
                
            root.after(5000, atualizar_interface)
            
        except Exception as e:
            registrar_log(f"Erro ao atualizar interface: {e}", tipo="erro")

    try:
        root = tk.Tk()
        root.title("Versionador - Indicadores")
        root.geometry("400x300")
        
        # Configurar o fechamento da janela
        def on_closing():
            root.quit()
            root.destroy()
            
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Iniciar primeira atualização
        atualizar_interface()
        
        # Executar mainloop na thread principal
        root.mainloop()
        
    except Exception as e:
        registrar_log(f"Erro ao criar interface gráfica: {e}", tipo="erro")

def main():
    print_header()
    
    # Lista arquivos .py disponíveis
    arquivos_py = listar_arquivos_py()
    
    if not arquivos_py:
        print_status("Nenhum arquivo .py encontrado no diretório atual!", "erro")
        registrar_log("Nenhum arquivo .py encontrado.", "erro")
        return
    
    print_status(f"Encontrados {len(arquivos_py)} arquivos Python", "info")
    
    # Cria a pergunta usando inquirer com estilo
    perguntas = [
        inquirer.List('arquivo',
                     message=f"{emoji.emojize(':file_folder:')} Selecione o arquivo para versionar",
                     choices=arquivos_py)
    ]
    
    # Obtém a resposta do usuário
    resposta = inquirer.prompt(perguntas)
    
    if resposta:
        arquivo_selecionado = resposta['arquivo']
        nova_versao = obter_proxima_versao(arquivo_selecionado)
        
        print_status(f"Iniciando versionamento do arquivo: {arquivo_selecionado}", "processo")
        
        try:
            shutil.copy2(arquivo_selecionado, nova_versao)
            
            print_status(f"Arquivo versionado com sucesso!", "sucesso")
            print(f"\n{Fore.GREEN}📄 Original:{Style.RESET_ALL} {arquivo_selecionado}")
            print(f"{Fore.GREEN}🔄 Nova versão:{Style.RESET_ALL} {nova_versao}")
            
            # Mostrar estatísticas
            dados = gerar_dados_indicadores()
            mostrar_estatisticas(dados)
            
            registrar_log(f"Arquivo '{arquivo_selecionado}' versionado para '{nova_versao}'", "sucesso")
            
        except Exception as e:
            print_status(f"Erro ao versionar arquivo: {e}", "erro")
            registrar_log(f"Erro ao versionar arquivo: {e}", "erro")
            
    print(f"\n{Back.BLUE + Fore.WHITE}{'='*60}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_status("\nOperação cancelada pelo usuário", "alerta")
    except Exception as e:
        print_status(f"Erro crítico: {e}", "erro")
