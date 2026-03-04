#!/usr/bin/env python3
"""
Lição 3: Padrões avançados de CrewAI com MCP Server

Objetivos:
- Implementar fluxos multi-agente
- Usar processos hierárquicos
- Compartilhar dados entre agentes via MCP
- Armazenar e recuperar resultados de pesquisa
- Implementar revisão de qualidade
"""

import os

try:
    from crewai import Agent, Task, Crew
except ImportError:
    print("Execute primeiro: pip install -r requirements.txt")
    raise


def main():
    print("=== Lição 3: Padrões avançados (multi-agente) ===\n")

    pesquisador = Agent(
        role="Pesquisador",
        goal="Coletar e resumir informações de forma precisa",
        backstory="Você é metódico e cita fontes.",
        verbose=True,
        allow_delegation=False,
    )

    redator = Agent(
        role="Redator",
        goal="Escrever relatórios claros e bem estruturados",
        backstory="Você transforma notas em textos profissionais.",
        verbose=True,
        allow_delegation=False,
    )

    revisor = Agent(
        role="Revisor",
        goal="Garantir qualidade e consistência do relatório",
        backstory="Você revisa conteúdo e sugere melhorias.",
        verbose=True,
        allow_delegation=False,
    )

    tarefa_pesquisa = Task(
        description="Pesquise e resuma em 3 bullet points: benefícios de usar multi-agentes em IA.",
        expected_output="Três bullet points objetivos.",
        agent=pesquisador,
    )

    tarefa_redacao = Task(
        description="Com base no resumo do pesquisador, escreva um parágrafo de relatório profissional.",
        expected_output="Um parágrafo bem formatado.",
        agent=redator,
        context=[tarefa_pesquisa],
    )

    tarefa_revisao = Task(
        description="Revise o parágrafo do redator e liste 1–2 sugestões de melhoria.",
        expected_output="Texto revisado e lista de sugestões.",
        agent=revisor,
        context=[tarefa_redacao],
    )

    crew = Crew(
        agents=[pesquisador, redator, revisor],
        tasks=[tarefa_pesquisa, tarefa_redacao, tarefa_revisao],
    )

    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Configure OPENAI_API_KEY (ou ANTHROPIC_API_KEY) e execute novamente.")
        return

    resultado = crew.kickoff()
    print("\n--- Resultado ---")
    print(resultado)


if __name__ == "__main__":
    main()
