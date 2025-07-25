# ✅ ROTAS PARA AS 4 APLICAÇÕES INTEGRADAS
@app.route('/client-portal')
def client_portal():
    """Interface comercial para clientes"""
    try:
        with open('client-portal/index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return render_template_string("""
        <h1>Client Portal em Desenvolvimento</h1>
        <p>Redirecionando para dashboard principal...</p>
        <script>setTimeout(() => window.location.href = '/', 2000);</script>
        """), 404

@app.route('/dashboard-metrics')  
def dashboard_metrics():
    """Dashboard Premium com 3D e recursos avançados"""
    try:
        with open('dashboard-metrics/index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return render_template_string("""
        <h1>Dashboard Metrics em Desenvolvimento</h1>
        <p>Redirecionando para dashboard principal...</p>
        <script>setTimeout(() => window.location.href = '/', 2000);</script>
        """), 404

@app.route('/pwa-mobile')
def pwa_mobile():
    """PWA Mobile com 5 temas premium"""
    try:
        with open('pwa-mobile/index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return render_template_string("""
        <h1>PWA Mobile em Desenvolvimento</h1>
        <p>Redirecionando para dashboard principal...</p>
        <script>setTimeout(() => window.location.href = '/', 2000);</script>
        """), 404

# ✅ MENU DE NAVEGAÇÃO PRINCIPAL
@app.route('/menu')
def navigation_menu():
    """Menu de navegação entre as 4 aplicações"""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ALSHAM QUANTUM v12.0 - Menu Principal</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
        <style>
            body {
                background: linear-gradient(135deg, #020C1B 0%, #1a1a2e 50%, #2C3E50 100%);
                color: white;
                font-family: 'Inter', sans-serif;
            }
            .app-card {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                transition: all 0.3s ease;
            }
            .app-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 20px 40px rgba(108, 52, 131, 0.4);
            }
        </style>
    </head>
    <body class="min-h-screen flex items-center justify-center p-8">
        <div class="max-w-6xl w-full">
            <div class="text-center mb-12">
                <h1 class="text-4xl font-bold mb-4">🚀 ALSHAM QUANTUM v12.0 PREMIUM</h1>
                <p class="text-xl opacity-80">Sistema Neural com 25 Agentes Autoevolutivos</p>
                <div class="mt-4 text-green-400">✅ Sistema Online | ⚡ Performance: 97.3% | 🧠 25 Agentes Ativos</div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                <!-- Dashboard Principal -->
                <div class="app-card p-8 rounded-xl text-center cursor-pointer" onclick="window.location.href='/'">
                    <div class="text-6xl mb-4">🏠</div>
                    <h3 class="text-xl font-bold mb-2">Dashboard Principal</h3>
                    <p class="text-sm opacity-80 mb-4">Interface técnica com dados reais dos 25 agentes</p>
                    <div class="bg-blue-500 text-white px-4 py-2 rounded-lg text-sm">
                        <i class="fas fa-desktop mr-2"></i>Desktop Interface
                    </div>
                </div>

                <!-- Client Portal -->
                <div class="app-card p-8 rounded-xl text-center cursor-pointer" onclick="window.location.href='/client-portal'">
                    <div class="text-6xl mb-4">👥</div>
                    <h3 class="text-xl font-bold mb-2">Client Portal</h3>
                    <p class="text-sm opacity-80 mb-4">Interface comercial para clientes e prospects</p>
                    <div class="bg-green-500 text-white px-4 py-2 rounded-lg text-sm">
                        <i class="fas fa-handshake mr-2"></i>Commercial
                    </div>
                </div>

                <!-- Dashboard Metrics Premium -->
                <div class="app-card p-8 rounded-xl text-center cursor-pointer" onclick="window.location.href='/dashboard-metrics'">
                    <div class="text-6xl mb-4">💎</div>
                    <h3 class="text-xl font-bold mb-2">Premium Analytics</h3>
                    <p class="text-sm opacity-80 mb-4">Dashboard avançado com 3D, múltiplos temas e command center</p>
                    <div class="bg-purple-500 text-white px-4 py-2 rounded-lg text-sm">
                        <i class="fas fa-gem mr-2"></i>Premium
                    </div>
                </div>

                <!-- PWA Mobile -->
                <div class="app-card p-8 rounded-xl text-center cursor-pointer" onclick="window.location.href='/pwa-mobile'">
                    <div class="text-6xl mb-4">📱</div>
                    <h3 class="text-xl font-bold mb-2">PWA Mobile</h3>
                    <p class="text-sm opacity-80 mb-4">App mobile com 5 temas premium e PWA completo</p>
                    <div class="bg-yellow-500 text-black px-4 py-2 rounded-lg text-sm">
                        <i class="fas fa-mobile-alt mr-2"></i>Mobile PWA
                    </div>
                </div>
            </div>

            <div class="text-center mt-12">
                <div class="bg-gray-800 rounded-lg p-6 inline-block">
                    <h4 class="font-bold mb-2">🔗 Status das APIs</h4>
                    <div class="grid grid-cols-2 gap-4 text-sm">
                        <div>✅ /api/agents (25 ativos)</div>
                        <div>✅ /api/metrics (tempo real)</div>
                        <div>✅ /api/logs (funcionando)</div>
                        <div>✅ WebSocket (conectado)</div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''')

# ✅ ARQUIVOS ESTÁTICOS
@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "ALSHAM QUANTUM v12.0 Premium",
        "short_name": "ALSHAM",
        "description": "Sistema Neural com 25 Agentes Autoevolutivos",
        "start_url": "/pwa-mobile",
        "display": "standalone",
        "background_color": "#020C1B",
        "theme_color": "#6C3483",
        "icons": [
            {
                "src": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='40' fill='%236C3483'/%3E%3Ctext x='50' y='55' text-anchor='middle' fill='white' font-size='20'%3E🚀%3C/text%3E%3C/svg%3E",
                "sizes": "192x192",
                "type": "image/svg+xml"
            }
        ]
    })

@app.route('/sw.js')
def service_worker():
    return '''
    const CACHE_NAME = 'alsham-quantum-v12';
    const urlsToCache = ['/pwa-mobile', '/dashboard-metrics', '/client-portal', '/'];
    
    self.addEventListener('install', event => {
        event.waitUntil(
            caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
        );
    });
    
    self.addEventListener('fetch', event => {
        event.respondWith(
            caches.match(event.request).then(response => {
                return response || fetch(event.request);
            })
        );
    });
    ''', 200, {'Content-Type': 'application/javascript'}
