# 🚀 SUNA-ALSHAM Multi-Agent Network - Guia de Deploy

## 🎯 Visão Geral do Deploy

Este guia fornece instruções completas para deploy do sistema SUNA-ALSHAM Multi-Agent Network em ambiente de produção, seguindo as melhores práticas de **microserviços** e **escalabilidade**.

## 🏗️ Arquitetura de Deploy

### Estratégia de Microserviços

Seguindo a **arquitetura de microserviços para sistemas multi-agente**, cada componente principal deve ser deployado como um serviço independente:

```
┌─────────────────────────────────────────────────────────────┐
│                    SUNA-ALSHAM Network                      │
├─────────────────────────────────────────────────────────────┤
│  🎼 Network Orchestrator (FastAPI)                         │
│  📡 Message Bus Service (Redis/RabbitMQ)                   │
│  🤖 Agent Services (FastAPI cada)                          │
│  📊 Monitoring Dashboard (React)                           │
│  🗄️ Database Service (PostgreSQL)                          │
│  🔒 Security Service (FastAPI)                             │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Pré-requisitos

### Ambiente de Produção
- **Python 3.11+**
- **Redis 6.0+** (para cache e message bus)
- **PostgreSQL 13+** (para persistência)
- **Docker & Docker Compose** (recomendado)
- **Kubernetes** (para orquestração avançada)

### Variáveis de Ambiente
```bash
# IA e APIs
OPENAI_API_KEY=sk-your-openai-key
OPENAI_API_BASE=https://api.openai.com/v1

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/suna_alsham
REDIS_URL=redis://localhost:6379

# Segurança
SECRET_KEY=your-super-secret-key
JWT_SECRET=your-jwt-secret

# Configurações de Produção
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Monitoramento
SENTRY_DSN=your-sentry-dsn
PROMETHEUS_PORT=9090
```

## 🐳 Deploy com Docker

### 1. Dockerfile para Network Orchestrator
```dockerfile
# Dockerfile.orchestrator
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Expor porta
EXPOSE 8001

# Comando de inicialização
CMD ["python", "-m", "uvicorn", "network_orchestrator:app", "--host", "0.0.0.0", "--port", "8001"]
```

### 2. Docker Compose para Ambiente Completo
```yaml
# docker-compose.yml
version: '3.8'

services:
  # Redis para cache e message bus
  redis:
    image: redis:6.2-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  # PostgreSQL para persistência
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: suna_alsham
      POSTGRES_USER: suna_user
      POSTGRES_PASSWORD: suna_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # Network Orchestrator
  orchestrator:
    build:
      context: .
      dockerfile: Dockerfile.orchestrator
    ports:
      - "8001:8001"
    environment:
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=postgresql://suna_user:suna_password@postgres:5432/suna_alsham
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - redis
      - postgres
    restart: unless-stopped

  # Agente de Otimização
  optimizer-agent:
    build:
      context: .
      dockerfile: Dockerfile.agent
    environment:
      - AGENT_TYPE=optimizer
      - ORCHESTRATOR_URL=http://orchestrator:8001
      - REDIS_URL=redis://redis:6379
    depends_on:
      - orchestrator
      - redis
    restart: unless-stopped
    deploy:
      replicas: 2

  # Agente de Segurança
  security-agent:
    build:
      context: .
      dockerfile: Dockerfile.agent
    environment:
      - AGENT_TYPE=security
      - ORCHESTRATOR_URL=http://orchestrator:8001
      - REDIS_URL=redis://redis:6379
    depends_on:
      - orchestrator
      - redis
    restart: unless-stopped

  # Agente de Dados
  data-agent:
    build:
      context: .
      dockerfile: Dockerfile.agent
    environment:
      - AGENT_TYPE=data
      - ORCHESTRATOR_URL=http://orchestrator:8001
      - REDIS_URL=redis://redis:6379
    depends_on:
      - orchestrator
      - redis
    restart: unless-stopped
    deploy:
      replicas: 3

  # Dashboard de Monitoramento
  dashboard:
    build:
      context: ./dashboard
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8001
    depends_on:
      - orchestrator

  # Prometheus para métricas
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  # Grafana para visualização
  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  redis_data:
  postgres_data:
  prometheus_data:
  grafana_data:
```

### 3. Dockerfile para Agentes
```dockerfile
# Dockerfile.agent
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Script de inicialização
COPY start_agent.py .

# Comando de inicialização
CMD ["python", "start_agent.py"]
```

### 4. Script de Inicialização de Agentes
```python
# start_agent.py
import os
import asyncio
import logging
from typing import Dict, Any

from multi_agent_network import MultiAgentNetwork
from specialized_agents import (
    OptimizationAgent, SecurityAgent, LearningAgent, 
    DataAgent, MonitoringAgent
)

logger = logging.getLogger(__name__)

AGENT_CLASSES = {
    "optimizer": OptimizationAgent,
    "security": SecurityAgent,
    "learning": LearningAgent,
    "data": DataAgent,
    "monitor": MonitoringAgent
}

async def start_agent():
    """Inicia agente baseado na variável de ambiente"""
    agent_type = os.getenv("AGENT_TYPE", "data")
    agent_id = f"{agent_type}_{os.getenv('HOSTNAME', 'unknown')}"
    
    # Conectar ao message bus
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Criar rede local (conecta ao message bus distribuído)
    network = MultiAgentNetwork(redis_url=redis_url)
    
    # Criar agente
    agent_class = AGENT_CLASSES.get(agent_type, DataAgent)
    agent = agent_class(agent_id, network.message_bus)
    
    # Adicionar à rede
    network.add_agent(agent)
    
    # Iniciar rede
    network.start()
    
    logger.info(f"🤖 Agente {agent_id} iniciado e conectado à rede")
    
    # Manter rodando
    try:
        while True:
            await asyncio.sleep(10)
            logger.info(f"💓 Agente {agent_id} ativo")
    except KeyboardInterrupt:
        logger.info(f"🛑 Parando agente {agent_id}")
        network.stop()

if __name__ == "__main__":
    asyncio.run(start_agent())
```

## ☸️ Deploy com Kubernetes

### 1. Namespace
```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: suna-alsham
```

### 2. ConfigMap
```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: suna-config
  namespace: suna-alsham
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
  REDIS_URL: "redis://redis-service:6379"
  DATABASE_URL: "postgresql://suna_user:suna_password@postgres-service:5432/suna_alsham"
```

### 3. Secrets
```yaml
# secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: suna-secrets
  namespace: suna-alsham
type: Opaque
data:
  OPENAI_API_KEY: <base64-encoded-key>
  SECRET_KEY: <base64-encoded-secret>
  JWT_SECRET: <base64-encoded-jwt-secret>
```

### 4. Redis Deployment
```yaml
# redis-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: suna-alsham
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:6.2-alpine
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: redis-storage
          mountPath: /data
      volumes:
      - name: redis-storage
        persistentVolumeClaim:
          claimName: redis-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
  namespace: suna-alsham
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
```

### 5. Orchestrator Deployment
```yaml
# orchestrator-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orchestrator
  namespace: suna-alsham
spec:
  replicas: 2
  selector:
    matchLabels:
      app: orchestrator
  template:
    metadata:
      labels:
        app: orchestrator
    spec:
      containers:
      - name: orchestrator
        image: suna-alsham/orchestrator:latest
        ports:
        - containerPort: 8001
        envFrom:
        - configMapRef:
            name: suna-config
        - secretRef:
            name: suna-secrets
        livenessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: orchestrator-service
  namespace: suna-alsham
spec:
  selector:
    app: orchestrator
  ports:
  - port: 8001
    targetPort: 8001
  type: LoadBalancer
```

### 6. Agent Deployments
```yaml
# agents-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: optimizer-agents
  namespace: suna-alsham
spec:
  replicas: 3
  selector:
    matchLabels:
      app: optimizer-agent
  template:
    metadata:
      labels:
        app: optimizer-agent
    spec:
      containers:
      - name: optimizer-agent
        image: suna-alsham/agent:latest
        env:
        - name: AGENT_TYPE
          value: "optimizer"
        envFrom:
        - configMapRef:
            name: suna-config
        - secretRef:
            name: suna-secrets
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-agents
  namespace: suna-alsham
spec:
  replicas: 5
  selector:
    matchLabels:
      app: data-agent
  template:
    metadata:
      labels:
        app: data-agent
    spec:
      containers:
      - name: data-agent
        image: suna-alsham/agent:latest
        env:
        - name: AGENT_TYPE
          value: "data"
        envFrom:
        - configMapRef:
            name: suna-config
        - secretRef:
            name: suna-secrets
```

## 🌐 Deploy no Railway

### 1. Preparação para Railway
```json
// railway.json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile.railway"
  },
  "deploy": {
    "startCommand": "python -m uvicorn network_orchestrator:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 2. Dockerfile para Railway
```dockerfile
# Dockerfile.railway
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Comando de inicialização
CMD python -m uvicorn network_orchestrator:app --host 0.0.0.0 --port $PORT
```

### 3. Requirements para Produção
```txt
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
openai==1.97.0
redis==6.2.0
psycopg2-binary==2.9.9
sqlalchemy==2.0.23
alembic==1.13.1
pydantic==2.11.7
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
prometheus-client==0.19.0
sentry-sdk[fastapi]==1.38.0
structlog==23.2.0
networkx==3.5
numpy==1.24.3
psutil==7.0.0
pytest==8.4.1
pytest-asyncio==0.21.1
```

## 📊 Monitoramento e Observabilidade

### 1. Prometheus Configuration
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'suna-orchestrator'
    static_configs:
      - targets: ['orchestrator:8001']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'suna-agents'
    static_configs:
      - targets: ['optimizer-agent:8002', 'data-agent:8003']
    metrics_path: '/metrics'
    scrape_interval: 10s
```

### 2. Grafana Dashboard
```json
{
  "dashboard": {
    "title": "SUNA-ALSHAM Multi-Agent Network",
    "panels": [
      {
        "title": "Active Agents",
        "type": "stat",
        "targets": [
          {
            "expr": "suna_active_agents_total"
          }
        ]
      },
      {
        "title": "Message Throughput",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(suna_messages_processed_total[5m])"
          }
        ]
      },
      {
        "title": "Task Completion Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(suna_tasks_completed_total[5m])"
          }
        ]
      }
    ]
  }
}
```

### 3. Logging Configuration
```python
# logging_config.py
import structlog
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(colors=False),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "suna_alsham.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "json",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "suna_alsham": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

## 🔒 Segurança em Produção

### 1. Configurações de Segurança
```python
# security_config.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

def configure_security(app: FastAPI):
    # HTTPS redirect
    app.add_middleware(HTTPSRedirectMiddleware)
    
    # Trusted hosts
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://yourdomain.com"],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
```

### 2. Autenticação JWT
```python
# auth.py
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

## 🚀 Scripts de Deploy

### 1. Script de Deploy Completo
```bash
#!/bin/bash
# deploy.sh

set -e

echo "🚀 Iniciando deploy do SUNA-ALSHAM Multi-Agent Network..."

# Verificar variáveis de ambiente
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY não definida"
    exit 1
fi

# Build das imagens
echo "🔨 Building Docker images..."
docker build -t suna-alsham/orchestrator:latest -f Dockerfile.orchestrator .
docker build -t suna-alsham/agent:latest -f Dockerfile.agent .

# Deploy com Docker Compose
echo "🐳 Deploying with Docker Compose..."
docker-compose down
docker-compose up -d

# Aguardar serviços
echo "⏳ Aguardando serviços iniciarem..."
sleep 30

# Verificar saúde
echo "🏥 Verificando saúde dos serviços..."
curl -f http://localhost:8001/health || exit 1

# Executar testes
echo "🧪 Executando testes de integração..."
python -m pytest tests/integration/ -v

echo "✅ Deploy concluído com sucesso!"
echo "🌐 Orchestrator: http://localhost:8001"
echo "📊 Dashboard: http://localhost:3000"
echo "📈 Grafana: http://localhost:3001"
```

### 2. Script de Monitoramento
```bash
#!/bin/bash
# monitor.sh

echo "📊 Status do SUNA-ALSHAM Multi-Agent Network"
echo "============================================"

# Status dos containers
echo "🐳 Docker Containers:"
docker-compose ps

# Status da API
echo -e "\n🌐 API Health:"
curl -s http://localhost:8001/health | jq .

# Métricas da rede
echo -e "\n📈 Network Metrics:"
curl -s http://localhost:8001/network/status | jq .network_metrics

# Agentes ativos
echo -e "\n🤖 Active Agents:"
curl -s http://localhost:8001/agents | jq 'keys | length'

# Uso de recursos
echo -e "\n💻 Resource Usage:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

## 📋 Checklist de Deploy

### Pré-Deploy
- [ ] Variáveis de ambiente configuradas
- [ ] Secrets configurados
- [ ] Database migrations executadas
- [ ] Testes passando
- [ ] Monitoramento configurado

### Deploy
- [ ] Build das imagens Docker
- [ ] Deploy dos serviços
- [ ] Verificação de saúde
- [ ] Testes de integração
- [ ] Configuração de DNS

### Pós-Deploy
- [ ] Monitoramento ativo
- [ ] Logs sendo coletados
- [ ] Alertas configurados
- [ ] Backup configurado
- [ ] Documentação atualizada

## 🆘 Troubleshooting

### Problemas Comuns

#### 1. Agentes não se conectam
```bash
# Verificar Redis
docker logs redis

# Verificar conectividade
telnet redis-host 6379

# Verificar logs dos agentes
docker logs optimizer-agent
```

#### 2. Performance baixa
```bash
# Verificar recursos
docker stats

# Verificar métricas
curl http://localhost:8001/metrics

# Verificar logs de performance
grep "performance" /var/log/suna_alsham.log
```

#### 3. Falhas de IA
```bash
# Verificar API key
echo $OPENAI_API_KEY

# Verificar cache
redis-cli info

# Verificar logs de IA
grep "openai" /var/log/suna_alsham.log
```

---

## 🎉 Conclusão

Este guia fornece uma base sólida para deploy do sistema SUNA-ALSHAM Multi-Agent Network em produção. A arquitetura de microserviços garante escalabilidade e robustez, enquanto as ferramentas de monitoramento proporcionam visibilidade completa do sistema.

**🚀 Seu sistema multi-agente está pronto para produção!**

