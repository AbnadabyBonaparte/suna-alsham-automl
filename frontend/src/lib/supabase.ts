import { createClient } from '@supabase/supabase-js';

// Hardcode temporário para garantir funcionamento
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://vktzdrsigrdnemdshcdp.supabase.co';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZrdHpkcnNpZ3JkbmVtZHNoY2RwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI4MzMyODksImV4cCI6MjA2ODQwOTI4OX0.W5n4HbmQqUcGe_tmRPBBfiDhVWcDwK6KF8FrQiR11jc';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
