import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from suna_alsham_core.multi_agent_network import BaseNetworkAgent, AgentMessage, ...

logger = logging.getLogger(__name__)

class CoreAgentV3(BaseNetworkAgent):
    """
    Agente Core v3 - Processamento central e coordenação de tarefas críticas
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.CORE, message_bus)
        
        # Capacidades avançadas
        self.add_capability(AgentCapability(
            name="core_processing",
            description="Processamento central de tarefas críticas",
            input_types=["task_request", "data_processing"],
            output_types=["processed_result", "status_update"],
            processing_time_ms=10.0,
            accuracy_score=0.95,
            resource_cost=0.3
        ))
        
        self.add_capability(AgentCapability(
            name="task_coordination",
            description="Coordenação entre agentes do sistema",
            input_types=["coordination_request"],
            output_types=["coordination_response"],
            processing_time_ms=5.0,
            accuracy_score=0.98,
            resource_cost=0.2
        ))
        
        self.processing_queue = []
        self.active_tasks = {}
        logger.info(f"✅ CoreAgent {self.agent_id} inicializado com processamento avançado")

    async def _handle_request(self, message: AgentMessage):
        """Processamento especializado para agentes Core"""
        try:
            request_type = message.content.get('request_type', 'unknown')
            
            if request_type == 'core_processing':
                result = await self._process_core_task(message.content)
            elif request_type == 'coordination':
                result = await self._coordinate_task(message.content)
            else:
                result = await self._default_processing(message.content)
            
            # Resposta especializada
            response = AgentMessage(
                id=f"resp_{message.id}",
                sender_id=self.agent_id,
                recipient_id=message.sender_id,
                message_type=MessageType.RESPONSE,
                priority=message.priority,
                content={
                    "status": "completed",
                    "result": result,
                    "processing_time_ms": self.performance_metrics['average_response_time'],
                    "capabilities_used": [cap.name for cap in self.capabilities]
                },
                timestamp=datetime.now(),
                correlation_id=message.id
            )
            
            await self.message_bus.publish(response)
            self.performance_metrics['tasks_completed'] += 1
            
        except Exception as e:
            logger.error(f"❌ Erro processando request em {self.agent_id}: {e}")

    async def _process_core_task(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Processamento específico de tarefas centrais"""
        task_data = content.get('task_data', {})
        
        # Simulação de processamento avançado
        processed_result = {
            "original_data": task_data,
            "processed_by": self.agent_id,
            "processing_method": "core_v3_advanced",
            "confidence_score": 0.95,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"🔧 {self.agent_id} processou tarefa core: {task_data.get('task_id', 'unknown')}")
        return processed_result

    async def _coordinate_task(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Coordenação entre agentes"""
        coordination_type = content.get('coordination_type', 'general')
        target_agents = content.get('target_agents', [])
        
        coordination_result = {
            "coordination_id": f"coord_{datetime.now().timestamp()}",
            "type": coordination_type,
            "coordinated_agents": target_agents,
            "coordinator": self.agent_id,
            "status": "coordinated"
        }
        
        logger.info(f"🎯 {self.agent_id} coordenou {len(target_agents)} agentes")
        return coordination_result

    async def _default_processing(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Processamento padrão para requisições não específicas"""
        return {
            "processed": True,
            "processor": self.agent_id,
            "method": "default_core_processing"
        }


class GuardAgentV3(BaseNetworkAgent):
    """
    Agente Guard v3 - Segurança, validação e proteção do sistema
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.GUARD, message_bus)
        
        # Capacidades de segurança
        self.add_capability(AgentCapability(
            name="security_validation",
            description="Validação de segurança de mensagens e operações",
            input_types=["message_validation", "security_check"],
            output_types=["validation_result", "security_report"],
            processing_time_ms=3.0,
            accuracy_score=0.99,
            resource_cost=0.1
        ))
        
        self.add_capability(AgentCapability(
            name="threat_detection",
            description="Detecção de ameaças e comportamentos suspeitos",
            input_types=["behavior_analysis", "anomaly_detection"],
            output_types=["threat_report", "security_alert"],
            processing_time_ms=8.0,
            accuracy_score=0.97,
            resource_cost=0.25
        ))
        
        self.security_rules = self._load_security_rules()
        self.threat_patterns = []
        self.blocked_agents = set()
        
        logger.info(f"🛡️ GuardAgent {self.agent_id} inicializado com segurança avançada")

    def _load_security_rules(self) -> List[Dict[str, Any]]:
        """Carrega regras de segurança do sistema"""
        return [
            {
                "rule_id": "MSG_RATE_LIMIT",
                "description": "Limite de mensagens por agente",
                "max_messages_per_minute": 100,
                "action": "throttle"
            },
            {
                "rule_id": "SUSPICIOUS_CONTENT",
                "description": "Detecção de conteúdo suspeito",
                "blocked_keywords": ["malicious", "exploit", "attack"],
                "action": "block"
            },
            {
                "rule_id": "AGENT_AUTHENTICATION",
                "description": "Verificação de autenticidade dos agentes",
                "required_fields": ["agent_id", "agent_type", "timestamp"],
                "action": "validate"
            }
        ]

    async def _handle_request(self, message: AgentMessage):
        """Processamento especializado para agentes Guard"""
        try:
            request_type = message.content.get('request_type', 'unknown')
            
            if request_type == 'security_check':
                result = await self._perform_security_check(message.content)
            elif request_type == 'validate_message':
                result = await self._validate_message(message.content)
            elif request_type == 'threat_analysis':
                result = await self._analyze_threats(message.content)
            else:
                result = await self._default_guard_processing(message.content)
            
            # Resposta de segurança
            response = AgentMessage(
                id=f"guard_resp_{message.id}",
                sender_id=self.agent_id,
                recipient_id=message.sender_id,
                message_type=MessageType.RESPONSE,
                priority=Priority.HIGH,  # Respostas de segurança têm alta prioridade
                content={
                    "security_status": "validated",
                    "guard_result": result,
                    "validated_by": self.agent_id,
                    "validation_timestamp": datetime.now().isoformat()
                },
                timestamp=datetime.now(),
                correlation_id=message.id
            )
            
            await self.message_bus.publish(response)
            
        except Exception as e:
            logger.error(f"❌ Erro em validação de segurança {self.agent_id}: {e}")

    async def _perform_security_check(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Executa verificação completa de segurança"""
        target = content.get('target', {})
        check_type = content.get('check_type', 'general')
        
        security_result = {
            "check_id": f"sec_{datetime.now().timestamp()}",
            "target": target,
            "check_type": check_type,
            "status": "passed",
            "threats_detected": 0,
            "rules_applied": len(self.security_rules),
            "validator": self.agent_id
        }
        
        # Aplicar regras de segurança
        for rule in self.security_rules:
            if self._apply_security_rule(rule, target):
                security_result["status"] = "flagged"
                security_result["threats_detected"] += 1
        
        logger.info(f"🛡️ {self.agent_id} executou security check: {security_result['status']}")
        return security_result

    def _apply_security_rule(self, rule: Dict[str, Any], target: Dict[str, Any]) -> bool:
        """Aplica uma regra de segurança específica"""
        # Implementação simplificada - na prática seria mais complexa
        if rule["rule_id"] == "SUSPICIOUS_CONTENT":
            content_str = str(target).lower()
            return any(keyword in content_str for keyword in rule["blocked_keywords"])
        return False

    async def _validate_message(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Valida estrutura e conteúdo de mensagens"""
        message_data = content.get('message_data', {})
        
        validation_result = {
            "validation_id": f"val_{datetime.now().timestamp()}",
            "message_valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Validações específicas
        required_fields = ["sender_id", "recipient_id", "message_type"]
        for field in required_fields:
            if field not in message_data:
                validation_result["errors"].append(f"Campo obrigatório ausente: {field}")
                validation_result["message_valid"] = False
        
        logger.info(f"✅ {self.agent_id} validou mensagem: {'válida' if validation_result['message_valid'] else 'inválida'}")
        return validation_result

    async def _analyze_threats(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Análise avançada de ameaças"""
        analysis_data = content.get('analysis_data', {})
        
        threat_analysis = {
            "analysis_id": f"threat_{datetime.now().timestamp()}",
            "threat_level": "low",
            "indicators": [],
            "recommendations": []
        }
        
        # Análise de padrões suspeitos (simplificada)
        if len(str(analysis_data)) > 10000:  # Mensagem muito grande
            threat_analysis["threat_level"] = "medium"
            threat_analysis["indicators"].append("Mensagem com tamanho suspeito")
            threat_analysis["recommendations"].append("Revisar conteúdo da mensagem")
        
        logger.info(f"🔍 {self.agent_id} analisou ameaças: nível {threat_analysis['threat_level']}")
        return threat_analysis

    async def _default_guard_processing(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Processamento padrão de segurança"""
        return {
            "guard_status": "processed",
            "security_level": "standard",
            "processed_by": self.agent_id
        }


class LearnAgentV3(BaseNetworkAgent):
    """
    Agente Learn v3 - Aprendizado adaptativo e otimização contínua
    """
    def __init__(self, agent_id: str, message_bus):
        super().__init__(agent_id, AgentType.LEARN, message_bus)
        
        # Capacidades de aprendizado
        self.add_capability(AgentCapability(
            name="pattern_recognition",
            description="Reconhecimento de padrões em dados e comportamentos",
            input_types=["pattern_data", "behavior_data"],
            output_types=["pattern_analysis", "learning_insight"],
            processing_time_ms=15.0,
            accuracy_score=0.92,
            resource_cost=0.4
        ))
        
        self.add_capability(AgentCapability(
            name="adaptive_optimization",
            description="Otimização adaptativa baseada em aprendizado",
            input_types=["optimization_request", "performance_data"],
            output_types=["optimization_suggestion", "improvement_plan"],
            processing_time_ms=20.0,
            accuracy_score=0.89,
            resource_cost=0.5
        ))
        
        self.learning_database = {}
        self.pattern_history = []
        self.optimization_suggestions = []
        
        logger.info(f"🧠 LearnAgent {self.agent_id} inicializado com aprendizado adaptativo")

    async def _handle_request(self, message: AgentMessage):
        """Processamento especializado para agentes Learn"""
        try:
            request_type = message.content.get('request_type', 'unknown')
            
            if request_type == 'pattern_analysis':
                result = await self._analyze_patterns(message.content)
            elif request_type == 'optimization_request':
                result = await self._generate_optimization(message.content)
            elif request_type == 'learning_update':
                result = await self._update_learning(message.content)
            else:
                result = await self._default_learning_processing(message.content)
            
            # Resposta de aprendizado
            response = AgentMessage(
                id=f"learn_resp_{message.id}",
                sender_id=self.agent_id,
                recipient_id=message.sender_id,
                message_type=MessageType.RESPONSE,
                priority=message.priority,
                content={
                    "learning_status": "processed",
                    "learning_result": result,
                    "patterns_identified": len(self.pattern_history),
                    "optimizations_available": len(self.optimization_suggestions),
                    "learned_by": self.agent_id
                },
                timestamp=datetime.now(),
                correlation_id=message.id
            )
            
            await self.message_bus.publish(response)
            
        except Exception as e:
            logger.error(f"❌ Erro no aprendizado {self.agent_id}: {e}")

    async def _analyze_patterns(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Análise avançada de padrões"""
        data = content.get('pattern_data', {})
        
        pattern_analysis = {
            "analysis_id": f"pattern_{datetime.now().timestamp()}",
            "patterns_found": [],
            "confidence_scores": {},
            "learning_insights": []
        }
        
        # Simulação de análise de padrões
        if isinstance(data, dict) and data:
            keys = list(data.keys())
            if len(keys) > 3:
                pattern_analysis["patterns_found"].append("Estrutura complexa detectada")
                pattern_analysis["confidence_scores"]["complexity"] = 0.85
            
            if any("error" in str(v).lower() for v in data.values()):
                pattern_analysis["patterns_found"].append("Padrão de erro identificado")
                pattern_analysis["confidence_scores"]["error_pattern"] = 0.92
                pattern_analysis["learning_insights"].append("Implementar tratamento preventivo de erros")
        
        # Armazenar padrão no histórico
        self.pattern_history.append({
            "timestamp": datetime.now(),
            "pattern": pattern_analysis,
            "data_source": content.get('source', 'unknown')
        })
        
        logger.info(f"🔍 {self.agent_id} identificou {len(pattern_analysis['patterns_found'])} padrões")
        return pattern_analysis

    async def _generate_optimization(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Gera sugestões de otimização baseadas em aprendizado"""
        target_system = content.get('target_system', 'general')
        performance_data = content.get('performance_data', {})
        
        optimization = {
            "optimization_id": f"opt_{datetime.now().timestamp()}",
            "target": target_system,
            "suggestions": [],
            "expected_improvements": {},
            "priority": "medium"
        }
        
        # Análise de performance e geração de sugestões
        if performance_data:
            avg_response_time = performance_data.get('average_response_time', 0)
            if avg_response_time > 100:  # ms
                optimization["suggestions"].append("Implementar cache para reduzir tempo de resposta")
                optimization["expected_improvements"]["response_time"] = "Redução de 30-50%"
                optimization["priority"] = "high"
            
            success_rate = performance_data.get('success_rate', 1.0)
            if success_rate < 0.95:
                optimization["suggestions"].append("Implementar retry automático para melhorar confiabilidade")
                optimization["expected_improvements"]["reliability"] = "Aumento de 5-10%"
        
        # Armazenar otimização
        self.optimization_suggestions.append(optimization)
        
        logger.info(f"⚡ {self.agent_id} gerou {len(optimization['suggestions'])} otimizações")
        return optimization

    async def _update_learning(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza base de conhecimento do agente"""
        learning_data = content.get('learning_data', {})
        learning_type = content.get('learning_type', 'general')
        
        update_result = {
            "update_id": f"update_{datetime.now().timestamp()}",
            "learning_type": learning_type,
            "data_points_added": 0,
            "knowledge_base_size": len(self.learning_database)
        }
        
        # Atualizar base de conhecimento
        if learning_type not in self.learning_database:
            self.learning_database[learning_type] = []
        
        if isinstance(learning_data, list):
            self.learning_database[learning_type].extend(learning_data)
            update_result["data_points_added"] = len(learning_data)
        else:
            self.learning_database[learning_type].append(learning_data)
            update_result["data_points_added"] = 1
        
        update_result["knowledge_base_size"] = len(self.learning_database)
        
        logger.info(f"📚 {self.agent_id} atualizou base de conhecimento: +{update_result['data_points_added']} pontos")
        return update_result

    async def _default_learning_processing(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Processamento padrão de aprendizado"""
        return {
            "learning_status": "processed",
            "method": "default_learning",
            "processed_by": self.agent_id
        }


def create_core_agents_v3(message_bus, num_instances=1) -> List[BaseNetworkAgent]:
    """
    Cria EXATAMENTE 5 agentes core v3 especializados sem duplicações
    
    Args:
        message_bus: Sistema de mensagens para comunicação
        num_instances: Número de instâncias (ignorado para manter exatamente 5)
    
    Returns:
        List[BaseNetworkAgent]: Lista com exatamente 5 agentes core v3
    """
    agents = []
    
    try:
        logger.info("🎯 Criando EXATAMENTE 5 agentes core v3 ESPECIALIZADOS...")
        
        # Validação do message_bus
        if not message_bus:
            logger.error("❌ MessageBus não fornecido - não é possível criar agentes")
            return []
        
        # Lista FIXA de 5 agentes especializados
        agents_config = [
            {
                "id": "core_v3_001",
                "class": CoreAgentV3,
                "description": "Agente Core principal - Processamento central"
            },
            {
                "id": "guard_v3_001", 
                "class": GuardAgentV3,
                "description": "Agente Guard primário - Segurança principal"
            },
            {
                "id": "learn_v3_001",
                "class": LearnAgentV3,
                "description": "Agente Learn principal - Aprendizado adaptativo"
            },
            {
                "id": "core_v3_002",
                "class": CoreAgentV3,
                "description": "Agente Core secundário - Backup e coordenação"
            },
            {
                "id": "guard_v3_002",
                "class": GuardAgentV3,
                "description": "Agente Guard secundário - Segurança redundante"
            }
        ]
        
        # Verificar agentes existentes para evitar duplicação
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
            logger.info(f"🔍 Agentes existentes detectados: {len(existing_agents)}")
        
        # Criar agentes apenas se não existirem
        for config in agents_config:
            agent_id = config["id"]
            
            if agent_id not in existing_agents:
                try:
                    # Criar instância do agente
                    agent = config["class"](agent_id, message_bus)
                    agents.append(agent)
                    
                    # Validar criação
                    if not hasattr(agent, 'agent_id') or not hasattr(agent, 'status'):
                        logger.error(f"❌ Agente {agent_id} criado incorretamente")
                        continue
                    
                    # Log de sucesso
                    logger.info(f"✅ {config['description']} criado com sucesso")
                    logger.info(f"   ├── ID: {agent.agent_id}")
                    logger.info(f"   ├── Tipo: {agent.agent_type}")
                    logger.info(f"   ├── Status: {agent.status}")
                    logger.info(f"   └── Capacidades: {len(agent.capabilities)}")
                    
                    existing_agents.add(agent_id)
                    
                except Exception as e:
                    logger.error(f"❌ Erro criando agente {agent_id}: {e}")
                    continue
            else:
                logger.warning(f"⚠️ Agente {agent_id} já existe - pulando para evitar duplicação")
        
        # Validação final
        if len(agents) == 5:
            logger.info("🎉 SUCESSO: Exatamente 5 agentes core v3 criados!")
            logger.info(f"📋 Lista de agentes: {[agent.agent_id for agent in agents]}")
            
            # Relatório de capacidades
            total_capabilities = sum(len(agent.capabilities) for agent in agents)
            logger.info(f"⚡ Total de capacidades do sistema: {total_capabilities}")
            
        else:
            logger.error(f"❌ ERRO: Criados {len(agents)} agentes, esperado exatamente 5")
            logger.error("🔧 Verificar se todos os módulos estão disponíveis e MessageBus está funcional")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando agentes core v3: {e}")
        logger.error("🚨 Sistema pode não funcionar corretamente sem agentes core")
        return []


# Função de teste para validação
def test_core_agents_v3():
    """Função de teste para validar criação dos agentes"""
    logger.info("🧪 Iniciando teste dos agentes core v3...")
    
    # Mock do message_bus para teste
    class MockMessageBus:
        def __init__(self):
            self.subscribers = {}
        
        def register_agent(self, agent_id, agent):
            self.subscribers[agent_id] = agent
    
    mock_bus = MockMessageBus()
    agents = create_core_agents_v3(mock_bus)
    
    if len(agents) == 5:
        logger.info("✅ Teste PASSOU: 5 agentes criados corretamente")
        for agent in agents:
            logger.info(f"   ✓ {agent.agent_id} - {agent.agent_type} - {len(agent.capabilities)} capacidades")
    else:
        logger.error(f"❌ Teste FALHOU: {len(agents)} agentes criados (esperado: 5)")
    
    return len(agents) == 5


if __name__ == "__main__":
    # Executar teste se rodado diretamente
    test_core_agents_v3()
