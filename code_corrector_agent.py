import logging
import os
import ast
import re
import shutil
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import difflib
from multi_agent_network import BaseNetworkAgent, AgentType

logger = logging.getLogger(__name__)

class CodeCorrectorAgent(BaseNetworkAgent):
    def __init__(self, agent_id: str, agent_type: str, message_bus):
        super().__init__(agent_id, agent_type, message_bus)
        self.capabilities = ['automatic_correction', 'code_refactoring', 'backup_management']
        self.status = 'active'
        self.correction_history = []
        self.backup_directory = './backups'
        self._ensure_backup_directory()
        logger.info(f"✅ {self.agent_id} inicializado com capacidades de correção automática")

    def _ensure_backup_directory(self):
        """Garante que o diretório de backup existe"""
        try:
            if not os.path.exists(self.backup_directory):
                os.makedirs(self.backup_directory)
                logger.info(f"📁 Diretório de backup criado: {self.backup_directory}")
        except Exception as e:
            logger.error(f"❌ Erro criando diretório de backup: {e}")

    def apply_corrections(self, file_path: str, suggestions: List[Dict]) -> Dict:
        """Aplica correções sugeridas em um arquivo de código"""
        try:
            if not os.path.exists(file_path):
                return {"error": f"Arquivo não encontrado: {file_path}"}

            # Criar backup antes de modificar
            backup_path = self._create_backup(file_path)
            
            # Ler código original
            with open(file_path, 'r', encoding='utf-8') as f:
                original_code = f.read()

            # Aplicar correções básicas
            corrected_code = original_code
            applied_corrections = []

            for suggestion in suggestions:
                try:
                    if suggestion.get('type') == 'syntax_fix':
                        corrected_code, applied = self._apply_syntax_fix(corrected_code, suggestion)
                        if applied:
                            applied_corrections.append(suggestion)
                    
                    elif suggestion.get('type') == 'best_practice':
                        corrected_code, applied = self._apply_best_practice(corrected_code, suggestion)
                        if applied:
                            applied_corrections.append(suggestion)
                            
                except Exception as e:
                    logger.warning(f"⚠️ Erro aplicando sugestão {suggestion.get('type', 'unknown')}: {e}")

            # Verificar se houveram mudanças
            if corrected_code != original_code:
                # Validar sintaxe do código corrigido
                if self._validate_syntax(corrected_code):
                    # Salvar código corrigido
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(corrected_code)
                    
                    # Registrar correção
                    correction_record = {
                        "file_path": file_path,
                        "timestamp": datetime.now().isoformat(),
                        "backup_path": backup_path,
                        "applied_corrections": applied_corrections,
                        "success": True
                    }
                    
                    self.correction_history.append(correction_record)
                    logger.info(f"✅ {len(applied_corrections)} correções aplicadas em {file_path}")
                    
                    return correction_record
                else:
                    # Restaurar backup se sintaxe inválida
                    self._restore_backup(file_path, backup_path)
                    return {
                        "error": "Código corrigido possui sintaxe inválida - backup restaurado",
                        "file_path": file_path,
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                return {
                    "message": "Nenhuma correção aplicável encontrada",
                    "file_path": file_path,
                    "timestamp": datetime.now().isoformat()
                }

        except Exception as e:
            logger.error(f"❌ Erro aplicando correções em {file_path}: {e}")
            return {"error": str(e), "file_path": file_path}

    def _create_backup(self, file_path: str) -> str:
        """Cria backup do arquivo antes da modificação"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(file_path)
            backup_path = os.path.join(self.backup_directory, f"{filename}.backup_{timestamp}")
            
            shutil.copy2(file_path, backup_path)
            logger.info(f"💾 Backup criado: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"❌ Erro criando backup: {e}")
            raise

    def _restore_backup(self, file_path: str, backup_path: str):
        """Restaura arquivo do backup"""
        try:
            shutil.copy2(backup_path, file_path)
            logger.info(f"🔄 Backup restaurado: {file_path}")
        except Exception as e:
            logger.error(f"❌ Erro restaurando backup: {e}")

    def _validate_syntax(self, code: str) -> bool:
        """Valida se o código Python tem sintaxe correta"""
        try:
            ast.parse(code)
            return True
        except SyntaxError as e:
            logger.warning(f"⚠️ Erro de sintaxe detectado: {e}")
            return False

    def _apply_syntax_fix(self, code: str, suggestion: Dict) -> Tuple[str, bool]:
        """Aplica correções de sintaxe básicas"""
        try:
            # Implementação básica de correções
            if 'unused import' in suggestion.get('message', '').lower():
                lines = code.split('\n')
                line_num = suggestion.get('line', 0)
                if 0 < line_num <= len(lines):
                    import_line = lines[line_num - 1]
                    if 'import' in import_line:
                        lines[line_num - 1] = f"# {import_line}  # Removido: import não utilizado"
                        modified_code = '\n'.join(lines)
                        logger.info(f"🔄 Import não utilizado comentado na linha {line_num}")
                        return modified_code, True
            
            return code, False
            
        except Exception as e:
            logger.error(f"❌ Erro aplicando correção de sintaxe: {e}")
            return code, False

    def _apply_best_practice(self, code: str, suggestion: Dict) -> Tuple[str, bool]:
        """Aplica melhores práticas básicas"""
        try:
            practice = suggestion.get('practice', '')
            
            # Exemplo: conversão para f-strings
            if 'f-string' in practice.lower():
                # Substituir .format() básico por f-strings
                format_pattern = r'"([^"]*)\{\}([^"]*)".format\(([^)]+)\)'
                
                def replace_with_fstring(match):
                    before, after, var = match.groups()
                    return f'f"{before}{{{var}}}{after}"'
                
                modified_code = re.sub(format_pattern, replace_with_fstring, code)
                
                if modified_code != code:
                    logger.info("🔄 .format() convertido para f-string")
                    return modified_code, True

            return code, False
            
        except Exception as e:
            logger.error(f"❌ Erro aplicando melhor prática: {e}")
            return code, False

    def get_correction_history(self) -> List[Dict]:
        """Retorna histórico de correções"""
        return self.correction_history

    def generate_correction_report(self) -> str:
        """Gera relatório das correções aplicadas"""
        if not self.correction_history:
            return "📊 Nenhuma correção aplicada ainda"
        
        report = f"📊 RELATÓRIO DE CORREÇÕES - {self.agent_id}\n"
        report += "=" * 60 + "\n\n"
        
        total_corrections = len(self.correction_history)
        successful_corrections = len([c for c in self.correction_history if c.get('success')])
        
        report += f"🔧 Total de correções: {total_corrections}\n"
        report += f"✅ Correções bem-sucedidas: {successful_corrections}\n\n"
        
        # Últimas 3 correções
        recent_corrections = self.correction_history[-3:]
        for i, correction in enumerate(recent_corrections, 1):
            file_name = os.path.basename(correction.get('file_path', 'unknown'))
            timestamp = correction.get('timestamp', '')[:19]
            applied_count = len(correction.get('applied_corrections', []))
            
            report += f"🔧 CORREÇÃO {i} - {timestamp}:\n"
            report += f"   📄 Arquivo: {file_name}\n"
            report += f"   ✅ Melhorias aplicadas: {applied_count}\n\n"
        
        return report

def create_code_corrector_agent(message_bus, num_instances=1) -> List['CodeCorrectorAgent']:
    """Cria agente de correção de código"""
    agents = []
    try:
        logger.info("🔧 Criando CodeCorrectorAgent...")
        
        agent_id = "code_corrector_001"
        agent = CodeCorrectorAgent(agent_id, AgentType.SPECIALIZED, message_bus)
        
        # Registrar no MessageBus
        if hasattr(message_bus, 'register_agent'):
            message_bus.register_agent(agent_id, agent)
        
        agents.append(agent)
        logger.info(f"✅ {len(agents)} agente de correção de código criado")
        return agents
        
    except Exception as e:
        logger.error(f"❌ Erro criando CodeCorrectorAgent: {e}")
        return []
