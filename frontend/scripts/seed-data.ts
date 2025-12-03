import { createClient } from '@supabase/supabase-js';

// Supabase configuration
const supabaseUrl = 'https://vktzdrsigrdnemdshcdp.supabase.co';
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZrdHpkcnNpZ3JkbmVtZHNoY2RwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI4MzMyODksImV4cCI6MjA2ODQwOTI4OX0.W5n4HbmQqUcGe_tmRPBBfiDhVWcDwK6KF8FrQiR11jc';

const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Seed data for DEALS
const deals = [
  {
    id: 'DEAL-001',
    title: 'Enterprise AI Platform - TechCorp',
    client_name: 'TechCorp Industries',
    value: 450000,
    probability: 85,
    status: 'negotiation',
    expected_close_date: '2025-12-15',
    stage: 'proposal',
    contact_email: 'sarah.chen@techcorp.com',
    notes: 'High priority deal. CEO very interested in quantum AI capabilities.'
  },
  {
    id: 'DEAL-002',
    title: 'Cloud Migration - DataFlow Inc',
    client_name: 'DataFlow Inc',
    value: 125000,
    probability: 60,
    status: 'lead',
    expected_close_date: '2026-01-20',
    stage: 'discovery',
    contact_email: 'mike.rodriguez@dataflow.io',
    notes: 'Initial meeting scheduled for next week.'
  },
  {
    id: 'DEAL-003',
    title: 'AI Training Infrastructure - NeuralLabs',
    client_name: 'NeuralLabs Research',
    value: 500000,
    probability: 95,
    status: 'closed_won',
    expected_close_date: '2025-11-28',
    stage: 'closed',
    contact_email: 'dr.williams@neurallabs.ai',
    notes: 'Successfully closed! Contract signed on 2025-11-28.'
  },
  {
    id: 'DEAL-004',
    title: 'Quantum Computing POC - FinanceFirst',
    client_name: 'FinanceFirst Bank',
    value: 75000,
    probability: 40,
    status: 'lead',
    expected_close_date: '2026-02-10',
    stage: 'qualification',
    contact_email: 'james.park@financefirst.com',
    notes: 'Budget constraints, exploring alternatives.'
  },
  {
    id: 'DEAL-005',
    title: 'Multi-Agent System - AutoDrive Co',
    client_name: 'AutoDrive Technologies',
    value: 320000,
    probability: 70,
    status: 'negotiation',
    expected_close_date: '2025-12-30',
    stage: 'negotiation',
    contact_email: 'lisa.yamamoto@autodrive.tech',
    notes: 'Contract review in progress. Legal team involved.'
  },
  {
    id: 'DEAL-006',
    title: 'Data Analytics Platform - RetailMax',
    client_name: 'RetailMax Corporation',
    value: 180000,
    probability: 25,
    status: 'closed_lost',
    expected_close_date: '2025-11-15',
    stage: 'closed',
    contact_email: 'alex.brown@retailmax.com',
    notes: 'Lost to competitor. Price was main concern.'
  },
  {
    id: 'DEAL-007',
    title: 'Smart City Infrastructure - CityTech',
    client_name: 'CityTech Solutions',
    value: 650000,
    probability: 90,
    status: 'negotiation',
    expected_close_date: '2025-12-20',
    stage: 'proposal',
    contact_email: 'maria.santos@citytech.gov',
    notes: 'Large government contract. High confidence level.'
  },
  {
    id: 'DEAL-008',
    title: 'Healthcare AI - MediCore',
    client_name: 'MediCore Health Systems',
    value: 95000,
    probability: 55,
    status: 'lead',
    expected_close_date: '2026-01-15',
    stage: 'discovery',
    contact_email: 'dr.patel@medicore.health',
    notes: 'Exploring AI diagnostics integration.'
  },
  {
    id: 'DEAL-009',
    title: 'Supply Chain Optimization - LogiFlow',
    client_name: 'LogiFlow Logistics',
    value: 210000,
    probability: 80,
    status: 'negotiation',
    expected_close_date: '2025-12-28',
    stage: 'negotiation',
    contact_email: 'kevin.zhang@logiflow.com',
    notes: 'Technical requirements finalized. Pricing discussion ongoing.'
  },
  {
    id: 'DEAL-010',
    title: 'Education Platform - EduTech Global',
    client_name: 'EduTech Global',
    value: 45000,
    probability: 50,
    status: 'lead',
    expected_close_date: '2026-02-01',
    stage: 'qualification',
    contact_email: 'emma.johnson@edutech.edu',
    notes: 'Non-profit organization. Exploring grant funding options.'
  }
];

// Seed data for SUPPORT_TICKETS
const supportTickets = [
  {
    id: 'TICKET-001',
    title: 'Agent UNIT_27 stuck in WARNING state',
    description: 'Agent UNIT_27 showing WARNING status for 2 hours. Neural load at 87%. Requires immediate attention.',
    status: 'in_progress',
    priority: 'high',
    category: 'technical',
    assigned_to: 'UNIT_12',
    created_by: 'system',
    tags: ['agents', 'warning', 'performance']
  },
  {
    id: 'TICKET-002',
    title: 'Dashboard loading slowly',
    description: 'Main dashboard takes 8+ seconds to load. Users reporting timeout errors.',
    status: 'open',
    priority: 'normal',
    category: 'performance',
    assigned_to: null,
    created_by: 'user_sarah',
    tags: ['dashboard', 'performance', 'ui']
  },
  {
    id: 'TICKET-003',
    title: 'Cannot export sales report',
    description: 'Export button on sales page returns 500 error. Tried multiple times.',
    status: 'resolved',
    priority: 'normal',
    category: 'bug',
    assigned_to: 'UNIT_05',
    created_by: 'user_mike',
    tags: ['export', 'sales', 'bug']
  },
  {
    id: 'TICKET-004',
    title: 'Critical: Database connection timeout',
    description: 'Supabase connection timing out intermittently. Affecting all users.',
    status: 'in_progress',
    priority: 'critical',
    category: 'infrastructure',
    assigned_to: 'UNIT_03',
    created_by: 'system',
    tags: ['database', 'critical', 'supabase']
  },
  {
    id: 'TICKET-005',
    title: 'Feature request: Dark mode',
    description: 'Users requesting dark mode option for better visibility at night.',
    status: 'open',
    priority: 'low',
    category: 'feature_request',
    assigned_to: null,
    created_by: 'user_lisa',
    tags: ['feature', 'ui', 'accessibility']
  },
  {
    id: 'TICKET-006',
    title: 'Email notifications not working',
    description: 'Haven\'t received any email notifications for the past 3 days.',
    status: 'resolved',
    priority: 'normal',
    category: 'bug',
    assigned_to: 'UNIT_08',
    created_by: 'user_james',
    tags: ['email', 'notifications', 'bug']
  },
  {
    id: 'TICKET-007',
    title: 'Agent logs showing incorrect timestamps',
    description: 'Timestamps in agent logs are 5 hours ahead. Timezone issue?',
    status: 'open',
    priority: 'low',
    category: 'bug',
    assigned_to: 'UNIT_15',
    created_by: 'user_maria',
    tags: ['logs', 'timezone', 'agents']
  },
  {
    id: 'TICKET-008',
    title: 'Need API documentation',
    description: 'Looking for comprehensive API docs to integrate with third-party system.',
    status: 'closed',
    priority: 'normal',
    category: 'documentation',
    assigned_to: 'UNIT_20',
    created_by: 'user_kevin',
    tags: ['api', 'documentation', 'integration']
  }
];

// Seed data for SOCIAL_POSTS
const socialPosts = [
  {
    id: 'POST-001',
    platform: 'twitter',
    content: '🚀 Just deployed our new Quantum AI agents! Performance improvements across the board. #AI #MachineLearning',
    author: 'alsham_official',
    likes: 342,
    shares: 89,
    comments: 45,
    sentiment_score: 0.92,
    reach: 15420,
    engagement_rate: 3.8
  },
  {
    id: 'POST-002',
    platform: 'linkedin',
    content: 'Proud to announce that ALSHAM QUANTUM has helped our clients process 1M+ transactions this month. Real-time AI making a difference! 💼',
    author: 'alsham_official',
    likes: 567,
    shares: 123,
    comments: 78,
    sentiment_score: 0.95,
    reach: 28900,
    engagement_rate: 4.2
  },
  {
    id: 'POST-003',
    platform: 'twitter',
    content: 'New blog post: "How Multi-Agent Systems are Revolutionizing Enterprise Software" - link in bio 📖',
    author: 'alsham_official',
    likes: 156,
    shares: 34,
    comments: 12,
    sentiment_score: 0.78,
    reach: 8200,
    engagement_rate: 2.5
  },
  {
    id: 'POST-004',
    platform: 'twitter',
    content: 'System maintenance scheduled for tonight 11PM-1AM EST. Expect brief downtime. ⚙️',
    author: 'alsham_official',
    likes: 23,
    shares: 12,
    comments: 8,
    sentiment_score: 0.45,
    reach: 3400,
    engagement_rate: 1.3
  },
  {
    id: 'POST-005',
    platform: 'linkedin',
    content: 'Q4 highlights: 99.7% uptime, 50+ new enterprise clients, 1000+ active AI agents deployed. Thank you for an incredible year! 🎉',
    author: 'alsham_official',
    likes: 891,
    shares: 234,
    comments: 145,
    sentiment_score: 0.98,
    reach: 45600,
    engagement_rate: 5.1
  },
  {
    id: 'POST-006',
    platform: 'twitter',
    content: 'Behind the scenes: Our neural network optimization reduces latency by 40%. Technical deep-dive coming soon! 🧠',
    author: 'alsham_official',
    likes: 412,
    shares: 67,
    comments: 34,
    sentiment_score: 0.88,
    reach: 18700,
    engagement_rate: 3.4
  },
  {
    id: 'POST-007',
    platform: 'linkedin',
    content: 'Case study released: How RetailMax increased efficiency by 60% using ALSHAM QUANTUM agents. Read more on our blog.',
    author: 'alsham_official',
    likes: 234,
    shares: 56,
    comments: 29,
    sentiment_score: 0.91,
    reach: 12300,
    engagement_rate: 3.7
  },
  {
    id: 'POST-008',
    platform: 'twitter',
    content: 'Hot take: The future of AI is not replacing humans, but augmenting human decision-making. What do you think? 🤔',
    author: 'alsham_official',
    likes: 678,
    shares: 234,
    comments: 189,
    sentiment_score: 0.82,
    reach: 32100,
    engagement_rate: 4.9
  },
  {
    id: 'POST-009',
    platform: 'twitter',
    content: 'Exciting partnership announcement coming tomorrow! Stay tuned... 👀',
    author: 'alsham_official',
    likes: 445,
    shares: 78,
    comments: 92,
    sentiment_score: 0.86,
    reach: 21500,
    engagement_rate: 4.1
  },
  {
    id: 'POST-010',
    platform: 'linkedin',
    content: 'We\'re hiring! Looking for Senior AI Engineers passionate about multi-agent systems. Join our quantum revolution! 💼🚀',
    author: 'alsham_official',
    likes: 523,
    shares: 167,
    comments: 98,
    sentiment_score: 0.93,
    reach: 28900,
    engagement_rate: 4.6
  },
  {
    id: 'POST-011',
    platform: 'twitter',
    content: 'Real-time dashboard update: All 50 agents operating at peak efficiency. System health: 98.5% 💚',
    author: 'alsham_official',
    likes: 289,
    shares: 45,
    comments: 23,
    sentiment_score: 0.94,
    reach: 13400,
    engagement_rate: 3.2
  },
  {
    id: 'POST-012',
    platform: 'linkedin',
    content: 'Webinar: "Building Scalable AI Systems" - December 15th, 2PM EST. Register now! Limited spots available.',
    author: 'alsham_official',
    likes: 356,
    shares: 89,
    comments: 67,
    sentiment_score: 0.87,
    reach: 19200,
    engagement_rate: 3.9
  },
  {
    id: 'POST-013',
    platform: 'twitter',
    content: 'Customer spotlight: "ALSHAM has transformed how we handle data processing" - CTO at TechCorp Industries ⭐',
    author: 'alsham_official',
    likes: 198,
    shares: 34,
    comments: 18,
    sentiment_score: 0.96,
    reach: 9800,
    engagement_rate: 3.1
  },
  {
    id: 'POST-014',
    platform: 'twitter',
    content: 'Security update deployed: Enhanced encryption for all agent communications. Your data security is our priority. 🔒',
    author: 'alsham_official',
    likes: 267,
    shares: 56,
    comments: 31,
    sentiment_score: 0.89,
    reach: 14200,
    engagement_rate: 3.5
  },
  {
    id: 'POST-015',
    platform: 'linkedin',
    content: 'Year in review: 2025 was our biggest year yet. Thank you to our amazing team and clients who made it possible! 🙏',
    author: 'alsham_official',
    likes: 1234,
    shares: 345,
    comments: 234,
    sentiment_score: 0.99,
    reach: 56700,
    engagement_rate: 5.8
  }
];

// Seed data for TRANSACTIONS
const transactions = [
  {
    id: 'TXN-001',
    type: 'payment',
    amount: 15000,
    currency: 'USD',
    status: 'completed',
    customer_id: 'CUST-001',
    customer_name: 'TechCorp Industries',
    description: 'Monthly subscription - Enterprise Plan',
    payment_method: 'credit_card',
    reference: 'INV-2025-001'
  },
  {
    id: 'TXN-002',
    type: 'payment',
    amount: 8500,
    currency: 'USD',
    status: 'completed',
    customer_id: 'CUST-002',
    customer_name: 'DataFlow Inc',
    description: 'Setup fee - Cloud Migration',
    payment_method: 'wire_transfer',
    reference: 'INV-2025-002'
  },
  {
    id: 'TXN-003',
    type: 'refund',
    amount: 2500,
    currency: 'USD',
    status: 'completed',
    customer_id: 'CUST-003',
    customer_name: 'RetailMax Corporation',
    description: 'Refund - Service cancellation',
    payment_method: 'credit_card',
    reference: 'REF-2025-001'
  },
  {
    id: 'TXN-004',
    type: 'subscription',
    amount: 12000,
    currency: 'USD',
    status: 'pending',
    customer_id: 'CUST-004',
    customer_name: 'NeuralLabs Research',
    description: 'Annual subscription - Pro Plan',
    payment_method: 'ach',
    reference: 'INV-2025-003'
  },
  {
    id: 'TXN-005',
    type: 'payment',
    amount: 25000,
    currency: 'USD',
    status: 'completed',
    customer_id: 'CUST-005',
    customer_name: 'AutoDrive Technologies',
    description: 'Implementation fee - Multi-Agent System',
    payment_method: 'wire_transfer',
    reference: 'INV-2025-004'
  },
  {
    id: 'TXN-006',
    type: 'payment',
    amount: 3500,
    currency: 'USD',
    status: 'failed',
    customer_id: 'CUST-006',
    customer_name: 'FinanceFirst Bank',
    description: 'Monthly subscription - Basic Plan',
    payment_method: 'credit_card',
    reference: 'INV-2025-005'
  },
  {
    id: 'TXN-007',
    type: 'subscription',
    amount: 45000,
    currency: 'USD',
    status: 'completed',
    customer_id: 'CUST-007',
    customer_name: 'CityTech Solutions',
    description: 'Enterprise contract - Q4 2025',
    payment_method: 'wire_transfer',
    reference: 'INV-2025-006'
  },
  {
    id: 'TXN-008',
    type: 'payment',
    amount: 6500,
    currency: 'USD',
    status: 'completed',
    customer_id: 'CUST-008',
    customer_name: 'MediCore Health Systems',
    description: 'POC project payment',
    payment_method: 'credit_card',
    reference: 'INV-2025-007'
  },
  {
    id: 'TXN-009',
    type: 'payment',
    amount: 18000,
    currency: 'USD',
    status: 'pending',
    customer_id: 'CUST-009',
    customer_name: 'LogiFlow Logistics',
    description: 'Monthly subscription - Enterprise Plus',
    payment_method: 'ach',
    reference: 'INV-2025-008'
  },
  {
    id: 'TXN-010',
    type: 'subscription',
    amount: 4200,
    currency: 'USD',
    status: 'completed',
    customer_id: 'CUST-010',
    customer_name: 'EduTech Global',
    description: 'Non-profit discount - Annual Plan',
    payment_method: 'credit_card',
    reference: 'INV-2025-009'
  },
  {
    id: 'TXN-011',
    type: 'payment',
    amount: 9800,
    currency: 'USD',
    status: 'completed',
    customer_id: 'CUST-001',
    customer_name: 'TechCorp Industries',
    description: 'Additional agent licenses',
    payment_method: 'credit_card',
    reference: 'INV-2025-010'
  },
  {
    id: 'TXN-012',
    type: 'refund',
    amount: 1500,
    currency: 'USD',
    status: 'pending',
    customer_id: 'CUST-006',
    customer_name: 'FinanceFirst Bank',
    description: 'Partial refund - Service issue',
    payment_method: 'credit_card',
    reference: 'REF-2025-002'
  }
];

// Seed data for ACHIEVEMENTS
const achievements = [
  {
    id: 'ACH-001',
    name: 'First Login',
    description: 'Successfully logged into ALSHAM QUANTUM for the first time',
    icon: '🎯',
    rarity: 'common',
    points: 10,
    category: 'onboarding',
    criteria: { action: 'login', count: 1 }
  },
  {
    id: 'ACH-002',
    name: 'Power User',
    description: 'Used the system for 30 consecutive days',
    icon: '⚡',
    rarity: 'rare',
    points: 100,
    category: 'engagement',
    criteria: { action: 'daily_login', count: 30 }
  },
  {
    id: 'ACH-003',
    name: 'Deal Closer',
    description: 'Closed your first deal worth over $100k',
    icon: '💰',
    rarity: 'uncommon',
    points: 50,
    category: 'sales',
    criteria: { action: 'close_deal', value: 100000 }
  },
  {
    id: 'ACH-004',
    name: 'Agent Master',
    description: 'Successfully managed 10 agents simultaneously',
    icon: '🤖',
    rarity: 'epic',
    points: 250,
    category: 'management',
    criteria: { action: 'manage_agents', count: 10 }
  },
  {
    id: 'ACH-005',
    name: 'Problem Solver',
    description: 'Resolved 50 support tickets',
    icon: '🔧',
    rarity: 'rare',
    points: 150,
    category: 'support',
    criteria: { action: 'resolve_ticket', count: 50 }
  },
  {
    id: 'ACH-006',
    name: 'Social Butterfly',
    description: 'Posted 100 times on social media',
    icon: '🦋',
    rarity: 'uncommon',
    points: 75,
    category: 'marketing',
    criteria: { action: 'social_post', count: 100 }
  },
  {
    id: 'ACH-007',
    name: 'Quantum Legend',
    description: 'Achieved 99.9% system uptime for 1 month',
    icon: '👑',
    rarity: 'legendary',
    points: 1000,
    category: 'operations',
    criteria: { action: 'uptime', percentage: 99.9, duration: 30 }
  },
  {
    id: 'ACH-008',
    name: 'Early Bird',
    description: 'Logged in before 6 AM on 10 occasions',
    icon: '🌅',
    rarity: 'common',
    points: 25,
    category: 'engagement',
    criteria: { action: 'early_login', count: 10 }
  },
  {
    id: 'ACH-009',
    name: 'Data Wizard',
    description: 'Processed over 1 million transactions',
    icon: '🧙',
    rarity: 'epic',
    points: 500,
    category: 'performance',
    criteria: { action: 'process_transactions', count: 1000000 }
  },
  {
    id: 'ACH-010',
    name: 'Team Player',
    description: 'Collaborated on 20 projects with other users',
    icon: '🤝',
    rarity: 'uncommon',
    points: 60,
    category: 'collaboration',
    criteria: { action: 'collaborate', count: 20 }
  }
];

async function seedData() {
  console.log('🚀 Starting ALSHAM QUANTUM seed data process...\n');

  try {
    // Seed DEALS
    console.log('📊 Seeding DEALS...');
    const { data: dealsData, error: dealsError } = await supabase
      .from('deals')
      .insert(deals);

    if (dealsError) {
      console.error('❌ Error seeding deals:', dealsError.message);
    } else {
      console.log(`✅ Successfully seeded ${deals.length} deals`);
    }

    // Seed SUPPORT_TICKETS
    console.log('\n🎫 Seeding SUPPORT_TICKETS...');
    const { data: ticketsData, error: ticketsError } = await supabase
      .from('support_tickets')
      .insert(supportTickets);

    if (ticketsError) {
      console.error('❌ Error seeding tickets:', ticketsError.message);
    } else {
      console.log(`✅ Successfully seeded ${supportTickets.length} support tickets`);
    }

    // Seed SOCIAL_POSTS
    console.log('\n📱 Seeding SOCIAL_POSTS...');
    const { data: postsData, error: postsError } = await supabase
      .from('social_posts')
      .insert(socialPosts);

    if (postsError) {
      console.error('❌ Error seeding posts:', postsError.message);
    } else {
      console.log(`✅ Successfully seeded ${socialPosts.length} social posts`);
    }

    // Seed TRANSACTIONS
    console.log('\n💳 Seeding TRANSACTIONS...');
    const { data: transactionsData, error: transactionsError } = await supabase
      .from('transactions')
      .insert(transactions);

    if (transactionsError) {
      console.error('❌ Error seeding transactions:', transactionsError.message);
    } else {
      console.log(`✅ Successfully seeded ${transactions.length} transactions`);
    }

    // Seed ACHIEVEMENTS
    console.log('\n🏆 Seeding ACHIEVEMENTS...');
    const { data: achievementsData, error: achievementsError } = await supabase
      .from('achievements')
      .insert(achievements);

    if (achievementsError) {
      console.error('❌ Error seeding achievements:', achievementsError.message);
    } else {
      console.log(`✅ Successfully seeded ${achievements.length} achievements`);
    }

    console.log('\n🎉 Seed data process completed successfully!');
    console.log('\n📊 Summary:');
    console.log(`   - Deals: ${deals.length}`);
    console.log(`   - Support Tickets: ${supportTickets.length}`);
    console.log(`   - Social Posts: ${socialPosts.length}`);
    console.log(`   - Transactions: ${transactions.length}`);
    console.log(`   - Achievements: ${achievements.length}`);
    console.log(`   - Total records: ${deals.length + supportTickets.length + socialPosts.length + transactions.length + achievements.length}`);

  } catch (error) {
    console.error('❌ Fatal error during seeding:', error);
    process.exit(1);
  }
}

// Run the seed function
seedData();
