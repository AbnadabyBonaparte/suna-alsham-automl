// service-worker.js - ALSHAM QUANTUM v11.0 PWA Service Worker
// Arquivo: central/pwa-mobile/service-worker.js

const CACHE_NAME = 'alsham-quantum-v11-cache';
const CACHE_VERSION = '1.0.0';
const FULL_CACHE_NAME = `${CACHE_NAME}-${CACHE_VERSION}`;

// Assets essenciais para cache
const ESSENTIAL_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  'https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css',
  'https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css',
  'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap',
  'https://cdn.jsdelivr.net/npm/chart.js',
  'https://cdn.jsdelivr.net/npm/three@0.158.0/build/three.min.js'
];

// APIs que devem ser cacheadas com estratégia Network First
const API_ENDPOINTS = [
  'https://suna-alsham-automl-production.up.railway.app/api/metrics',
  'https://suna-alsham-automl-production.up.railway.app/api/health',
  'https://suna-alsham-automl-production.up.railway.app/api/agents'
];

// === INSTALL EVENT ===
self.addEventListener('install', event => {
  console.log('🔧 ALSHAM QUANTUM SW: Installing Service Worker v11.0');
  
  event.waitUntil(
    caches.open(FULL_CACHE_NAME)
      .then(cache => {
        console.log('📦 ALSHAM QUANTUM SW: Caching essential assets');
        return cache.addAll(ESSENTIAL_ASSETS);
      })
      .then(() => {
        console.log('✅ ALSHAM QUANTUM SW: Installation complete');
        return self.skipWaiting();
      })
      .catch(error => {
        console.error('❌ ALSHAM QUANTUM SW: Installation failed:', error);
      })
  );
});

// === ACTIVATE EVENT ===
self.addEventListener('activate', event => {
  console.log('🚀 ALSHAM QUANTUM SW: Activating Service Worker v11.0');
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== FULL_CACHE_NAME) {
              console.log('🗑️ ALSHAM QUANTUM SW: Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('✅ ALSHAM QUANTUM SW: Activation complete');
        return self.clients.claim();
      })
  );
});

// === FETCH EVENT - Estratégias de Cache ===
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Ignorar requisições não HTTP/HTTPS
  if (!request.url.startsWith('http')) {
    return;
  }
  
  // Estratégia para APIs - Network First com Cache Fallback
  if (isAPIRequest(request.url)) {
    event.respondWith(networkFirstStrategy(request));
  }
  // Estratégia para assets estáticos - Cache First
  else if (isStaticAsset(request.url)) {
    event.respondWith(cacheFirstStrategy(request));
  }
  // Estratégia para HTML - Network First
  else {
    event.respondWith(networkFirstStrategy(request));
  }
});

// === BACKGROUND SYNC ===
self.addEventListener('sync', event => {
  console.log('🔄 ALSHAM QUANTUM SW: Background sync triggered:', event.tag);
  
  if (event.tag === 'metrics-sync') {
    event.waitUntil(syncMetrics());
  }
  
  if (event.tag === 'agents-sync') {
    event.waitUntil(syncAgentsData());
  }
});

// === PUSH NOTIFICATIONS ===
self.addEventListener('push', event => {
  console.log('🔔 ALSHAM QUANTUM SW: Push notification received');
  
  let data = {};
  if (event.data) {
    data = event.data.json();
  }
  
  const options = {
    body: data.body || 'Sistema ALSHAM QUANTUM atualizado!',
    icon: '/icon-192x192.png',
    badge: '/badge-72x72.png',
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: data.primaryKey || 'default'
    },
    actions: [
      {
        action: 'explore',
        title: 'Ver Dashboard',
        icon: '/action-icon.png'
      },
      {
        action: 'close',
        title: 'Fechar',
        icon: '/close-icon.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification(
      data.title || 'ALSHAM QUANTUM v11.0',
      options
    )
  );
});

// Manipular cliques em notificações
self.addEventListener('notificationclick', event => {
  console.log('🖱️ ALSHAM QUANTUM SW: Notification clicked:', event.action);
  
  event.notification.close();
  
  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// === UTILITY FUNCTIONS ===

// Verifica se é uma requisição de API
function isAPIRequest(url) {
  return API_ENDPOINTS.some(endpoint => url.includes(endpoint));
}

// Verifica se é um asset estático
function isStaticAsset(url) {
  return url.includes('.css') || 
         url.includes('.js') || 
         url.includes('fonts') ||
         url.includes('.png') ||
         url.includes('.jpg') ||
         url.includes('.svg');
}

// Estratégia Network First - Tenta rede primeiro, cache como fallback
async function networkFirstStrategy(request) {
  try {
    const networkResponse = await fetch(request);
    
    // Se a resposta é boa, atualiza o cache
    if (networkResponse.ok) {
      const responseClone = networkResponse.clone();
      const cache = await caches.open(FULL_CACHE_NAME);
      await cache.put(request, responseClone);
      
      console.log('🌐 ALSHAM QUANTUM SW: Network response cached:', request.url);
    }
    
    return networkResponse;
  } catch (error) {
    console.log('📡 ALSHAM QUANTUM SW: Network failed, trying cache:', request.url);
    
    const cachedResponse = await caches.match(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Se não tem cache, retorna página offline básica
    if (request.destination === 'document') {
      return caches.match('/offline.html') || createOfflineResponse();
    }
    
    throw error;
  }
}

// Estratégia Cache First - Cache primeiro, rede como fallback
async function cacheFirstStrategy(request) {
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    console.log('💾 ALSHAM QUANTUM SW: Serving from cache:', request.url);
    return cachedResponse;
  }
  
  console.log('🌐 ALSHAM QUANTUM SW: Cache miss, fetching:', request.url);
  return fetch(request);
}

// Sincronização de métricas em background
async function syncMetrics() {
  try {
    console.log('📊 ALSHAM QUANTUM SW: Syncing metrics data');
    
    const response = await fetch('https://suna-alsham-automl-production.up.railway.app/api/metrics');
    
    if (response.ok) {
      const cache = await caches.open(FULL_CACHE_NAME);
      await cache.put('/api/metrics', response.clone());
      
      console.log('✅ ALSHAM QUANTUM SW: Metrics synced successfully');
    }
  } catch (error) {
    console.error('❌ ALSHAM QUANTUM SW: Metrics sync failed:', error);
  }
}

// Sincronização de dados dos agentes
async function syncAgentsData() {
  try {
    console.log('🤖 ALSHAM QUANTUM SW: Syncing agents data');
    
    const response = await fetch('https://suna-alsham-automl-production.up.railway.app/api/agents');
    
    if (response.ok) {
      const cache = await caches.open(FULL_CACHE_NAME);
      await cache.put('/api/agents', response.clone());
      
      console.log('✅ ALSHAM QUANTUM SW: Agents data synced successfully');
    }
  } catch (error) {
    console.error('❌ ALSHAM QUANTUM SW: Agents sync failed:', error);
  }
}

// Cria resposta offline básica
function createOfflineResponse() {
  const offlineHTML = `
    
    
    
        
        
        ALSHAM QUANTUM - Offline
        
            body { 
                font-family: 'Inter', sans-serif; 
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                color: white; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                min-height: 100vh; 
                text-align: center;
                margin: 0;
            }
            .offline-container {
                max-width: 500px;
                padding: 2rem;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                border: 1px solid rgba(244, 208, 63, 0.3);
            }
            .icon { font-size: 4rem; margin-bottom: 1rem; color: #F4D03F; }
            .title { font-size: 2rem; font-weight: bold; margin-bottom: 1rem; }
            .message { font-size: 1.1rem; margin-bottom: 2rem; opacity: 0.8; }
            .retry-btn {
                background: linear-gradient(45deg, #F4D03F, #2ECC71);
                color: #020C1B;
                padding: 1rem 2rem;
                border: none;
                border-radius: 50px;
                font-weight: bold;
                cursor: pointer;
                font-size: 1rem;
            }
        
    
    
        
            📡
            ALSHAM QUANTUM
            
                Sistema funcionando offline com dados em cache.
                Conecte-se à internet para atualizações em tempo real.
            
            
                🔄 Tentar Novamente
            
        
    
    
  `;

  return new Response(offlineHTML, {
    headers: { 'Content-Type': 'text/html' }
  });
}

// Log de inicialização
console.log('🚀 ALSHAM QUANTUM Service Worker v11.0 - 24 Agentes Autoevolutivos');
console.log('📱 PWA Mobile com Cache Inteligente e Background Sync');
console.log('🔔 Push Notifications e Funcionamento Offline Habilitado');
