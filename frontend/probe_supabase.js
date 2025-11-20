const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

// Carrega chaves do .env.local manualmente
function loadEnv() {
    try {
        const envPath = path.resolve(process.cwd(), '.env.local');
        if (!fs.existsSync(envPath)) return null;
        const content = fs.readFileSync(envPath, 'utf8');
        const env = {};
        content.split('\n').forEach(line => {
            const [key, val] = line.split('=');
            if (key && val) env[key.trim()] = val.trim().replace(/"/g, '');
        });
        return env;
    } catch (e) { return null; }
}

async function testConnection() {
    console.log('\n📡 TESTANDO CONEXÃO SUPABASE...');
    const env = loadEnv();
    
    if (!env || !env.NEXT_PUBLIC_SUPABASE_URL) {
        console.log('❌ ERRO: Chaves não encontradas no .env.local');
        return;
    }

    console.log('🌐 URL:', env.NEXT_PUBLIC_SUPABASE_URL);
    const supabase = createClient(env.NEXT_PUBLIC_SUPABASE_URL, env.NEXT_PUBLIC_SUPABASE_ANON_KEY);

    // Tenta ler a tabela 'agents'
    const { data, error } = await supabase.from('agents').select('name, role').limit(3);

    if (error) {
        console.log('❌ FALHA NA CONEXÃO:', error.message);
        if (error.code === '42P01') console.log('👉 CAUSA PROVÁVEL: Tabela "agents" não foi criada no Supabase.');
    } else {
        console.log('✅ SUCESSO! Conectado ao Banco de Dados.');
        console.log('📊 Dados recebidos:', data.length > 0 ? data : 'Tabela vazia (mas funcional)');
    }
}

testConnection();
