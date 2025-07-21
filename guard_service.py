# 🔗 DASHBOARD INTEGRADO - CORREÇÃO DO LOOP INFINITO
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Serve o dashboard HTML completo diretamente - SEM REDIRECIONAMENTO"""
    
    # HTML COMPLETO INTEGRADO (baseado em https://pttywdii.gensparkspace.com/)
    dashboard_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SUNA-ALSHAM Enterprise Dashboard - Perfect </title>
    
    <!-- External Libraries -->
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.155.0/build/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.2/dist/gsap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/countup.js@2.0.7/dist/countUp.min.js"></script>
    
    <style>
        :root {
            --primary-gold: #FFD700;
            --primary-blue: #1E3A8A;
            --primary-cyan: #00F5FF;
            --primary-purple: #9333EA;
            --dark-bg: #0A0A0F;
            --card-bg: rgba(15, 15, 25, 0.85);
            --glass-bg: rgba(255, 255, 255, 0.05);
            --neon-glow: 0 0 20px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0A0A0F 0%, #1A1A2E 25%, #16213E 50%, #0E1B3C 75%, #0A0A0F 100%);
            color: white;
            overflow-x: hidden;
            min-height: 100vh;
            position: relative;
        }

        /* MEGA COUNTER STYLES */
        .mega-counter {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
            backdrop-filter: blur(30px);
            border: 2px solid rgba(255, 215, 0, 0.3);
            border-radius: 25px;
            padding: 3rem;
            text-align: center;
            box-shadow: 0 30px 60px rgba(255, 215, 0, 0.2);
            position: relative;
            overflow: hidden;
            margin: 2rem auto;
        }

        .mega-counter::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(from 0deg, transparent, rgba(0, 245, 255, 0.3), transparent);
            animation: energyRotate 4s linear infinite;
            z-index: -1;
        }

        .mega-counter-number {
            font-family: 'Orbitron', monospace;
            font-size: 6rem;
            font-weight: 900;
            background: linear-gradient(45deg, #FFD700, #00F5FF, #9333EA, #FFD700);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: holographicShift 3s ease-in-out infinite, pulseGlow 2s ease-in-out infinite;
            text-shadow: 0 0 50px rgba(255, 215, 0, 0.8);
            margin-bottom: 1rem;
        }

        .mega-counter-label {
            font-family: 'Orbitron', monospace;
            font-size: 1.5rem;
            color: #FFD700;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
            margin-bottom: 1rem;
        }

        .uptime-display {
            font-size: 1.2rem;
            color: #00F5FF;
            margin-bottom: 0.5rem;
        }

        /* MICRO UPDATE POPUP */
        .micro-update {
            position: fixed;
            top: 100px;
            right: 30px;
            background: rgba(0, 0, 0, 0.9);
            border: 2px solid;
            border-radius: 15px;
            padding: 15px 20px;
            backdrop-filter: blur(20px);
            z-index: 1000;
            transform: translateX(400px);
            animation: slideIn 0.5s ease-out forwards, slideOut 0.5s ease-out 3s forwards;
            min-width: 250px;
        }

        @keyframes slideIn {
            from { transform: translateX(400px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(400px); opacity: 0; }
        }

        @keyframes energyRotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @keyframes holographicShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        @keyframes pulseGlow {
            0%, 100% { 
                filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.5));
                transform: scale(1);
            }
            50% { 
                filter: drop-shadow(0 0 40px rgba(255, 215, 0, 0.8));
                transform: scale(1.05);
            }
        }

        /* Resto do CSS do dashboard... */
        .luxury-card {
            background: linear-gradient(135deg, 
                rgba(255, 255, 255, 0.08) 0%, 
                rgba(255, 255, 255, 0.04) 50%, 
                rgba(255, 255, 255, 0.08) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 20px;
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
            cursor: pointer;
        }

        .luxury-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 25px 50px rgba(255, 215, 0, 0.3);
            border-color: var(--primary-gold);
        }

        .data-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
        }
    </style>
</head>
<body>
    <div class="min-h-screen p-6 relative z-10">
        <!-- Header -->
        <header class="text-center mb-8">
            <h1 class="text-6xl font-bold mb-4" style="font-family: 'Orbitron', monospace; background: linear-gradient(45deg, #FFD700, #00F5FF, #9333EA); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                SUNA-ALSHAM
            </h1>
            <p class="text-xl text-gray-300 mb-6">Sistema Unificado Neural Avançado - Arquitetura Transcendental</p>
            <div class="text-4xl font-bold mb-4">R$ 1.430M</div>
        </header>

        <!-- MEGA CONTADOR -->
        <div class="mega-counter">
            <div class="mega-counter-number" id="mega-counter">0</div>
            <div class="mega-counter-label">CICLOS TOTAIS EXECUTADOS</div>
            <div class="uptime-display" id="uptime-display">Uptime: 0d 0h 0m</div>
            <div class="text-sm mt-2">
                <span id="cycles-per-second">0.000</span> ciclos/segundo •
                <span id="cycles-per-hour">12</span>/hora
            </div>
        </div>

        <!-- Cards dos Agentes -->
        <div class="data-grid mb-8">
            <!-- Core Agent -->
            <div class="luxury-card p-6 border-l-4 border-red-500" onclick="openAgentModal('core')">
                <h3 class="text-xl font-bold mb-4 text-red-400">
                    <i class="fas fa-brain mr-3"></i>Core Agent
                </h3>
                <div class="text-3xl font-bold text-yellow-400 mb-2" id="corePerformance">75.0%</div>
                <div class="text-lg text-green-400" id="coreImprovement">+0.0%</div>
                <div class="mt-4 space-y-2">
                    <div class="flex justify-between">
                        <span>Ciclos</span>
                        <span id="coreCycles">0</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Trials</span>
                        <span id="coreTrials">0</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Valor</span>
                        <span class="text-yellow-400">R$ 550k</span>
                    </div>
                </div>
            </div>

            <!-- Learn Agent -->
            <div class="luxury-card p-6 border-l-4 border-purple-500" onclick="openAgentModal('learn')">
                <h3 class="text-xl font-bold mb-4 text-purple-400">
                    <i class="fas fa-graduation-cap mr-3"></i>Learn Agent
                </h3>
                <div class="text-3xl font-bold text-yellow-400 mb-2" id="learnPerformance">83.1%</div>
                <div class="text-lg text-green-400" id="learnAccuracy">94.7%</div>
                <div class="mt-4 space-y-2">
                    <div class="flex justify-between">
                        <span>Ciclos</span>
                        <span id="learnCycles">0</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Status</span>
                        <span class="text-green-400">ATIVO</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Valor</span>
                        <span class="text-yellow-400">R$ 550k</span>
                    </div>
                </div>
            </div>

            <!-- Guard Agent -->
            <div class="luxury-card p-6 border-l-4 border-blue-500" onclick="openAgentModal('guard')">
                <h3 class="text-xl font-bold mb-4 text-blue-400">
                    <i class="fas fa-shield-alt mr-3"></i>Guard Agent
                </h3>
                <div class="text-3xl font-bold text-yellow-400 mb-2" id="guardUptime">99.9%</div>
                <div class="text-lg text-green-400">NORMAL</div>
                <div class="mt-4 space-y-2">
                    <div class="flex justify-between">
                        <span>Verificações</span>
                        <span id="guardChecks">0</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Incidentes</span>
                        <span id="guardIncidents">0</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Valor</span>
                        <span class="text-yellow-400">R$ 330k</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Event Log -->
        <div class="luxury-card p-6 mb-8">
            <h3 class="text-xl font-bold mb-4 text-cyan-400">
                <i class="fas fa-list mr-3"></i>Log de Eventos ao Vivo
            </h3>
            <div id="eventLog" class="space-y-2 max-h-60 overflow-y-auto">
                <!-- Eventos aparecerão aqui -->
            </div>
        </div>
    </div>

    <script>
        let ws = null;
        let countUp = null;

        // Conectar WebSocket
        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = protocol + '//' + window.location.host + '/ws';
            
            ws = new WebSocket(wsUrl);
            
            ws.onopen = function() {
                console.log('WebSocket conectado');
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                
                if (data.type === 'initial_data' || data.type === 'metrics_update') {
                    updateDashboard(data.data);
                }
                
                if (data.type === 'cycle_completed') {
                    addEventToLog(data);
                }
                
                if (data.type === 'micro_update') {
                    showMicroUpdate(data);
                }
            };
            
            ws.onclose = function() {
                console.log('WebSocket desconectado, tentando reconectar...');
                setTimeout(connectWebSocket, 5000);
            };
        }

        // Atualizar dashboard
        function updateDashboard(data) {
            // MEGA CONTADOR
            if (data.cycle_counter) {
                const totalCycles = data.cycle_counter.total_cycles || 0;
                
                if (countUp) {
                    countUp.update(totalCycles);
                } else {
                    countUp = new CountUp('mega-counter', totalCycles, {
                        duration: 2,
                        useGrouping: true,
                        separator: '.',
                        decimal: ','
                    });
                    countUp.start();
                }
                
                // Uptime
                const uptime = data.cycle_counter.uptime || {days: 0, hours: 0, minutes: 0};
                document.getElementById('uptime-display').textContent = 
                    `Uptime: ${uptime.days}d ${uptime.hours}h ${uptime.minutes}m`;
                
                // Ciclos por segundo
                const cyclesPerSecond = data.cycle_counter.cycles_per_second || 0;
                document.getElementById('cycles-per-second').textContent = cyclesPerSecond.toFixed(3);
                
                // Ciclos por hora
                const cyclesPerHour = data.cycle_counter.cycles_per_hour || 12;
                document.getElementById('cycles-per-hour').textContent = cyclesPerHour;
            }

            // Agentes
            if (data.agents) {
                // Core Agent
                if (data.agents.core) {
                    const corePerf = (data.agents.core.performance * 100);
                    document.getElementById('corePerformance').textContent = corePerf.toFixed(1) + '%';
                    document.getElementById('coreImprovement').textContent = '+' + data.agents.core.improvement.toFixed(1) + '%';
                    document.getElementById('coreCycles').textContent = data.agents.core.automl_cycles;
                    document.getElementById('coreTrials').textContent = data.agents.core.trials;
                }

                // Learn Agent
                if (data.agents.learn) {
                    const learnPerf = (data.agents.learn.performance * 100);
                    document.getElementById('learnPerformance').textContent = learnPerf.toFixed(1) + '%';
                    document.getElementById('learnAccuracy').textContent = data.agents.learn.accuracy.toFixed(1) + '%';
                    document.getElementById('learnCycles').textContent = data.agents.learn.training_cycles;
                }

                // Guard Agent
                if (data.agents.guard) {
                    document.getElementById('guardUptime').textContent = data.agents.guard.uptime.toFixed(1) + '%';
                    document.getElementById('guardChecks').textContent = data.agents.guard.checks;
                    document.getElementById('guardIncidents').textContent = data.agents.guard.incidents_detected;
                }
            }
        }

        // Mostrar micro update
        function showMicroUpdate(data) {
            const popup = document.createElement('div');
            popup.className = 'micro-update';
            popup.style.borderColor = data.color;
            popup.innerHTML = `
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5rem;">${data.icon}</span>
                    <div>
                        <div style="color: ${data.color}; font-weight: bold;">${data.message}</div>
                        <div style="color: #888; font-size: 0.9rem;">${data.agent.toUpperCase()} Agent</div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(popup);
            
            // Remover após 4 segundos
            setTimeout(() => {
                document.body.removeChild(popup);
            }, 4000);
        }

        // Adicionar evento ao log
        function addEventToLog(data) {
            const eventLog = document.getElementById('eventLog');
            const eventDiv = document.createElement('div');
            eventDiv.style.color = data.color;
            eventDiv.innerHTML = `
                <span style="color: #666;">[${data.timestamp}]</span>
                <span style="margin: 0 8px;">${data.icon}</span>
                ${data.message}
            `;
            
            eventLog.insertBefore(eventDiv, eventLog.firstChild);
            
            // Manter apenas 20 eventos
            while (eventLog.children.length > 20) {
                eventLog.removeChild(eventLog.lastChild);
            }
        }

        // Modal placeholder
        function openAgentModal(agent) {
            alert(`Modal do ${agent.toUpperCase()} Agent ainda não implementado nesta versão simplificada.`);
        }

        // Inicializar
        document.addEventListener('DOMContentLoaded', function() {
            connectWebSocket();
        });
    </script>
</body>
</html>"""
    
    return dashboard_html
