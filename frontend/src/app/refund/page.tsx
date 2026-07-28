/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM — /refund — Política de Reembolso e Cancelamento
 * ═══════════════════════════════════════════════════════════════
 * Honra o art. 49 do CDC (arrependimento 7 dias) E a "Garantia de
 * 30 dias" que a UI de /pricing já promete. Lei 7: não promete o
 * que não se cumpre. Revisão por advogado humano obrigatória.
 * ═══════════════════════════════════════════════════════════════
 */

import type { Metadata } from 'next';
import LegalShell, { LegalSection, Pendente } from '@/components/legal/LegalShell';

export const metadata: Metadata = {
  title: 'Política de Reembolso — ALSHAM QUANTUM',
  description: 'Política de Reembolso e Cancelamento da ALSHAM QUANTUM.',
};

export default function RefundPage() {
  return (
    <LegalShell title="Política de Reembolso e Cancelamento" updatedAt="julho de 2026">
      <p>
        Esta Política explica quando e como você pode pedir reembolso da assinatura ALSHAM QUANTUM. Ela
        soma dois direitos: o <strong>arrependimento legal de 7 dias</strong> do Código de Defesa do
        Consumidor e a <strong>garantia de satisfação de 30 dias</strong> oferecida pela ALSHAM.
      </p>

      <LegalSection n="1." title="Direito de arrependimento — 7 dias (CDC, art. 49)">
        <p>
          Por ser contratação feita fora do estabelecimento físico (pela internet), você pode desistir
          da assinatura em até <strong>7 dias corridos</strong> a partir da contratação. Nesse prazo, o
          reembolso é <strong>integral</strong>, sem necessidade de justificativa. É um direito legal e
          não pode ser reduzido.
        </p>
      </LegalSection>

      <LegalSection n="2." title="Garantia de satisfação — 30 dias">
        <p>
          Além do direito legal, a ALSHAM oferece uma garantia de satisfação de{' '}
          <strong>30 dias corridos</strong> a partir da primeira contratação: se a Plataforma não
          atender você nesse período, pode solicitar o reembolso do valor pago no ciclo vigente.
        </p>
        <p>
          Esta garantia vale <Pendente>definir: fundador — reembolso integral ou proporcional após os
          7 dias legais</Pendente> e aplica-se <Pendente>definir: fundador — apenas à primeira
          assinatura ou a todo novo ciclo</Pendente>. Enquanto o fundador não definir, honramos o que a
          página de planos anuncia: &quot;Garantia de 30 dias&quot;.
        </p>
      </LegalSection>

      <LegalSection n="3." title="Após 30 dias — renovações">
        <p>
          Passados os 30 dias, as renovações seguintes não são reembolsáveis de forma retroativa. Você
          pode cancelar a qualquer momento para evitar a próxima cobrança: o cancelamento encerra a
          renovação e o acesso permanece até o fim do período já pago, sem novo débito.
        </p>
      </LegalSection>

      <LegalSection n="4." title="Como pedir reembolso">
        <ol className="list-decimal pl-6 space-y-1">
          <li>
            Envie um e-mail para{' '}
            <a href="mailto:comercial@alshamglobal.com.br" className="text-[var(--color-primary)] hover:underline">comercial@alshamglobal.com.br</a>{' '}
            com o assunto &quot;Reembolso&quot;, informando o e-mail da conta e o plano.
          </li>
          <li>A ALSHAM confirma o pedido e verifica o prazo aplicável (7 ou 30 dias).</li>
          <li>
            Aprovado, o estorno é feito pelo mesmo meio de pagamento (via Stripe). O valor costuma
            retornar em <Pendente>definir: fundador — prazo real, sugestão 5 a 10 dias úteis</Pendente>,
            conforme o prazo da operadora do cartão.
          </li>
        </ol>
      </LegalSection>

      <LegalSection n="5." title="O que não é reembolsável">
        <ul className="list-disc pl-6 space-y-1">
          <li>Ciclos já renovados após o período de garantia de 30 dias.</li>
          <li>Contas suspensas ou encerradas por violação dos Termos (uso indevido, redistribuição não autorizada).</li>
        </ul>
        <p className="text-textSecondary text-sm">
          Nenhuma cláusula desta Política afasta os direitos indisponíveis do consumidor. Em conflito,
          o CDC prevalece.
        </p>
      </LegalSection>
    </LegalShell>
  );
}
