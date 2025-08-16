#!/usr/bin/env python3
"""
Teste para verificar se a aplicação está pronta para o Render
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Testa se todas as importações funcionam"""
    print("🔍 Testando importações...")
    
    try:
        import flask
        print("✅ Flask importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar Flask: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar Pandas: {e}")
        return False
    
    try:
        import openpyxl
        print("✅ OpenPyXL importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar OpenPyXL: {e}")
        return False
    
    return True

def test_app_file():
    """Testa se o arquivo app.py existe e pode ser importado"""
    print("\n🔍 Testando arquivo app.py...")
    
    app_file = Path("app.py")
    if not app_file.exists():
        print("❌ Arquivo app.py não encontrado")
        return False
    
    print("✅ Arquivo app.py encontrado")
    
    try:
        # Testa se pode importar o app
        sys.path.insert(0, str(Path.cwd()))
        from app import app
        print("✅ Aplicação Flask importada com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao importar aplicação: {e}")
        return False

def test_requirements():
    """Testa se o requirements.txt existe e tem as dependências necessárias"""
    print("\n🔍 Testando requirements.txt...")
    
    req_file = Path("requirements.txt")
    if not req_file.exists():
        print("❌ Arquivo requirements.txt não encontrado")
        return False
    
    print("✅ Arquivo requirements.txt encontrado")
    
    with open(req_file, 'r') as f:
        requirements = f.read()
    
    required_packages = ['Flask', 'pandas', 'openpyxl']
    missing_packages = []
    
    for package in required_packages:
        if package.lower() not in requirements.lower():
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Pacotes faltando: {', '.join(missing_packages)}")
        return False
    
    print("✅ Todos os pacotes necessários estão no requirements.txt")
    return True

def test_render_config():
    """Testa se o render.yaml está configurado corretamente"""
    print("\n🔍 Testando render.yaml...")
    
    render_file = Path("render.yaml")
    if not render_file.exists():
        print("❌ Arquivo render.yaml não encontrado")
        return False
    
    print("✅ Arquivo render.yaml encontrado")
    
    with open(render_file, 'r') as f:
        config = f.read()
    
    required_configs = [
        'type: web',
        'name: zapcampanhas',
        'env: python',
        'buildCommand: pip install -r requirements.txt',
        'startCommand: python app.py'
    ]
    
    missing_configs = []
    for config_item in required_configs:
        if config_item not in config:
            missing_configs.append(config_item)
    
    if missing_configs:
        print(f"❌ Configurações faltando: {', '.join(missing_configs)}")
        return False
    
    print("✅ Configuração do Render está correta")
    return True

def test_directory_structure():
    """Testa se a estrutura de diretórios está correta"""
    print("\n🔍 Testando estrutura de diretórios...")
    
    required_dirs = ['src', 'config', 'templates']
    missing_dirs = []
    
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"❌ Diretórios faltando: {', '.join(missing_dirs)}")
        return False
    
    print("✅ Estrutura de diretórios está correta")
    return True

def test_environment_variables():
    """Testa se as variáveis de ambiente estão configuradas"""
    print("\n🔍 Testando variáveis de ambiente...")
    
    # Testa se a porta está configurada
    port = os.environ.get('PORT', '5000')
    print(f"✅ Porta configurada: {port}")
    
    # Testa se o ambiente está configurado
    env = os.environ.get('FLASK_ENV', 'development')
    print(f"✅ Ambiente Flask: {env}")
    
    return True

def main():
    """Executa todos os testes"""
    print("🚀 Testando configuração para o Render...\n")
    
    tests = [
        test_imports,
        test_app_file,
        test_requirements,
        test_render_config,
        test_directory_structure,
        test_environment_variables
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Tudo pronto para o deploy no Render!")
        print("\n📋 Próximos passos:")
        print("1. Faça commit e push para o GitHub")
        print("2. Acesse render.com e conecte seu repositório")
        print("3. Configure o serviço web")
        print("4. Deploy automático!")
    else:
        print("⚠️  Alguns problemas foram encontrados. Corrija antes do deploy.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
