#!/bin/bash
# Script para adicionar novos agentes ao SUNA-ALSHAM
# Uso: ./add_agent.sh nome_do_agente categoria

AGENT_NAME=$1
CATEGORY=${2:-"specialized"}  # categoria padrão

if [ -z "$AGENT_NAME" ]; then
    echo "❌ Erro: Nome do agente é obrigatório"
    echo "📖 Uso: ./add_agent.sh nome_do_agente [categoria]"
    echo "📂 Categorias: specialized, ai_powered, core_v3, system, service, meta_cognitive"
    exit 1
fi

echo "🚀 Criando agente: $AGENT_NAME"
echo "📂 Categoria: $CATEGORY"

# 1. Criar arquivo do agente
cat > "suna_alsham/agents/${AGENT_NAME}.py" << EOF
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List
from multi_agent_network import BaseNetworkAgent, AgentType, MessageType, Priority

logger = logging.getLogger(__name__)

class ${AGENT_NAME^}Agent(BaseNetworkAgent):
    def __init__(self):
        super().__init__(
            agent_id="${AGENT_NAME}",
            agent_type=AgentType.SPECIALIZED,
            capabilities=[]
        )
        self.status = "active"
        logger.info(f"✅ {self.agent_id} inicializado")
    
    async def handle_message(self, message):
        try:
            logger.info(f"📩 {self.agent_id} processando mensagem {message.id} de {message.sender_id}")
            
            # TODO: Implementar lógica específica do agente aqui
            
            # Responder heartbeat
            if message.message_type == MessageType.HEARTBEAT:
                logger.info(f"💓 {self.agent_id} recebeu heartbeat de {message.sender_id}")
                return
            
            # Processar outras mensagens
            await self._process_specific_message(message)
            
        except Exception as e:
            logger.error(f"❌ Erro em {self.agent_id}: {e}")
    
    async def _process_specific_message(self, message):
        # TODO: Implementar processamento específico
        logger.info(f"🔄 {self.agent_id} processou mensagem: {message.content}")

def create_${AGENT_NAME}_agent():
    """Factory function para criar o agente"""
    try:
        agent = ${AGENT_NAME^}Agent()
        logger.info(f"✅ Agente {agent.agent_id} criado com sucesso")
        return [agent]
    except Exception as e:
        logger.error(f"❌ Erro criando agente ${AGENT_NAME}: {e}")
        return []
EOF

echo "✅ 1. Arquivo do agente criado: suna_alsham/agents/${AGENT_NAME}.py"

# 2. Adicionar import no main
IMPORT_LINE="try:\n    from ${AGENT_NAME} import create_${AGENT_NAME}_agent\nexcept ImportError:\n    create_${AGENT_NAME}_agent = None"

# Encontrar linha onde adicionar
LINE_NUM=$(grep -n "create_performance_monitor_agent = None" main_complete_system_v2.py | cut -d: -f1)
if [ ! -z "$LINE_NUM" ]; then
    sed -i "${LINE_NUM}a\\${IMPORT_LINE}" main_complete_system_v2.py
    echo "✅ 2. Import adicionado no main_complete_system_v2.py"
else
    echo "⚠️ 2. Adicione manualmente o import no main_complete_system_v2.py"
fi

echo "🎯 Agente $AGENT_NAME criado com sucesso!"
echo "📝 Próximos passos:"
echo "   1. Edite suna_alsham/agents/${AGENT_NAME}.py"
echo "   2. Implemente a lógica em _process_specific_message()"
echo "   3. Adicione na lista de módulos em verificar_arquivos()"
echo "   4. Registre na inicialização do sistema"
echo "   5. Teste antes de fazer deploy!"
