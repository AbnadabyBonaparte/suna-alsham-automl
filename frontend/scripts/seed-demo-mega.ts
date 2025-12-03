import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;
const supabase = createClient(supabaseUrl, supabaseKey);

// ⚠️ SUBSTITUIR PELO UUID REAL DO USUÁRIO DEMO
const DEMO_USER_ID = 'COLE_O_UUID_AQUI';

// =====================================================
// UTILITÁRIOS PARA GERAR DADOS REALISTAS
// =====================================================

// Gerar data aleatória nos últimos N dias
function randomDate(daysAgo: number): string {
  const date = new Date();
  date.setDate(date.getDate() - Math.floor(Math.random() * daysAgo));
  date.setHours(Math.floor(Math.random() * 24));
  date.setMinutes(Math.floor(Math.random() * 60));
  return date.toISOString();
}

// Gerar data sequencial para métricas (hora por hora)
function sequentialDate(hoursAgo: number): string {
  const date = new Date();
  date.setHours(date.getHours() - hoursAgo);
  return date.toISOString();
}

// Gerar valor monetário realista
function randomMoney(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min) + min);
}

// Escolher aleatório de array
function randomFrom<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

// Gerar ID único
function generateId(prefix: string, index: number): string {
  return `${prefix}-${String(index).padStart(4, '0')}`;
}

// =====================================================
// DADOS BASE PARA GERAÇÃO
// =====================================================

const COMPANIES = [
  'TechCorp Industries', 'Global Finance Ltd', 'StartupXYZ', 'MegaRetail Corp',
  'HealthTech Solutions', 'EduLearn Platform', 'AutoDrive Inc', 'CloudBase Systems',
  'SecureNet Defense', 'MediaStream Co', 'DataVault Analytics', 'GreenEnergy Corp',
  'SmartHome Systems', 'BioPharm Research', 'AeroSpace Dynamics', 'FinTech Innovations',
  'LogiChain Solutions', 'CyberShield Inc', 'QuantumAI Labs', 'NexGen Robotics',
  'VirtualReality Co', 'BlockChain Ventures', 'IoT Connected', 'MachineLearning Pro',
  'DeepData Analytics', 'CloudNative Corp', 'AgriTech Solutions', 'EdTech Global',
  'InsurTech Partners', 'PropTech Ventures', 'LegalTech Systems', 'HRTech Solutions',
  'MarTech Agency', 'SalesTech Pro', 'ServiceNow Partners', 'Workday Consultants',
  'Salesforce Experts', 'SAP Integrators', 'Oracle Partners', 'Microsoft Gold',
  'AWS Advanced', 'Google Cloud Premier', 'Azure Specialists', 'IBM Platinum',
  'Cisco Champions', 'Dell Technologies', 'HP Enterprise', 'Lenovo Business',
  'VMware Experts', 'RedHat Partners'
];

const CONTACT_NAMES = [
  'Sarah Chen', 'Michael Johnson', 'Emily Rodriguez', 'David Kim', 'Jessica Williams',
  'Robert Martinez', 'Amanda Thompson', 'Christopher Lee', 'Jennifer Garcia', 'Matthew Brown',
  'Ashley Davis', 'Daniel Wilson', 'Stephanie Moore', 'Andrew Taylor', 'Nicole Anderson',
  'Joshua Thomas', 'Samantha Jackson', 'Kevin White', 'Rachel Harris', 'Brandon Martin',
  'Michelle Robinson', 'Ryan Clark', 'Laura Lewis', 'Justin Walker', 'Christina Hall',
  'Tyler Allen', 'Heather Young', 'Aaron King', 'Megan Wright', 'Sean Lopez'
];

const DEAL_STAGES = ['discovery', 'qualification', 'proposal', 'negotiation', 'closed'];
const DEAL_STATUS = ['lead', 'negotiation', 'closed_won', 'closed_lost'];
const TICKET_STATUS = ['open', 'in_progress', 'resolved', 'closed'];
const TICKET_PRIORITY = ['low', 'normal', 'high', 'critical'];
const PLATFORMS = ['twitter', 'linkedin', 'instagram', 'facebook', 'youtube'];
const TRANSACTION_TYPES = ['payment', 'refund', 'subscription', 'upgrade', 'downgrade'];
const TRANSACTION_STATUS = ['completed', 'pending', 'failed', 'refunded'];

const TICKET_TITLES = [
  'Dashboard loading slowly', 'API rate limit exceeded', 'Feature request: Dark mode',
  'Export to PDF not working', 'Agent offline', 'Billing cycle question',
  'Slack integration broken', 'Mobile app crashes', 'Login issues on Safari',
  'Data sync delay', 'Report generation fails', 'Permission denied error',
  'Webhook not triggering', 'Email notifications delayed', 'Search not working',
  'Filter not saving', 'Chart rendering issue', 'Bulk import failing',
  'SSO configuration help', '2FA not working', 'API documentation unclear',
  'Rate limiting too strict', 'Timezone issues', 'Language translation missing',
  'Custom field not saving', 'Workflow automation stuck', 'Integration disconnected',
  'Data export incomplete', 'User management question', 'Role permissions issue'
];

const SOCIAL_CONTENT = [
  '🚀 ALSHAM QUANTUM just hit a new milestone!',
  'Our AI agents are getting smarter every day 🤖',
  'Enterprise-grade security for your business 🔒',
  'Real-time analytics that actually work ⚡',
  'Customer success story: 40% efficiency boost',
  'New feature alert: Advanced reporting 📊',
  'Behind the scenes of our neural network',
  'Tips for maximizing your CRM potential',
  'Industry trends we\'re watching closely',
  'Team spotlight: Meet our engineers',
  'Webinar recap: AI in enterprise',
  'Product update: Performance improvements',
  'Case study: Fortune 500 implementation',
  'Best practices for data management',
  'Security audit passed with flying colors',
  'New integration: Salesforce connector',
  'Customer feedback drives our roadmap',
  'Celebrating 1000+ active agents',
  'How we handle 1M+ requests daily',
  'The future of enterprise AI is here'
];

const AGENT_IDS = Array.from({ length: 139 }, (_, i) =>
  i === 0 ? 'ORCHESTRATOR_ALPHA' : `UNIT_${String(i).padStart(2, '0')}`
);

const AGENT_ACTIONS = [
  'Processed customer inquiry', 'Analyzed sales data', 'Generated report',
  'Optimized workflow', 'Detected anomaly', 'Escalated ticket',
  'Completed task assignment', 'Updated customer record', 'Synced external data',
  'Performed security scan', 'Balanced workload', 'Archived old records',
  'Sent automated notification', 'Validated data integrity', 'Executed scheduled job'
];

// =====================================================
// FUNÇÕES DE GERAÇÃO DE DADOS
// =====================================================

async function seedDeals(count: number = 100) {
  console.log(`💰 Seeding ${count} deals...`);

  // Limpar dados antigos do demo
  await supabase.from('deals').delete().eq('user_id', DEMO_USER_ID);

  const deals = [];
  for (let i = 1; i <= count; i++) {
    const status = randomFrom(DEAL_STATUS);
    const stage = status === 'closed_won' || status === 'closed_lost' ? 'closed' : randomFrom(DEAL_STAGES.slice(0, 4));
    const probability = status === 'closed_won' ? 100 : status === 'closed_lost' ? 0 : randomMoney(10, 95);
    const company = randomFrom(COMPANIES);
    const contact = randomFrom(CONTACT_NAMES);
    const createdAt = randomDate(180); // Últimos 6 meses

    deals.push({
      id: generateId('DEAL', i),
      user_id: DEMO_USER_ID,
      title: `${company} - Enterprise License`,
      client_name: company,
      contact_name: contact,
      contact_email: `${contact.toLowerCase().replace(' ', '.')}@${company.toLowerCase().replace(/\s+/g, '')}.com`,
      value: randomMoney(5000, 500000),
      probability,
      status,
      stage,
      expected_close_date: new Date(Date.now() + randomMoney(-30, 90) * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      notes: `Initial contact via ${randomFrom(['LinkedIn', 'Website', 'Referral', 'Conference', 'Cold outreach'])}. ${randomFrom(['High priority', 'Strategic account', 'Expansion opportunity', 'New territory', 'Competitive deal'])}.`,
      created_at: createdAt,
      updated_at: randomDate(30)
    });
  }

  // Inserir em batches de 50
  for (let i = 0; i < deals.length; i += 50) {
    const batch = deals.slice(i, i + 50);
    const { error } = await supabase.from('deals').insert(batch);
    if (error) console.error(`Deals batch ${i/50 + 1} error:`, error);
  }

  console.log(`✅ Deals seeded: ${count} records`);
}

async function seedSupportTickets(count: number = 80) {
  console.log(`🎫 Seeding ${count} support tickets...`);

  await supabase.from('support_tickets').delete().eq('user_id', DEMO_USER_ID);

  const tickets = [];
  for (let i = 1; i <= count; i++) {
    const status = randomFrom(TICKET_STATUS);
    const priority = randomFrom(TICKET_PRIORITY);
    const createdAt = randomDate(90); // Últimos 3 meses

    tickets.push({
      id: generateId('TKT', i),
      user_id: DEMO_USER_ID,
      title: randomFrom(TICKET_TITLES),
      description: `Customer reported issue with ${randomFrom(['dashboard', 'API', 'mobile app', 'integration', 'reports'])}. ${randomFrom(['Urgent fix needed', 'Affecting multiple users', 'First time occurrence', 'Recurring issue', 'Intermittent problem'])}.`,
      status,
      priority,
      category: randomFrom(['Technical', 'Billing', 'Feature Request', 'Bug Report', 'General Inquiry']),
      sentiment: randomMoney(10, 95),
      assigned_to: status !== 'open' ? randomFrom(AGENT_IDS.slice(0, 20)) : null,
      resolution_notes: status === 'resolved' || status === 'closed' ? 'Issue resolved after investigation. Root cause identified and fix deployed.' : null,
      created_at: createdAt,
      updated_at: status !== 'open' ? randomDate(14) : createdAt
    });
  }

  for (let i = 0; i < tickets.length; i += 50) {
    const batch = tickets.slice(i, i + 50);
    const { error } = await supabase.from('support_tickets').insert(batch);
    if (error) console.error(`Tickets batch ${i/50 + 1} error:`, error);
  }

  console.log(`✅ Support tickets seeded: ${count} records`);
}

async function seedSocialPosts(count: number = 150) {
  console.log(`📱 Seeding ${count} social posts...`);

  await supabase.from('social_posts').delete().eq('user_id', DEMO_USER_ID);

  const posts = [];
  for (let i = 1; i <= count; i++) {
    const platform = randomFrom(PLATFORMS);
    const likes = randomMoney(10, 500);
    const shares = Math.floor(likes * (Math.random() * 0.3));
    const comments = Math.floor(likes * (Math.random() * 0.15));

    posts.push({
      id: generateId('POST', i),
      user_id: DEMO_USER_ID,
      content: `${randomFrom(SOCIAL_CONTENT)} #ALSHAMQUANTUM #Enterprise #AI #CRM`,
      platform,
      engagement_score: likes + (shares * 2) + (comments * 3),
      sentiment_score: randomMoney(60, 98),
      likes,
      shares,
      comments,
      reach: likes * randomMoney(5, 20),
      impressions: likes * randomMoney(10, 50),
      scheduled_at: Math.random() > 0.7 ? randomDate(-7) : null,
      published_at: randomDate(90),
      created_at: randomDate(120),
      updated_at: randomDate(30)
    });
  }

  for (let i = 0; i < posts.length; i += 50) {
    const batch = posts.slice(i, i + 50);
    const { error } = await supabase.from('social_posts').insert(batch);
    if (error) console.error(`Posts batch ${i/50 + 1} error:`, error);
  }

  console.log(`✅ Social posts seeded: ${count} records`);
}

async function seedTransactions(count: number = 120) {
  console.log(`💳 Seeding ${count} transactions...`);

  await supabase.from('transactions').delete().eq('user_id', DEMO_USER_ID);

  const transactions = [];
  const plans = [
    { name: 'Starter', price: 99 },
    { name: 'Pro', price: 299 },
    { name: 'Enterprise', price: 999 },
    { name: 'White-Label', price: 2499 }
  ];

  for (let i = 1; i <= count; i++) {
    const type = randomFrom(TRANSACTION_TYPES);
    const plan = randomFrom(plans);
    const status = type === 'refund' ? 'refunded' : randomFrom(TRANSACTION_STATUS);

    transactions.push({
      id: generateId('TXN', i),
      user_id: DEMO_USER_ID,
      type,
      amount: type === 'refund' ? -plan.price : plan.price,
      currency: 'USD',
      status,
      description: `${plan.name} Plan - ${type === 'subscription' ? 'Monthly' : type === 'upgrade' ? 'Upgrade' : 'Payment'}`,
      payment_method: randomFrom(['credit_card', 'bank_transfer', 'paypal', 'crypto']),
      invoice_id: `INV-${Date.now()}-${i}`,
      created_at: randomDate(180),
      updated_at: randomDate(30)
    });
  }

  for (let i = 0; i < transactions.length; i += 50) {
    const batch = transactions.slice(i, i + 50);
    const { error } = await supabase.from('transactions').insert(batch);
    if (error) console.error(`Transactions batch ${i/50 + 1} error:`, error);
  }

  console.log(`✅ Transactions seeded: ${count} records`);
}

async function seedAgentLogs(count: number = 500) {
  console.log(`📝 Seeding ${count} agent logs...`);

  await supabase.from('agent_logs').delete().eq('user_id', DEMO_USER_ID);

  const logs = [];
  for (let i = 1; i <= count; i++) {
    const agentId = randomFrom(AGENT_IDS);
    const level = randomFrom(['info', 'info', 'info', 'warning', 'error']); // Mostly info

    logs.push({
      id: generateId('LOG', i),
      user_id: DEMO_USER_ID,
      agent_id: agentId,
      action: randomFrom(AGENT_ACTIONS),
      level,
      message: `Agent ${agentId} ${randomFrom(['completed', 'started', 'processed', 'handled', 'executed'])} ${randomFrom(['task', 'request', 'job', 'operation', 'workflow'])}`,
      metadata: JSON.stringify({
        duration_ms: randomMoney(50, 5000),
        memory_used: randomMoney(100, 500),
        cpu_percent: randomMoney(5, 80)
      }),
      created_at: randomDate(30)
    });
  }

  for (let i = 0; i < logs.length; i += 100) {
    const batch = logs.slice(i, i + 100);
    const { error } = await supabase.from('agent_logs').insert(batch);
    if (error) console.error(`Agent logs batch ${i/100 + 1} error:`, error);
  }

  console.log(`✅ Agent logs seeded: ${count} records`);
}

async function seedSystemMetrics(hoursBack: number = 720) { // 30 dias
  console.log(`📊 Seeding ${hoursBack} hours of system metrics...`);

  await supabase.from('system_metrics').delete().eq('user_id', DEMO_USER_ID);

  const metrics = [];
  for (let i = 0; i < hoursBack; i++) {
    // Simular variação realista ao longo do dia
    const hour = (24 - (i % 24)) % 24;
    const isBusinessHours = hour >= 9 && hour <= 18;
    const baseLoad = isBusinessHours ? 60 : 30;

    metrics.push({
      id: generateId('MET', i + 1),
      user_id: DEMO_USER_ID,
      metric_type: 'system_health',
      cpu_usage: baseLoad + randomMoney(-10, 25),
      memory_usage: baseLoad + randomMoney(-5, 20),
      disk_usage: 45 + randomMoney(-5, 15),
      network_in: randomMoney(100, 1000),
      network_out: randomMoney(50, 500),
      active_connections: isBusinessHours ? randomMoney(50, 200) : randomMoney(10, 50),
      requests_per_second: isBusinessHours ? randomMoney(100, 500) : randomMoney(20, 100),
      error_rate: Math.random() * 2, // 0-2% error rate
      response_time_avg: randomMoney(50, 200),
      health_score: 85 + randomMoney(-10, 15),
      created_at: sequentialDate(i)
    });
  }

  for (let i = 0; i < metrics.length; i += 100) {
    const batch = metrics.slice(i, i + 100);
    const { error } = await supabase.from('system_metrics').insert(batch);
    if (error) console.error(`System metrics batch ${i/100 + 1} error:`, error);
  }

  console.log(`✅ System metrics seeded: ${hoursBack} records (${hoursBack/24} days)`);
}

async function seedAchievements(count: number = 50) {
  console.log(`🏆 Seeding ${count} achievements...`);

  await supabase.from('achievements').delete().eq('user_id', DEMO_USER_ID);

  const achievementTemplates = [
    { name: 'First Login', description: 'Welcome to ALSHAM QUANTUM!', rarity: 'common', points: 10 },
    { name: 'Profile Complete', description: 'Completed your profile setup', rarity: 'common', points: 25 },
    { name: 'First Deal', description: 'Created your first deal', rarity: 'common', points: 50 },
    { name: 'Deal Closer', description: 'Closed 10 deals', rarity: 'uncommon', points: 100 },
    { name: 'Sales Champion', description: 'Closed 50 deals', rarity: 'rare', points: 250 },
    { name: 'Million Dollar Club', description: 'Total deal value exceeded $1M', rarity: 'epic', points: 500 },
    { name: 'Ticket Master', description: 'Resolved 100 support tickets', rarity: 'rare', points: 200 },
    { name: 'Social Butterfly', description: 'Published 50 social posts', rarity: 'uncommon', points: 75 },
    { name: 'Viral Sensation', description: 'Got 1000+ engagement on a post', rarity: 'rare', points: 150 },
    { name: 'Agent Commander', description: 'Managed 100+ agent tasks', rarity: 'epic', points: 300 },
    { name: 'Data Analyst', description: 'Exported 50 reports', rarity: 'uncommon', points: 100 },
    { name: 'Power User', description: 'Logged in 30 consecutive days', rarity: 'rare', points: 200 },
    { name: 'Integration Guru', description: 'Connected 5 external integrations', rarity: 'uncommon', points: 125 },
    { name: 'Security Expert', description: 'Enabled all security features', rarity: 'rare', points: 175 },
    { name: 'Quantum Master', description: 'Unlocked all system features', rarity: 'legendary', points: 1000 },
    { name: 'Early Adopter', description: 'Joined during beta phase', rarity: 'epic', points: 400 },
    { name: 'Feedback Champion', description: 'Submitted 10 feature requests', rarity: 'uncommon', points: 80 },
    { name: 'Team Player', description: 'Invited 5 team members', rarity: 'uncommon', points: 100 },
    { name: 'Automation Hero', description: 'Created 20 automated workflows', rarity: 'rare', points: 250 },
    { name: 'Customer Whisperer', description: '100% satisfaction on 50 tickets', rarity: 'epic', points: 350 }
  ];

  const achievements = [];
  for (let i = 0; i < Math.min(count, achievementTemplates.length); i++) {
    const template = achievementTemplates[i];
    achievements.push({
      id: generateId('ACH', i + 1),
      user_id: DEMO_USER_ID,
      name: template.name,
      description: template.description,
      rarity: template.rarity,
      points: template.points,
      icon: `🏆`,
      unlocked: Math.random() > 0.3, // 70% chance of being unlocked
      unlocked_at: Math.random() > 0.3 ? randomDate(180) : null,
      progress: Math.floor(Math.random() * 100),
      created_at: randomDate(180)
    });
  }

  const { error } = await supabase.from('achievements').insert(achievements);
  if (error) console.error('Achievements error:', error);

  console.log(`✅ Achievements seeded: ${achievements.length} records`);
}

async function seedNotifications(count: number = 200) {
  console.log(`🔔 Seeding ${count} notifications...`);

  await supabase.from('notifications').delete().eq('user_id', DEMO_USER_ID);

  const notificationTypes = [
    { type: 'deal_update', title: 'Deal Updated', message: 'Deal status changed to' },
    { type: 'ticket_new', title: 'New Ticket', message: 'New support ticket created:' },
    { type: 'ticket_resolved', title: 'Ticket Resolved', message: 'Support ticket resolved:' },
    { type: 'agent_alert', title: 'Agent Alert', message: 'Agent status changed:' },
    { type: 'system_update', title: 'System Update', message: 'System maintenance scheduled' },
    { type: 'achievement', title: 'Achievement Unlocked!', message: 'You earned a new badge:' },
    { type: 'mention', title: 'You were mentioned', message: 'Someone mentioned you in:' },
    { type: 'report_ready', title: 'Report Ready', message: 'Your report is ready to download' }
  ];

  const notifications = [];
  for (let i = 1; i <= count; i++) {
    const template = randomFrom(notificationTypes);

    notifications.push({
      id: generateId('NOT', i),
      user_id: DEMO_USER_ID,
      type: template.type,
      title: template.title,
      message: `${template.message} ${randomFrom(['Deal #123', 'Ticket #456', 'Agent UNIT_05', 'Report Q4'])}`,
      read: Math.random() > 0.4, // 60% read
      action_url: `/dashboard/${randomFrom(['deals', 'support', 'agents', 'analytics'])}`,
      created_at: randomDate(30)
    });
  }

  for (let i = 0; i < notifications.length; i += 50) {
    const batch = notifications.slice(i, i + 50);
    const { error } = await supabase.from('notifications').insert(batch);
    if (error) console.error(`Notifications batch ${i/50 + 1} error:`, error);
  }

  console.log(`✅ Notifications seeded: ${count} records`);
}

async function seedAuditLogs(count: number = 300) {
  console.log(`📋 Seeding ${count} audit logs...`);

  await supabase.from('audit_log').delete().eq('user_id', DEMO_USER_ID);

  const actions = [
    'CREATE', 'UPDATE', 'DELETE', 'VIEW', 'EXPORT', 'LOGIN', 'LOGOUT',
    'PERMISSION_CHANGE', 'SETTINGS_UPDATE', 'API_CALL'
  ];

  const resources = [
    'deal', 'ticket', 'agent', 'user', 'report', 'settings', 'integration', 'workflow'
  ];

  const logs = [];
  for (let i = 1; i <= count; i++) {
    logs.push({
      id: generateId('AUD', i),
      user_id: DEMO_USER_ID,
      action: randomFrom(actions),
      resource_type: randomFrom(resources),
      resource_id: generateId(randomFrom(['DEAL', 'TKT', 'UNIT']), randomMoney(1, 100)),
      old_value: JSON.stringify({ status: 'old_status' }),
      new_value: JSON.stringify({ status: 'new_status' }),
      ip_address: `192.168.${randomMoney(1, 255)}.${randomMoney(1, 255)}`,
      user_agent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
      created_at: randomDate(90)
    });
  }

  for (let i = 0; i < logs.length; i += 50) {
    const batch = logs.slice(i, i + 50);
    const { error } = await supabase.from('audit_log').insert(batch);
    if (error) console.error(`Audit logs batch ${i/50 + 1} error:`, error);
  }

  console.log(`✅ Audit logs seeded: ${count} records`);
}

async function seedRequests(count: number = 50) {
  console.log(`📝 Seeding ${count} requests...`);

  await supabase.from('requests').delete().eq('user_id', DEMO_USER_ID);

  const requestTypes = [
    { title: 'Generate monthly report', type: 'report' },
    { title: 'Export customer data', type: 'export' },
    { title: 'Bulk update contacts', type: 'batch' },
    { title: 'Sync external CRM', type: 'integration' },
    { title: 'Analyze sales trends', type: 'analysis' },
    { title: 'Train AI model', type: 'ml' },
    { title: 'Optimize agent performance', type: 'optimization' },
    { title: 'Security scan request', type: 'security' }
  ];

  const requests = [];
  for (let i = 1; i <= count; i++) {
    const template = randomFrom(requestTypes);
    const status = randomFrom(['queued', 'processing', 'completed', 'failed']);

    requests.push({
      id: generateId('REQ', i),
      user_id: DEMO_USER_ID,
      title: template.title,
      description: `Request for ${template.type} operation`,
      type: template.type,
      status,
      priority: randomFrom(['low', 'normal', 'high']),
      progress: status === 'completed' ? 100 : status === 'processing' ? randomMoney(10, 90) : 0,
      result: status === 'completed' ? JSON.stringify({ success: true, records_processed: randomMoney(100, 10000) }) : null,
      created_at: randomDate(60),
      updated_at: randomDate(14)
    });
  }

  const { error } = await supabase.from('requests').insert(requests);
  if (error) console.error('Requests error:', error);

  console.log(`✅ Requests seeded: ${count} records`);
}

async function createDemoProfile() {
  console.log(`👤 Creating demo profile...`);

  const { error } = await supabase.from('profiles').upsert({
    id: DEMO_USER_ID,
    auth_user_id: DEMO_USER_ID,
    username: 'demo_enterprise',
    full_name: 'Demo Enterprise Account',
    email: 'demo@alshamglobal.com',
    avatar_url: null,
    role: 'admin',
    company: 'ALSHAM GLOBAL Demo',
    department: 'Executive',
    timezone: 'America/Sao_Paulo',
    language: 'pt-BR',
    created_at: new Date(Date.now() - 180 * 24 * 60 * 60 * 1000).toISOString(), // 6 meses atrás
    updated_at: new Date().toISOString()
  });

  if (error) console.error('Profile error:', error);
  else console.log('✅ Demo profile created');
}

// =====================================================
// EXECUÇÃO PRINCIPAL
// =====================================================

async function main() {
  console.log('\n' + '='.repeat(60));
  console.log('🚀 ALSHAM QUANTUM - MEGA DEMO SEED');
  console.log('='.repeat(60) + '\n');

  if (DEMO_USER_ID === 'COLE_O_UUID_AQUI') {
    console.error('❌ ERROR: Substitua DEMO_USER_ID pelo UUID real!');
    console.log('\n📝 Passos:');
    console.log('1. Vá no Supabase Dashboard > Authentication > Users');
    console.log('2. Clique "Add User"');
    console.log('3. Email: demo@alshamglobal.com');
    console.log('4. Password: AlshamDemo2025!');
    console.log('5. Copie o UUID e cole neste script');
    console.log('6. Execute novamente\n');
    return;
  }

  const startTime = Date.now();

  try {
    // Criar profile primeiro
    await createDemoProfile();

    // Seed todos os dados
    await seedDeals(100);
    await seedSupportTickets(80);
    await seedSocialPosts(150);
    await seedTransactions(120);
    await seedAgentLogs(500);
    await seedSystemMetrics(720); // 30 dias
    await seedAchievements(20);
    await seedNotifications(200);
    await seedAuditLogs(300);
    await seedRequests(50);

    const duration = ((Date.now() - startTime) / 1000).toFixed(2);

    console.log('\n' + '='.repeat(60));
    console.log('🎉 MEGA SEED COMPLETO!');
    console.log('='.repeat(60));
    console.log(`\n⏱️  Tempo total: ${duration}s`);
    console.log('\n📊 Dados criados:');
    console.log('   • 100 deals (pipeline de vendas)');
    console.log('   • 80 support tickets');
    console.log('   • 150 social posts');
    console.log('   • 120 transactions');
    console.log('   • 500 agent logs');
    console.log('   • 720 system metrics (30 dias)');
    console.log('   • 20 achievements');
    console.log('   • 200 notifications');
    console.log('   • 300 audit logs');
    console.log('   • 50 requests');
    console.log('   ─────────────────');
    console.log('   📦 TOTAL: 2,340 registros\n');
    console.log('📧 Login: demo@alshamglobal.com');
    console.log('🔑 Senha: AlshamDemo2025!');
    console.log('='.repeat(60) + '\n');

  } catch (error) {
    console.error('❌ Fatal error:', error);
  }
}

main();
