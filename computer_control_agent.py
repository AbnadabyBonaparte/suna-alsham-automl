import logging
import asyncio
import subprocess
import os
import time
import socket
import base64
import json
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from suna_alsham_core.computer_control_agent import BaseNetworkAgent, AgentMessage, ...
)

# Importações opcionais com verificação
try:
    import paramiko
    HAS_PARAMIKO = True
except ImportError:
    HAS_PARAMIKO = False
    
try:
    import websocket
    HAS_WEBSOCKET = True
except ImportError:
    HAS_WEBSOCKET = False
    
try:
    from cryptography.fernet import Fernet
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

logger = logging.getLogger(__name__)

class AutomationType(Enum):
    """Tipos de automação"""
    BROWSER = "browser"
    DESKTOP = "desktop"
    API = "api"
    CODE_GENERATION = "code_generation"
    FILE_SYSTEM = "file_system"
    TERMINAL = "terminal"
    MISSION_COMPLEX = "mission_complex"
    REMOTE_CONTROL = "remote_control"

class ControlStatus(Enum):
    """Status de controle"""
    IDLE = "idle"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

@dataclass
class AutomationTask:
    """Tarefa de automação"""
    task_id: str
    automation_type: AutomationType
    description: str
    parameters: Dict[str, Any]
    priority: Priority
    status: ControlStatus = ControlStatus.IDLE
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

@dataclass
class AutomationMission:
    """Missão complexa de automação"""
    mission_id: str
    name: str
    description: str
    steps: List[AutomationTask]
    dependencies: Dict[str, List[str]] = field(default_factory=dict)
    status: ControlStatus = ControlStatus.IDLE
    progress: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)

class RemoteControlCapability:
    """Adiciona capacidades de controle remoto ao ComputerControlAgent"""
    
    def __init__(self, agent):
        self.agent = agent
        self.remote_sessions = {}
        if HAS_CRYPTO:
            self.encryption_key = Fernet.generate_key()
            self.cipher = Fernet(self.encryption_key)
        else:
            self.encryption_key = None
            self.cipher = None
            logger.warning("⚠️ Cryptography não disponível - conexões remotas menos seguras")
        
    async def establish_remote_connection(self, connection_data: Dict[str, Any]) -> Dict[str, Any]:
        """Estabelece conexão remota com computador"""
        connection_type = connection_data.get('type')  # ssh, rdp, vnc, custom
        host = connection_data.get('host')
        credentials = connection_data.get('credentials', {})
        
        try:
            if connection_type == 'ssh':
                return await self._connect_ssh(host, credentials)
            elif connection_type == 'rdp':
                return await self._connect_rdp(host, credentials)
            elif connection_type == 'vnc':
                return await self._connect_vnc(host, credentials)
            elif connection_type == 'websocket':
                return await self._connect_websocket(host, credentials)
            elif connection_type == 'anydesk_api':
                return await self._connect_anydesk_api(credentials)
            else:
                return {'status': 'error', 'message': 'Tipo de conexão não suportado'}
                
        except Exception as e:
            logger.error(f"❌ Erro estabelecendo conexão remota: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _connect_ssh(self, host: str, credentials: Dict) -> Dict[str, Any]:
        """Conecta via SSH"""
        if not HAS_PARAMIKO:
            return {
                'status': 'error',
                'message': 'Paramiko não instalado. Execute: pip install paramiko'
            }
            
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(
                hostname=host,
                port=credentials.get('port', 22),
                username=credentials.get('username'),
                password=credentials.get('password'),
                key_filename=credentials.get('key_file')
            )
            
            session_id = f"ssh_{host}_{int(time.time())}"
            self.remote_sessions[session_id] = {
                'type': 'ssh',
                'client': ssh,
                'host': host
            }
            
            logger.info(f"✅ Conexão SSH estabelecida: {session_id}")
            
            return {
                'status': 'connected',
                'session_id': session_id,
                'host': host,
                'type': 'ssh'
            }
        except Exception as e:
            logger.error(f"❌ SSH falhou: {str(e)}")
            return {'status': 'error', 'message': f'SSH falhou: {str(e)}'}
    
    async def _connect_rdp(self, host: str, credentials: Dict) -> Dict[str, Any]:
        """Conecta via RDP (Windows Remote Desktop)"""
        # Implementação simplificada - requer biblioteca adicional como pyrdp
        return {
            'status': 'error',
            'message': 'RDP ainda não implementado. Use SSH ou VNC.'
        }
    
    async def _connect_vnc(self, host: str, credentials: Dict) -> Dict[str, Any]:
        """Conecta via VNC"""
        # Implementação simplificada - requer biblioteca VNC
        return {
            'status': 'error',
            'message': 'VNC ainda não implementado. Use SSH.'
        }
    
    async def _connect_websocket(self, host: str, credentials: Dict) -> Dict[str, Any]:
        """Conecta via WebSocket"""
        if not HAS_WEBSOCKET:
            return {
                'status': 'error',
                'message': 'WebSocket não instalado. Execute: pip install websocket-client'
            }
            
        try:
            ws_url = f"wss://{host}:{credentials.get('port', 8443)}/control"
            ws = websocket.WebSocket()
            ws.connect(ws_url)
            
            session_id = f"ws_{host}_{int(time.time())}"
            self.remote_sessions[session_id] = {
                'type': 'websocket',
                'client': ws,
                'host': host
            }
            
            return {
                'status': 'connected',
                'session_id': session_id,
                'host': host,
                'type': 'websocket'
            }
        except Exception as e:
            return {'status': 'error', 'message': f'WebSocket falhou: {str(e)}'}
    
    async def _connect_anydesk_api(self, credentials: Dict) -> Dict[str, Any]:
        """Conecta usando API do AnyDesk (requer licença)"""
        if not HAS_REQUESTS:
            return {
                'status': 'error',
                'message': 'Requests não instalado. Execute: pip install requests'
            }
            
        try:
            # NOTA: AnyDesk oferece API apenas para licenças Enterprise
            api_key = credentials.get('api_key')
            device_id = credentials.get('device_id')
            
            if not api_key or not device_id:
                return {
                    'status': 'error',
                    'message': 'API key e device_id são obrigatórios para AnyDesk'
                }
            
            # Simulação de conexão via API
            # Na prática, você usaria a API REST do AnyDesk
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            # Endpoint fictício - substituir pelo real
            response = requests.post(
                f'https://api.anydesk.com/v1/sessions/create',
                headers=headers,
                json={
                    'device_id': device_id,
                    'permissions': ['full_control']
                },
                timeout=30
            )
            
            if response.status_code == 200:
                session_data = response.json()
                return {
                    'status': 'connected',
                    'session_id': session_data['session_id'],
                    'type': 'anydesk',
                    'connection_url': session_data['connection_url']
                }
            else:
                return {'status': 'error', 'message': 'Falha na API AnyDesk'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def execute_remote_command(self, session_id: str, command: str) -> Dict[str, Any]:
        """Executa comando em máquina remota"""
        if session_id not in self.remote_sessions:
            return {'status': 'error', 'message': 'Sessão não encontrada'}
        
        session = self.remote_sessions[session_id]
        
        try:
            if session['type'] == 'ssh':
                ssh_client = session['client']
                stdin, stdout, stderr = ssh_client.exec_command(command)
                
                return {
                    'status': 'completed',
                    'stdout': stdout.read().decode(),
                    'stderr': stderr.read().decode(),
                    'exit_code': stdout.channel.recv_exit_status()
                }
            else:
                return {'status': 'error', 'message': 'Tipo de sessão não suportado para comandos'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def remote_screen_control(self, session_id: str, action: Dict) -> Dict[str, Any]:
        """Controla tela remota (mouse, teclado)"""
        if session_id not in self.remote_sessions:
            return {'status': 'error', 'message': 'Sessão não encontrada'}
        
        session = self.remote_sessions[session_id]
        action_type = action.get('type')  # click, move, type, screenshot
        
        try:
            if session['type'] == 'vnc' and hasattr(session, 'vnc_client'):
                vnc = session['vnc_client']
                
                if action_type == 'click':
                    x, y = action.get('x'), action.get('y')
                    vnc.click(x, y)
                elif action_type == 'type':
                    text = action.get('text')
                    vnc.type(text)
                elif action_type == 'screenshot':
                    screenshot = vnc.capture_screen()
                    return {
                        'status': 'completed',
                        'screenshot': base64.b64encode(screenshot).decode()
                    }
                    
            return {'status': 'completed', 'action': action_type}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    async def close_session(self, session_id: str) -> Dict[str, Any]:
        """Fecha sessão remota"""
        if session_id not in self.remote_sessions:
            return {'status': 'error', 'message': 'Sessão não encontrada'}
        
        try:
            session = self.remote_sessions[session_id]
            
            if session['type'] == 'ssh':
                session['client'].close()
            elif session['type'] == 'websocket':
                session['client'].close()
                
            del self.remote_sessions[session_id]
            
            return {'status': 'closed', 'session_id': session_id}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

class SecureRemoteTunnel:
    """Cria túnel seguro para controle remoto"""
    
    def __init__(self):
        if HAS_CRYPTO:
            self.tunnel_key = Fernet.generate_key()
        else:
            self.tunnel_key = None
        self.active_tunnels = {}
        
    async def create_reverse_tunnel(self, target_host: str, local_port: int = 8888):
        """Cria túnel reverso seguro"""
        try:
            # Comando para criar túnel SSH reverso
            tunnel_command = f"ssh -R {local_port}:localhost:22 {target_host}"
            
            # Estabelecer túnel
            process = await asyncio.create_subprocess_shell(
                tunnel_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            tunnel_id = f"tunnel_{target_host}_{local_port}"
            self.active_tunnels[tunnel_id] = {
                'process': process,
                'host': target_host,
                'port': local_port
            }
            
            return {
                'status': 'tunnel_created',
                'tunnel_id': tunnel_id,
                'local_port': local_port
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

class ComputerControlAgent(BaseNetworkAgent):
    """Agente de controle computacional avançado integrado ao SUNA-ALSHAM"""
    
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = [
            'browser_automation',
            'desktop_control',
            'api_integration', 
            'code_generation',
            'file_management',
            'terminal_execution',
            'mission_orchestration',
            'real_world_automation',
            'remote_ssh_control',
            'remote_desktop_access',
            'multi_computer_orchestration',
            'secure_remote_execution'
        ]
        self.status = 'active'
        
        # Estado do agente
        self.active_tasks = {}  # task_id -> AutomationTask
        self.completed_tasks = []
        self.active_missions = {}  # mission_id -> AutomationMission
        self.automation_queue = asyncio.Queue()
        
        # Configurações de automação
        self.browser_drivers = {}  # Para múltiplas sessões
        self.api_sessions = {}
        self.code_templates = self._load_code_templates()
        self.automation_history = []
        
        # Recursos externos (serão verificados)
        self.has_selenium = self._check_selenium()
        self.has_pyautogui = self._check_pyautogui()
        self.has_requests = HAS_REQUESTS
        
        # Controle remoto
        self.remote_control = RemoteControlCapability(self)
        self.secure_tunnel = SecureRemoteTunnel()
        
        # Métricas
        self.automation_metrics = {
            'tasks_executed': 0,
            'missions_completed': 0,
            'browser_sessions': 0,
            'api_calls_made': 0,
            'files_created': 0,
            'remote_sessions': 0,
            'success_rate': 1.0
        }
        
        # Tasks de background
        self._automation_task = None
        self._monitoring_task = None
        
        logger.info(f"🤖 {self.agent_id} inicializado com controle computacional avançado")
        self._log_capabilities()
    
    def _check_selenium(self) -> bool:
        """Verifica se Selenium está disponível"""
        try:
            import selenium
            return True
        except ImportError:
            logger.warning("⚠️ Selenium não disponível - automação de browser limitada")
            return False
    
    def _check_pyautogui(self) -> bool:
        """Verifica se PyAutoGUI está disponível"""
        try:
            import pyautogui
            return True
        except ImportError:
            logger.warning("⚠️ PyAutoGUI não disponível - controle de desktop limitado")
            return False
    
    def _log_capabilities(self):
        """Log das capacidades disponíveis"""
        logger.info(f"🔧 Capacidades disponíveis:")
        logger.info(f"   ├── Browser Control: {'✅' if self.has_selenium else '❌'}")
        logger.info(f"   ├── Desktop Control: {'✅' if self.has_pyautogui else '❌'}")
        logger.info(f"   ├── API Integration: {'✅' if self.has_requests else '❌'}")
        logger.info(f"   ├── Remote SSH: {'✅' if HAS_PARAMIKO else '❌'}")
        logger.info(f"   ├── Secure Encryption: {'✅' if HAS_CRYPTO else '❌'}")
        logger.info(f"   ├── Terminal Access: ✅")
        logger.info(f"   ├── File System: ✅")
        logger.info(f"   └── Code Generation: ✅")
    
    def _load_code_templates(self) -> Dict[str, str]:
        """Carrega templates de código"""
        return {
            'fastapi_basic': '''from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="{title}")

@app.get("/")
async def root():
    return {{"message": "Hello from {title}!"}}

@app.get("/health")
async def health():
    return {{"status": "healthy"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
''',
            'react_component': '''import React, {{ useState }} from 'react';

const {component_name} = () => {{
    const [state, setState] = useState({initial_state});

    return (
        <div className="{class_name}">
            <h1>{title}</h1>
            {{/* Component content */}}
        </div>
    );
}};

export default {component_name};
''',
            'python_script': '''#!/usr/bin/env python3
"""
{description}
Generated by SUNA-ALSHAM ComputerControlAgent
"""

import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main function"""
    logger.info("Script {script_name} started")
    
    # Your code here
    
    logger.info("Script completed successfully")

if __name__ == "__main__":
    main()
''',
            'automation_script': '''"""
Automation Script: {script_name}
Generated by SUNA-ALSHAM
"""

import asyncio
import json
from datetime import datetime

async def execute_automation():
    """Execute automation task"""
    results = {{
        'started_at': datetime.now().isoformat(),
        'steps_completed': [],
        'status': 'success'
    }}
    
    # Automation steps here
    
    return results

if __name__ == "__main__":
    result = asyncio.run(execute_automation())
    print(json.dumps(result, indent=2))
'''
        }
    
    async def start_automation_service(self):
        """Inicia serviço de automação"""
        if not self._automation_task:
            self._automation_task = asyncio.create_task(self._automation_loop())
            self._monitoring_task = asyncio.create_task(self._monitoring_loop())
            logger.info(f"🤖 {self.agent_id} iniciou serviço de automação")
    
    async def stop_automation_service(self):
        """Para serviço de automação"""
        if self._automation_task:
            self._automation_task.cancel()
            self._automation_task = None
        if self._monitoring_task:
            self._monitoring_task.cancel()
            self._monitoring_task = None
        
        # Fechar sessões ativas
        await self._cleanup_sessions()
        
        logger.info(f"🛑 {self.agent_id} parou serviço de automação")
    
    async def _automation_loop(self):
        """Loop principal de automação"""
        while True:
            try:
                # Processar fila de automação
                if not self.automation_queue.empty():
                    automation_request = await self.automation_queue.get()
                    await self._process_automation_request(automation_request)
                
                # Verificar tasks ativas
                await self._check_active_tasks()
                
                await asyncio.sleep(1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no loop de automação: {e}")
    
    async def _monitoring_loop(self):
        """Loop de monitoramento"""
        while True:
            try:
                # Verificar saúde das sessões
                await self._health_check_sessions()
                
                # Limpar recursos não utilizados
                await self._cleanup_unused_resources()
                
                await asyncio.sleep(30)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro no monitoramento: {e}")
    
    async def handle_message(self, message: AgentMessage):
        """Processa mensagens recebidas"""
        await super().handle_message(message)
        
        if message.message_type == MessageType.REQUEST:
            request_type = message.content.get('request_type')
            
            if request_type == 'execute_automation':
                result = await self.execute_automation(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'browser_control':
                result = await self.browser_automation(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'generate_code':
                result = await self.generate_code(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'execute_mission':
                result = await self.execute_complex_mission(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'api_integration':
                result = await self.api_automation(message.content)
                await self._send_response(message, result)
                
            elif request_type == 'file_operations':
                result = await self.file_system_automation(message.content)
                await self._send_response(message, result)
                
            # Controle remoto
            elif request_type == 'remote_connect':
                result = await self.remote_control.establish_remote_connection(
                    message.content.get('connection_data')
                )
                await self._send_response(message, result)
                
            elif request_type == 'remote_execute':
                result = await self.remote_control.execute_remote_command(
                    message.content.get('session_id'),
                    message.content.get('command')
                )
                await self._send_response(message, result)
                
            elif request_type == 'remote_screen':
                result = await self.remote_control.remote_screen_control(
                    message.content.get('session_id'),
                    message.content.get('action')
                )
                await self._send_response(message, result)
                
            elif request_type == 'remote_disconnect':
                result = await self.remote_control.close_session(
                    message.content.get('session_id')
                )
                await self._send_response(message, result)
    
    async def execute_automation(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa automação geral"""
        try:
            automation_type = AutomationType(request_data.get('type', 'terminal'))
            description = request_data.get('description', 'Automação geral')
            parameters = request_data.get('parameters', {})
            
            # Criar task
            task = AutomationTask(
                task_id=f"auto_{len(self.active_tasks)}",
                automation_type=automation_type,
                description=description,
                parameters=parameters,
                priority=Priority(request_data.get('priority', 'medium'))
            )
            
            self.active_tasks[task.task_id] = task
            
            # Executar baseado no tipo
            if automation_type == AutomationType.BROWSER:
                result = await self._execute_browser_task(task)
            elif automation_type == AutomationType.TERMINAL:
                result = await self._execute_terminal_task(task)
            elif automation_type == AutomationType.CODE_GENERATION:
                result = await self._execute_code_generation_task(task)
            elif automation_type == AutomationType.API:
                result = await self._execute_api_task(task)
            elif automation_type == AutomationType.FILE_SYSTEM:
                result = await self._execute_file_task(task)
            elif automation_type == AutomationType.REMOTE_CONTROL:
                result = await self._execute_remote_task(task)
            else:
                result = await self._execute_generic_task(task)
            
            # Atualizar task
            task.status = ControlStatus.COMPLETED if result.get('success') else ControlStatus.FAILED
            task.completed_at = datetime.now()
            task.result = result
            
            # Mover para completadas
            self.completed_tasks.append(task)
            del self.active_tasks[task.task_id]
            
            self.automation_metrics['tasks_executed'] += 1
            
            return {
                'status': 'completed',
                'task_id': task.task_id,
                'result': result,
                'execution_time': (task.completed_at - task.created_at).total_seconds()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro executando automação: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def browser_automation(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Automação de browser avançada"""
        if not self.has_selenium:
            return {
                'status': 'error',
                'message': 'Selenium não disponível - instale com: pip install selenium'
            }
        
        try:
            action = request_data.get('action')
            url = request_data.get('url')
            session_id = request_data.get('session_id', 'default')
            
            logger.info(f"🌐 Executando automação de browser: {action}")
            
            # Gerenciar sessão do browser
            if session_id not in self.browser_drivers:
                await self._create_browser_session(session_id)
            
            driver = self.browser_drivers[session_id]
            
            result = {'success': False, 'data': {}}
            
            if action == 'navigate':
                driver.get(url)
                result = {'success': True, 'current_url': driver.current_url}
                
            elif action == 'fill_form':
                form_data = request_data.get('form_data', {})
                for field_name, value in form_data.items():
                    try:
                        element = driver.find_element('name', field_name)
                        element.clear()
                        element.send_keys(value)
                    except:
                        try:
                            element = driver.find_element('id', field_name)
                            element.clear()
                            element.send_keys(value)
                        except:
                            logger.warning(f"⚠️ Campo {field_name} não encontrado")
                
                result = {'success': True, 'fields_filled': len(form_data)}
                
            elif action == 'click_element':
                selector = request_data.get('selector')
                try:
                    element = driver.find_element('css selector', selector)
                    element.click()
                    result = {'success': True, 'element_clicked': selector}
                except Exception as e:
                    result = {'success': False, 'error': str(e)}
                    
            elif action == 'extract_data':
                selectors = request_data.get('selectors', {})
                extracted = {}
                for key, selector in selectors.items():
                    try:
                        element = driver.find_element('css selector', selector)
                        extracted[key] = element.text
                    except:
                        extracted[key] = None
                
                result = {'success': True, 'extracted_data': extracted}
                
            elif action == 'screenshot':
                screenshot_path = f"screenshot_{session_id}_{int(time.time())}.png"
                driver.save_screenshot(screenshot_path)
                result = {'success': True, 'screenshot_path': screenshot_path}
            
            self.automation_metrics['browser_sessions'] += 1
            
            return {
                'status': 'completed',
                'action': action,
                'session_id': session_id,
                'result': result
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na automação de browser: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def generate_code(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera código automaticamente"""
        try:
            template_type = request_data.get('template_type', 'python_script')
            parameters = request_data.get('parameters', {})
            output_path = request_data.get('output_path')
            
            logger.info(f"💻 Gerando código: {template_type}")
            
            if template_type not in self.code_templates:
                return {
                    'status': 'error',
                    'message': f'Template {template_type} não disponível'
                }
            
            # Gerar código do template
            template = self.code_templates[template_type]
            generated_code = template.format(**parameters)
            
            # Salvar se caminho especificado
            if output_path:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(generated_code)
                
                self.automation_metrics['files_created'] += 1
                
                return {
                    'status': 'completed',
                    'template_type': template_type,
                    'output_path': output_path,
                    'lines_generated': len(generated_code.split('\n')),
                    'code_preview': generated_code[:200] + '...' if len(generated_code) > 200 else generated_code
                }
            else:
                return {
                    'status': 'completed',
                    'template_type': template_type,
                    'generated_code': generated_code,
                    'lines_generated': len(generated_code.split('\n'))
                }
                
        except Exception as e:
            logger.error(f"❌ Erro gerando código: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def api_automation(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Automação de APIs"""
        if not self.has_requests:
            return {
                'status': 'error',
                'message': 'Requests não disponível - instale com: pip install requests'
            }
        
        try:
            import requests
            
            method = request_data.get('method', 'GET').upper()
            url = request_data.get('url')
            headers = request_data.get('headers', {})
            data = request_data.get('data')
            json_data = request_data.get('json')
            
            logger.info(f"🔗 Executando chamada API: {method} {url}")
            
            # Fazer requisição
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                json=json_data,
                timeout=30
            )
            
            self.automation_metrics['api_calls_made'] += 1
            
            return {
                'status': 'completed',
                'method': method,
                'url': url,
                'status_code': response.status_code,
                'response_headers': dict(response.headers),
                'response_data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text[:1000]
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na automação de API: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def file_system_automation(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Automação do sistema de arquivos"""
        try:
            operation = request_data.get('operation')
            path = request_data.get('path')
            
            logger.info(f"📁 Operação de arquivo: {operation} em {path}")
            
            result = {'success': False}
            
            if operation == 'create_directory':
                Path(path).mkdir(parents=True, exist_ok=True)
                result = {'success': True, 'directory_created': path}
                
            elif operation == 'write_file':
                content = request_data.get('content', '')
                Path(path).parent.mkdir(parents=True, exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                result = {'success': True, 'file_written': path, 'bytes_written': len(content)}
                self.automation_metrics['files_created'] += 1
                
            elif operation == 'read_file':
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                result = {'success': True, 'content': content, 'bytes_read': len(content)}
                
            elif operation == 'copy_file':
                destination = request_data.get('destination')
                import shutil
                shutil.copy2(path, destination)
                result = {'success': True, 'copied_from': path, 'copied_to': destination}
                
            elif operation == 'delete_file':
                Path(path).unlink()
                result = {'success': True, 'file_deleted': path}
                
            elif operation == 'list_directory':
                files = [str(p) for p in Path(path).iterdir()]
                result = {'success': True, 'files': files, 'count': len(files)}
            
            return {
                'status': 'completed',
                'operation': operation,
                'path': path,
                'result': result
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na operação de arquivo: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def execute_complex_mission(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa missão complexa com múltiplos passos"""
        try:
            mission_name = request_data.get('mission_name', 'Missão Automática')
            steps = request_data.get('steps', [])
            
            logger.info(f"🚀 Executando missão complexa: {mission_name}")
            
            # Criar missão
            mission = AutomationMission(
                mission_id=f"mission_{len(self.active_missions)}",
                name=mission_name,
                description=request_data.get('description', ''),
                steps=[]
            )
            
            # Converter steps em AutomationTasks
            for i, step in enumerate(steps):
                task = AutomationTask(
                    task_id=f"mission_{mission.mission_id}_step_{i}",
                    automation_type=AutomationType(step.get('type', 'terminal')),
                    description=step.get('description', f'Passo {i+1}'),
                    parameters=step,
                    priority=Priority.HIGH
                )
                mission.steps.append(task)
            
            self.active_missions[mission.mission_id] = mission
            mission.status = ControlStatus.EXECUTING
            
            # Executar steps sequencialmente
            results = []
            for i, task in enumerate(mission.steps):
                logger.info(f"🔄 Executando passo {i+1}/{len(mission.steps)}: {task.description}")
                
                # Executar task
                if task.automation_type == AutomationType.BROWSER:
                    result = await self.browser_automation(task.parameters)
                elif task.automation_type == AutomationType.API:
                    result = await self.api_automation(task.parameters)
                elif task.automation_type == AutomationType.CODE_GENERATION:
                    result = await self.generate_code(task.parameters)
                elif task.automation_type == AutomationType.FILE_SYSTEM:
                    result = await self.file_system_automation(task.parameters)
                elif task.automation_type == AutomationType.TERMINAL:
                    result = await self._execute_terminal_command(task.parameters.get('command', ''))
                elif task.automation_type == AutomationType.REMOTE_CONTROL:
                    result = await self._execute_remote_mission_step(task.parameters)
                else:
                    result = {'status': 'skipped', 'message': f'Tipo {task.automation_type.value} não implementado'}
                
                results.append({
                    'step': i + 1,
                    'task_id': task.task_id,
                    'description': task.description,
                    'result': result
                })
                
                # Verificar se step falhou
                if result.get('status') == 'error':
                    # Tentar alternativa se existir
                    alternative = task.parameters.get('alternative')
                    if alternative:
                        logger.info(f"⚠️ Tentando alternativa para passo {i+1}")
                        alt_result = await self._execute_alternative(alternative)
                        if alt_result.get('status') == 'completed':
                            results[-1]['alternative_used'] = True
                            results[-1]['result'] = alt_result
                        else:
                            mission.status = ControlStatus.FAILED
                            break
                    else:
                        mission.status = ControlStatus.FAILED
                        break
                
                # Atualizar progresso
                mission.progress = ((i + 1) / len(mission.steps)) * 100
                
                # Pequeno delay entre steps
                await asyncio.sleep(1)
            
            # Finalizar missão
            if mission.status != ControlStatus.FAILED:
                mission.status = ControlStatus.COMPLETED
                self.automation_metrics['missions_completed'] += 1
            
            # Mover para histórico
            self.automation_history.append(mission)
            del self.active_missions[mission.mission_id]
            
            return {
                'status': 'completed',
                'mission_id': mission.mission_id,
                'mission_name': mission_name,
                'steps_executed': len(results),
                'steps_successful': sum(1 for r in results if r['result'].get('status') == 'completed'),
                'mission_status': mission.status.value,
                'progress': mission.progress,
                'results': results
            }
            
        except Exception as e:
            logger.error(f"❌ Erro executando missão complexa: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _execute_terminal_command(self, command: str) -> Dict[str, Any]:
        """Executa comando no terminal"""
        try:
            logger.info(f"💻 Executando comando: {command}")
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return {
                'status': 'completed',
                'command': command,
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
            
        except subprocess.TimeoutExpired:
            return {
                'status': 'error',
                'message': 'Comando excedeu timeout de 60 segundos'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    async def _execute_remote_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Executa task remota"""
        params = task.parameters
        
        if params.get('action') == 'connect':
            return await self.remote_control.establish_remote_connection(params)
        elif params.get('action') == 'execute':
            return await self.remote_control.execute_remote_command(
                params.get('session_id'),
                params.get('command')
            )
        else:
            return {'status': 'error', 'message': 'Ação remota não especificada'}
    
    async def _execute_remote_mission_step(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Executa passo de missão remota"""
        action = params.get('action', 'execute')
        
        if action == 'connect':
            return await self.remote_control.establish_remote_connection({
                'type': params.get('connection_type', 'ssh'),
                'host': params.get('host'),
                'credentials': params.get('credentials', {})
            })
        elif action == 'execute':
            return await self.remote_control.execute_remote_command(
                params.get('session_id'),
                params.get('command')
            )
        else:
            return {'status': 'error', 'message': f'Ação remota {action} não suportada'}
    
    async def _create_browser_session(self, session_id: str):
        """Cria nova sessão de browser"""
        if self.has_selenium:
            try:
                from selenium import webdriver
                from selenium.webdriver.chrome.options import Options
                
                options = Options()
                options.add_argument('--headless')  # Executar sem interface gráfica
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                
                driver = webdriver.Chrome(options=options)
                self.browser_drivers[session_id] = driver
                
                logger.info(f"🌐 Sessão de browser criada: {session_id}")
            except Exception as e:
                logger.error(f"❌ Erro criando sessão de browser: {e}")
    
    async def _cleanup_sessions(self):
        """Limpa todas as sessões ativas"""
        # Limpar sessões de browser
        for session_id, driver in self.browser_drivers.items():
            try:
                driver.quit()
                logger.info(f"🌐 Sessão {session_id} encerrada")
            except:
                pass
        
        self.browser_drivers.clear()
        
        # Limpar sessões remotas
        for session_id in list(self.remote_control.remote_sessions.keys()):
            await self.remote_control.close_session(session_id)
    
    async def _health_check_sessions(self):
        """Verifica saúde das sessões"""
        # Browser sessions
        inactive_sessions = []
        
        for session_id, driver in self.browser_drivers.items():
            try:
                # Testar se sessão ainda está ativa
                driver.current_url
            except:
                inactive_sessions.append(session_id)
        
        # Remover sessões inativas
        for session_id in inactive_sessions:
            del self.browser_drivers[session_id]
            logger.warning(f"⚠️ Sessão inativa removida: {session_id}")
    
    async def _cleanup_unused_resources(self):
        """Limpa recursos não utilizados"""
        # Limpar arquivos temporários antigos
        temp_files = Path('.').glob('screenshot_*.png')
        for temp_file in temp_files:
            try:
                if time.time() - temp_file.stat().st_mtime > 3600:  # 1 hora
                    temp_file.unlink()
            except:
                pass
    
    # Métodos auxiliares para execução de tasks
    async def _execute_browser_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Executa task de browser"""
        return await self.browser_automation(task.parameters)
    
    async def _execute_terminal_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Executa task de terminal"""
        command = task.parameters.get('command', '')
        return await self._execute_terminal_command(command)
    
    async def _execute_code_generation_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Executa task de geração de código"""
        return await self.generate_code(task.parameters)
    
    async def _execute_api_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Executa task de API"""
        return await self.api_automation(task.parameters)
    
    async def _execute_file_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Executa task de arquivo"""
        return await self.file_system_automation(task.parameters)
    
    async def _execute_generic_task(self, task: AutomationTask) -> Dict[str, Any]:
        """Executa task genérica"""
        return {
            'status': 'completed',
            'message': f'Task {task.automation_type.value} executada genericamente'
        }
    
    async def _execute_alternative(self, alternative: Dict[str, Any]) -> Dict[str, Any]:
        """Executa alternativa para um step que falhou"""
        alt_type = alternative.get('type', 'terminal')
        
        if alt_type == 'terminal':
            return await self._execute_terminal_command(alternative.get('command', ''))
        elif alt_type == 'api':
            return await self.api_automation(alternative)
        else:
            return {'status': 'error', 'message': 'Alternativa não suportada'}
    
    async def _process_automation_request(self, request: Dict[str, Any]):
        """Processa requisição da fila de automação"""
        # Implementar processamento da fila se necessário
        pass
    
    async def _check_active_tasks(self):
        """Verifica status das tasks ativas"""
        # Implementar verificação de tasks se necessário
        pass
    
    async def _send_response(self, original_message: AgentMessage, response_data: Dict[str, Any]):
        """Envia resposta para mensagem original"""
        response = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id=original_message.sender_id,
            message_type=MessageType.RESPONSE,
            priority=original_message.priority,
            content=response_data,
            timestamp=datetime.now(),
            correlation_id=original_message.id
        )
        await self.message_bus.publish(response)

def create_computer_control_agent(message_bus, num_instances=1) -> List[ComputerControlAgent]:
    """
    Cria agente de controle computacional
    
    Args:
        message_bus: Barramento de mensagens para comunicação
        num_instances: Número de instâncias (mantido para compatibilidade)
        
    Returns:
        Lista com 1 agente de controle computacional
    """
    agents = []
    
    try:
        logger.info("🤖 Criando ComputerControlAgent para automação avançada...")
        
        # Verificar se já existe
        existing_agents = set()
        if hasattr(message_bus, 'subscribers'):
            existing_agents = set(message_bus.subscribers.keys())
        
        agent_id = "computer_control_001"
        
        if agent_id not in existing_agents:
            try:
                agent = ComputerControlAgent(agent_id, AgentType.AUTOMATOR, message_bus)
                
                # Iniciar serviços de automação
                asyncio.create_task(agent.start_automation_service())
                
                agents.append(agent)
                logger.info(f"✅ {agent_id} criado com controle computacional avançado")
                logger.info(f"   └── Capabilities: {', '.join(agent.capabilities)}")
                
            except Exception as e:
                logger.error(f"❌ Erro criando {agent_id}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.warning(f"⚠️ {agent_id} já existe - pulando")
        
        logger.info(f"✅ {len(agents)} agente de controle computacional criado")
        
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro crítico criando ComputerControlAgent: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []

# Exemplo de uso completo
async def demonstrate_full_capabilities():
    """Demonstra todas as capacidades do agente"""
    
    examples = {
        # Controle remoto SSH
        'ssh_control': {
            'request_type': 'remote_connect',
            'connection_data': {
                'type': 'ssh',
                'host': '192.168.1.100',
                'credentials': {
                    'username': 'user',
                    'password': 'secure_password',
                    'port': 22
                }
            }
        },
        
        # Missão complexa multi-servidor
        'multi_server_deploy': {
            'request_type': 'execute_mission',
            'mission_name': 'Deploy Multi-Servidor',
            'description': 'Deploy automático em múltiplos servidores',
            'steps': [
                {
                    'type': 'remote_control',
                    'action': 'connect',
                    'connection_type': 'ssh',
                    'host': 'server1.example.com',
                    'credentials': {'username': 'deploy', 'key_file': '/path/to/key'},
                    'description': 'Conectar ao servidor 1'
                },
                {
                    'type': 'remote_control',
                    'action': 'execute',
                    'session_id': 'ssh_server1.example.com_XXX',
                    'command': 'cd /app && git pull origin main',
                    'description': 'Atualizar código'
                },
                {
                    'type': 'remote_control',
                    'action': 'execute',
                    'session_id': 'ssh_server1.example.com_XXX',
                    'command': 'docker-compose down && docker-compose up -d',
                    'description': 'Reiniciar containers'
                },
                {
                    'type': 'remote_control',
                    'action': 'connect',
                    'connection_type': 'ssh',
                    'host': 'server2.example.com',
                    'credentials': {'username': 'deploy', 'key_file': '/path/to/key'},
                    'description': 'Conectar ao servidor 2'
                },
                {
                    'type': 'remote_control',
                    'action': 'execute',
                    'session_id': 'ssh_server2.example.com_XXX',
                    'command': 'cd /app && git pull origin main && docker-compose up -d',
                    'description': 'Deploy no servidor 2'
                }
            ]
        },
        
        # Automação completa de projeto
        'create_full_project': {
            'request_type': 'execute_mission',
            'mission_name': 'Criar Sistema Completo',
            'description': 'Criar projeto full-stack com deploy automático',
            'steps': [
                {
                    'type': 'file_system',
                    'operation': 'create_directory',
                    'path': './my_awesome_project',
                    'description': 'Criar estrutura do projeto'
                },
                {
                    'type': 'code_generation',
                    'template_type': 'fastapi_basic',
                    'parameters': {'title': 'My Awesome API'},
                    'output_path': './my_awesome_project/backend/main.py',
                    'description': 'Gerar backend API'
                },
                {
                    'type': 'code_generation',
                    'template_type': 'react_component',
                    'parameters': {
                        'component_name': 'App',
                        'title': 'My Awesome App',
                        'class_name': 'app-container',
                        'initial_state': '{ loading: false, data: [] }'
                    },
                    'output_path': './my_awesome_project/frontend/App.jsx',
                    'description': 'Gerar frontend React'
                },
                {
                    'type': 'terminal',
                    'command': 'cd my_awesome_project && git init && git add . && git commit -m "Initial commit"',
                    'description': 'Inicializar Git'
                },
                {
                    'type': 'api',
                    'method': 'POST',
                    'url': 'https://api.github.com/user/repos',
                    'headers': {'Authorization': 'token YOUR_GITHUB_TOKEN'},
                    'json': {
                        'name': 'my-awesome-project',
                        'description': 'Projeto criado automaticamente pelo SUNA-ALSHAM',
                        'private': False
                    },
                    'description': 'Criar repositório no GitHub'
                },
                {
                    'type': 'browser',
                    'action': 'navigate',
                    'url': 'https://railway.app/new',
                    'description': 'Abrir Railway para deploy'
                }
            ]
        }
    }
    
    return examples
