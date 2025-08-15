#!/usr/bin/env python3
"""
Diagnóstico do Sistema ZapCampanhas
"""

import sys
import os
from pathlib import Path

def check_python_version():
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Diretório atual: {os.getcwd()}")

def check_dependencies():
    print("\n📦 Verificando dependências...")
    
    dependencies = [
        'flask',
        'pandas',
        'werkzeug',
        'pathlib'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - NÃO INSTALADO")

def check_directories():
    print("\n📁 Verificando diretórios...")
    
    dirs = [
        'data/input',
        'data/output',
        'templates',
        'src'
    ]
    
    for dir_path in dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - NÃO EXISTE")
            try:
                path.mkdir(parents=True, exist_ok=True)
                print(f"   📝 Criado: {dir_path}")
            except Exception as e:
                print(f"   ❌ Erro ao criar: {e}")

def check_files():
    print("\n📄 Verificando arquivos importantes...")
    
    files = [
        'templates/index.html',
        'web_app_flask.py',
        'requirements.txt',
        'src/__init__.py'
    ]
    
    for file_path in files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} - NÃO EXISTE")

def check_flask_app():
    print("\n🚀 Testando Flask...")
    
    try:
        from flask import Flask
        app = Flask(__name__)
        print("✅ Flask importado com sucesso")
        
        # Testa renderização de template
        try:
            from flask import render_template
            print("✅ render_template disponível")
        except Exception as e:
            print(f"❌ Erro com render_template: {e}")
            
    except Exception as e:
        print(f"❌ Erro ao importar Flask: {e}")

def main():
    print("🔍 DIAGNÓSTICO ZAPCAMPANHAS")
    print("=" * 50)
    
    check_python_version()
    check_dependencies()
    check_directories()
    check_files()
    check_flask_app()
    
    print("\n" + "=" * 50)
    print("🏁 Diagnóstico concluído!")

if __name__ == '__main__':
    main()
