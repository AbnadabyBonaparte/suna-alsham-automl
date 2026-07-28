/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM — /privacy — Política de Privacidade (LGPD)
 * ═══════════════════════════════════════════════════════════════
 * Ancorada na LGPD (Lei 13.709/2018) e no Marco Civil (Lei 12.965/2014).
 * NÃO nomeia fornecedor de IA (lei do motor interno) — "processadores
 * de IA terceirizados". Revisão por advogado humano obrigatória.
 * ═══════════════════════════════════════════════════════════════
 */

import type { Metadata } from 'next';
import LegalShell, { LegalSection, Pendente } from '@/components/legal/LegalShell';

export const metadata: Metadata = {
  title: 'Política de Privacidade — ALSHAM QUANTUM',
  description: 'Como a ALSHAM QUANTUM trata dados pessoais, conforme a LGPD.',
};

export default function PrivacyPage() {
  return (
    <LegalShell title="Política de Privacidade" updatedAt="julho de 2026">
      <p>
        Esta Política explica como a ALSHAM Global Commerce Ltda. (&quot;ALSHAM&quot;, controladora dos
        dados) coleta, usa e protege os dados pessoais de quem usa a Plataforma ALSHAM QUANTUM, conforme
        a Lei Geral de Proteção de Dados (Lei 13.709/2018 — LGPD).
      </p>

      <LegalSection n="1." title="Dados que coletamos">
        <ul className="list-disc pl-6 space-y-1">
          <li><strong>Conta:</strong> nome, e-mail e credenciais de acesso.</li>
          <li><strong>Pagamento:</strong> processado pela Stripe. A ALSHAM recebe dados da transação (plano, status, identificadores), <strong>não</strong> os dados completos do cartão.</li>
          <li><strong>Uso:</strong> registros de acesso, requisições aos agentes e dados de navegação (IP, dispositivo), conforme o Marco Civil da Internet.</li>
          <li><strong>Conteúdo:</strong> o texto e os dados que você envia aos agentes de IA durante o uso.</li>
        </ul>
      </LegalSection>

      <LegalSection n="2." title="Para que usamos e a base legal">
        <ul className="list-disc pl-6 space-y-1">
          <li><strong>Executar o contrato</strong> (art. 7º, V, LGPD): dar acesso, processar a assinatura, prestar suporte.</li>
          <li><strong>Cumprir obrigação legal</strong> (art. 7º, II): guarda de registros e obrigações fiscais.</li>
          <li><strong>Legítimo interesse</strong> (art. 7º, IX): segurança, prevenção a fraude e melhoria do serviço, sem prejuízo dos seus direitos.</li>
          <li><strong>Consentimento</strong> (art. 7º, I): quando aplicável, para comunicações opcionais.</li>
        </ul>
      </LegalSection>

      <LegalSection n="3." title="Processamento por IA">
        <p>
          A Plataforma opera por agentes de inteligência artificial. Para gerar as respostas, o conteúdo
          que você envia aos agentes pode ser processado por{' '}
          <strong>processadores de IA terceirizados</strong> contratados pela ALSHAM, sob obrigação de
          confidencialidade e segurança. Recomendamos <strong>não inserir dados sensíveis</strong>
          (art. 5º, II, LGPD — saúde, biometria, entre outros) ou segredos que não sejam necessários à
          tarefa. A ALSHAM não usa o seu conteúdo para finalidade estranha à prestação do serviço.
        </p>
      </LegalSection>

      <LegalSection n="4." title="Compartilhamento">
        <p>
          A ALSHAM não vende dados pessoais. Compartilha apenas com operadores necessários à operação —
          o processador de pagamento (Stripe), a infraestrutura de nuvem e os processadores de IA — e
          quando exigido por lei ou ordem de autoridade competente.
        </p>
      </LegalSection>

      <LegalSection n="5." title="Transferência internacional">
        <p>
          Alguns operadores podem processar dados fora do Brasil. Nesses casos, a ALSHAM exige garantias
          de proteção compatíveis com a LGPD (art. 33).
        </p>
      </LegalSection>

      <LegalSection n="6." title="Retenção">
        <p>
          Mantemos os dados enquanto durar a conta e pelos prazos legais aplicáveis após o encerramento
          (obrigações fiscais e registros de acesso do Marco Civil). Depois disso, são eliminados ou
          anonimizados. Prazos específicos: <Pendente>definir: fundador — política de retenção por tipo de dado</Pendente>.
        </p>
      </LegalSection>

      <LegalSection n="7." title="Seus direitos (art. 18 da LGPD)">
        <p>
          Você pode solicitar confirmação de tratamento, acesso, correção, anonimização, portabilidade,
          eliminação e informações sobre compartilhamento, além de revogar consentimento. Para exercer,
          escreva para{' '}
          <a href="mailto:comercial@alshamglobal.com.br" className="text-[var(--color-primary)] hover:underline">comercial@alshamglobal.com.br</a>.
          Responderemos nos prazos da LGPD.
        </p>
      </LegalSection>

      <LegalSection n="8." title="Segurança">
        <p>
          Adotamos medidas técnicas e organizacionais para proteger os dados (controle de acesso,
          criptografia em trânsito, isolamento por conta). Nenhum sistema é 100% imune; em caso de
          incidente relevante, comunicaremos os titulares e a ANPD conforme a LGPD.
        </p>
      </LegalSection>

      <LegalSection n="9." title="Encarregado (DPO) e contato">
        <p>
          Controlador: ALSHAM Global Commerce Ltda., CNPJ 59.332.265/0001-30. Contato do encarregado
          pelo tratamento de dados:{' '}
          <a href="mailto:comercial@alshamglobal.com.br" className="text-[var(--color-primary)] hover:underline">comercial@alshamglobal.com.br</a>{' '}
          <Pendente>definir: fundador — indicar DPO nomeado, se houver</Pendente>.
        </p>
      </LegalSection>
    </LegalShell>
  );
}
