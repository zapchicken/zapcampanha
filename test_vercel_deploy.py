#!/usr/bin/env python3
"""
Teste para verificar se o arquivo está pronto para deploy no Vercel
"""

import os
import sys
from pathlib import Path

def test_file_structure():
    """Testa a estrutura de arquivos necessária"""
    print("🔍 Testando estrutura de arquivos...")
    
    required_files = [
        'api/index-vercel.py',
        'api/requirements.txt',
        'vercel.json'
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} - NÃO EXISTE")
            return False
    
    return True

def test_python_syntax():
    """Testa a sintaxe do arquivo Python"""
    print("\n🐍 Testando sintaxe Python...")
    
    try:
        # Lê o arquivo
        with open('api/index-vercel.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Compila para verificar sintaxe
        compile(content, 'api/index-vercel.py', 'exec')
        print("✅ Sintaxe Python válida")
        return True
        
    except SyntaxError as e:
        print(f"❌ Erro de sintaxe: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar: {e}")
        return False

def test_requirements():
    """Testa o arquivo requirements.txt"""
    print("\n📦 Testando requirements.txt...")
    
    try:
        with open('api/requirements.txt', 'r') as f:
            content = f.read().strip()
        
        if 'Flask' in content:
            print("✅ Flask encontrado no requirements.txt")
            return True
        else:
            print("❌ Flask não encontrado no requirements.txt")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao ler requirements.txt: {e}")
        return False

def test_vercel_config():
    """Testa a configuração do Vercel"""
    print("\n⚙️ Testando configuração do Vercel...")
    
    try:
        with open('vercel.json', 'r') as f:
            content = f.read()
        
        if 'api/index-vercel.py' in content:
            print("✅ Arquivo correto configurado no vercel.json")
            return True
        else:
            print("❌ Arquivo incorreto no vercel.json")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao ler vercel.json: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 TESTE DE DEPLOY VERCEL")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_python_syntax,
        test_requirements,
        test_vercel_config
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Arquivo pronto para deploy no Vercel")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("🔧 Corrija os problemas antes do deploy")
    
    return all_passed

if __name__ == '__main__':
    main()
