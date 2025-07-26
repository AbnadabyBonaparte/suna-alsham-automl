FROM python:3.11-slim-bullseye

# Criar usuário
RUN groupadd --gid 1000 suna && \
    useradd --uid 1000 --gid suna --shell /bin/bash --create-home suna

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl wget git build-essential gcc g++ \
    libopenblas-dev liblapack-dev gfortran \
    libpq-dev postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Diretório de trabalho
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install psutil redis aiohttp autopep8 uvicorn

# Copiar código
COPY . .

# Criar diretórios necessários
RUN mkdir -p /app/logs /app/data /app/mlruns /app/optuna_storage && \
    chown -R suna:suna /app

# Mudar para usuário suna
USER suna

# Expor porta
EXPOSE 8080

# Executar o main.py que usa uvicorn
CMD ["python", "-u", "main.py"]
