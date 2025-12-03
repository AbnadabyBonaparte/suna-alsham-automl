// ALSHAM QUANTUM - System Metrics Collector
// Runs every 10 minutes via cron to collect system health metrics

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    // Create Supabase client
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseServiceRoleKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const supabase = createClient(supabaseUrl, supabaseServiceRoleKey);

    console.log('📊 System Metrics Collector Started...');

    // Collect metrics
    const timestamp = new Date().toISOString();
    const metrics = [];

    // Get agent statistics
    const { data: agents, error: agentsError } = await supabase
      .from('agents')
      .select('status, efficiency');

    if (agentsError) {
      throw new Error(`Failed to fetch agents: ${agentsError.message}`);
    }

    // Calculate system health metrics
    const totalAgents = agents.length;
    const activeAgents = agents.filter(a => a.status === 'ACTIVE').length;
    const warningAgents = agents.filter(a => a.status === 'WARNING').length;
    const processingAgents = agents.filter(a => a.status === 'PROCESSING').length;

    const avgEfficiency = agents.reduce((sum, a) => sum + a.efficiency, 0) / totalAgents;

    // Calculate overall health score (0-100)
    const healthScore = (
      (activeAgents / totalAgents) * 40 +  // 40% weight for active agents
      (avgEfficiency / 100) * 40 +          // 40% weight for average efficiency
      (1 - warningAgents / totalAgents) * 20 // 20% weight for lack of warnings
    );

    // Simulate CPU usage (would be real in production)
    const cpuUsage = 20 + Math.random() * 30; // 20-50%

    // Simulate memory usage (would be real in production)
    const memoryUsage = 40 + Math.random() * 20; // 40-60%

    // Simulate disk usage (would be real in production)
    const diskUsage = 30 + Math.random() * 15; // 30-45%

    // Simulate network throughput (would be real in production)
    const networkThroughput = 100 + Math.random() * 400; // 100-500 Mbps

    // Create metric entries
    metrics.push(
      {
        metric_type: 'cpu',
        value: parseFloat(cpuUsage.toFixed(2)),
        unit: 'percent',
        metadata: {
          timestamp,
          source: 'system_metrics_worker'
        }
      },
      {
        metric_type: 'memory',
        value: parseFloat(memoryUsage.toFixed(2)),
        unit: 'percent',
        metadata: {
          timestamp,
          source: 'system_metrics_worker'
        }
      },
      {
        metric_type: 'disk',
        value: parseFloat(diskUsage.toFixed(2)),
        unit: 'percent',
        metadata: {
          timestamp,
          source: 'system_metrics_worker'
        }
      },
      {
        metric_type: 'network',
        value: parseFloat(networkThroughput.toFixed(2)),
        unit: 'mbps',
        metadata: {
          timestamp,
          source: 'system_metrics_worker'
        }
      },
      {
        metric_type: 'health_score',
        value: parseFloat(healthScore.toFixed(2)),
        unit: 'score',
        metadata: {
          timestamp,
          total_agents: totalAgents,
          active_agents: activeAgents,
          warning_agents: warningAgents,
          processing_agents: processingAgents,
          avg_efficiency: parseFloat(avgEfficiency.toFixed(2)),
          source: 'system_metrics_worker'
        }
      }
    );

    // Insert metrics into database
    const { error: insertError } = await supabase
      .from('system_metrics')
      .insert(metrics);

    if (insertError) {
      throw new Error(`Failed to insert metrics: ${insertError.message}`);
    }

    // Create system log entry
    const healthLevel = healthScore >= 90 ? 'SUCCESS' : healthScore >= 70 ? 'INFO' : 'WARN';
    await supabase
      .from('system_logs')
      .insert({
        level: healthLevel,
        message: `System Health: ${healthScore.toFixed(1)}% | Agents: ${activeAgents}/${totalAgents} Active`,
        source: 'SYSTEM_METRICS',
        agent_id: null
      });

    const response = {
      success: true,
      message: 'System metrics collected',
      metrics_collected: metrics.length,
      health_score: parseFloat(healthScore.toFixed(2)),
      summary: {
        cpu: parseFloat(cpuUsage.toFixed(2)),
        memory: parseFloat(memoryUsage.toFixed(2)),
        disk: parseFloat(diskUsage.toFixed(2)),
        network: parseFloat(networkThroughput.toFixed(2)),
        agents: {
          total: totalAgents,
          active: activeAgents,
          warning: warningAgents,
          processing: processingAgents,
        },
        avg_efficiency: parseFloat(avgEfficiency.toFixed(2)),
      },
      timestamp,
    };

    console.log('✅ Metrics collection completed:', response);

    return new Response(JSON.stringify(response), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 200,
    });

  } catch (error) {
    console.error('❌ Metrics collection error:', error);

    return new Response(JSON.stringify({
      success: false,
      error: error.message
    }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 500,
    });
  }
});
