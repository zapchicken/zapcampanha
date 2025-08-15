#!/usr/bin/env python3
"""
Teste do sistema ZapCampanhas
"""

print("🚀 ZapCampanhas - Sistema de Business Intelligence")
print("=" * 50)

try:
    import pandas as pd
    print("✅ Pandas importado com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar Pandas: {e}")

try:
    import click
    print("✅ Click importado com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar Click: {e}")

try:
    from rich.console import Console
    print("✅ Rich importado com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar Rich: {e}")

try:
    from pathlib import Path
    print("✅ Pathlib importado com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar Pathlib: {e}")

print("\n📋 Funcionalidades Disponíveis:")
print("1. python main.py setup - Configurar ambiente")
print("2. python main.py zapchicken - Processar dados da ZapChicken")
print("3. python main.py chat - Chat com IA")
print("4. python main.py process - Processamento genérico")
print("5. python main.py analyze - Analisar planilhas")

print("\n🎯 Para usar com dados da ZapChicken:")
print("1. Coloque os 4 arquivos em data/input/")
print("2. Execute: python main.py zapchicken")
print("3. Para chat: python main.py chat")

print("\n📚 Documentação:")
print("- README.md - Guia geral")
print("- GUIA_ZAPCHICKEN.md - Guia específico")
print("- INSTALACAO.md - Guia de instalação")
