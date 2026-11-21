"""
Módulo da Base de Conhecimento e Regras de Negócio
Projeto: SE-RISK-TRADE (A1_LFA) - Sistema Especialista em Gestão de Risco Operacional na Bolsa de Valores
Autores: João Paulo de Oliveira Paiva e Danilo Hellu
Instituição: UDF Centro Universitário
Disciplina: Inteligência Artificial e LFA
Professora: Profa. Kadidja Valéria

Fundamentação Regulatória e Técnica:
- Resolução CVM nº 35/2021 (Normas de negociação automatizada e sistemas algorítmicos).
- Manual de Procedimentos Operacionais de Negociação da B3 (Regras de Circuit Breaker e Risco).
- Diretrizes de Gestão de Riscos de Mercado e Liquidez do Banco Central do Brasil (Bacen / dados.gov.br).
- Modelagem Quantitativa de Trading Sistemático (XM_Trade / Metodologias de Volatilidade e Tendência).
"""

REGRAS_RISCO_TRADE = [
    {
        "id": "R01",
        "nome": "Circuit Breaker Institucional da Bolsa (B3)",
        "prioridade": 100,
        "condicoes": {
            "circuit_breaker_bolsa": "sim"
        },
        "acao": "BLOQUEAR_OPERACAO_CIRCUIT_BREAKER_B3",
        "explicacao": "O pregão da B3 acionou o mecanismo oficial de Circuit Breaker (queda superior a 10% do índice). Bloqueio compulsório de novas entradas.",
        "fundamento_legal": "Regulamento de Negociação B3 e Art. 45 da Resolução CVM nº 35/2021 (Interrupção Ordenada)."
    },
    {
        "id": "R02",
        "nome": "Teto Máximo de Perda Diária Atingido (Daily Drawdown)",
        "prioridade": 95,
        "condicoes": {
            "drawdown_diario_excedido": "sim"
        },
        "acao": "BLOQUEAR_OPERACAO_TETO_PERDA_ATINGIDO",
        "explicacao": "A perda financeira acumulada na sessão atingiu o limite máximo de segurança patrimonial (drawdown diário). Bloqueio do robô até a próxima sessão.",
        "fundamento_legal": "Diretrizes de Risco Operacional CVM / Anbima para preservação de capital."
    },
    {
        "id": "R03",
        "nome": "Incerteza / Falha de Telemetria de Mercado ('?')",
        "prioridade": 90,
        "condicoes_custom": lambda fatos: any(
            fatos.get(k) == "?" for k in ["circuit_breaker_bolsa", "spread_dentro_do_limite", "horario_operacional_permitido"]
        ),
        "acao": "SUSPENDER_POR_FALHA_TELEMETRIA",
        "explicacao": "Informações essenciais de conectividade ou cotação estão em estado desconhecido ('?'). O sistema veta qualquer execução por precaução.",
        "fundamento_legal": "Princípio da Precaução da CVM: ausência de telemetria auditável veta a operação autônoma."
    },
    {
        "id": "R04",
        "nome": "Disjuntor de Divulgação Macroeconômica de Alto Impacto",
        "prioridade": 85,
        "condicoes": {
            "evento_macro_proximo": "sim"
        },
        "acao": "PAUSAR_OPERACAO_DISJUNTOR_MACROECONOMICO",
        "explicacao": "Janela temporal de 15 minutos antes/depois de eventos do Banco Central (Copom SELIC) ou Fed. Pausa preventiva para evitar derrapagem extrema de liquidez.",
        "fundamento_legal": "Boas práticas de negociação automatizada frente à volatilidade exógena induzida por comunicados oficiais."
    },
    {
        "id": "R05",
        "nome": "Spread Fora do Limite Máximo Aceitável",
        "prioridade": 80,
        "condicoes": {
            "spread_dentro_do_limite": "não"
        },
        "acao": "BLOQUEAR_ENTRADA_SPREAD_EXCESSIVO",
        "explicacao": "O spread de compra/venda ultrapassa o limite calibrado, tornando o custo operacional desfavorável e gerando slippage negativo.",
        "fundamento_legal": "Manual de Melhores Práticas de Execução de Ordens (Best Execution)."
    },
    {
        "id": "R06",
        "nome": "Disjuntor Direcional após Perdas Consecutivas sob Risco Alto",
        "prioridade": 75,
        "condicoes": {
            "perdas_consecutivas_mesma_direcao": "sim",
            "regime_mercado_ml": "alto_risco"
        },
        "acao": "BLOQUEAR_DIRECAO_DISJUNTOR_CONSECUTIVO",
        "explicacao": "Ocorreram duas ou mais perdas consecutivas no mesmo sentido em regime de alto risco previsto pelo modelo de ML. Bloqueio na direção perdedora.",
        "fundamento_legal": "Mecanismo de Circuit Breaker Direcional proprietário (evita efeito cascata em reversões falsas)."
    },
    {
        "id": "R07",
        "nome": "Ajuste Defensivo de Volume sob Perdas Consecutivas em Regime Favorável",
        "prioridade": 70,
        "condicoes": {
            "perdas_consecutivas_mesma_direcao": "sim",
            "regime_mercado_ml": "favoravel"
        },
        "acao": "REDUZIR_EXPOSICAO_LOTE_MINIMO",
        "explicacao": "Mercado estatisticamente favorável, porém com perdas recentes. Ação de prudência reduzindo o volume do lote ao valor mínimo fracionado.",
        "fundamento_legal": "Controle Adaptativo de Posição e Gestão de Drawdown."
    },
    {
        "id": "R08",
        "nome": "Mercado Errático Lateral com Alto Risco Estatístico",
        "prioridade": 65,
        "condicoes": {
            "regime_mercado_ml": "alto_risco",
            "adx_tendencia_forte": "não"
        },
        "acao": "BLOQUEAR_ENTRADA_MERCADO_LATERAL_ERRATICO",
        "explicacao": "Modelo de Árvore de Decisão apontou alto risco e o ADX indica ausência de tendência clara (< 18.0). Mercado sem direção com ruído destrutivo.",
        "fundamento_legal": "Critério Quantitativo de Exclusão de Operações de Ruído (Chop Market Filter)."
    },
    {
        "id": "R09",
        "nome": "Rompimento de Tendência em Alta Volatilidade",
        "prioridade": 60,
        "condicoes": {
            "regime_mercado_ml": "alto_risco",
            "adx_tendencia_forte": "sim",
            "spread_dentro_do_limite": "sim"
        },
        "acao": "AUTORIZAR_OPERACAO_STOP_AMPLIADO",
        "explicacao": "Mercado em forte movimento direcional (ADX elevado) apesar da alta volatilidade. Operação autorizada com multiplicador de Stop Loss estendido (2.0x ATR).",
        "fundamento_legal": "Estratégia Quantitativa de Breakout com Stop Dinâmico baseado em ATR."
    },
    {
        "id": "R10",
        "nome": "Condições Ideais de Liquidez e Tendência (Execução Padrão)",
        "prioridade": 50,
        "condicoes": {
            "regime_mercado_ml": "favoravel",
            "adx_tendencia_forte": "sim",
            "spread_dentro_do_limite": "sim",
            "horario_operacional_permitido": "sim"
        },
        "acao": "AUTORIZAR_EXECUCAO_PADRAO",
        "explicacao": "Todos os indicadores quantitativos favoráveis, liquidez plena, spread estreito e regime estatístico validado pela Árvore de Decisão.",
        "fundamento_legal": "Conformidade Total com os Critérios do Algoritmo de Execução Direta."
    },
    {
        "id": "R11",
        "nome": "Regime Favorável em Mercado Calmo (Scalping com Parcial Rápida)",
        "prioridade": 45,
        "condicoes": {
            "regime_mercado_ml": "favoravel",
            "adx_tendencia_forte": "não"
        },
        "acao": "AUTORIZAR_COM_REALIZACAO_PARCIAL_PRECOCE",
        "explicacao": "Regime favorável e estável, porém sem tendência acelerada. Operação autorizada com ordem de realização parcial no primeiro alvo curto (0.5x ATR).",
        "fundamento_legal": "Técnica de Desriscamento Prematuro de Posição em Operações de Retração."
    },
    {
        "id": "R12",
        "nome": "Fallback / Supervisão do Analista de Risco",
        "prioridade": 10,
        "condicoes": {},  # Sempre verdadeira se nenhuma outra disparar
        "acao": "ENCAMINHAR_REVISAO_GESTOR_RISCO",
        "explicacao": "Combinação não mapeada de parâmetros de mercado. Decisão repassada para supervisão humana do gestor da mesa.",
        "fundamento_legal": "Art. 4º da Resolução CVM nº 35/2021 (Obrigatoriedade de Supervisão Humana em Negociação Automatizada)."
    }
]
