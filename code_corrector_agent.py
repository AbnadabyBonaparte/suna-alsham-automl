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

    def apply_improvements(self, file_path: str, suggestions: List[Dict]) -> Dict:
        """Aplica melhorias sugeridas em um arquivo de código"""
        try:
            if not os.path.exists(file_path):
                return {"error": f"Arquivo não encontrado: {file_path}"}

            # Criar backup antes de modificar
            backup_path = self._create_backup(file_path)
            
            # Ler código original
            with open(file_path, 'r', encoding='utf-8') as f:
                original_code = f.read()

            # Aplicar correções
            corrected_code = original_code
            applied_corrections = []

            for suggestion in suggestions:
                try:
                    if suggestion.get('type') == 'library_upgrade':
                        corrected_code, applied = self._apply_library_upgrade(corrected_code, suggestion)
                        if applied:
                            applied_corrections.append(suggestion)
                    
                    elif suggestion.get('type') == 'best_practice':
                        corrected_code, applied = self._apply_best_practice(corrected_code, suggestion)
                        if applied:
                            applied_corrections.append(suggestion)
                    
                    elif suggestion.get('type') == 'performance_optimization':
                        corrected_code, applied = self._apply_performance_optimization(corrected_code, suggestion)
                        if applied:
                            applied_corrections.append(suggestion)
                    
                    elif suggestion.get('type') == 'syntax_fix':
                        corrected_code, applied = self._apply_syntax_fix(corrected_code, suggestion)
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
                        "lines_changed": len(difflib.unified_diff(
                            original_code.splitlines(), 
                            corrected_code.splitlines()
                        )),
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
            logger.error(f"❌ Erro aplicando melhorias em {file_path}: {e}")
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

    def _apply_library_upgrade(self, code: str, suggestion: Dict) -> Tuple[str, bool]:
        """Aplica upgrade de biblioteca"""
        try:
            description = suggestion.get('description', '')
            
            # Extrair biblioteca atual e nova
            if 'upgrade' in description.lower():
                # Exemplo: "Consider upgrading requests to httpx"
                pattern = r'upgrading\s+(\w+)\s+to\s+(\w+)'
                match = re.search(pattern, description, re.IGNORECASE)
                
                if match:
                    old_lib, new_lib = match.groups()
                    
                    # Substituir imports
                    import_pattern = f'import\\s+{old_lib}'
                    from_pattern = f'from\\s+{old_lib}'
                    
                    modified_code = re.sub(import_pattern, f'import {new_lib}', code)
                    modified_code = re.sub(from_pattern, f'from {new_lib}', modified_code)
                    
                    if modified_code != code:
                        logger.info(f"🔄 Biblioteca {old_lib} atualizada para {new_lib}")
                        return modified_code, True
            
            return code, False
            
        except Exception as e:
            logger.error(f"❌ Erro aplicando upgrade de biblioteca: {e}")
            return code, False

    def _apply_best_practice(self, code: str, suggestion: Dict) -> Tuple[str, bool]:
        """Aplica melhores práticas"""
        try:
            practice = suggestion.get('practice', '')
            
            # List comprehensions
            if 'list comprehension' in practice.lower():
                # Procurar padrões de loop simples que podem ser list comprehension
                loop_pattern = r'(\w+)\s*=\s*\[\]\s*\n\s*for\s+(\w+)\s+in\s+(\w+):\s*\n\s*\1\.append\(([^)]+)\)'
                
                def replace_with_comprehension(match):
                    result_var, item_var, iterable, expression = match.groups()
                    return f'{result_var} = [{expression} for {item_var} in {iterable}]'
                
                modified_code = re.sub(loop_pattern, replace_with_comprehension, code, flags=re.MULTILINE)
                
                if modified_code != code:
                    logger.info("🔄 Loop convertido para list comprehension")
                    return modified_code, True

            # F-strings
            if 'f-string' in practice.lower():
                # Substituir .format() por f-strings (casos simples)
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

    def _apply_performance_optimization(self, code: str, suggestion: Dict) -> Tuple[str, bool]:
        """Aplica otimizações de performance"""
        try:
            description = suggestion.get('description', '')
            
            # Otimizar concatenação de strings em loops
            if 'string concatenation' in description.lower():
                # Procurar padrões de concatenação em loops
                concat_pattern = r'(\w+)\s*=\s*["\']["\']?\s*\n\s*for\s+\w+\s+in\s+\w+:\s*\n\s*\1\s*\+=\s*'
                
                if re.search(concat_pattern, code, re.MULTILINE):
                    # Sugerir uso de join (implementação básica)
                    logger.info("💡 Padrão de concatenação de string em loop detectado")
                    # Por simplicidade, apenas log a detecção
                    return code, False

            return code, False
            
        except Exception as e:
            logger.error(f"❌ Erro aplicando otimização: {e}")
            return code, False

    def _apply_syntax_fix(self, code: str, suggestion: Dict) -> Tuple[str, bool]:
        """Aplica correções de sintaxe"""
        try:
            if 'line' in suggestion and 'message' in suggestion:
                line_num = suggestion['line']
                lines = code.split('\n')
                
                if line_num <= len(lines):
                    # Correções simples baseadas na mensagem
                    message = suggestion['message'].lower()
                    
                    if 'unused import' in message:
                        # Remover import não utilizado
                        import_line = lines[line_num - 1]
                        if 'import' in import_line:
                            lines[line_num - 1] = f"# {import_line}  # Removido: import não utilizado"
                            modified_code = '\n'.join(lines)
                            logger.info(f"🔄 Import não utilizado comentado na linha {line_num}")
                            return modified_code, True
                    
                    elif 'line too long' in message:
                        # Quebrar linha longa (implementação básica)
                        long_line = lines[line_num - 1]
                        if len(long_line) > 120:
                            # Tentar quebrar na vírgula mais próxima do meio
                            mid_point = len(long_line) // 2
                            comma_pos = long_line.rfind(',', 0, mid_point + 20)
                            
                            if comma_pos > 0:
                                part1 = long_line[:comma_pos + 1]
                                part2 = '    ' + long_line[comma_pos + 1:].lstrip()
                                lines[line_num - 1] = part1
                                lines.insert(line_num, part2)
                                modified_code = '\n'.join(lines)
                                logger.info(f"🔄 Linha longa quebrada na linha {line_num}")
                                return modified_code, True

            return code, False
            
        except Exception as e:
            logger.error(f"❌ Erro aplicando correção de sintaxe: {e}")
            return code, False

    def rollback_changes(self, file_path: str) -> Dict:
        """Desfaz a última correção aplicada em um arquivo"""
        try:
            # Encontrar a correção mais recente para este arquivo
            recent_correction = None
            for correction in reversed(self.correction_history):
                if correction.get('file_path') == file_path and correction.get('success'):
                    recent_correction = correction
                    break
            
            if not recent_correction:
                return {"error": f"Nenhuma correção recente encontrada para {file_path}"}
            
            backup_path = recent_correction.get('backup_path')
            if backup_path and os.path.exists(backup_path):
                self._restore_backup(file_path, backup_path)
                
                rollback_record = {
                    "file_path": file_path,
                    "timestamp": datetime.now().isoformat(),
                    "restored_from": backup_path,
                    "success": True
                }
                
                logger.info(f"🔄 Rollback realizado para {file_path}")
                return rollback_record
            else:
                return {"error": f"Backup não encontrado: {backup_path}"}
                
        except Exception as e:
            logger.error(f"❌ Erro no rollback: {e}")
            return {"error": str(e)}

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
        total_changes = sum(c.get('lines_changed', 0) for c in self.correction_history)
        
        report += f"🔧 Total de correções: {total_corrections}\n"
        report += f"✅ Correções bem-sucedidas: {successful_corrections}\n"
        report += f"📝 Total de linhas modificadas: {total_changes}\n\n"
        
        # Últimas 5 correções
        recent_corrections = self.correction_history[-5:]
        for i, correction in enumerate(recent_corrections, 1):
            file_name = os.path.basename(correction.get('file_path', 'unknown'))
            timestamp = correction.get('timestamp', '')[:19]
            applied_count = len(correction.get('applied_corrections', []))
            
            report += f"🔧 CORREÇÃO {i} - {timestamp}:\n"
            report += f"   📄 Arquivo: {file_name}\n"
            report += f"   ✅ Melhorias aplicadas: {applied_count}\n"
            
            for improvement in correction.get('applied_corrections', [])[:2]:
                improvement_type = improvement.get('type', 'unknown')
                report += f"      - {improvement_type}\n"
            
            report += "\n"
        
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
