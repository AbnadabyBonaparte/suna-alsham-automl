// ALSHAM QUANTUM - Agent Task Processor
// Processes pending tasks and simulates agent interactions

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

// Task templates for simulation
const TASK_TEMPLATES = {
  CORE: [
    'Synchronizing neural network nodes',
    'Optimizing core system parameters',
    'Coordinating multi-agent workflows',
    'Balancing computational load',
    'Executing system-wide optimization',
  ],
  SPECIALIST: [
    'Analyzing revenue patterns',
    'Processing customer support tickets',
    'Generating performance reports',
    'Optimizing conversion funnels',
    'Conducting data analysis',
  ],
  GUARD: [
    'Scanning for security threats',
    'Monitoring network integrity',
    'Validating authentication requests',
    'Performing security audit',
    'Analyzing access patterns',
  ],
  ANALYST: [
    'Predicting market trends',
    'Mining data insights',
    'Creating content recommendations',
    'Analyzing user behavior',
    'Generating analytics reports',
  ],
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

    console.log('⚙️ Agent Task Processor Started...');

    // Get all agents
    const { data: agents, error: agentsError } = await supabase
      .from('agents')
      .select('*');

    if (agentsError) {
      throw new Error(`Failed to fetch agents: ${agentsError.message}`);
    }

    console.log(`🤖 Processing tasks for ${agents.length} agents...`);

    const taskLogs = [];
    const interactions = [];
    const agentUpdates = [];

    // Process each agent
    for (const agent of agents) {
      // Skip agents in WARNING state for task assignment
      if (agent.status === 'WARNING') {
        continue;
      }

      // Randomly assign new tasks to IDLE agents
      if (agent.status === 'IDLE' && Math.random() > 0.5) {
        const tasks = TASK_TEMPLATES[agent.role] || TASK_TEMPLATES.CORE;
        const newTask = tasks[Math.floor(Math.random() * tasks.length)];

        agentUpdates.push({
          id: agent.id,
          status: 'PROCESSING',
          current_task: newTask,
          last_active: 'Now',
        });

        taskLogs.push({
          agent_id: agent.id,
          event_type: 'task_start',
          message: `Started: ${newTask}`,
          metadata: {
            previous_task: agent.current_task,
            new_task: newTask,
          },
        });
      }

      // Complete tasks for PROCESSING agents
      else if (agent.status === 'PROCESSING' && Math.random() > 0.6) {
        agentUpdates.push({
          id: agent.id,
          status: 'ACTIVE',
          current_task: 'Ready for next assignment',
          last_active: 'Now',
        });

        taskLogs.push({
          agent_id: agent.id,
          event_type: 'task_complete',
          message: `Completed: ${agent.current_task}`,
          metadata: {
            task: agent.current_task,
            completion_time: new Date().toISOString(),
          },
        });
      }

      // Generate agent interactions (agent-to-agent communication)
      if (agent.status === 'ACTIVE' && Math.random() > 0.8) {
        // Find another active agent
        const otherAgents = agents.filter(a =>
          a.id !== agent.id && (a.status === 'ACTIVE' || a.status === 'PROCESSING')
        );

        if (otherAgents.length > 0) {
          const targetAgent = otherAgents[Math.floor(Math.random() * otherAgents.length)];

          const interactionMessages = [
            'Data sync request',
            'Resource allocation query',
            'Task coordination handoff',
            'Performance metric share',
            'Status update notification',
          ];

          const message = interactionMessages[Math.floor(Math.random() * interactionMessages.length)];

          interactions.push({
            from_agent_id: agent.id,
            to_agent_id: targetAgent.id,
            interaction_type: 'request',
            message,
            metadata: {
              timestamp: new Date().toISOString(),
              from_role: agent.role,
              to_role: targetAgent.role,
            },
          });
        }
      }
    }

    // Apply agent updates
    for (const update of agentUpdates) {
      const { error: updateError } = await supabase
        .from('agents')
        .update(update)
        .eq('id', update.id);

      if (updateError) {
        console.error(`Failed to update agent ${update.id}:`, updateError);
      }
    }

    // Insert task logs
    if (taskLogs.length > 0) {
      const { error: logsError } = await supabase
        .from('agent_logs')
        .insert(taskLogs);

      if (logsError) {
        console.error('Failed to insert task logs:', logsError);
      }
    }

    // Insert agent interactions
    if (interactions.length > 0) {
      const { error: interactionsError } = await supabase
        .from('agent_interactions')
        .insert(interactions);

      if (interactionsError) {
        console.error('Failed to insert interactions:', interactionsError);
      }
    }

    const response = {
      success: true,
      message: 'Agent task processing completed',
      agents_updated: agentUpdates.length,
      logs_created: taskLogs.length,
      interactions_created: interactions.length,
      timestamp: new Date().toISOString(),
    };

    console.log('✅ Task processing completed:', response);

    return new Response(JSON.stringify(response), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 200,
    });

  } catch (error) {
    console.error('❌ Task processing error:', error);

    return new Response(JSON.stringify({
      success: false,
      error: error.message
    }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 500,
    });
  }
});
