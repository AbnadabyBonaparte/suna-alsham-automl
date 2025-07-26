#!/bin/bash

# Script de instalação de dependências para SUNA-ALSHAM v2.0
# Este script instala todos os módulos Python necessários

# Para em caso de erro
set -e

echo "🚀 Instalando dependências do SUNA-ALSHAM v2.0..."
echo "=============================================="

# Verificar se pip está instalado
if ! command -v pip &> /dev/null; then
    if command -v pip3 &> /dev/null; then
        alias pip='pip3'
    else
        echo "❌ pip não encontrado. Por favor, instale o Python primeiro."
        exit 1
    fi
fi

# Atualizar pip
echo "📦 Atualizando pip..."
python -m pip install --upgrade pip

# Instalar dependências principais
echo ""
echo "📦 Instalando módulos essenciais..."

# Módulos de sistema
pip install psutil  # Monitoramento de recursos do sistema

# Cache e armazenamento
pip install redis  # Cache distribuído
pip install "redis[hiredis]"  # Performance otimizada para Redis

# Requisições assíncronas
pip install aiohttp  # Cliente HTTP assíncrono
pip install aiofiles  # Operações de arquivo assíncronas

# Análise e correção de código
pip install autopep8  # Formatação automática de código Python
pip install black  # Formatador de código Python
pip install pylint  # Análise estática de código
pip install flake8  # Verificação de estilo de código

# Dependências adicionais recomendadas
echo ""
echo "📦 Instalando dependências adicionais recomendadas..."

# Processamento de dados
pip install numpy  # Computação numérica
pip install pandas  # Análise de dados
pip install scikit-learn  # Machine Learning

# Utilitários
pip install python-dotenv  # Gerenciamento de variáveis de ambiente
pip install pyyaml  # Suporte para arquivos YAML
pip install colorama  # Cores no terminal
pip install tqdm  # Barras de progresso

# Async e concorrência
pip install aiodns  # Resolução DNS assíncrona
pip install cchardet  # Detecção de charset rápida

# Web scraping (caso necessário)
pip install beautifulsoup4  # Parsing HTML
pip install lxml  # Parser XML/HTML rápido

# Logging avançado
pip install loguru  # Sistema de logging moderno

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "📋 Resumo das instalações:"
echo "  - psutil: Monitoramento de sistema"
echo "  - redis: Cache distribuído"
echo "  - aiohttp: Requisições HTTP assíncronas"
echo "  - autopep8: Formatação de código Python"
echo "  - E várias outras dependências úteis!"
echo ""
echo "🔄 Reinicie o sistema SUNA-ALSHAM para aplicar as mudanças."
