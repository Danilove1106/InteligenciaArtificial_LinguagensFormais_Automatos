"""
Bateria de Testes Automatizados com Pytest
Projeto: SE-RISK-TRADE (A1_LFA) - Sistema Especialista de Gestão de Risco Operacional na Bolsa de Valores
Autores: João Paulo de Oliveira Paiva e Danilo Hellu
"""

import pytest
from modelo_ml import ClassificadorRegimeMercado
from main import SistemaEspecialistaTrade

@pytest.fixture
def sistema():
    return SistemaEspecialistaTrade()

def test_modelo_ml_treinamento_e_acuracia():
    clf = ClassificadorRegimeMercado()
    metricas = clf.carregar_e_treinar()
    assert metricas["total_amostras"] >= 30
    assert metricas["acuracia"] >= 0.85
    assert clf.modelo is not None

def test_r01_circuit_breaker_b3(sistema):
    res = sistema.avaliar_operacao(
        volatilidade_atr=55.0, adx_tendencia=12.0, spread_pontos=80, retorno_recente_pct=-5.0,
        circuit_breaker_bolsa="sim"
    )
    assert res["regra_id"] == "R01"
    assert res["acao_recomendada"] == "BLOQUEAR_OPERACAO_CIRCUIT_BREAKER_B3"

def test_r02_drawdown_diario(sistema):
    res = sistema.avaliar_operacao(
        volatilidade_atr=20.0, adx_tendencia=25.0, spread_pontos=20, retorno_recente_pct=-1.5,
        circuit_breaker_bolsa="não", drawdown_diario_excedido="sim"
    )
    assert res["regra_id"] == "R02"
    assert res["acao_recomendada"] == "BLOQUEAR_OPERACAO_TETO_PERDA_ATINGIDO"

def test_r03_tratamento_incerteza_interrogacao(sistema):
    res = sistema.avaliar_operacao(
        volatilidade_atr=15.0, adx_tendencia=30.0, spread_pontos=18, retorno_recente_pct=1.0,
        circuit_breaker_bolsa="?", spread_dentro_do_limite="sim"
    )
    assert res["regra_id"] == "R03"
    assert res["acao_recomendada"] == "SUSPENDER_POR_FALHA_TELEMETRIA"

def test_r04_disjuntor_macroeconomico(sistema):
    res = sistema.avaliar_operacao(
        volatilidade_atr=22.0, adx_tendencia=26.0, spread_pontos=22, retorno_recente_pct=0.4,
        circuit_breaker_bolsa="não", drawdown_diario_excedido="não", evento_macro_proximo="sim"
    )
    assert res["regra_id"] == "R04"
    assert res["acao_recomendada"] == "PAUSAR_OPERACAO_DISJUNTOR_MACROECONOMICO"

def test_r05_spread_excessivo(sistema):
    res = sistema.avaliar_operacao(
        volatilidade_atr=15.0, adx_tendencia=30.0, spread_pontos=90, retorno_recente_pct=1.0,
        circuit_breaker_bolsa="não", drawdown_diario_excedido="não", evento_macro_proximo="não",
        spread_dentro_do_limite="não"
    )
    assert res["regra_id"] == "R05"
    assert res["acao_recomendada"] == "BLOQUEAR_ENTRADA_SPREAD_EXCESSIVO"

def test_r06_disjuntor_direcional_alto_risco(sistema):
    res = sistema.avaliar_operacao(
        volatilidade_atr=50.0, adx_tendencia=13.0, spread_pontos=75, retorno_recente_pct=-3.5,
        circuit_breaker_bolsa="não", drawdown_diario_excedido="não", evento_macro_proximo="não",
        perdas_consecutivas_mesma_direcao="sim", spread_dentro_do_limite="sim"
    )
    assert res["regime_mercado_ml"] == "alto_risco"
    assert res["regra_id"] == "R06"
    assert res["acao_recomendada"] == "BLOQUEAR_DIRECAO_DISJUNTOR_CONSECUTIVO"

def test_r07_ajuste_volume_favoravel(sistema):
    res = sistema.avaliar_operacao(
        volatilidade_atr=14.0, adx_tendencia=30.0, spread_pontos=18, retorno_recente_pct=0.9,
        circuit_breaker_bolsa="não", drawdown_diario_excedido="não", evento_macro_proximo="não",
        perdas_consecutivas_mesma_direcao="sim", spread_dentro_do_limite="sim"
    )
    assert res["regime_mercado_ml"] == "favoravel"
    assert res["regra_id"] == "R07"
    assert res["acao_recomendada"] == "REDUZIR_EXPOSICAO_LOTE_MINIMO"

def test_r08_mercado_lateral_erratico(sistema):
    res = sistema.avaliar_operacao(
        volatilidade_atr=45.0, adx_tendencia=12.0, spread_pontos=60, retorno_recente_pct=-2.5,
        circuit_breaker_bolsa="não", drawdown_diario_excedido="não", evento_macro_proximo="não",
        perdas_consecutivas_mesma_direcao="não", spread_dentro_do_limite="sim", adx_tendencia_forte="não"
    )
    assert res["regime_mercado_ml"] == "alto_risco"
    assert res["regra_id"] == "R08"
    assert res["acao_recomendada"] == "BLOQUEAR_ENTRADA_MERCADO_LATERAL_ERRATICO"

def test_r10_autorizar_execucao_padrao(sistema):
    res = sistema.avaliar_operacao(
        volatilidade_atr=15.0, adx_tendencia=32.0, spread_pontos=16, retorno_recente_pct=1.2,
        circuit_breaker_bolsa="não", drawdown_diario_excedido="não", evento_macro_proximo="não",
        perdas_consecutivas_mesma_direcao="não", spread_dentro_do_limite="sim", adx_tendencia_forte="sim",
        horario_operacional_permitido="sim"
    )
    assert res["regime_mercado_ml"] == "favoravel"
    assert res["regra_id"] == "R10"
    assert res["acao_recomendada"] == "AUTORIZAR_EXECUCAO_PADRAO"

def test_explicabilidade_e_auditoria(sistema):
    res = sistema.avaliar_operacao(
        volatilidade_atr=15.0, adx_tendencia=32.0, spread_pontos=16, retorno_recente_pct=1.2,
        circuit_breaker_bolsa="não", drawdown_diario_excedido="não", evento_macro_proximo="não",
        perdas_consecutivas_mesma_direcao="não", spread_dentro_do_limite="sim", adx_tendencia_forte="sim"
    )
    assert "explicacao_como" in res
    assert "fundamento_legal" in res
    assert res["total_regras_avaliadas"] > 0

def test_validacao_parametros_invalidos(sistema):
    with pytest.raises(ValueError):
        sistema.avaliar_operacao(
            volatilidade_atr=-10.0, adx_tendencia=30.0, spread_pontos=20, retorno_recente_pct=0.0
        )
    with pytest.raises(ValueError):
        sistema.avaliar_operacao(
            volatilidade_atr=15.0, adx_tendencia=150.0, spread_pontos=20, retorno_recente_pct=0.0
        )
    with pytest.raises(ValueError):
        sistema.avaliar_operacao(
            volatilidade_atr=15.0, adx_tendencia=30.0, spread_pontos=-5, retorno_recente_pct=0.0
        )
