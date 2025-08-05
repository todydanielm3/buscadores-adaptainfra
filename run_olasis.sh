#!/bin/bash

# Script para executar o OLASIS com design moderno
# Versão: 2.0.0
# Data: 29 de julho de 2025

echo "🚀 OLASIS - Sistema de Información Sostenible"
echo "============================================="

# Verificar se estamos no diretório correto
if [ ! -f "app/main.py" ]; then
    echo "❌ Erro: Execute este script na pasta raiz do projeto"
    echo "   Exemplo: ./run_olasis.sh"
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -d "../.venv" ]; then
    echo "⚠️  Ambiente virtual não encontrado em ../. venv"
    echo "   Tentando criar um novo ambiente virtual..."
    python3 -m venv .venv
    echo "✅ Ambiente virtual criado"
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
if [ -d "../.venv" ]; then
    source ../.venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "❌ Não foi possível encontrar o ambiente virtual"
    exit 1
fi

echo "✅ Ambiente virtual ativado"

# Verificar e instalar dependências
echo "🔄 Verificando dependências..."
pip install -q streamlit pandas numpy &> /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Dependências básicas instaladas"
else
    echo "⚠️  Erro ao instalar dependências básicas"
fi

# Instalar dependências opcionais
echo "🔄 Instalando dependências opcionais..."
pip install -q google-generativeai python-dotenv langchain langchain-community langchain-google-genai faiss-cpu scikit-learn requests beautifulsoup4 &> /dev/null

# Verificar se o arquivo de configuração existe
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado"
    echo "   Criando arquivo .env de exemplo..."
    cat > .env << EOL
# Configurações do OLASIS
GOOGLE_API_KEY=sua_chave_da_api_gemini_aqui

# Outras configurações opcionais
# DEBUG=true
# LOG_LEVEL=info
EOL
    echo "✅ Arquivo .env criado. Configure sua chave da API do Gemini."
fi

# Navegar para a pasta app
cd app

# Verificar se há conflitos de porta
PORT=8501
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null; then
    echo "⚠️  Porta $PORT em uso, tentando porta $((PORT+1))"
    PORT=$((PORT+1))
fi

# Executar o Streamlit
echo "🎉 Iniciando OLASIS na porta $PORT..."
echo "   Acesse: http://localhost:$PORT"
echo "============================================="

streamlit run main.py --server.port $PORT --server.headless true

echo ""
echo "👋 OLASIS encerrado. Obrigado por usar!"
