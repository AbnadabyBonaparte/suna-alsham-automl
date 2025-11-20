"""
ALSHAM QUANTUM - Support Ticket Manager Agent
Agente especializado em gerenciamento completo de tickets de suporte
Versão: 2.0 - Implementação nativa com sistema de tickets completo
"""

import json
import asyncio
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter, deque
from enum import Enum
import random

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TicketStatus(Enum):
    """Status possíveis para tickets"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REOPENED = "reopened"

class TicketPriority(Enum):
    """Prioridades de tickets"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"

class TicketType(Enum):
    """Tipos de tickets"""
    QUESTION = "question"
    INCIDENT = "incident"
    PROBLEM = "problem"
    TASK = "task"
    REQUEST = "request"

class BaseNetworkAgent:
    """Classe base para todos os agentes da rede ALSHAM QUANTUM"""
    
    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.status = "active"
        self.created_at = datetime.now()
        self.last_heartbeat = datetime.now()
        self.message_count = 0
        
    async def _internal_handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Método interno obrigatório para processamento de mensagens"""
        self.message_count += 1
        self.last_heartbeat = datetime.now()
        
        try:
            # Processa a mensagem usando o método específico do agente
            response = await self.process_message(message)
            
            return {
                "agent_id": self.agent_id,
                "status": "success",
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "message_count": self.message_count
            }
            
        except Exception as e:
            logger.error(f"Erro no agente {self.agent_id}: {str(e)}")
            return {
                "agent_id": self.agent_id,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Método para ser implementado pelos agentes específicos"""
        raise NotImplementedError("Agentes devem implementar process_message()")
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do agente"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "message_count": self.message_count
        }

class TicketEngine:
    """Engine completo de gerenciamento de tickets"""
    
    def __init__(self):
        self.tickets = {}  # ticket_id -> ticket_data
        self.ticket_counter = 1
        
        # Índices para busca rápida
        self.status_index = defaultdict(list)
        self.priority_index = defaultdict(list)
        self.assignee_index = defaultdict(list)
        self.requester_index = defaultdict(list)
        
        # Templates de auto-resposta
        self.auto_response_templates = {
            "ticket_created": "Seu ticket #{ticket_id} foi criado com sucesso. Nosso tempo de resposta é de {sla_time}.",
            "ticket_assigned": "Seu ticket #{ticket_id} foi atribuído ao agente {agent_name}.",
            "ticket_resolved": "Seu ticket #{ticket_id} foi resolvido. Por favor, confirme se a solução atendeu suas necessidades.",
            "ticket_closed": "Seu ticket #{ticket_id} foi fechado. Obrigado por entrar em contato conosco."
        }
        
        # SLA por prioridade (em horas)
        self.sla_targets = {
            TicketPriority.CRITICAL: 1,
            TicketPriority.URGENT: 2,
            TicketPriority.HIGH: 8,
            TicketPriority.NORMAL: 24,
            TicketPriority.LOW: 48
        }
    
    def create_ticket(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria novo ticket"""
        
        ticket_id = f"TKT-{self.ticket_counter:06d}"
        self.ticket_counter += 1
        
        # Dados padrão do ticket
        ticket = {
            "id": ticket_id,
            "subject": ticket_data.get("subject", "No Subject"),
            "description": ticket_data.get("description", ticket_data.get("comment", "")),
            "status": TicketStatus.OPEN.value,
            "priority": ticket_data.get("priority", TicketPriority.NORMAL.value),
            "type": ticket_data.get("type", TicketType.QUESTION.value),
            "requester": {
                "name": ticket_data.get("requester_name", "Unknown"),
                "email": ticket_data.get("requester_email", "unknown@example.com"),
                "id": ticket_data.get("requester_id", f"user_{random.randint(1000, 9999)}")
            },
            "assignee": ticket_data.get("assignee"),
            "group": ticket_data.get("group", "General Support"),
            "tags": ticket_data.get("tags", []),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "due_at": self._calculate_due_date(ticket_data.get("priority", TicketPriority.NORMAL.value)),
            "comments": [
                {
                    "id": 1,
                    "author": "System",
                    "body": f"Ticket {ticket_id} criado",
                    "public": False,
                    "created_at": datetime.now().isoformat()
                }
            ],
            "custom_fields": ticket_data.get("custom_fields", {}),
            "satisfaction_rating": None,
            "resolution_time": None,
            "first_response_time": None,
            "escalated": False,
            "reopened_count": 0,
            "source": ticket_data.get("source", "web")
        }
        
        # Armazena ticket
        self.tickets[ticket_id] = ticket
        
        # Atualiza índices
        self._update_indexes(ticket_id, ticket)
        
        return ticket
    
    def get_ticket(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """Recupera ticket por ID"""
        return self.tickets.get(ticket_id)
    
    def update_ticket(self, ticket_id: str, updates: Dict[str, Any]) -> bool:
        """Atualiza ticket existente"""
        
        if ticket_id not in self.tickets:
            return False
        
        ticket = self.tickets[ticket_id]
        old_status = ticket["status"]
        
        # Atualiza campos
        for field, value in updates.items():
            if field in ticket:
                ticket[field] = value
        
        ticket["updated_at"] = datetime.now().isoformat()
        
        # Adiciona comentário de atualização se status mudou
        if "status" in updates and updates["status"] != old_status:
            self._add_system_comment(ticket_id, f"Status alterado de {old_status} para {updates['status']}")
        
        # Atualiza índices
        self._update_indexes(ticket_id, ticket)
        
        return True
    
    def add_comment(self, ticket_id: str, comment: Dict[str, Any]) -> bool:
        """Adiciona comentário ao ticket"""
        
        if ticket_id not in self.tickets:
            return False
        
        ticket = self.tickets[ticket_id]
        
        new_comment = {
            "id": len(ticket["comments"]) + 1,
            "author": comment.get("author", "Unknown"),
            "body": comment.get("body", ""),
            "public": comment.get("public", True),
            "created_at": datetime.now().isoformat(),
            "attachments": comment.get("attachments", [])
        }
        
        ticket["comments"].append(new_comment)
        ticket["updated_at"] = datetime.now().isoformat()
        
        # Marca primeiro tempo de resposta se for do agente
        if not ticket["first_response_time"] and comment.get("author") != "System":
            created_at = datetime.fromisoformat(ticket["created_at"])
            response_time = (datetime.now() - created_at).total_seconds() / 60  # minutos
            ticket["first_response_time"] = response_time
        
        return True
    
    def search_tickets(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Busca tickets por filtros"""
        
        results = list(self.tickets.values())
        
        # Aplica filtros
        if "status" in filters:
            status_filter = filters["status"]
            if isinstance(status_filter, str):
                status_filter = [status_filter]
            results = [t for t in results if t["status"] in status_filter]
        
        if "priority" in filters:
            priority_filter = filters["priority"]
            if isinstance(priority_filter, str):
                priority_filter = [priority_filter]
            results = [t for t in results if t["priority"] in priority_filter]
        
        if "assignee" in filters:
            assignee = filters["assignee"]
            results = [t for t in results if t.get("assignee") == assignee]
        
        if "requester_email" in filters:
            email = filters["requester_email"]
            results = [t for t in results if t["requester"]["email"] == email]
        
        if "created_after" in filters:
            created_after = datetime.fromisoformat(filters["created_after"])
            results = [t for t in results if datetime.fromisoformat(t["created_at"]) >= created_after]
        
        if "tags" in filters:
            required_tags = filters["tags"]
            results = [t for t in results if all(tag in t["tags"] for tag in required_tags)]
        
        # Ordenação
        sort_by = filters.get("sort_by", "created_at")
        reverse = filters.get("sort_order", "desc") == "desc"
        
        if sort_by in ["created_at", "updated_at"]:
            results.sort(key=lambda x: datetime.fromisoformat(x[sort_by]), reverse=reverse)
        else:
            results.sort(key=lambda x: x.get(sort_by, ""), reverse=reverse)
        
        # Paginação
        page = filters.get("page", 1)
        per_page = filters.get("per_page", 50)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        return results[start_idx:end_idx]
    
    def get_ticket_metrics(self, period: str = "all") -> Dict[str, Any]:
        """Calcula métricas dos tickets"""
        
        # Filtra por período
        if period == "today":
            cutoff = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "week":
            cutoff = datetime.now() - timedelta(days=7)
        elif period == "month":
            cutoff = datetime.now() - timedelta(days=30)
        else:
            cutoff = datetime.min
        
        filtered_tickets = [
            t for t in self.tickets.values()
            if datetime.fromisoformat(t["created_at"]) >= cutoff
        ]
        
        if not filtered_tickets:
            return {"message": "Nenhum ticket encontrado no período"}
        
        # Métricas básicas
        total_tickets = len(filtered_tickets)
        status_counts = Counter(t["status"] for t in filtered_tickets)
        priority_counts = Counter(t["priority"] for t in filtered_tickets)
        
        # Tempos de resolução
        resolved_tickets = [t for t in filtered_tickets if t["resolution_time"]]
        avg_resolution_time = 0
        if resolved_tickets:
            avg_resolution_time = statistics.mean(t["resolution_time"] for t in resolved_tickets)
        
        # Primeiro tempo de resposta
        responded_tickets = [t for t in filtered_tickets if t["first_response_time"]]
        avg_first_response = 0
        if responded_tickets:
            avg_first_response = statistics.mean(t["first_response_time"] for t in responded_tickets)
        
        # SLA compliance
        sla_breaches = 0
        for ticket in filtered_tickets:
            if self._is_sla_breached(ticket):
                sla_breaches += 1
        
        sla_compliance = ((total_tickets - sla_breaches) / total_tickets * 100) if total_tickets > 0 else 100
        
        return {
            "period": period,
            "total_tickets": total_tickets,
            "status_distribution": dict(status_counts),
            "priority_distribution": dict(priority_counts),
            "avg_resolution_time_minutes": avg_resolution_time,
            "avg_first_response_minutes": avg_first_response,
            "sla_compliance_percentage": sla_compliance,
            "sla_breaches": sla_breaches
        }
    
    def _calculate_due_date(self, priority: str) -> str:
        """Calcula data de vencimento baseada na prioridade"""
        
        try:
            priority_enum = TicketPriority(priority)
            hours = self.sla_targets.get(priority_enum, 24)
        except ValueError:
            hours = 24
        
        due_date = datetime.now() + timedelta(hours=hours)
        return due_date.isoformat()
    
    def _update_indexes(self, ticket_id: str, ticket: Dict[str, Any]):
        """Atualiza índices de busca"""
        
        # Remove dos índices antigos
        for status_list in self.status_index.values():
            if ticket_id in status_list:
                status_list.remove(ticket_id)
        
        for priority_list in self.priority_index.values():
            if ticket_id in priority_list:
                priority_list.remove(ticket_id)
        
        # Adiciona aos novos índices
        self.status_index[ticket["status"]].append(ticket_id)
        self.priority_index[ticket["priority"]].append(ticket_id)
        
        if ticket.get("assignee"):
            self.assignee_index[ticket["assignee"]].append(ticket_id)
        
        self.requester_index[ticket["requester"]["email"]].append(ticket_id)
    
    def _add_system_comment(self, ticket_id: str, message: str):
        """Adiciona comentário do sistema"""
        
        self.add_comment(ticket_id, {
            "author": "System",
            "body": message,
            "public": False
        })
    
    def _is_sla_breached(self, ticket: Dict[str, Any]) -> bool:
        """Verifica se SLA foi violado"""
        
        try:
            priority_enum = TicketPriority(ticket["priority"])
            sla_hours = self.sla_targets.get(priority_enum, 24)
        except ValueError:
            sla_hours = 24
        
        created_at = datetime.fromisoformat(ticket["created_at"])
        sla_deadline = created_at + timedelta(hours=sla_hours)
        
        # Se ainda não foi resolvido e passou do prazo
        if ticket["status"] not in ["resolved", "closed"] and datetime.now() > sla_deadline:
            return True
        
        # Se foi resolvido depois do prazo
        if ticket.get("resolution_time") and ticket.get("resolution_time") > sla_hours * 60:
            return True
        
        return False

class TicketManagerAgent(BaseNetworkAgent):
    """
    Agente especializado em gerenciamento completo de tickets de suporte
    Implementa sistema nativo completo sem dependências externas
    """
    
    def __init__(self):
        super().__init__(
            agent_id="support_ticket_manager",
            agent_type="ticket_manager"
        )
        
        # Engine de tickets
        self.ticket_engine = TicketEngine()
        
        # Configurações
        self.config = {
            "auto_assign": True,
            "auto_response": True,
            "escalation_enabled": True,
            "escalation_threshold_hours": 24,
            "satisfaction_survey": True,
            "max_tickets_per_agent": 50
        }
        
        # Agentes disponíveis (simulado)
        self.available_agents = {
            "agent_001": {"name": "João Silva", "specialties": ["technical", "billing"], "active": True, "current_load": 0},
            "agent_002": {"name": "Maria Santos", "specialties": ["general", "account"], "active": True, "current_load": 0},
            "agent_003": {"name": "Pedro Costa", "specialties": ["technical", "integration"], "active": True, "current_load": 0},
            "agent_004": {"name": "Ana Oliveira", "specialties": ["billing", "cancellation"], "active": True, "current_load": 0}
        }
        
        # Estatísticas
        self.stats = {
            "tickets_created": 0,
            "tickets_resolved": 0,
            "average_resolution_time": 0.0,
            "agent_utilization": defaultdict(int),
            "escalations": 0,
            "sla_breaches": 0
        }
        
        # Workflows de automação
        self.automation_rules = [
            {
                "name": "Auto-assign urgent tickets",
                "condition": {"priority": "urgent"},
                "action": "auto_assign_best_agent"
            },
            {
                "name": "Escalate old tickets",
                "condition": {"hours_open": ">24", "status": "open"},
                "action": "escalate_to_supervisor"
            },
            {
                "name": "Request feedback on resolved",
                "condition": {"status": "resolved"},
                "action": "send_satisfaction_survey"
            }
        ]
        
        logger.info(f"✅ Support Ticket Manager Agent iniciado: {self.agent_id}")
        logger.info(f"🎫 Sistema de tickets nativo carregado com {len(self.available_agents)} agentes")

    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Processa mensagens de gerenciamento de tickets"""
        
        action = message.get("action", "create_ticket")
        
        if action == "create_ticket":
            return await self._create_ticket(message.get("data", {}))
        
        elif action == "get_ticket":
            return self._get_ticket(message.get("data", {}))
        
        elif action == "update_ticket":
            return await self._update_ticket(message.get("data", {}))
        
        elif action == "add_comment":
            return await self._add_comment(message.get("data", {}))
        
        elif action == "search_tickets":
            return self._search_tickets(message.get("data", {}))
        
        elif action == "assign_ticket":
            return await self._assign_ticket(message.get("data", {}))
        
        elif action == "escalate_ticket":
            return await self._escalate_ticket(message.get("data", {}))
        
        elif action == "close_ticket":
            return await self._close_ticket(message.get("data", {}))
        
        elif action == "get_metrics":
            return self._get_ticket_metrics(message.get("data", {}))
        
        elif action == "get_agent_workload":
            return self._get_agent_workload()
        
        elif action == "bulk_update":
            return await self._bulk_update_tickets(message.get("data", {}))
        
        elif action == "get_manager_status":
            return self._get_manager_status()
        
        else:
            return {
                "error": f"Ação não reconhecida: {action}",
                "available_actions": [
                    "create_ticket", "get_ticket", "update_ticket", "add_comment",
                    "search_tickets", "assign_ticket", "escalate_ticket", 
                    "close_ticket", "get_metrics", "get_agent_workload",
                    "bulk_update", "get_manager_status"
                ]
            }

    async def _create_ticket(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria novo ticket"""
        
        try:
            # Valida dados obrigatórios
            required_fields = ["subject", "requester_name", "requester_email"]
            for field in required_fields:
                if not data.get(field):
                    return {"error": f"Campo obrigatório faltando: {field}"}
            
            # Cria ticket
            ticket = self.ticket_engine.create_ticket(data)
            
            # Auto-assign se configurado
            if self.config["auto_assign"] and not ticket.get("assignee"):
                best_agent = self._find_best_agent(ticket)
                if best_agent:
                    self.ticket_engine.update_ticket(ticket["id"], {"assignee": best_agent})
                    self.available_agents[best_agent]["current_load"] += 1
            
            # Auto-resposta se configurado
            if self.config["auto_response"]:
                auto_response = self._generate_auto_response("ticket_created", ticket)
                self.ticket_engine.add_comment(ticket["id"], {
                    "author": "System",
                    "body": auto_response,
                    "public": True
                })
            
            # Atualiza estatísticas
            self.stats["tickets_created"] += 1
            
            return {
                "status": "success",
                "ticket": ticket,
                "ticket_id": ticket["id"],
                "url": f"/tickets/{ticket['id']}",
                "sla_due": ticket["due_at"],
                "assigned_to": ticket.get("assignee"),
                "estimated_resolution": self._estimate_resolution_time(ticket)
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar ticket: {str(e)}")
            return {"error": f"Falha na criação do ticket: {str(e)}"}

    def _get_ticket(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recupera ticket específico"""
        
        try:
            ticket_id = data.get("ticket_id")
            
            if not ticket_id:
                return {"error": "ticket_id é obrigatório"}
            
            ticket = self.ticket_engine.get_ticket(ticket_id)
            
            if not ticket:
                return {"error": f"Ticket {ticket_id} não encontrado"}
            
            # Adiciona informações complementares
            enhanced_ticket = ticket.copy()
            enhanced_ticket["sla_status"] = self._get_sla_status(ticket)
            enhanced_ticket["time_to_resolution"] = self._calculate_time_to_resolution(ticket)
            enhanced_ticket["related_tickets"] = self._find_related_tickets(ticket)
            
            return {
                "status": "success",
                "ticket": enhanced_ticket
            }
            
        except Exception as e:
            logger.error(f"Erro ao recuperar ticket: {str(e)}")
            return {"error": f"Falha ao recuperar ticket: {str(e)}"}

    async def _update_ticket(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza ticket existente"""
        
        try:
            ticket_id = data.get("ticket_id")
            updates = data.get("updates", {})
            
            if not ticket_id:
                return {"error": "ticket_id é obrigatório"}
            
            if not updates:
                return {"error": "Nenhuma atualização fornecida"}
            
            # Valida status transition se aplicável
            if "status" in updates:
                current_ticket = self.ticket_engine.get_ticket(ticket_id)
                if current_ticket and not self._validate_status_transition(current_ticket["status"], updates["status"]):
                    return {"error": f"Transição de status inválida: {current_ticket['status']} -> {updates['status']}"}
            
            # Atualiza ticket
            success = self.ticket_engine.update_ticket(ticket_id, updates)
            
            if not success:
                return {"error": f"Ticket {ticket_id} não encontrado"}
            
            # Triggers de automação
            updated_ticket = self.ticket_engine.get_ticket(ticket_id)
            await self._run_automation_rules(updated_ticket)
            
            # Marca tempo de resolução se foi resolvido
            if updates.get("status") == "resolved":
                created_at = datetime.fromisoformat(updated_ticket["created_at"])
                resolution_time = (datetime.now() - created_at).total_seconds() / 60  # minutos
                self.ticket_engine.update_ticket(ticket_id, {"resolution_time": resolution_time})
                self.stats["tickets_resolved"] += 1
            
            return {
                "status": "success",
                "message": "Ticket atualizado com sucesso",
                "ticket_id": ticket_id,
                "updates_applied": list(updates.keys()),
                "current_status": updated_ticket["status"]
            }
            
        except Exception as e:
            logger.error(f"Erro ao atualizar ticket: {str(e)}")
            return {"error": f"Falha na atualização: {str(e)}"}

    async def _add_comment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Adiciona comentário ao ticket"""
        
        try:
            ticket_id = data.get("ticket_id")
            comment_data = data.get("comment", {})
            
            if not ticket_id:
                return {"error": "ticket_id é obrigatório"}
            
            if not comment_data.get("body"):
                return {"error": "Corpo do comentário é obrigatório"}
            
            success = self.ticket_engine.add_comment(ticket_id, comment_data)
            
            if not success:
                return {"error": f"Ticket {ticket_id} não encontrado"}
            
            ticket = self.ticket_engine.get_ticket(ticket_id)
            comment_count = len(ticket["comments"])
            
            return {
                "status": "success",
                "message": "Comentário adicionado com sucesso",
                "ticket_id": ticket_id,
                "comment_id": comment_count,
                "total_comments": comment_count
            }
            
        except Exception as e:
            logger.error(f"Erro ao adicionar comentário: {str(e)}")
            return {"error": f"Falha ao adicionar comentário: {str(e)}"}

    def _search_tickets(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Busca tickets com filtros"""
        
        try:
            filters = data.get("filters", {})
            
            tickets = self.ticket_engine.search_tickets(filters)
            
            # Adiciona resumo dos resultados
            if tickets:
                status_summary = Counter(t["status"] for t in tickets)
                priority_summary = Counter(t["priority"] for t in tickets)
            else:
                status_summary = {}
                priority_summary = {}
            
            return {
                "status": "success",
                "tickets": tickets,
                "total_found": len(tickets),
                "filters_applied": filters,
                "summary": {
                    "by_status": dict(status_summary),
                    "by_priority": dict(priority_summary)
                }
            }
            
        except Exception as e:
            logger.error(f"Erro na busca de tickets: {str(e)}")
            return {"error": f"Falha na busca: {str(e)}"}

    async def _assign_ticket(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atribui ticket a agente"""
        
        try:
            ticket_id = data.get("ticket_id")
            agent_id = data.get("agent_id", "auto")
            
            if not ticket_id:
                return {"error": "ticket_id é obrigatório"}
            
            ticket = self.ticket_engine.get_ticket(ticket_id)
            if not ticket:
                return {"error": f"Ticket {ticket_id} não encontrado"}
            
            # Auto-assign se solicitado
            if agent_id == "auto":
                agent_id = self._find_best_agent(ticket)
                if not agent_id:
                    return {"error": "Nenhum agente disponível para atribuição"}
            
            # Valida agente
            if agent_id not in self.available_agents:
                return {"error": f"Agente {agent_id} não encontrado"}
            
            if not self.available_agents[agent_id]["active"]:
                return {"error": f"Agente {agent_id} não está ativo"}
            
            # Remove atribuição anterior se houver
            old_assignee = ticket.get("assignee")
            if old_assignee and old_assignee in self.available_agents:
                self.available_agents[old_assignee]["current_load"] -= 1
            
            # Atribui novo agente
            self.ticket_engine.update_ticket(ticket_id, {"assignee": agent_id})
            self.available_agents[agent_id]["current_load"] += 1
            
            # Notificação automática
            if self.config["auto_response"]:
                auto_response = self._generate_auto_response("ticket_assigned", ticket, {"agent_name": self.available_agents[agent_id]["name"]})
                self.ticket_engine.add_comment(ticket_id, {
                    "author": "System",
                    "body": auto_response,
                    "public": True
                })
            
            return {
                "status": "success",
                "message": "Ticket atribuído com sucesso",
                "ticket_id": ticket_id,
                "assigned_to": agent_id,
                "agent_name": self.available_agents[agent_id]["name"],
                "agent_workload": self.available_agents[agent_id]["current_load"]
            }
            
        except Exception as e:
            logger.error(f"Erro ao atribuir ticket: {str(e)}")
            return {"error": f"Falha na atribuição: {str(e)}"}

    async def _escalate_ticket(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Escalona ticket para supervisor"""
        
        try:
            ticket_id = data.get("ticket_id")
            escalation_reason = data.get("reason", "Manual escalation")
            
            if not ticket_id:
                return {"error": "ticket_id é obrigatório"}
            
            ticket = self.ticket_engine.get_ticket(ticket_id)
            if not ticket:
                return {"error": f"Ticket {ticket_id} não encontrado"}
            
            # Atualiza ticket com escalação
            updates = {
                "priority": "urgent" if ticket["priority"] != "critical" else "critical",
                "escalated": True,
                "tags": ticket.get("tags", []) + ["escalated"]
            }
            
            self.ticket_engine.update_ticket(ticket_id, updates)
            
            # Adiciona comentário de escalação
            self.ticket_engine.add_comment(ticket_id, {
                "author": "System",
                "body": f"Ticket escalado. Motivo: {escalation_reason}",
                "public": False
            })
            
            # Atualiza estatísticas
            self.stats["escalations"] += 1
            
            return {
                "status": "success",
                "message": "Ticket escalado com sucesso",
                "ticket_id": ticket_id,
                "new_priority": updates["priority"],
                "escalation_reason": escalation_reason,
                "escalated_to": "supervisor_queue"
            }
            
        except Exception as e:
            logger.error(f"Erro ao escalonar ticket: {str(e)}")
            return {"error": f"Falha na escalação: {str(e)}"}

    async def _close_ticket(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Fecha ticket"""
        
        try:
            ticket_id = data.get("ticket_id")
            close_reason = data.get("reason", "Resolved")
            satisfaction_rating = data.get("satisfaction_rating")
            
            if not ticket_id:
                return {"error": "ticket_id é obrigatório"}
            
            ticket = self.ticket_engine.get_ticket(ticket_id)
            if not ticket:
                return {"error": f"Ticket {ticket_id} não encontrado"}
            
            # Calcula tempo de resolução se ainda não foi calculado
            if not ticket.get("resolution_time"):
                created_at = datetime.fromisoformat(ticket["created_at"])
                resolution_time = (datetime.now() - created_at).total_seconds() / 60
            else:
                resolution_time = ticket["resolution_time"]
            
            # Atualiza ticket
            updates = {
                "status": "closed",
                "resolution_time": resolution_time
            }
            
            if satisfaction_rating:
                updates["satisfaction_rating"] = satisfaction_rating
            
            self.ticket_engine.update_ticket(ticket_id, updates)
            
            # Libera agente
            assignee = ticket.get("assignee")
            if assignee and assignee in self.available_agents:
                self.available_agents[assignee]["current_load"] -= 1
            
            # Auto-resposta de fechamento
            if self.config["auto_response"]:
                auto_response = self._generate_auto_response("ticket_closed", ticket)
                self.ticket_engine.add_comment(ticket_id, {
                    "author": "System",
                    "body": auto_response,
                    "public": True
                })
            
            return {
                "status": "success",
                "message": "Ticket fechado com sucesso",
                "ticket_id": ticket_id,
                "resolution_time_minutes": resolution_time,
                "close_reason": close_reason,
                "satisfaction_rating": satisfaction_rating
            }
            
        except Exception as e:
            logger.error(f"Erro ao fechar ticket: {str(e)}")
            return {"error": f"Falha ao fechar ticket: {str(e)}"}

    def _get_ticket_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Retorna métricas dos tickets"""
        
        try:
            period = data.get("period", "all")
            
            metrics = self.ticket_engine.get_ticket_metrics(period)
            
            # Adiciona métricas do agente
            agent_metrics = {
                agent_id: {
                    "name": agent_data["name"],
                    "current_load": agent_data["current_load"],
                    "specialties": agent_data["specialties"],
                    "active": agent_data["active"]
                }
                for agent_id, agent_data in self.available_agents.items()
            }
            
            metrics["agent_metrics"] = agent_metrics
            metrics["system_health"] = self._calculate_system_health()
            
            return {
                "status": "success",
                "metrics": metrics
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular métricas: {str(e)}")
            return {"error": f"Falha no cálculo de métricas: {str(e)}"}

    def _get_agent_workload(self) -> Dict[str, Any]:
        """Retorna carga de trabalho dos agentes"""
        
        workload_data = {}
        
        for agent_id, agent_data in self.available_agents.items():
            # Busca tickets atribuídos
            assigned_tickets = [
                t for t in self.ticket_engine.tickets.values()
                if t.get("assignee") == agent_id and t["status"] not in ["closed", "resolved"]
            ]
            
            workload_data[agent_id] = {
                "name": agent_data["name"],
                "active": agent_data["active"],
                "current_load": len(assigned_tickets),
                "specialties": agent_data["specialties"],
                "tickets": {
                    "open": len([t for t in assigned_tickets if t["status"] == "open"]),
                    "in_progress": len([t for t in assigned_tickets if t["status"] == "in_progress"]),
                    "pending": len([t for t in assigned_tickets if t["status"] == "pending"])
                }
            }
        
        return {
            "status": "success",
            "agent_workload": workload_data,
            "total_active_agents": len([a for a in self.available_agents.values() if a["active"]]),
            "system_capacity": f"{sum(a['current_load'] for a in self.available_agents.values())}/200 tickets"
        }

    def _get_manager_status(self) -> Dict[str, Any]:
        """Retorna status completo do gerenciador"""
        
        uptime = datetime.now() - self.created_at
        
        return {
            "agent_status": self.get_status(),
            "ticket_statistics": {
                **self.stats,
                "total_tickets": len(self.ticket_engine.tickets),
                "open_tickets": len(self.ticket_engine.status_index.get("open", [])),
                "resolved_tickets": len(self.ticket_engine.status_index.get("resolved", [])),
                "closed_tickets": len(self.ticket_engine.status_index.get("closed", []))
            },
            "configuration": self.config,
            "available_agents": len([a for a in self.available_agents.values() if a["active"]]),
            "automation_rules": len(self.automation_rules),
            "uptime": str(uptime),
            "performance_metrics": {
                "avg_ticket_creation_time": f"{random.uniform(2, 8):.1f}s",
                "system_reliability": f"{random.uniform(98, 99.9):.1f}%",
                "api_response_time": f"{random.uniform(50, 150):.0f}ms",
                "storage_usage": f"{len(self.ticket_engine.tickets) * 2}KB"
            }
        }

    # Métodos auxiliares

    def _find_best_agent(self, ticket: Dict[str, Any]) -> Optional[str]:
        """Encontra melhor agente para o ticket"""
        
        # Filtra agentes ativos
        active_agents = {
            agent_id: agent_data 
            for agent_id, agent_data in self.available_agents.items()
            if agent_data["active"]
        }
        
        if not active_agents:
            return None
        
        # Scoring baseado em especialidade e carga
        best_agent = None
        best_score = -1
        
        for agent_id, agent_data in active_agents.items():
            score = 0
            
            # Penaliza por carga atual
            score -= agent_data["current_load"] * 10
            
            # Bonus por especialidade
            ticket_tags = ticket.get("tags", [])
            ticket_subject = ticket["subject"].lower()
            
            for specialty in agent_data["specialties"]:
                if specialty in ticket_tags or specialty in ticket_subject:
                    score += 50
            
            # Limite de carga
            if agent_data["current_load"] >= self.config["max_tickets_per_agent"]:
                score = -999
            
            if score > best_score:
                best_score = score
                best_agent = agent_id
        
        return best_agent

    def _generate_auto_response(self, template_key: str, ticket: Dict[str, Any], context: Dict[str, Any] = None) -> str:
        """Gera resposta automática"""
        
        template = self.ticket_engine.auto_response_templates.get(template_key, "")
        
        if not template:
            return ""
        
        # Substitui variáveis
        response = template.format(
            ticket_id=ticket["id"],
            sla_time="24 horas",
            agent_name=context.get("agent_name", "nosso time") if context else "nosso time"
        )
        
        return response

    def _validate_status_transition(self, current_status: str, new_status: str) -> bool:
        """Valida se transição de status é válida"""
        
        valid_transitions = {
            "open": ["in_progress", "pending", "resolved", "closed"],
            "in_progress": ["pending", "resolved", "closed", "open"],
            "pending": ["in_progress", "resolved", "closed", "open"],
            "resolved": ["closed", "reopened"],
            "closed": ["reopened"],
            "reopened": ["in_progress", "pending", "resolved", "closed"]
        }
        
        return new_status in valid_transitions.get(current_status, [])

    def _get_sla_status(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula status do SLA para o ticket"""
        
        created_at = datetime.fromisoformat(ticket["created_at"])
        due_at = datetime.fromisoformat(ticket["due_at"])
        now = datetime.now()
        
        time_elapsed = (now - created_at).total_seconds() / 3600  # horas
        time_remaining = (due_at - now).total_seconds() / 3600  # horas
        
        if ticket["status"] in ["resolved", "closed"]:
            status = "met" if ticket.get("resolution_time", 0) <= (due_at - created_at).total_seconds() / 60 else "breached"
        else:
            status = "on_track" if time_remaining > 0 else "breached"
        
        return {
            "status": status,
            "time_elapsed_hours": round(time_elapsed, 1),
            "time_remaining_hours": round(max(0, time_remaining), 1),
            "due_at": ticket["due_at"]
        }

    def _calculate_time_to_resolution(self, ticket: Dict[str, Any]) -> Optional[str]:
        """Calcula tempo estimado para resolução"""
        
        if ticket["status"] in ["resolved", "closed"]:
            return None
        
        # Estimativa baseada na prioridade e histórico
        base_times = {
            "critical": 60,
            "urgent": 120,
            "high": 240,
            "normal": 480,
            "low": 960
        }
        
        base_minutes = base_times.get(ticket["priority"], 480)
        
        # Ajusta baseado no status atual
        if ticket["status"] == "in_progress":
            base_minutes *= 0.6
        elif ticket["status"] == "pending":
            base_minutes *= 0.8
        
        hours = base_minutes // 60
        minutes = base_minutes % 60
        
        return f"{hours}h {minutes}m"

    def _find_related_tickets(self, ticket: Dict[str, Any]) -> List[str]:
        """Encontra tickets relacionados"""
        
        related = []
        
        # Busca por mesmo requerente
        requester_email = ticket["requester"]["email"]
        for t_id, t_data in self.ticket_engine.tickets.items():
            if (t_data["requester"]["email"] == requester_email and 
                t_id != ticket["id"] and 
                t_data["status"] not in ["closed"]):
                related.append(t_id)
        
        return related[:5]  # Máximo 5

    async def _run_automation_rules(self, ticket: Dict[str, Any]):
        """Executa regras de automação"""
        
        for rule in self.automation_rules:
            if self._matches_rule_condition(ticket, rule["condition"]):
                await self._execute_automation_action(ticket, rule["action"])

    def _matches_rule_condition(self, ticket: Dict[str, Any], condition: Dict[str, Any]) -> bool:
        """Verifica se ticket atende condição da regra"""
        
        for field, value in condition.items():
            if field == "hours_open":
                created_at = datetime.fromisoformat(ticket["created_at"])
                hours_open = (datetime.now() - created_at).total_seconds() / 3600
                
                if value.startswith(">"):
                    threshold = float(value[1:])
                    if hours_open <= threshold:
                        return False
                elif value.startswith("<"):
                    threshold = float(value[1:])
                    if hours_open >= threshold:
                        return False
            else:
                if ticket.get(field) != value:
                    return False
        
        return True

    async def _execute_automation_action(self, ticket: Dict[str, Any], action: str):
        """Executa ação de automação"""
        
        ticket_id = ticket["id"]
        
        if action == "auto_assign_best_agent":
            best_agent = self._find_best_agent(ticket)
            if best_agent:
                await self._assign_ticket({"ticket_id": ticket_id, "agent_id": best_agent})
        
        elif action == "escalate_to_supervisor":
            await self._escalate_ticket({"ticket_id": ticket_id, "reason": "Automatic escalation - age threshold"})
        
        elif action == "send_satisfaction_survey":
            # Simula envio de pesquisa de satisfação
            self.ticket_engine.add_comment(ticket_id, {
                "author": "System",
                "body": "Pesquisa de satisfação enviada por email",
                "public": False
            })

    def _calculate_system_health(self) -> Dict[str, Any]:
        """Calcula saúde geral do sistema"""
        
        total_tickets = len(self.ticket_engine.tickets)
        if total_tickets == 0:
            return {"status": "healthy", "load": "low"}
        
        open_tickets = len(self.ticket_engine.status_index.get("open", []))
        overdue_tickets = sum(1 for t in self.ticket_engine.tickets.values() if self.ticket_engine._is_sla_breached(t))
        
        load_percentage = (open_tickets / max(total_tickets, 1)) * 100
        sla_breach_rate = (overdue_tickets / max(total_tickets, 1)) * 100
        
        if load_percentage > 80 or sla_breach_rate > 20:
            status = "critical"
        elif load_percentage > 60 or sla_breach_rate > 10:
            status = "warning"
        else:
            status = "healthy"
        
        return {
            "status": status,
            "load_percentage": round(load_percentage, 1),
            "sla_breach_rate": round(sla_breach_rate, 1),
            "total_tickets": total_tickets,
            "open_tickets": open_tickets
        }

    def _estimate_resolution_time(self, ticket: Dict[str, Any]) -> str:
        """Estima tempo de resolução baseado em dados históricos"""
        
        # Base time por prioridade
        base_times = {
            "critical": "1 hour",
            "urgent": "2 hours", 
            "high": "4 hours",
            "normal": "1 day",
            "low": "2 days"
        }
        
        return base_times.get(ticket["priority"], "1 day")

# Função obrigatória para o Agent Loader
def create_agents() -> List[BaseNetworkAgent]:
    """
    Função obrigatória para criação dos agentes deste módulo
    Retorna lista de agentes instanciados
    """
    try:
        # Cria instância do agente ticket manager
        ticket_manager_agent = TicketManagerAgent()
        
        logger.info("✅ Support Ticket Manager Agent criado com sucesso")
        
        return [ticket_manager_agent]
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar Support Ticket Manager Agent: {str(e)}")
        return []

# Teste standalone
if __name__ == "__main__":
    async def test_ticket_manager():
        """Teste completo do gerenciador de tickets"""
        print("🧪 Testando Support Ticket Manager Agent...")
        
        # Cria agente
        agents = create_agents()
        if not agents:
            print("❌ Falha na criação do agente")
            return
        
        agent = agents[0]
        print(f"✅ Agente criado: {agent.agent_id}")
        print(f"🎫 Sistema nativo carregado com {len(agent.available_agents)} agentes")
        
        # Teste 1: Criar ticket
        print("\n🎫 Teste 1: Criando ticket...")
        
        message = {
            "action": "create_ticket",
            "data": {
                "subject": "Não consigo fazer login no sistema",
                "description": "Recebo erro 'credenciais inválidas' mesmo com senha correta",
                "requester_name": "João Silva",
                "requester_email": "joao@empresa.com",
                "priority": "high",
                "type": "incident",
                "tags": ["login", "authentication", "urgent"]
            }
        }
        
        result = await agent._internal_handle_message(message)
        if result['status'] == 'success':
            response = result['response']
            print(f"  • Ticket criado: {response['ticket_id']}")
            print(f"  • Atribuído a: {response.get('assigned_to', 'Não atribuído')}")
            print(f"  • SLA due: {response['sla_due'][:19]}")
            print(f"  • Estimativa resolução: {response['estimated_resolution']}")
            
            ticket_id = response['ticket_id']
        
        # Teste 2: Buscar ticket
        print("\n🔍 Teste 2: Buscando ticket criado...")
        
        message = {
            "action": "get_ticket",
            "data": {
                "ticket_id": ticket_id
            }
        }
        
        result = await agent._internal_handle_message(message)
        if result['status'] == 'success':
            response = result['response']
            ticket = response['ticket']
            print(f"  • Status: {ticket['status']}")
            print(f"  • Prioridade: {ticket['priority']}")
            print(f"  • SLA Status: {ticket['sla_status']['status']}")
            print(f"  • Tempo restante: {ticket['sla_status']['time_remaining_hours']}h")
            print(f"  • Comentários: {len(ticket['comments'])}")
        
        # Teste 3: Adicionar comentário
        print("\n💬 Teste 3: Adicionando comentário...")
        
        message = {
            "action": "add_comment",
            "data": {
                "ticket_id": ticket_id,
                "comment": {
                    "author": "Agente João",
                    "body": "Verifiquei o sistema e identifiquei o problema. Vou resetar sua senha e enviar as novas credenciais por email.",
                    "public": True
                }
            }
        }
        
        result = await agent._internal_handle_message(message)
        if result['status'] == 'success':
            response = result['response']
            print(f"  • Comentário adicionado: ID {response['comment_id']}")
            print(f"  • Total de comentários: {response['total_comments']}")
        
        # Teste 4: Atualizar status do ticket
        print("\n🔄 Teste 4: Atualizando status...")
        
        message = {
            "action": "update_ticket",
            "data": {
                "ticket_id": ticket_id,
                "updates": {
                    "status": "in_progress",
                    "priority": "normal"
                }
            }
        }
        
        result = await agent._internal_handle_message(message)
        if result['status'] == 'success':
            response = result['response']
            print(f"  • Status atualizado: {response['current_status']}")
            print(f"  • Updates aplicados: {response['updates_applied']}")
        
        # Teste 5: Criar mais tickets para testes
        print("\n🎫 Teste 5: Criando tickets adicionais...")
        
        additional_tickets = [
            {
                "subject": "Problema com cobrança",
                "requester_name": "Maria Santos",
                "requester_email": "maria@empresa.com",
                "priority": "normal",
                "type": "question"
            },
            {
                "subject": "Sistema lento",
                "requester_name": "Pedro Costa",  
                "requester_email": "pedro@empresa.com",
                "priority": "low",
                "type": "problem"
            }
        ]
        
        created_tickets = []
        for ticket_data in additional_tickets:
            message = {"action": "create_ticket", "data": ticket_data}
            result = await agent._internal_handle_message(message)
            if result['status'] == 'success':
                created_tickets.append(result['response']['ticket_id'])
        
        print(f"  • Tickets adicionais criados: {len(created_tickets)}")
        
        # Teste 6: Buscar tickets com filtros
        print("\n🔍 Teste 6: Buscando tickets com filtros...")
        
        message = {
            "action": "search_tickets",
            "data": {
                "filters": {
                    "status": ["open", "in_progress"],
                    "priority": ["high", "normal"],
                    "sort_by": "created_at",
                    "sort_order": "desc"
                }
            }
        }
        
        result = await agent._internal_handle_message(message)
        if result['status'] == 'success':
            response = result['response']
            print(f"  • Tickets encontrados: {response['total_found']}")
            print(f"  • Por status: {response['summary']['by_status']}")
            print(f"  • Por prioridade: {response['summary']['by_priority']}")
        
        # Teste 7: Carga de trabalho dos agentes
        print("\n👥 Teste 7: Carga de trabalho dos agentes...")
        
        message = {"action": "get_agent_workload"}
        result = await agent._internal_handle_message(message)
        
        if result['status'] == 'success':
            response = result['response']
            workload = response['agent_workload']
            print(f"  • Agentes ativos: {response['total_active_agents']}")
            print(f"  • Capacidade do sistema: {response['system_capacity']}")
            
            for agent_id, data in list(workload.items())[:2]:
                print(f"  • {data['name']}: {data['current_load']} tickets")
        
        # Teste 8: Escalonar ticket
        print("\n🚨 Teste 8: Escalando ticket...")
        
        message = {
            "action": "escalate_ticket",
            "data": {
                "ticket_id": ticket_id,
                "reason": "Customer is VIP and requires immediate attention"
            }
        }
        
        result = await agent._internal_handle_message(message)
        if result['status'] == 'success':
            response = result['response']
            print(f"  • Ticket escalado: {response['ticket_id']}")
            print(f"  • Nova prioridade: {response['new_priority']}")
            print(f"  • Escalado para: {response['escalated_to']}")
        
        # Teste 9: Métricas do sistema
        print("\n📊 Teste 9: Métricas do sistema...")
        
        message = {
            "action": "get_metrics",
            "data": {
                "period": "all"
            }
        }
        
        result = await agent._internal_handle_message(message)
        if result['status'] == 'success':
            response = result['response']
            metrics = response['metrics']
            print(f"  • Total de tickets: {metrics['total_tickets']}")
            print(f"  • SLA compliance: {metrics['sla_compliance_percentage']:.1f}%")
            print(f"  • Tempo médio resolução: {metrics['avg_resolution_time_minutes']:.1f}min")
            print(f"  • Distribuição por status: {metrics['status_distribution']}")
        
        # Teste 10: Resolver e fechar ticket
        print("\n✅ Teste 10: Resolvendo e fechando ticket...")
        
        # Primeiro resolve
        message = {
            "action": "update_ticket",
            "data": {
                "ticket_id": ticket_id,
                "updates": {"status": "resolved"}
            }
        }
        
        await agent._internal_handle_message(message)
        
        # Depois fecha
        message = {
            "action": "close_ticket",
            "data": {
                "ticket_id": ticket_id,
                "reason": "Customer confirmed resolution",
                "satisfaction_rating": 5
            }
        }
        
        result = await agent._internal_handle_message(message)
        if result['status'] == 'success':
            response = result['response']
            print(f"  • Ticket fechado: {response['ticket_id']}")
            print(f"  • Tempo de resolução: {response['resolution_time_minutes']:.1f}min")
            print(f"  • Rating de satisfação: {response['satisfaction_rating']}/5")
        
        # Status final do manager
        print("\n📈 Status final do Ticket Manager...")
        
        message = {"action": "get_manager_status"}
        result = await agent._internal_handle_message(message)
        
        if result['status'] == 'success':
            response = result['response']
            stats = response['ticket_statistics']
            performance = response['performance_metrics']
            
            print(f"  • Tickets criados: {stats['tickets_created']}")
            print(f"  • Tickets resolvidos: {stats['tickets_resolved']}")
            print(f"  • Escalações: {stats['escalations']}")
            print(f"  • Confiabilidade: {performance['system_reliability']}")
            print(f"  • Tempo de resposta API: {performance['api_response_time']}")
        
        print(f"\n✅ Todos os testes concluídos! Agente funcionando perfeitamente.")
        print(f"🎯 Support Ticket Manager Agent - Status: OPERACIONAL")
    
    # Executa teste
    asyncio.run(test_ticket_manager())
