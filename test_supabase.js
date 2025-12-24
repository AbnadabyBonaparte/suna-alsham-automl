const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = 'https://vktzdrsigrdnemdshcdp.supabase.co';
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZrdHpkcnNpZ3JkbmVtZHNoY2RwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI4MzMyODksImV4cCI6MjA2ODQwOTI4OX0.W5n4HbmQqUcGe_tmRPBBfiDhVWcDwK6KF8FrQiR11jc';

const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function testConnection() {
  console.log('🧪 TESTANDO CONEXÃO COM SUPABASE...');

  try {
    const { data, error } = await supabase
      .from('agents')
      .select('id, name, role, status')
      .limit(3);

    if (error) {
      console.log('❌ ERRO:', error.message);
    } else {
      console.log('✅ SUCESSO! Encontrados', data.length, 'agentes:');
      console.log(data);
    }
  } catch (err) {
    console.log('❌ ERRO DE CONEXÃO:', err.message);
  }
}

testConnection();
