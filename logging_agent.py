async def _monitor_log_source(self, source_id: str, source_info: Dict[str, Any]):
        """
        Monitora uma fonte de logs específica com tail e parsing inteligente.
        Implementação enterprise com buffer circular e detecção de padrões.
        """
        try:
            # Se source_info é string, converter para dict
            if isinstance(source_info, str):
                source_info = {
                    'path': source_info,
                    'type': 'file' if source_info.startswith('/') or source_info.endswith('.log') else 'stream',
                    'status': 'unknown',
                    'last_position': 0
                }
            
            source_type = source_info.get('type', 'file')
            
            if source_type == 'file':
                file_path = Path(source_info['path'])
                
                # Verificar se arquivo existe
                if not file_path.exists():
                    if not file_path.parent.exists():
                        file_path.parent.mkdir(parents=True, exist_ok=True)
                    # Criar arquivo vazio se não existe
                    file_path.touch()
                    logger.info(f"📝 Arquivo de log criado: {file_path}")
                
                # Obter posição anterior ou iniciar do fim
                last_position = source_info.get('last_position', 0)
                
                # Se primeira vez, começar do fim do arquivo
                if last_position == 0:
                    last_position = file_path.stat().st_size
                    source_info['last_position'] = last_position
                
                # Abrir arquivo e ler novas linhas
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    # Ir para última posição conhecida
                    f.seek(last_position)
                    
                    # Ler novas linhas
                    new_lines = []
                    for line in f:
                        line = line.strip()
                        if line:  # Ignorar linhas vazias
                            new_lines.append(line)
                    
                    # Atualizar posição
                    source_info['last_position'] = f.tell()
                    
                    # Processar novas linhas se houver
                    if new_lines:
                        await self._process_new_log_lines(source_id, source_info, new_lines)
                
                # Atualizar status
                source_info['status'] = 'active'
                source_info['last_check'] = datetime.now()
                
            elif source_type == 'stream':
                # Monitoramento de stdout/stderr (implementação simplificada)
                logger.debug(f"Stream monitoring para {source_id} não implementado ainda")
                source_info['status'] = 'not_implemented'
                
        except PermissionError:
            logger.error(f"❌ Sem permissão para ler: {source_info.get('path', source_id)}")
            source_info['status'] = 'permission_denied'
        except Exception as e:
            logger.error(f"❌ Erro monitorando {source_id}: {e}")
            source_info['status'] = 'error'
            source_info['error'] = str(e)

    async def _process_new_log_lines(self, source_id: str, source_info: Dict[str, Any], lines: List[str]):
        """
        Processa novas linhas de log com parsing e análise inteligente.
        Detecta formatos automaticamente e aplica parsing apropriado.
        """
        try:
            for line in lines:
                # Tentar diferentes parsers
                log_entry = None
                
                # 1. Tentar formato JSON
                if line.startswith('{'):
                    try:
                        log_data = json.loads(line)
                        log_entry = self._parse_log_entry(log_data)
                    except json.JSONDecodeError:
                        pass
                
                # 2. Tentar formato syslog
                if not log_entry:
                    log_entry = self._parse_syslog_format(line)
                
                # 3. Tentar formato comum de aplicação
                if not log_entry:
                    log_entry = self._parse_common_format(line)
                
                # 4. Fallback - criar entrada genérica
                if not log_entry:
                    log_entry = LogEntry(
                        timestamp=datetime.now(),
                        level=LogLevel.INFO,
                        source=source_id,
                        message=line,
                        metadata={'raw_line': line, 'parse_failed': True}
                    )
                
                # Adicionar ao buffer
                self.log_buffer.append(log_entry)
                self.processed_logs.append(log_entry)
                self.processing_metrics['logs_processed'] += 1
                
                # Análise em tempo real para logs críticos
                if log_entry.level in [LogLevel.CRITICAL, LogLevel.ERROR]:
                    await self._real_time_analysis(log_entry)
                    
        except Exception as e:
            logger.error(f"❌ Erro processando linhas de log: {e}")

    def _parse_syslog_format(self, line: str) -> Optional[LogEntry]:
        """Parser para formato syslog"""
        try:
            # Padrão syslog comum: Mon DD HH:MM:SS hostname process[pid]: message
            syslog_pattern = re.compile(
                r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\S+?)(?:\[(\d+)\])?: (.*)$'
            )
            match = syslog_pattern.match(line)
            
            if match:
                timestamp_str, hostname, process, pid, message = match.groups()
                
                # Parse timestamp (assumir ano atual)
                current_year = datetime.now().year
                timestamp = datetime.strptime(f"{current_year} {timestamp_str}", "%Y %b %d %H:%M:%S")
                
                # Determinar nível baseado no conteúdo
                level = self._detect_log_level(message)
                
                return LogEntry(
                    timestamp=timestamp,
                    level=level,
                    source=process,
                    message=message,
                    component=hostname,
                    thread_id=pid,
                    metadata={'format': 'syslog', 'raw': line}
                )
                
        except Exception:
            pass
        
        return None

    def _parse_common_format(self, line: str) -> Optional[LogEntry]:
        """Parser para formato comum de aplicação"""
        try:
            # Padrões comuns: [TIMESTAMP] LEVEL - SOURCE: MESSAGE
            patterns = [
                # Pattern 1: [2024-01-01 12:00:00] ERROR - ComponentName: Message
                re.compile(r'^\[([^\]]+)\]\s+(\w+)\s*-\s*(\w+):\s*(.*)$'),
                # Pattern 2: 2024-01-01 12:00:00 ERROR ComponentName: Message
                re.compile(r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(\w+)\s+(\w+):\s*(.*)$'),
                # Pattern 3: ERROR [ComponentName] Message
                re.compile(r'^(\w+)\s+\[([^\]]+)\]\s+(.*)$'),
            ]
            
            for pattern in patterns:
                match = pattern.match(line)
                if match:
                    groups = match.groups()
                    
                    # Diferentes formatos têm diferentes ordens
                    if len(groups) == 4:  # Patterns 1 e 2
                        timestamp_str, level_str, source, message = groups
                        timestamp = self._parse_timestamp(timestamp_str)
                    elif len(groups) == 3:  # Pattern 3
                        level_str, source, message = groups
                        timestamp = datetime.now()
                    else:
                        continue
                    
                    # Parse level
                    try:
                        level = LogLevel(level_str.upper())
                    except ValueError:
                        level = self._detect_log_level(level_str + " " + message)
                    
                    return LogEntry(
                        timestamp=timestamp,
                        level=level,
                        source=source,
                        message=message,
                        metadata={'format': 'common', 'raw': line}
                    )
                    
        except Exception:
            pass
        
        return None

    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse de timestamp em vários formatos"""
        formats = [
            '%Y-%m-%d %H:%M:%S,%f',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%d %H:%M:%S',
            '%d/%b/%Y:%H:%M:%S',
            '%b %d %H:%M:%S'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue
        
        # Se nenhum formato funcionar, retornar agora
        return datetime.now()

    def _detect_log_level(self, text: str) -> LogLevel:
        """Detecta nível de log baseado no conteúdo"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['critical', 'fatal', 'panic']):
            return LogLevel.CRITICAL
        elif any(word in text_lower for word in ['error', 'err', 'exception', 'fail']):
            return LogLevel.ERROR
        elif any(word in text_lower for word in ['warning', 'warn']):
            return LogLevel.WARNING
        elif any(word in text_lower for word in ['debug', 'trace']):
            return LogLevel.DEBUG
        else:
            return LogLevel.INFO

    async def _process_log_buffer(self):
        """Processa buffer de logs acumulados"""
        try:
            # Processar em lotes para eficiência
            batch_size = 100
            processed_count = 0
            
            while len(self.log_buffer) > 0 and processed_count < batch_size:
                # Pegar próximo log (FIFO)
                if self.log_buffer:
                    log_entry = self.log_buffer.popleft()
                    
                    # Aplicar filtros e agregação
                    if await self._should_process_log(log_entry):
                        # Análise adicional se necessário
                        await self._analyze_log_entry(log_entry)
                        
                        processed_count += 1
                        
        except Exception as e:
            logger.error(f"❌ Erro processando buffer de logs: {e}")

    async def _should_process_log(self, log_entry: LogEntry) -> bool:
        """Determina se log deve ser processado baseado em filtros"""
        # Aplicar noise reduction
        if self.aggregation_rules['noise_reduction']['enabled']:
            for ignore_pattern in self.aggregation_rules['noise_reduction']['ignore_patterns']:
                if re.search(ignore_pattern, log_entry.message, re.IGNORECASE):
                    return False
        
        # Rate limiting
        rate_limit = self.aggregation_rules['noise_reduction']['rate_limit']
        # TODO: Implementar rate limiting por fonte
        
        return True

    async def _analyze_log_entry(self, log_entry: LogEntry):
        """Análise adicional de entrada de log"""
        # Atualizar baselines de componente
        if log_entry.source not in self.component_baselines:
            self.component_baselines[log_entry.source] = {
                'first_seen': datetime.now(),
                'log_count': 0,
                'error_count': 0,
                'last_seen': datetime.now()
            }
        
        baseline = self.component_baselines[log_entry.source]
        baseline['log_count'] += 1
        baseline['last_seen'] = datetime.now()
        
        if log_entry.level == LogLevel.ERROR:
            baseline['error_count'] += 1

    async def _identify_patterns(self) -> List[LogPattern]:
        """Identifica novos padrões nos logs"""
        new_patterns = []
        
        try:
            # Analisar logs recentes
            recent_logs = list(self.processed_logs)[-1000:]  # Últimos 1000 logs
            
            # Agrupar mensagens similares
            message_groups = defaultdict(list)
            
            for log in recent_logs:
                # Normalizar mensagem
                normalized = self._normalize_message(log.message)
                message_groups[normalized].append(log)
            
            # Identificar padrões frequentes
            for pattern, logs in message_groups.items():
                if len(logs) >= 5:  # Padrão deve aparecer pelo menos 5 vezes
                    # Verificar se é um novo padrão
                    pattern_id = hashlib.md5(pattern.encode()).hexdigest()[:8]
                    
                    if pattern_id not in self.known_patterns:
                        # Determinar severidade baseada nos logs
                        severity = self._determine_pattern_severity(logs)
                        
                        new_pattern = LogPattern(
                            pattern_id=pattern_id,
                            pattern_type='recurring',
                            regex=pattern,
                            frequency=len(logs),
                            last_seen=max(log.timestamp for log in logs),
                            severity=severity,
                            description=f"Padrão recorrente: {pattern[:100]}...",
                            examples=[log.message for log in logs[:3]]
                        )
                        
                        self.known_patterns[pattern_id] = new_pattern
                        new_patterns.append(new_pattern)
                        
        except Exception as e:
            logger.error(f"❌ Erro identificando padrões: {e}")
            
        return new_patterns

    def _normalize_message(self, message: str) -> str:
        """Normaliza mensagem para detecção de padrões"""
        # Remover números
        normalized = re.sub(r'\d+', 'N', message)
        # Remover IDs hexadecimais
        normalized = re.sub(r'[a-f0-9]{8,}', 'ID', normalized)
        # Remover IPs
        normalized = re.sub(r'\d+\.\d+\.\d+\.\d+', 'IP', normalized)
        # Remover paths
        normalized = re.sub(r'[/\\][\w/\\]+', 'PATH', normalized)
        
        return normalized

    def _determine_pattern_severity(self, logs: List[LogEntry]) -> AlertSeverity:
        """Determina severidade de um padrão baseado nos logs"""
        # Contar níveis
        level_counts = defaultdict(int)
        for log in logs:
            level_counts[log.level] += 1
        
        # Determinar severidade baseada nos níveis predominantes
        if level_counts[LogLevel.CRITICAL] > 0:
            return AlertSeverity.CRITICAL
        elif level_counts[LogLevel.ERROR] > len(logs) * 0.5:
            return AlertSeverity.HIGH
        elif level_counts[LogLevel.WARNING] > len(logs) * 0.5:
            return AlertSeverity.MEDIUM
        else:
            return AlertSeverity.LOW

    async def _update_patterns(self, new_patterns: List[LogPattern]):
        """Atualiza padrões conhecidos"""
        for pattern in new_patterns:
            logger.info(f"📊 Novo padrão identificado: {pattern.pattern_id} - {pattern.description}")
            
            # Notificar sobre padrões de alta severidade
            if pattern.severity in [AlertSeverity.CRITICAL, AlertSeverity.HIGH]:
                await self._notify_new_pattern(pattern)

    async def _notify_new_pattern(self, pattern: LogPattern):
        """Notifica sobre novo padrão identificado"""
        notification = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="orchestrator_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.MEDIUM,
            content={
                'notification_type': 'new_log_pattern',
                'pattern': {
                    'id': pattern.pattern_id,
                    'type': pattern.pattern_type,
                    'frequency': pattern.frequency,
                    'severity': pattern.severity.value,
                    'description': pattern.description,
                    'examples': pattern.examples
                }
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(notification)

    async def _generate_periodic_report(self):
        """Gera relatório periódico de logs"""
        try:
            # Calcular período
            now = datetime.now()
            period_start = now - timedelta(hours=1)
            
            # Filtrar logs do período
            period_logs = [
                log for log in self.processed_logs 
                if log.timestamp >= period_start
            ]
            
            if not period_logs:
                return
            
            # Calcular métricas
            metrics = self._calculate_log_metrics(period_logs, period_start, now)
            
            # Coletar anomalias do período
            period_anomalies = [
                anomaly for anomaly in self.anomaly_history
                if anomaly.detected_at >= period_start
            ]
            
            # Coletar padrões ativos
            active_patterns = [
                pattern for pattern in self.known_patterns.values()
                if pattern.last_seen >= period_start
            ]
            
            # Gerar recomendações
            recommendations = self._generate_recommendations(metrics, period_anomalies)
            
            # Calcular health score
            health_score = self._calculate_health_score(metrics, period_anomalies)
            
            # Criar relatório
            report = LogReport(
                report_id=f"report_{now.timestamp()}",
                period_start=period_start,
                period_end=now,
                total_processed=len(period_logs),
                metrics=metrics,
                anomalies=period_anomalies,
                patterns=active_patterns,
                recommendations=recommendations,
                health_score=health_score
            )
            
            # Salvar e notificar
            await self._save_report(report)
            
        except Exception as e:
            logger.error(f"❌ Erro gerando relatório: {e}")

    def _calculate_log_metrics(self, logs: List[LogEntry], start: datetime, end: datetime) -> LogMetrics:
        """Calcula métricas dos logs"""
        # Contar por nível
        entries_by_level = defaultdict(int)
        for log in logs:
            entries_by_level[log.level] += 1
        
        # Top sources
        source_counts = defaultdict(int)
        for log in logs:
            source_counts[log.source] += 1
        top_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Top messages (normalizadas)
        message_counts = defaultdict(int)
        for log in logs:
            normalized = self._normalize_message(log.message)[:50]  # Primeiros 50 chars
            message_counts[normalized] += 1
        top_messages = sorted(message_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Taxas
        total = len(logs)
        error_rate = entries_by_level[LogLevel.ERROR] / total if total > 0 else 0
        warning_rate = entries_by_level[LogLevel.WARNING] / total if total > 0 else 0
        
        return LogMetrics(
            total_entries=total,
            entries_by_level=dict(entries_by_level),
            error_rate=error_rate,
            warning_rate=warning_rate,
            top_sources=top_sources,
            top_messages=top_messages,
            time_range=(start, end),
            anomalies_detected=len([a for a in self.anomaly_history if start <= a.detected_at <= end])
        )

    def _generate_recommendations(self, metrics: LogMetrics, anomalies: List[LogAnomaly]) -> List[str]:
        """Gera recomendações baseadas nas métricas e anomalias"""
        recommendations = []
        
        # Baseado em taxa de erro
        if metrics.error_rate > 0.1:
            recommendations.append("Taxa de erro muito alta (>10%). Investigar causa raiz urgentemente.")
        elif metrics.error_rate > 0.05:
            recommendations.append("Taxa de erro elevada (>5%). Monitorar de perto.")
        
        # Baseado em anomalias
        critical_anomalies = [a for a in anomalies if a.severity == AlertSeverity.CRITICAL]
        if critical_anomalies:
            recommendations.append(f"{len(critical_anomalies)} anomalias críticas detectadas. Ação imediata necessária.")
        
        # Baseado em top sources
        if metrics.top_sources and metrics.top_sources[0][1] > metrics.total_entries * 0.5:
            recommendations.append(f"Componente {metrics.top_sources[0][0]} gerando >50% dos logs. Verificar verbosidade.")
        
        # Recomendações gerais
        if not recommendations:
            recommendations.append("Sistema operando dentro dos parâmetros normais.")
        
        return recommendations

    def _calculate_health_score(self, metrics: LogMetrics, anomalies: List[LogAnomaly]) -> float:
        """Calcula score de saúde do sistema baseado nos logs"""
        score = 100.0
        
        # Penalizar por taxa de erro
        score -= metrics.error_rate * 100 * 2  # -2 pontos por cada 1% de erro
        
        # Penalizar por anomalias
        for anomaly in anomalies:
            if anomaly.severity == AlertSeverity.CRITICAL:
                score -= 10
            elif anomaly.severity == AlertSeverity.HIGH:
                score -= 5
            elif anomaly.severity == AlertSeverity.MEDIUM:
                score -= 2
        
        # Garantir score entre 0 e 100
        return max(0.0, min(100.0, score))

    async def _save_report(self, report: LogReport):
        """Salva relatório de logs"""
        # TODO: Implementar persistência de relatórios
        logger.info(f"📊 Relatório gerado: Health Score = {report.health_score:.1f}%")

    async def _apply_aggregation_rules(self):
        """Aplica regras de agregação aos logs"""
        # TODO: Implementar agregação completa
        pass

    async def _noise_reduction(self):
        """Reduz ruído nos logs"""
        # TODO: Implementar redução de ruído
        pass

    async def _intelligent_grouping(self):
        """Agrupa logs similares inteligentemente"""
        # TODO: Implementar agrupamento inteligente
        pass

    async def _archive_old_logs(self):
        """Arquiva logs antigos comprimidos"""
        try:
            # Criar diretório de arquivo se não existir
            archive_dir = Path("./logs/archive")
            archive_dir.mkdir(parents=True, exist_ok=True)
            
            # Logs mais antigos que 24 horas
            cutoff_time = datetime.now() - timedelta(hours=24)
            old_logs = [
                log for log in self.processed_logs 
                if log.timestamp < cutoff_time
            ]
            
            if len(old_logs) >= 1000:  # Arquivar se tiver muitos logs antigos
                # Criar arquivo com timestamp
                archive_file = archive_dir / f"logs_{cutoff_time.strftime('%Y%m%d_%H%M%S')}.json.gz"
                
                # Serializar e comprimir
                logs_data = [self._log_entry_to_dict(log) for log in old_logs]
                
                with gzip.open(archive_file, 'wt', encoding='utf-8') as f:
                    json.dump(logs_data, f)
                
                logger.info(f"📦 Arquivados {len(old_logs)} logs em {archive_file}")
                
                # Remover logs arquivados do buffer
                self.processed_logs = deque([
                    log for log in self.processed_logs 
                    if log.timestamp >= cutoff_time
                ], maxlen=50000)
                
        except Exception as e:
            logger.error(f"❌ Erro arquivando logs: {e}")

    async def _send_security_alert(self, alert: Dict[str, Any]):
        """Envia alerta de segurança"""
        message = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="security_guardian_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.CRITICAL,
            content={
                'notification_type': 'security_alert',
                'alert': alert
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(message)

    async def _send_performance_alert(self, alert: Dict[str, Any]):
        """Envia alerta de performance"""
        message = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="performance_monitor_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.HIGH,
            content={
                'notification_type': 'performance_alert',
                'alert': alert
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(message)

    async def _send_cascade_alert(self, alert: Dict[str, Any]):
        """Envia alerta de cascata de erros"""
        message = AgentMessage(
            id=str(uuid4()),
            sender_id=self.agent_id,
            recipient_id="orchestrator_001",
            message_type=MessageType.NOTIFICATION,
            priority=Priority.HIGH,
            content={
                'notification_type': 'error_cascade',
                'alert': alert
            },
            timestamp=datetime.now()
        )
        await self.message_bus.publish(message)

    async def analyze_logs(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa logs sob demanda"""
        # Implementação do método público analyze_logs
        return await self.search_logs(request_data)

    async def detect_anomalies_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detecta anomalias sob demanda"""
        anomalies = await self._detect_anomalies()
        return {
            'status': 'completed',
            'anomalies_found': len(anomalies),
            'anomalies': [self._anomaly_to_dict(a) for a in anomalies]
        }

    async def get_log_report(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Obtém relatório de logs"""
        # TODO: Implementar busca de relatórios salvos
        return {
            'status': 'completed',
            'message': 'Report generation in progress'
        }

    async def monitor_component(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Monitora componente específico"""
        component = request_data.get('component')
        if component:
            # Adicionar componente para monitoramento especial
            # TODO: Implementar monitoramento focado
            return {
                'status': 'monitoring',
                'component': component
            }
        return {'status': 'error', 'message': 'Component not specified'}

    async def _process_notification(self, content: Dict[str, Any]):
        """Processa notificações de outros agentes"""
        # TODO: Implementar processamento de notificações
        pass

    async def _monitor_log_source(self, source: str):
        """
        Wrapper para compatibilidade - converte string source para o formato esperado
        """
        # Converter source string para o formato de dict esperado
        source_info = {
            'path': source,
            'type': 'file' if source.startswith('/') or source.endswith('.log') else 'stream',
            'status': 'unknown',
            'last_position': 0
        }
        
        # Chamar o método real com source_id e source_info
        await self._monitor_log_source(source, source_info)
