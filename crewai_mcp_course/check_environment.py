#!/usr/bin/env python3
"""
Verifica se o ambiente está pronto para executar as lições do curso.
Execute a partir da pasta crewai_mcp_course com o venv ativado.
"""

import sys


def main():
    print("Verificando ambiente do curso CrewAI + FastMCP...\n")

    # Python 3.10+
    ver = sys.version_info
    if ver.major < 3 or (ver.major == 3 and ver.minor < 10):
        print(
            f"[X] Python 3.10+ necessário. Atual: {ver.major}.{ver.minor}.{ver.micro}\n"
            "    Use pyenv, python3.10, ou outro instalador para Python 3.10+."
        )
        sys.exit(1)
    print(f"[OK] Python {ver.major}.{ver.minor}.{ver.micro}")

    # Dependências
    try:
        import crewai
        print("[OK] crewai instalado")
    except ImportError:
        print("[X] crewai não encontrado. Execute: pip install -r requirements.txt")
        sys.exit(1)

    try:
        import fastmcp
        print("[OK] fastmcp instalado")
    except ImportError:
        print("[ ] fastmcp não instalado (opcional para lições 1 e 3). Para lição 2: pip install fastmcp")

    import os
    if os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY"):
        print("[OK] API key de LLM configurada")
    else:
        print("[ ] OPENAI_API_KEY ou ANTHROPIC_API_KEY não definidas (necessário para executar tarefas)")

    if os.environ.get("FASTMCP_URL"):
        print("[OK] FASTMCP_URL configurada")
    else:
        print("[ ] FASTMCP_URL não definida (necessário para lição 2 com MCP real)")

    print("\nAmbiente pronto. Execute: python lesson1_setup.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
