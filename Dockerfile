# ===== FASE 1: Builder =====
# Usamos uma imagem base leve do Python para construir nossas dependências.
FROM python:3.11-slim-bullseye AS builder

# Define variáveis de ambiente para otimizar o Python no Docker
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências de produção
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do código da aplicação
COPY . .


# ===== FASE 2: Final =====
# Começamos de novo com uma imagem limpa para criar o container final e leve.
FROM python:3.11-slim-bullseye

# Define o mesmo diretório de trabalho
WORKDIR /app

# Copia apenas o código da aplicação e as dependências já instaladas da fase 'builder'
# Isso resulta em uma imagem final menor e mais segura, sem ferramentas de build.
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Expõe a porta que nossa aplicação irá usar (o Railway detecta isso)
EXPOSE 8080

# O comando para iniciar nosso sistema quando o container rodar.
# Ele executa o nosso ponto de entrada principal, start.py.
CMD ["python", "start.py"]
