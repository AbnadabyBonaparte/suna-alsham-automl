#!/bin/bash
# 🚀 SUNA-ALSHAM Deploy Script
# Gerado automaticamente em 2025-07-22T11:36:54.909873

echo "🚀 Iniciando deploy do SUNA-ALSHAM..."

# Verificar Python
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 não encontrado"
    exit 1
fi

# Instalar dependências
echo "📦 Instalando dependências..."
pip3 install -r requirements_production.txt

# Verificar variáveis de ambiente
echo "🔍 Verificando variáveis de ambiente..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️ OPENAI_API_KEY não configurada"
fi

if [ -z "$REDIS_URL" ]; then
    echo "⚠️ REDIS_URL não configurada"
fi

# Executar testes
echo "🧪 Executando testes..."
python3 comprehensive_test_suite.py
if [ $? -ne 0 ]; then
    echo "❌ Testes falharam"
    exit 1
fi

# Iniciar aplicação
echo "🎯 Iniciando aplicação..."
if [ "${config.platform}" = "railway" ]; then
    python3 main_complete_system.py
elif [ "${config.platform}" = "heroku" ]; then
    gunicorn main_complete_system:app --bind 0.0.0.0:$PORT
else
    python3 main_complete_system.py
fi

echo "✅ Deploy concluído com sucesso!"
