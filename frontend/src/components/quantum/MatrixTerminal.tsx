'use client';

import { useState, useEffect, useRef } from 'react';
import { Badge } from '@/components/ui/badge';
import { supabase } from '@/lib/supabase';

const INITIAL_BOOT_SEQUENCE = [
  'Initializing ALSHAM Quantum Core v11.0...',
  'Loading neural pathways...',
  'Connecting to active agents...',
  'Establishing secure handshake with payment gateway...',
  'Syncing with data cluster...',
  'System Status: ONLINE',
];

interface KernelLog {
  type: string;
  source: string;
  msg: string;
  timestamp: string;
}

// Mapeia o event_type real da tabela agent_logs para o rótulo exibido no terminal
function mapEventType(eventType: string | null): string {
  switch (eventType) {
    case 'error':
      return 'ERROR';
    case 'task_complete':
      return 'SUCCESS';
    case 'status_change':
      return 'WARNING';
    default:
      return 'INFO';
  }
}

export default function MatrixTerminal() {
  const [logs, setLogs] = useState<KernelLog[]>([]);
  const [booted, setBooted] = useState(false);
  const [bootDone, setBootDone] = useState(false);
  const [showIntro, setShowIntro] = useState(true);
  const [introText, setIntroText] = useState('');
  const [hasSource, setHasSource] = useState(true);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Efeito 1: "Wake up, Bonaparte..."
  useEffect(() => {
    const text = 'Wake up, Bonaparte... The ALSHAM has you.';
    let i = 0;
    const timer = setInterval(() => {
      setIntroText(text.substring(0, i));
      i++;
      if (i > text.length) {
        clearInterval(timer);
        setTimeout(() => {
          setShowIntro(false); // Sai da intro
          setBooted(true); // Inicia o boot
        }, 2000);
      }
    }, 100); // Velocidade de digitação
    return () => clearInterval(timer);
  }, []);

  // Efeito 2: Boot Sequence
  useEffect(() => {
    if (!booted) return;

    let i = 0;
    const timer = setInterval(() => {
      if (i < INITIAL_BOOT_SEQUENCE.length) {
        setLogs((prev) => [
          ...prev,
          {
            type: 'SYSTEM',
            source: 'BOOT',
            msg: INITIAL_BOOT_SEQUENCE[i],
            timestamp: new Date().toLocaleTimeString(),
          },
        ]);
        i++;
      } else {
        clearInterval(timer);
        setBootDone(true);
      }
    }, 300);
    return () => clearInterval(timer);
  }, [booted]);

  // Efeito 3: Logs reais do kernel (tabela agent_logs)
  useEffect(() => {
    if (!bootDone) return;

    let cancelled = false;

    async function fetchLogs() {
      try {
        const { data, error } = await supabase
          .from('agent_logs')
          .select('agent_id, timestamp, event_type, message')
          .order('timestamp', { ascending: false })
          .limit(50);

        if (error) throw error;
        if (cancelled) return;

        const realLogs: KernelLog[] = (data || [])
          .slice()
          .reverse()
          .map(
            (row: {
              agent_id?: string;
              timestamp?: string;
              event_type?: string;
              message?: string;
            }) => ({
              type: mapEventType(row.event_type ?? null),
              source: row.agent_id || 'KERNEL',
              msg: row.message || '',
              timestamp: row.timestamp
                ? new Date(row.timestamp).toLocaleTimeString()
                : new Date().toLocaleTimeString(),
            }),
          );

        setHasSource(realLogs.length > 0);
        setLogs((prev) => {
          // Mantém a sequência de boot no topo, seguida dos logs reais
          const bootLogs = prev.filter((l) => l.type === 'SYSTEM');
          return [...bootLogs, ...realLogs];
        });

        if (scrollRef.current) {
          scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
      } catch (err) {
        console.error('MatrixTerminal: failed to fetch agent_logs:', err);
        if (!cancelled) setHasSource(false);
      }
    }

    fetchLogs();
    const timer = setInterval(fetchLogs, 5000);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [bootDone]);

  // Renderização da Intro Cinematográfica
  if (showIntro) {
    return (
      <div className="h-full w-full flex items-center justify-center bg-background text-success font-mono text-2xl md:text-4xl">
        <span className="animate-pulse">{introText}</span>
        <span className="animate-blink">_</span>
      </div>
    );
  }

  const realLogCount = logs.filter((l) => l.type !== 'SYSTEM').length;

  // Renderização do Terminal
  return (
    <div className="h-full w-full bg-background border border-success/20 rounded-lg p-4 font-mono text-sm relative overflow-hidden shadow-[0_0_30px_rgba(34,197,94,0.1)]">
      {/* Scanline Effect */}
      <div className="absolute inset-0 bg-[linear-gradient(transparent_50%,rgba(0,0,0,0.25)_50%)] bg-[length:100%_4px] pointer-events-none z-10 opacity-20"></div>

      <div className="flex justify-between items-center border-b border-success/30 pb-2 mb-4">
        <h3 className="text-green-400 font-bold flex items-center gap-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          LIVE KERNEL STREAM
        </h3>
        <Badge variant="outline" className="border-success/50 text-success">
          SECURE CONNECTION
        </Badge>
      </div>

      <div className="h-[calc(100%-3rem)] overflow-y-auto space-y-2 scrollbar-hide" ref={scrollRef}>
        {logs.map((log, i) => (
          <div
            key={i}
            className="flex gap-3 animate-in fade-in slide-in-from-bottom-1 duration-300"
          >
            <span className="text-green-800">[{log.timestamp || 'INIT'}]</span>
            <span
              className={`font-bold w-24 ${
                log.type === 'ERROR'
                  ? 'text-red-500'
                  : log.type === 'WARNING'
                    ? 'text-yellow-500'
                    : log.type === 'SUCCESS'
                      ? 'text-blue-400'
                      : 'text-green-600'
              }`}
            >
              {log.type}
            </span>
            <span className="text-green-700 w-32">@{log.source}:</span>
            <span className="text-green-400 flex-1">{log.msg}</span>
          </div>
        ))}

        {/* Estado honesto: boot concluído porém sem telemetria real */}
        {bootDone && realLogCount === 0 && (
          <div className="text-green-800 italic">
            {hasSource
              ? 'Aguardando atividade do kernel...'
              : 'Sem logs ainda — nenhuma atividade registrada.'}
          </div>
        )}

        <div className="animate-pulse text-success">_</div>
      </div>
    </div>
  );
}
