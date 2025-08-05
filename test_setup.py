#!/usr/bin/env python3
"""
Script de teste para o novo design OLASIS
Execute este arquivo para verificar se todas as dependências estão corretas
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Testa se todas as importações estão funcionando"""
    try:
        print("🔄 Testando importações...")
        
        # Testar Streamlit
        import streamlit as st
        print("✅ Streamlit OK")
        
        # Mudar para o diretório app para testar importações
        import os
        old_cwd = os.getcwd()
        os.chdir('app')
        
        try:
            # Testar módulos do app
            from artigos import show_inteligente
            print("✅ Artigos OK")
            
            from especialistas import show_especialistas
            print("✅ Especialistas OK")
            
            from olacefs import show_olacefs_search
            print("✅ OLACEFS OK")
            
            from chatbot import show_chatbot
            print("✅ Chatbot OK")
            
            from db_view import show_dados
            print("✅ DB View OK")
            
        finally:
            os.chdir(old_cwd)
        
        print("\n🎉 Todas as importações estão funcionando!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_assets():
    """Testa se os assets existem"""
    print("\n🔄 Testando assets...")
    
    assets_dir = Path("assets")
    if assets_dir.exists():
        print("✅ Diretório assets encontrado")
        
        # Verificar logo
        logo_path = assets_dir / "logo.png"
        if logo_path.exists():
            print("✅ Logo encontrado")
        else:
            print("⚠️  Logo não encontrado")
            
        # Verificar VerichIA
        verichia_path = assets_dir / "VerichIA.png"
        if verichia_path.exists():
            print("✅ VerichIA encontrado")
        else:
            print("⚠️  VerichIA não encontrado")
    else:
        print("⚠️  Diretório assets não encontrado")

def main():
    """Função principal do teste"""
    print("🚀 OLASIS - Teste do Novo Design")
    print("=" * 40)
    
    # Testar importações
    imports_ok = test_imports()
    
    # Testar assets
    test_assets()
    
    # Resultado final
    print("\n" + "=" * 40)
    if imports_ok:
        print("🎉 Sistema pronto para execução!")
        print("\nPara executar o sistema:")
        print("cd app && streamlit run main.py")
    else:
        print("❌ Corrigir erros antes de executar")
        
    print("\n📄 Consulte VISUAL_UPDATES.md para detalhes das melhorias")

if __name__ == "__main__":
    main()
