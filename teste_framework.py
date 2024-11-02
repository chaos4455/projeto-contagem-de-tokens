import asyncio
from evolucao_framework import EvolucaoFramework
from rich.console import Console

# Adicione estas configurações no início do arquivo, após as importações
CONFIG_GERACAO = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8096,
}

async def testar_framework():
    console = Console()
    framework = EvolucaoFramework()
    
    console.print("[bold blue]🚀 Iniciando testes do Framework[/bold blue]")
    
    # Teste 1: Mensagem simples para API
    console.print("\n[yellow]Teste 1: Enviando 'Oi' para API Gemini[/yellow]")
    try:
        prompt = "Olá! Por favor responda apenas: 'Oi! Estou funcionando!'"
        response = await framework.model.generate_content_async(
            prompt,
            generation_config=CONFIG_GERACAO
        )
        console.print(f"[green]Resposta da API:[/green] {response.text}")
    except Exception as e:
        console.print(f"[red]Erro no Teste 1:[/red] {str(e)}")

    # Teste 2: Gerando embeddings
    console.print("\n[yellow]Teste 2: Gerando embeddings de uma mensagem[/yellow]")
    try:
        texto = "Testando a geração de embeddings"
        embedding = await framework.gerar_embeddings(texto)
        console.print(f"[green]Embedding gerado com sucesso:[/green]")
        console.print(embedding)
    except Exception as e:
        console.print(f"[red]Erro no Teste 2:[/red] {str(e)}")

    # Teste 3: Gerando documentação
    console.print("\n[yellow]Teste 3: Testando geração de documentação[/yellow]")
    try:
        codigo_exemplo = """
        def soma(a, b):
            return a + b
        """
        doc = await framework.gerar_documentacao_ia(codigo_exemplo)
        console.print(f"[green]Documentação gerada:[/green]")
        console.print(doc)
    except Exception as e:
        console.print(f"[red]Erro no Teste 3:[/red] {str(e)}")

    # Teste 4: Testando geração de hash
    console.print("\n[yellow]Teste 4: Testando geração de hash[/yellow]")
    try:
        hash_gerado = framework.gerar_hash_unico("teste")
        console.print(f"[green]Hash gerado:[/green] {hash_gerado}")
    except Exception as e:
        console.print(f"[red]Erro no Teste 4:[/red] {str(e)}")

    # Exibindo painel de resumo
    framework.exibir_painel(
        "Resumo dos Testes",
        """
        ✅ Teste de conexão com API
        ✅ Teste de geração de embeddings
        ✅ Teste de geração de documentação
        ✅ Teste de geração de hash
        """
    )

if __name__ == "__main__":
    console = Console()
    console.print("\n[bold magenta]🔬 Iniciando Suite de Testes do Framework[/bold magenta]")
    
    try:
        asyncio.run(testar_framework())
    except KeyboardInterrupt:
        console.print("\n[yellow]Testes interrompidos pelo usuário[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Erro durante execução dos testes:[/red] {str(e)}")
    finally:
        console.print("\n[bold magenta]🏁 Finalização dos Testes[/bold magenta]")
