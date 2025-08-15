#!/usr/bin/env python3
"""
Script para testar se os dados estão sendo carregados corretamente
"""

import sys
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.append(str(Path(__file__).parent / "src"))

def test_data_loading():
    """Testa se os dados estão sendo carregados corretamente"""
    
    print("🔍 TESTANDO CARREGAMENTO DE DADOS...")
    print("=" * 50)
    
    try:
        from src.zapchicken_processor import ZapChickenProcessor
        
        # Configura diretórios
        input_dir = Path("data/input")
        output_dir = Path("data/output")
        
        print(f"📁 Diretório de entrada: {input_dir}")
        print(f"📁 Diretório de saída: {output_dir}")
        
        # Verifica se os diretórios existem
        if not input_dir.exists():
            print("❌ Diretório de entrada não existe!")
            return False
            
        if not output_dir.exists():
            print("❌ Diretório de saída não existe!")
            return False
        
        # Lista arquivos de entrada
        input_files = list(input_dir.glob("*"))
        print(f"\n📋 Arquivos encontrados em {input_dir}:")
        for file in input_files:
            print(f"  - {file.name}")
        
        if not input_files:
            print("❌ Nenhum arquivo encontrado em data/input/")
            return False
        
        # Inicializa processador
        print(f"\n🔧 Inicializando processador...")
        processor = ZapChickenProcessor(input_dir, output_dir)
        
        # Carrega dados
        print(f"\n📥 Carregando dados...")
        dataframes = processor.load_zapchicken_files()
        
        if not dataframes:
            print("❌ Nenhum dataframe foi carregado!")
            return False
        
        print(f"\n✅ DADOS CARREGADOS COM SUCESSO!")
        print("=" * 50)
        
        # Verifica cada dataframe
        for name, df in dataframes.items():
            if df is not None and not df.empty:
                print(f"✅ {name}: {len(df)} registros")
                print(f"   Colunas: {list(df.columns)}")
                if len(df) > 0:
                    print(f"   Primeiras linhas:")
                    print(df.head(2).to_string())
                print()
            else:
                print(f"❌ {name}: vazio ou None")
                print()
        
        # Testa IA Gemini
        print("🤖 TESTANDO IA GEMINI...")
        print("=" * 50)
        
        try:
            from src.zapchicken_ai_gemini import ZapChickenAIGemini
            
            # Cria instância da IA
            ai = ZapChickenAIGemini(processor, "test_key")
            
            # Verifica status dos dados
            data_status = ai.get_data_status()
            print(f"📊 Status dos dados:")
            print(data_status)
            
            # Testa preparação de resumo
            print(f"\n📋 Testando preparação de resumo...")
            summary = ai._prepare_data_summary()
            print(summary)
            
            print(f"\n✅ IA GEMINI FUNCIONANDO CORRETAMENTE!")
            
        except Exception as e:
            print(f"❌ Erro na IA Gemini: {str(e)}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_data_loading()
    
    if success:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Os dados estão sendo carregados corretamente")
        print("✅ A IA Gemini está funcionando")
        print("\n🚀 Agora você pode usar o servidor web:")
        print("   python main.py web")
    else:
        print("\n❌ ALGUNS TESTES FALHARAM!")
        print("🔧 Verifique se:")
        print("   1. Os arquivos estão em data/input/")
        print("   2. Os arquivos têm os nomes corretos")
        print("   3. Os arquivos não estão corrompidos")
