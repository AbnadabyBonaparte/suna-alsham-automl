// src/components/email/WeeklyValueEmail.tsx
import React from 'react';
import { Email, Item, Span, Section, Text, Button, Header, Footer } from '@react-email/components';

export default function WeeklyValueEmail({
    weekRange = '01/11 - 07/11',
    totalValue = 'R$ 18.430,00',
    timeSaved = '247h',
    tasksAutomated = 1847,
    rank = 'Top 8%',
}) {
    return (
        <Email title="Resumo Semanal de Valor">
            <Header style={{ background: '#020C1B', color: '#fff', padding: '20px', textAlign: 'center' }}>
                <h1>Seu Resumo Semanal de Impacto</h1>
            </Header>
            <Section style={{ padding: '20px' }}>
                <Item>
                    <Text style={{ fontSize: '24px', fontWeight: 'bold' }}>{totalValue}</Text>
                    <Span style={{ color: '#888' }}>Valor Gerado Esta Semana</Span>
                </Item>
                <Item style={{ marginTop: '20px' }}>
                    <Text>🏆 <strong>Conquista da Semana</strong></Text>
                    <Text>Você bateu seu recorde mensal de produtividade: +94%!</Text>
                </Item>
                <Item style={{ marginTop: '20px' }}>
                    <Text>⚡ <strong>Destaques</strong></Text>
                    <ul style={{ margin: 0, paddingLeft: '20px' }}>
                        <li>{timeSaved} economizadas através de automação</li>
                        <li>{tasksAutomated} tarefas processadas pelos seus agentes</li>
                        <li>{rank} dos usuários mais produtivos</li>
                    </ul>
                </Item>
                <Item style={{ marginTop: '20px' }}>
                    <Button href="https://suna-alsaham.com/dashboard" style={{ background: '#6C3483', color: '#fff', padding: '10px 20px', borderRadius: '5px' }}>
                        Otimizar Agente CORE (+15% performance)
                    </Button>
                </Item>
            </Section>
            <Footer style={{ background: '#020C1B', color: '#fff', padding: '10px', textAlign: 'center' }}>
                <Text>Continue assim! Você está no caminho para Elite status.</Text>
            </Footer>
        </Email>
    );
}
