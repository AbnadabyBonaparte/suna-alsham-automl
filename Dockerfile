# =====================================================
# SUNA-ALSHAM Dockerfile
# Sistema de Agentes Auto-Evolutivos com AutoML Real
# =====================================================

# Base image otimizada para Python e ML
FROM python:3.11-slim-bullseye

# Metadata
LABEL maintainer="SUNA-ALSHAM Team"
LABEL description="Sistema Auto-Evolutivo de IA com AutoML Real"
LABEL version="2.1.0"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Configurações do sistema
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Criar usuário não-root para segurança
RUN groupadd --gid 1000 suna && \
    useradd --uid 1000 --gid suna --shell /bin/bash --create-home suna

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    gcc \
    g++ \
    libopenblas-dev \
    liblapack-dev \
    gfortran \
    libpq-dev \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (para cache do Docker)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p /app/logs \
    /app/data \
    /app/mlruns \
    /app/optuna_storage \
    && chown -R suna:suna /app

# Configurar permissões
RUN chmod +x suna_alsham_bootstrap.py

# Mudar para usuário não-root
USER suna

# Expor porta (Railway define automaticamente)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5 )" || exit 1

# Comando padrão
CMD ["python", "suna_alsham_bootstrap.py"]
