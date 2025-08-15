#!/usr/bin/env python3
"""
Script de teste para verificar se o Vercel está funcionando
"""

import requests
import json
import time

def test_vercel_deploy():
    """Testa se o deploy no Vercel está funcionando"""
    
    # URL base (substitua pela sua URL do Vercel)
    base_url = "https://zapcampanha.vercel.app"  # ou sua URL
    
    print("🧪 TESTANDO DEPLOY NO VERCEL...")
    print("=" * 50)
    
    try:
        # Teste 1: Página principal
        print("1. Testando página principal...")
        response = requests.get(base_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Página principal carregou!")
        else:
            print(f"❌ Erro na página principal: {response.status_code}")
            return False
        
        # Teste 2: API de status
        print("2. Testando API de status...")
        response = requests.get(f"{base_url}/check_files", timeout=10)
        
        if response.status_code == 200:
            print("✅ API de status funcionando!")
            data = response.json()
            print(f"   Relatórios disponíveis: {len(data)}")
        else:
            print(f"❌ Erro na API: {response.status_code}")
        
        # Teste 3: Upload de arquivo pequeno
        print("3. Testando upload de arquivo...")
        
        # Cria um arquivo CSV pequeno para teste
        test_csv = "Nome,Telefone\nJoão,11999999999\nMaria,11888888888"
        
        files = {'file': ('teste.csv', test_csv, 'text/csv')}
        data = {'file_type': 'contacts'}
        
        response = requests.post(f"{base_url}/upload", files=files, data=data, timeout=15)
        
        if response.status_code in [200, 302]:  # 302 é redirect
            print("✅ Upload funcionando!")
        else:
            print(f"❌ Erro no upload: {response.status_code}")
        
        print("\n🎉 TESTES CONCLUÍDOS!")
        print("✅ Se todos os testes passaram, o Vercel está funcionando!")
        
        return True
        
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT - O Vercel está demorando muito para responder")
        return False
        
    except requests.exceptions.ConnectionError:
        print("❌ ERRO DE CONEXÃO - Verifique se a URL está correta")
        return False
        
    except Exception as e:
        print(f"❌ ERRO GERAL: {str(e)}")
        return False

def test_performance():
    """Testa performance do Vercel"""
    
    base_url = "https://zapcampanha.vercel.app"
    
    print("\n⚡ TESTE DE PERFORMANCE...")
    print("=" * 30)
    
    try:
        start_time = time.time()
        response = requests.get(base_url, timeout=10)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if response_time < 5:
            print(f"✅ Rápido! {response_time:.2f}s")
        elif response_time < 10:
            print(f"⚠️ Lento! {response_time:.2f}s")
        else:
            print(f"❌ Muito lento! {response_time:.2f}s")
            
    except Exception as e:
        print(f"❌ Erro no teste de performance: {str(e)}")

if __name__ == "__main__":
    print("🚀 TESTE DO VERCEL - ZAPCAMPANHAS")
    print("=" * 50)
    
    success = test_vercel_deploy()
    
    if success:
        test_performance()
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("1. Teste com arquivos pequenos (< 5MB)")
        print("2. Configure a API Gemini")
        print("3. Teste o processamento de dados")
    else:
        print("\n🔧 PROBLEMAS DETECTADOS:")
        print("1. Verifique se o deploy foi concluído")
        print("2. Confirme a URL do Vercel")
        print("3. Verifique os logs do Vercel")
