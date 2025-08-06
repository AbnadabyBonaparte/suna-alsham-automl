# Forçando a invalidação do cache de build - v1
# ===== FASE 1: Builder =====
FROM python:3.11-slim-bullseye AS builder

ARG CACHE_BUSTER

# Define variáveis de ambiente para otimizar o Python no Docker
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Instala dependências do sistema necessárias para gitpython e docker
RUN apt-get update && apt-get install -y \
    git \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências de produção
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --upgrade gitpython docker

# Copia todo o resto do código da aplicação
COPY . .

# ===== FASE 2: Final =====
FROM python:3.11-slim-bullseye

# Instala apenas as dependências do sistema necessárias para runtime
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Define o mesmo diretório de trabalho
WORKDIR /app

# Copia apenas o código da aplicação e as dependências já instaladas da fase 'builder'
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Expõe a porta padrão usada pelo app (8000)
EXPOSE 8000

# Comando de inicialização robusto (pode ser alterado para gunicorn se desejar)
CMD ["python", "start.py"]
