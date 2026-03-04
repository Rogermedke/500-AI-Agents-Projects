#!/usr/bin/env python3
"""
Lição 2: Integrando o MCP Server com CrewAI

Objetivos:
- Criar ferramentas customizadas para acesso ao MCP
- Configurar autenticação e conexão
- Usar dados do MCP nas tarefas do agente
- Tratar erros e exceções
"""

import os

try:
    from crewai import Agent, Task, Crew
except ImportError:
    print("Execute primeiro: pip install -r requirements.txt")
    raise

# Ferramenta customizada: use crewai.tools se disponível (versões recentes)
try:
    from crewai.tools import tool
except ImportError:
    try:
        from crewai_tools import tool
    except ImportError:
        tool = None

# URL e chave do servidor FastMCP (configure no ambiente)
FASTMCP_URL = os.environ.get("FASTMCP_URL", "")
FASTMCP_API_KEY = os.environ.get("FASTMCP_API_KEY", "")


def _consulta_mcp_impl(consulta: str) -> str:
    """Implementação da consulta ao MCP."""
    if not FASTMCP_URL:
        return (
            "Servidor MCP não configurado. "
            "Defina FASTMCP_URL e FASTMCP_API_KEY no ambiente."
        )
    return f"[Simulação] Resposta do MCP para: {consulta}"


if tool is not None:
    @tool("Consulta ao MCP")
    def consulta_mcp(consulta: str) -> str:
        """Faz uma consulta ao servidor MCP configurado."""
        return _consulta_mcp_impl(consulta)
else:
    consulta_mcp = None


def main():
    print("=== Lição 2: Integração MCP com CrewAI ===\n")

    if not FASTMCP_URL:
        print(
            "Dica: export FASTMCP_URL=http://seu-servidor:porta\n"
            "      export FASTMCP_API_KEY=sua-chave\n"
        )

    tools_list = [consulta_mcp] if consulta_mcp else []
    agente = Agent(
        role="Analista com acesso a dados MCP",
        goal="Usar o MCP para enriquecer análises",
        backstory="Você usa ferramentas MCP quando precisa de dados externos.",
        tools=tools_list,
        verbose=True,
        allow_delegation=False,
    )

    tarefa = Task(
        description="Use a ferramenta MCP para obter informações sobre o tema: 'estado do projeto'.",
        expected_output="Resumo do que o MCP retornou.",
        agent=agente,
    )

    crew = Crew(agents=[agente], tasks=[tarefa])

    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Configure OPENAI_API_KEY (ou ANTHROPIC_API_KEY) e execute novamente.")
        return

    resultado = crew.kickoff()
    print("\n--- Resultado ---")
    print(resultado)


if __name__ == "__main__":
    main()
