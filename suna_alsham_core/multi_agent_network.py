# ... (todo o início do arquivo é igual) ...

class BaseNetworkAgent:
    def __init__(self, agent_id: str, agent_type: AgentType, message_bus: MessageBus):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.message_bus = message_bus
        self.inbox = self.message_bus.subscribe(self.agent_id)
        self.status = "active"
        self.capabilities: List[str] = []
        self.task = asyncio.create_task(self._run())

    async def _run(self):
        while True:
            try:
                message = await self.inbox.get()
                await self._internal_handle_message(message)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Erro no loop do agente {self.agent_id}: {e}", exc_info=True)

    async def _internal_handle_message(self, message: AgentMessage):
        pass # A ser sobrescrito

    def create_message(self, recipient_id: str, message_type: MessageType, content: Dict, priority: Priority = Priority.NORMAL, callback_id: Optional[str] = None) -> AgentMessage:
        return AgentMessage(sender_id=self.agent_id, recipient_id=recipient_id, message_type=message_type, content=content, priority=priority, callback_id=callback_id)

    async def publish_response(self, original_message: AgentMessage, content: Dict):
        response = self.create_message(
            recipient_id=original_message.sender_id,
            message_type=MessageType.RESPONSE,
            content=content,
            callback_id=original_message.callback_id
        )
        await self.message_bus.publish(response)
        
    # --- MÉTODO ADICIONADO AQUI ---
    async def publish_error_response(self, original_message: AgentMessage, error_message: str):
        """Cria e publica uma mensagem de erro padronizada."""
        error_content = {"status": "error", "message": error_message}
        error_response = self.create_message(
            recipient_id=original_message.sender_id,
            message_type=MessageType.ERROR,
            content=error_content,
            callback_id=original_message.callback_id
        )
        await self.message_bus.publish(error_response)
