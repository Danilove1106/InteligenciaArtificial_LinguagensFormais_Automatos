"""
Módulo de Aprendizado de Máquina (Machine Learning)
Projeto: SE-RISK-TRADE (A1_LFA) - Sistema Especialista em Gestão de Risco Operacional na Bolsa de Valores
Autores: João Paulo de Oliveira Paiva e Danilo Hellu
Instituição: UDF Centro Universitário
Disciplina: Inteligência Artificial e LFA
Professora: Profa. Kadidja Valéria

Objetivo:
Treinar um classificador de Árvore de Decisão a partir de séries e indicadores quantitativos
de mercado financeiro (Volatilidade ATR, Força de Tendência ADX, Custo de Liquidez/Spread e Retorno Recente)
obtidos a partir de séries públicas da B3 / Banco Central do Brasil (SGS/Bacen / dados.gov.br).
O modelo prevê o fato 'regime_mercado' ('favoravel' ou 'alto_risco'), que é integrado
como premissa no motor de inferência determinístico.
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, confusion_matrix

class ClassificadorRegimeMercado:
    def __init__(self, caminho_csv=None, max_depth=3, random_state=42):
        self.caminho_csv = caminho_csv or os.path.join(
            os.path.dirname(__file__), "dataset_mercado_financeiro.csv"
        )
        self.max_depth = max_depth
        self.random_state = random_state
        self.modelo = None
        self.atributos = [
            "volatilidade_atr",
            "adx_tendencia",
            "spread_pontos",
            "retorno_recente_pct"
        ]
        self.rotulo = "regime_mercado"
        self.acuracia = 0.0
        self.matriz_confusao = None
        self.X_treino = None
        self.X_teste = None
        self.y_treino = None
        self.y_teste = None
        self.regras_arvore_texto = ""

    def carregar_e_treinar(self):
        """Carrega o dataset, realiza divisão estratificada (75% treino, 25% teste) e treina a árvore."""
        if not os.path.exists(self.caminho_csv):
            raise FileNotFoundError(f"Arquivo do dataset não encontrado em: {self.caminho_csv}")

        dados = pd.read_csv(self.caminho_csv)
        X = dados[self.atributos]
        y = dados[self.rotulo]

        # Divisão com estratificação para manter a proporção exata das classes
        self.X_treino, self.X_teste, self.y_treino, self.y_teste = train_test_split(
            X, y, test_size=0.25, random_state=self.random_state, stratify=y
        )

        self.modelo = DecisionTreeClassifier(
            max_depth=self.max_depth,
            random_state=self.random_state
        )
        self.modelo.fit(self.X_treino, self.y_treino)

        # Avaliação no conjunto de teste independente
        y_pred = self.modelo.predict(self.X_teste)
        self.acuracia = float(accuracy_score(self.y_teste, y_pred))
        self.matriz_confusao = confusion_matrix(self.y_teste, y_pred, labels=["favoravel", "alto_risco"])
        self.regras_arvore_texto = export_text(self.modelo, feature_names=self.atributos)

        return {
            "total_amostras": len(dados),
            "treino": len(self.X_treino),
            "teste": len(self.X_teste),
            "acuracia": self.acuracia,
            "matriz_confusao": self.matriz_confusao
        }

    def prever_regime(self, volatilidade_atr: float, adx_tendencia: float, spread_pontos: int, retorno_recente_pct: float):
        """
        Executa a predição do regime de mercado para os parâmetros informados.
        Retorna:
            regime (str): 'favoravel' ou 'alto_risco'
            fora_intervalo (bool): Indica se algum atributo ultrapassou os limites do conjunto de treino.
        """
        if self.modelo is None:
            self.carregar_e_treinar()

        # Validações de consistência técnica
        if volatilidade_atr <= 0:
            raise ValueError("Volatilidade ATR deve ser estritamente positiva.")
        if adx_tendencia < 0 or adx_tendencia > 100:
            raise ValueError("Indicador ADX deve situar-se entre 0 e 100.")
        if spread_pontos < 0:
            raise ValueError("Spread não pode ser negativo.")

        instancia = pd.DataFrame([{
            "volatilidade_atr": float(volatilidade_atr),
            "adx_tendencia": float(adx_tendencia),
            "spread_pontos": int(spread_pontos),
            "retorno_recente_pct": float(retorno_recente_pct)
        }])

        predicao = self.modelo.predict(instancia)[0]

        # Verificação de segurança: parâmetros fora dos limites de treinamento
        fora = any(
            not self.X_treino[c].min() <= instancia[c].iloc[0] <= self.X_treino[c].max()
            for c in self.atributos
        )

        return predicao, fora

if __name__ == "__main__":
    clf = ClassificadorRegimeMercado()
    res = clf.carregar_e_treinar()
    print("=== MODELO DE ÁRVORE DE DECISÃO TREINADO ===")
    print(f"Total de Amostras: {res['total_amostras']} | Treino: {res['treino']} | Teste: {res['teste']}")
    print(f"Acurácia no Teste: {res['acuracia'] * 100:.2f}%")
    print("Matriz de Confusão:")
    print(res["matriz_confusao"])
    print("\nRegras Aprendidas pela Árvore:")
    print(clf.regras_arvore_texto)
