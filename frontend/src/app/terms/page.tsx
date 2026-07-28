/**
 * ═══════════════════════════════════════════════════════════════
 * ALSHAM QUANTUM — /terms — Termos de Assinatura e de Uso
 * ═══════════════════════════════════════════════════════════════
 * Texto jurídico ancorado no CDC (Lei 8.078/1990) e no Código Civil.
 * Revisão por advogado humano é obrigatória antes da 1ª venda.
 * ═══════════════════════════════════════════════════════════════
 */

import type { Metadata } from 'next';
import LegalShell, { LegalSection, Pendente } from '@/components/legal/LegalShell';

export const metadata: Metadata = {
  title: 'Termos de Assinatura — ALSHAM QUANTUM',
  description: 'Termos de Assinatura e de Uso da plataforma ALSHAM QUANTUM.',
};

export default function TermsPage() {
  return (
    <LegalShell title="Termos de Assinatura e de Uso" updatedAt="julho de 2026">
      <p>
        Estes Termos regem o uso da plataforma <strong>ALSHAM QUANTUM</strong> (&quot;Plataforma&quot;),
        fornecida pela ALSHAM Global Commerce Ltda. (&quot;ALSHAM&quot;). Ao criar uma conta, contratar
        um plano ou usar a Plataforma, você (&quot;Assinante&quot;) declara ter lido e aceitado estes
        Termos, a Política de Privacidade e a Política de Reembolso.
      </p>

      <LegalSection n="1." title="Objeto">
        <p>
          A ALSHAM concede ao Assinante acesso, mediante assinatura, a uma plataforma de agentes de
          inteligência artificial voltada à automação de operações. O acesso é liberado após a
          confirmação do pagamento e enquanto a assinatura estiver ativa.
        </p>
      </LegalSection>

      <LegalSection n="2." title="Planos e valores">
        <p>Os planos e valores vigentes são:</p>
        <ul className="list-disc pl-6 space-y-1">
          <li><strong>Starter</strong> — R$ 990,00 por mês.</li>
          <li><strong>Pro</strong> — R$ 4.900,00 por mês.</li>
          <li><strong>Enterprise</strong> — R$ 9.900,00 por mês.</li>
        </ul>
        <p>
          Há a opção de cobrança anual com desconto, quando ofertada no ato da contratação. Os limites
          de cada plano (número de agentes, requisições e recursos) são os descritos na página de
          planos no momento da contratação. Reajustes de preço serão comunicados com antecedência
          mínima de <strong>30 dias</strong> e não afetam o ciclo já pago.
        </p>
      </LegalSection>

      <LegalSection n="3." title="Cobrança recorrente e renovação">
        <p>
          A assinatura é recorrente e se renova automaticamente ao fim de cada ciclo (mensal ou anual),
          pelo mesmo meio de pagamento, até que o Assinante a cancele. O processamento de pagamento é
          feito pela Stripe; a ALSHAM não armazena os dados completos do cartão. A falha de pagamento
          pode suspender o acesso até a regularização.
        </p>
      </LegalSection>

      <LegalSection n="4." title="Cancelamento">
        <p>
          O Assinante pode cancelar a qualquer momento, pela própria conta ou pelo e-mail{' '}
          <a href="mailto:comercial@alshamglobal.com.br" className="text-[var(--color-primary)] hover:underline">comercial@alshamglobal.com.br</a>.
          O cancelamento encerra a renovação seguinte; o acesso permanece ativo até o fim do período já
          pago, sem cobrança adicional. Reembolsos seguem a Política de Reembolso.
        </p>
      </LegalSection>

      <LegalSection n="5." title="O que a Plataforma é — e o que NÃO é">
        <p>
          A Plataforma é uma ferramenta de apoio e automação. Ela <strong>não substitui o julgamento
          de um profissional humano habilitado</strong> em áreas reguladas. Nenhuma resposta gerada por
          um agente constitui, por si só, aconselhamento jurídico, diagnóstico ou tratamento médico,
          recomendação de investimento ou parecer contábil.
        </p>
        <ul className="list-disc pl-6 space-y-1">
          <li><strong>Jurídico:</strong> orientação de primeiro filtro; não substitui advogado habilitado na OAB.</li>
          <li><strong>Saúde:</strong> conteúdo informativo; não substitui médico, nutricionista ou profissional de saúde.</li>
          <li><strong>Financeiro:</strong> apoio analítico; não é recomendação de investimento nem consultoria financeira registrada.</li>
        </ul>
        <p>
          Decisões tomadas pelo Assinante com base na Plataforma são de sua responsabilidade. O
          Assinante é responsável pelo uso lícito da Plataforma e pelo conteúdo que nela insere.
        </p>
      </LegalSection>

      <LegalSection n="6." title="Propriedade intelectual e licença de uso">
        <p>
          A Plataforma, os agentes de IA, seus prompts, arquitetura, marca e materiais são de
          propriedade exclusiva da ALSHAM Global. A assinatura concede ao Assinante uma licença{' '}
          <strong>pessoal, intransferível e não exclusiva</strong> de uso, limitada à vigência do plano.
        </p>
        <p>É vedado ao Assinante, sem autorização escrita da ALSHAM:</p>
        <ul className="list-disc pl-6 space-y-1">
          <li>revender, sublicenciar, compartilhar ou redistribuir o acesso ou as saídas da Plataforma a terceiros;</li>
          <li>extrair, copiar ou tentar reproduzir os agentes, seus prompts ou seu funcionamento interno;</li>
          <li>usar a Plataforma para construir produto ou serviço concorrente.</li>
        </ul>
        <p>
          As saídas entregues ao Assinante trazem a marca de origem da ALSHAM e destinam-se a uso
          próprio. A conta é individual e o compartilhamento de credenciais é proibido.
        </p>
      </LegalSection>

      <LegalSection n="7." title="Disponibilidade e suporte">
        <p>
          A ALSHAM empenha-se em manter a Plataforma disponível, mas não garante operação
          ininterrupta — pode haver manutenção, atualização ou indisponibilidade de terceiros. O
          suporte é prestado por e-mail (<a href="mailto:comercial@alshamglobal.com.br" className="text-[var(--color-primary)] hover:underline">comercial@alshamglobal.com.br</a>),
          em horário comercial, com prioridade de atendimento crescente nos planos Pro e Enterprise. Os
          prazos de resposta são os anunciados na página de planos no momento da contratação.
        </p>
      </LegalSection>

      <LegalSection n="8." title="Limitação de responsabilidade">
        <p>
          Nos limites permitidos pela lei brasileira — e sem prejuízo dos direitos indisponíveis do
          consumidor —, a responsabilidade da ALSHAM por danos diretos comprovados relacionados à
          Plataforma fica limitada ao valor pago pelo Assinante nos 12 meses anteriores ao fato. A
          ALSHAM não responde por decisões do Assinante tomadas com base em saídas da Plataforma nas
          áreas reguladas descritas na cláusula 5.
        </p>
      </LegalSection>

      <LegalSection n="9." title="Alterações destes Termos">
        <p>
          A ALSHAM pode atualizar estes Termos. Mudanças relevantes serão comunicadas por e-mail ou na
          Plataforma com antecedência razoável. O uso continuado após a vigência implica concordância;
          quem não concordar pode cancelar sem custo adicional além do ciclo já pago.
        </p>
      </LegalSection>

      <LegalSection n="10." title="Lei aplicável e foro">
        <p>
          Aplica-se a lei brasileira. Fica eleito o foro da comarca da sede da ALSHAM Global, no Estado
          de Goiás <Pendente>definir: fundador — comarca exata</Pendente>, ressalvado o direito do
          consumidor de demandar no foro de seu domicílio (art. 101, I, do CDC).
        </p>
      </LegalSection>
    </LegalShell>
  );
}
