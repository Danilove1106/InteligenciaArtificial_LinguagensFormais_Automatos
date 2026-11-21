"""
Módulo Principal de Integração e Execução
Projeto: SE-RISK-TRADE (A1_LFA) - Sistema Especialista de Gestão de Risco Operacional na Bolsa de Valores
Integrantes: João Paulo de Oliveira Paiva e Danilo Hellu
Instituição: UDF Centro Universitário
Disciplina: Inteligência Artificial e LFA
Professora: Profa. Kadidja Valéria
Data: Novembro/2026
"""

from modelo_ml import ClassificadorRegimeMercado
from motor_inferencia import MotorInferenciaRisco

class SistemaEspecialistaTrade:
    def __init__(self):
        self.classificador = ClassificadorRegimeMercado()
        self.classificador.carregar_e_treinar()
        self.motor = MotorInferenciaRisco()

    def avaliar_operacao(
        self,
        volatilidade_atr: float,
        adx_tendencia: float,
        spread_pontos: int,
        retorno_recente_pct: float,
        circuit_breaker_bolsa: str = "não",
        drawdown_diario_excedido: str = "não",
        evento_macro_proximo: str = "não",
        perdas_consecutivas_mesma_direcao: str = "não",
        spread_dentro_do_limite: str = "sim",
        adx_tendencia_forte: str = "sim",
        horario_operacional_permitido: str = "sim"
    ):
        """
        Integração Híbrida:
        1. Fase Estatística (ML): Prediz o 'regime_mercado' ('favoravel' ou 'alto_risco') via Árvore de Decisão.
        2. Fase Simbólica (SE): Aplica regras regulatórias (CVM/B3/Bacen) por Encadeamento para Frente.
        """
        # Fase 1: Árvore de Decisão
        regime_ml, fora_intervalo = self.classificador.prever_regime(
            volatilidade_atr=volatilidade_atr,
            adx_tendencia=adx_tendencia,
            spread_pontos=spread_pontos,
            retorno_recente_pct=retorno_recente_pct
        )

        # Fase 2: Montagem da Memória de Trabalho
        fatos = {
            "regime_mercado_ml": regime_ml,
            "circuit_breaker_bolsa": circuit_breaker_bolsa,
            "drawdown_diario_excedido": drawdown_diario_excedido,
            "evento_macro_proximo": evento_macro_proximo,
            "perdas_consecutivas_mesma_direcao": perdas_consecutivas_mesma_direcao,
            "spread_dentro_do_limite": spread_dentro_do_limite,
            "adx_tendencia_forte": adx_tendencia_forte,
            "horario_operacional_permitido": horario_operacional_permitido
        }

        # Execução da Inferência
        resultado = self.motor.executar(fatos)
        resultado["regime_mercado_ml"] = regime_ml
        resultado["aviso_estatistico"] = (
            "Aviso: Os parâmetros quantitativos extrapolaram os limites do conjunto de treino."
            if fora_intervalo else "Parâmetros quantitativos dentro da distribuição de calibração."
        )
        resultado["fatos_completos"] = fatos

        return resultado

def imprimir_relatorio_caso(caso_num, dados_caso, resultado):
    print("=" * 85)
    print(f"📈 CASO OPERACIONAL Nº {caso_num}: {dados_caso['descricao']}")
    print("-" * 85)
    print(f"• Indicadores Técnicos: ATR={dados_caso['atr']} | ADX={dados_caso['adx']} | Spread={dados_caso['spread']} pts | Retorno={dados_caso['retorno']}%")
    print(f"• Fatos Operacionais (s/n/?): Circuit Breaker={dados_caso['cb']} | Drawdown Diário={dados_caso['dd']} | Evento Macro={dados_caso['macro']} | Perdas Consec.={dados_caso['perdas']} | Spread OK={dados_caso['spread_ok']} | Horário Permitido={dados_caso['horario']}")
    print("-" * 85)
    print(f"🤖 Predição da Árvore de Decisão: REGIME {resultado['regime_mercado_ml'].upper()}")
    print(f"⚙️  Regra Acionada pelo Motor: [{resultado['regra_id']}] {resultado['regra_nome']}")
    print(f"🎯 DECISÃO OPERACIONAL: >>> {resultado['acao_recomendada']} <<<")
    print(f"📋 Justificativa Técnica: {resultado['explicacao']}")
    print(f"⚖️  Fundamento Regulatório: {resultado['fundamento_legal']}")
    print(f"🔍 Trilha de Auditoria ('Como?'): {resultado['explicacao_como']}")
    print(f"ℹ️  Diagnóstico Estatístico: {resultado['aviso_estatistico']}")
    print("=" * 85 + "\n")

def executar_demonstracao():
    sistema = SistemaEspecialistaTrade()

    casos = [
        {
            "descricao": "Condições Ideais de Mercado para Entrada Automática Regular",
            "atr": 15.0, "adx": 31.0, "spread": 18, "retorno": 1.10,
            "cb": "não", "dd": "não", "macro": "não", "perdas": "não",
            "spread_ok": "sim", "adx_forte": "sim", "horario": "sim"
        },
        {
            "descricao": "Ativação de Circuit Breaker Institucional na B3 (Queda > 10% no Ibovespa)",
            "atr": 58.0, "adx": 12.0, "spread": 85, "retorno": -4.80,
            "cb": "sim", "dd": "não", "macro": "não", "perdas": "não",
            "spread_ok": "não", "adx_forte": "não", "horario": "sim"
        },
        {
            "descricao": "Preservação da Incerteza ('?') diante de Falha de Telemetria/Cotação",
            "atr": 16.0, "adx": 28.0, "spread": 20, "retorno": 0.50,
            "cb": "não", "dd": "não", "macro": "não", "perdas": "não",
            "spread_ok": "?", "adx_forte": "sim", "horario": "sim"
        },
        {
            "descricao": "Disjuntor Macroeconômico: Comunicado de Taxa de Juros do Banco Central (Copom)",
            "atr": 22.0, "adx": 25.0, "spread": 25, "retorno": 0.20,
            "cb": "não", "dd": "não", "macro": "sim", "perdas": "não",
            "spread_ok": "sim", "adx_forte": "sim", "horario": "sim"
        },
        {
            "descricao": "Circuit Breaker Direcional: 2 Perdas Consecutivas sob Regime de Alto Risco",
            "atr": 49.0, "adx": 14.0, "spread": 70, "retorno": -3.20,
            "cb": "não", "dd": "não", "macro": "não", "perdas": "sim",
            "spread_ok": "não", "adx_forte": "não", "horario": "sim"
        }
    ]

    print("\n" + "#" * 85)
    print("   SISTEMA ESPECIALISTA EM GESTÃO DE RISCO OPERACIONAL NA BOLSA DE VALORES")
    print("   Projeto A1_LFA | Integrantes: João Paulo de Oliveira Paiva e Danilo Hellu")
    print("   Disciplina: Inteligência Artificial e LFA | Professora: Profa. Kadidja Valéria")
    print("#" * 85 + "\n")

    for i, caso in enumerate(casos, 1):
        res = sistema.avaliar_operacao(
            volatilidade_atr=caso["atr"],
            adx_tendencia=caso["adx"],
            spread_pontos=caso["spread"],
            retorno_recente_pct=caso["retorno"],
            circuit_breaker_bolsa=caso["cb"],
            drawdown_diario_excedido=caso["dd"],
            evento_macro_proximo=caso["macro"],
            perdas_consecutivas_mesma_direcao=caso["perdas"],
            spread_dentro_do_limite=caso["spread_ok"],
            adx_tendencia_forte=caso["adx_forte"],
            horario_operacional_permitido=caso["horario"]
        )
        imprimir_relatorio_caso(i, caso, res)

if __name__ == "__main__":
    executar_demonstracao()
