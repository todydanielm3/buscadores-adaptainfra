#!/bin/bash

# Script para executar o sistema OLASIS com todas as dependências configuradas
echo "🚀 Iniciando Sistema OLASIS - Versão Corrigida"
echo "================================================"

# Verificar se estamos no diretório correto
if [ ! -f "app/main.py" ]; then
    echo "❌ Erro: Execute este script a partir do diretório raiz do projeto"
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao criar ambiente virtual"
        exit 1
    fi
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Verificar se as dependências estão instaladas
if [ ! -f "venv/pyvenv.cfg" ] || [ ! -f "venv/lib/python*/site-packages/streamlit" ]; then
    echo "📥 Instalando dependências..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao instalar dependências"
        exit 1
    fi
fi

# Configurar variável de ambiente da API key do Google
echo "🔑 Configurando API key..."
export GOOGLE_API_KEY="AIzaSyCyafUCrwzxm8DCxn3XCmGULnynruRWL30"

# Exibir informações do sistema
echo "✅ Ambiente configurado com sucesso!"
echo "📍 URL Local: http://localhost:8501"
echo "🌐 URL Rede: http://$(hostname -I | awk '{print $1}'):8501"
echo ""
echo "🎯 Funcionalidades disponíveis:"
echo "   • Menu modernizado com design responsivo"
echo "   • Chatbot integrado com Google Gemini"
echo "   • Buscadores de artigos e especialistas"
echo "   • Interface OLACEFS atualizada"
echo "   • Visualizador de banco de dados"
echo ""
echo "🚀 Iniciando aplicação..."
echo "📝 Para parar o servidor, pressione Ctrl+C"
echo ""

# Executar o sistema
streamlit run app/main.py

echo ""
echo "👋 Sistema OLASIS encerrado."
