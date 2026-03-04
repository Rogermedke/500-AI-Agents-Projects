#!/usr/bin/env python3
"""
Lição 1: Configurando CrewAI com acesso ao MCP Server

Objetivos:
- Instalar pacotes necessários
- Configurar variáveis de ambiente (opcional nesta lição)
- Criar um agente CrewAI básico
- Executar uma tarefa simples
"""

import os

# Verifica se as dependências estão instaladas
try:
    from crewai import Agent, Task, Crew
except ImportError:
    print("Execute primeiro: pip install -r requirements.txt")
    raise


def main():
    print("=== Lição 1: Setup CrewAI ===\n")

    # Criar um agente simples (usa LLM padrão; configure OPENAI_API_KEY ou outro provider)
    agente = Agent(
        role="Assistente de pesquisa",
        goal="Responder perguntas de forma clara e objetiva",
        backstory="Você é um assistente prestativo e preciso.",
        verbose=True,
        allow_delegation=False,
    )

    tarefa = Task(
        description="Resuma em uma frase: o que é CrewAI?",
        expected_output="Uma frase objetiva explicando CrewAI.",
        agent=agente,
    )

    crew = Crew(agents=[agente], tasks=[tarefa])

    # Executar (requer API key configurada, ex: OPENAI_API_KEY)
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print(
            "Dica: defina OPENAI_API_KEY ou ANTHROPIC_API_KEY para executar a tarefa.\n"
            "Exemplo: export OPENAI_API_KEY=sua-chave"
        )
        print("Agente e tarefa criados com sucesso. Configure a API key e execute novamente.")
        return

    resultado = crew.kickoff()
    print("\n--- Resultado ---")
    print(resultado)


if __name__ == "__main__":
    main()
