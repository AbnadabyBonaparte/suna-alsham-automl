// ALSHAM QUANTUM - Agent Heartbeat Worker
// Runs every 5 minutes via cron to update agent status

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

    console.log('🔄 Agent Heartbeat Worker Started...');

    // Get all agents
    const { data: agents, error: agentsError } = await supabase
      .from('agents')
      .select('*');

    if (agentsError) {
      throw new Error(`Failed to fetch agents: ${agentsError.message}`);
    }

    console.log(`📊 Processing ${agents.length} agents...`);

    const updates = [];
    const logs = [];

    // Update each agent
    for (const agent of agents) {
      // Simulate efficiency calculation based on current status
      let newEfficiency = agent.efficiency;
      let newStatus = agent.status;

      // Random performance fluctuations
      const performanceDelta = (Math.random() - 0.5) * 2; // -1 to +1

      if (agent.status === 'ACTIVE') {
        newEfficiency = Math.min(100, agent.efficiency + performanceDelta * 0.5);
      } else if (agent.status === 'WARNING') {
        newEfficiency = Math.max(70, agent.efficiency + performanceDelta * 0.3);

        // Chance to recover from WARNING
        if (newEfficiency > 85 && Math.random() > 0.7) {
          newStatus = 'ACTIVE';
        }
      } else if (agent.status === 'PROCESSING') {
        newEfficiency = Math.min(95, agent.efficiency + performanceDelta * 0.2);
      }

      // Determine if agent should go into WARNING
      if (newEfficiency < 80 && newStatus === 'ACTIVE') {
        newStatus = 'WARNING';
      }

      // Prepare update
      const update = {
        id: agent.id,
        efficiency: parseFloat(newEfficiency.toFixed(2)),
        status: newStatus,
        last_active: newStatus === 'ACTIVE' || newStatus === 'PROCESSING' ? 'Now' : agent.last_active,
        updated_at: new Date().toISOString(),
      };

      updates.push(update);

      // Create log entry
      logs.push({
        agent_id: agent.id,
        event_type: 'metric_update',
        message: `Heartbeat: Efficiency ${update.efficiency}%, Status: ${update.status}`,
        metadata: {
          previous_efficiency: agent.efficiency,
          new_efficiency: update.efficiency,
          previous_status: agent.status,
          new_status: update.status,
        },
      });
    }

    // Batch update agents
    for (const update of updates) {
      const { error: updateError } = await supabase
        .from('agents')
        .update(update)
        .eq('id', update.id);

      if (updateError) {
        console.error(`Failed to update agent ${update.id}:`, updateError);
      }
    }

    // Batch insert logs
    const { error: logsError } = await supabase
      .from('agent_logs')
      .insert(logs);

    if (logsError) {
      console.error('Failed to insert logs:', logsError);
    }

    const response = {
      success: true,
      message: 'Agent heartbeat completed',
      agents_updated: updates.length,
      logs_created: logs.length,
      timestamp: new Date().toISOString(),
    };

    console.log('✅ Heartbeat completed:', response);

    return new Response(JSON.stringify(response), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 200,
    });

  } catch (error) {
    console.error('❌ Heartbeat error:', error);

    return new Response(JSON.stringify({
      success: false,
      error: error.message
    }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 500,
    });
  }
});
