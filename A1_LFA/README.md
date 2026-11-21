# Aprendizado de Máquina Aplicado à Gestão de Risco Operacional na Bolsa de Valores

**Sistema especialista com aprendizado supervisionado — atividade adaptada ao mercado financeiro e bolsa de valores (B3)**

**Atividade Avaliativa A1 — Disciplina de Inteligência Artificial e LFA**  
**Instituição:** UDF Centro Universitário  
**Professora:** Profa. Kadidja Valéria  
**Turma:** 3ª feira — Novembro de 2026  

**Autores (Grupo):**  
- **Nome:** João Paulo de Oliveira Paiva  
- **Nome:** Danilo Hellu  

**Repositório do Projeto:** [GitHub - Danilove1106/InteligenciaArtificial_LinguagensFormais_Automatos](https://github.com/Danilove1106/InteligenciaArtificial_LinguagensFormais_Automatos)  
**Notebook Google Colab:** [notebook_sistema_especialista.ipynb](./notebook_sistema_especialista.ipynb)  
**Declaração de Ética:** [Etica_e_Impactos_da_Inteligencia_Artificial/README.md](./Etica_e_Impactos_da_Inteligencia_Artificial/README.md)  

> [!IMPORTANT]
> Este projeto constitui um **protótipo didático desenvolvido para a Atividade Avaliativa A1** da disciplina de Inteligência Artificial e LFA. O sistema tem como objetivo o aprendizado e a demonstração prática da integração entre técnicas de **Machine Learning (Árvore de Decisão)** e **Sistemas Especialistas Simbólicos (Encadeamento para Frente)**. Não se destina à operação real em contas de custódia nem substitui profissionais credenciados de investimento (CNPI/CGA) ou as plataformas oficiais de negociação da B3.

---

## 🎯 Visão Geral

O projeto desenvolve um Sistema Especialista Híbrido em Python para apoiar a **governança de risco operacional e a proteção patrimonial** na execução de ordens na Bolsa de Valores brasileira (B3). A ferramenta analisa indicadores quantitativos de mercado, estima o regime de volatilidade e risco através de aprendizado supervisionado e submete a decisão a um conjunto de **regras regulatórias e operacionais explícitas (SE... ENTÃO...)** baseadas nas normas da **Comissão de Valores Mobiliários (CVM - Resolução nº 35/2021)** e no regulamento de operações da B3.

O sistema classifica as situações de mercado e gera recomendações como:
- **`AUTORIZAR_EXECUCAO_PADRAO`**;
- **`BLOQUEAR_OPERACAO_CIRCUIT_BREAKER_B3`**;
- **`BLOQUEAR_OPERACAO_TETO_PERDA_ATINGIDO`**;
- **`PAUSAR_OPERACAO_DISJUNTOR_MACROECONOMICO`**;
- **`SUSPENDER_POR_FALHA_TELEMETRIA`** (tratamento rigoroso de incerteza `'?'`);
- **`BLOQUEAR_DIRECAO_DISJUNTOR_CONSECUTIVO`**;
- **`REDUZIR_EXPOSICAO_LOTE_MINIMO`**.

---

## 1. Fundamentação Teórica

### O que são Sistemas Especialistas?
Sistemas Especialistas são programas de Inteligência Artificial simbólica que simulam o processo de raciocínio de especialistas humanos em domínios restritos e complexos. Ao contrário de modelos puramente heurísticos, operam por meio de uma base de conhecimento formalizada em regras lógicas condicionais (`SE... ENTÃO...`) e de um motor de inferência determinístico, permitindo auditar o rastro de raciocínio e justificar tecnicamente o porquê de cada orientação.

### Conceitos de Aprendizado de Máquina
- **Aprendizado de Máquina:** Paradigma computacional em que algoritmos identificam padrões estatísticos diretamente a partir de exemplos prévios, sem necessidade de programação manual de cada variação.
- **Aprendizado Supervisionado:** Treinamento conduzido com dados rotulados, onde cada instância possui suas variáveis explicativas e a respectiva classe alvo conhecida.
- **Atributos de Entrada (Features):** Variáveis quantitativas de mercado:
  - `volatilidade_atr`: Média de variação real do preço (*Average True Range*);
  - `adx_tendencia`: Força da direção da tendência (*Average Directional Index*, escala de 0 a 100);
  - `spread_pontos`: Custo de liquidez entre os melhores preços de compra e venda no livro de ofertas;
  - `retorno_recente_pct`: Variação percentual observada nas últimas barras de negociação.
- **Rótulo (Classe Alvo):** `regime_mercado` classificado em `'favoravel'` ou `'alto_risco'`.
- **Classificação vs. Regressão:** O modelo realiza classificação categórica (separando regimes de risco), em vez de estimar valores numéricos contínuos de preços futuros.
- **Treino e Teste:** Separação do dataset em 75% para ajuste do modelo e 25% para validação independente, utilizando estratificação (`stratify=y`) e semente determinística (`random_state=42`) para garantir reprodutibilidade.

### Como as Duas Abordagens Trabalham Juntas
1. O fluxo de dados recebe as métricas técnicas da sessão (ATR, ADX, Spread, Retorno) e os fatos operacionais (status de Circuit Breaker da B3, Drawdown financeiro, horário e proximidade de comunicados do Banco Central/Copom).
2. A **Árvore de Decisão** processa as métricas numéricas e prediz o fato probabilístico `regime_mercado_ml` (`favoravel` ou `alto_risco`).
3. Esse resultado é injetado como um fato derivado na memória de trabalho do **Motor de Inferência Simbólico**.
4. O motor aplica as regras regulatórias em ordem decrescente de prioridade (100 a 10), garantindo que disjuntores compulsórios prevaleçam sobre predições estatísticas.
5. A ferramenta apresenta a ação recomendada, a regra acionada, a fundamentação regulatória e a trilha de auditoria explicativa ("Como?" e "Por quê?").

---

## 2. Dataset e Atributos de Mercado

O dataset [`dataset_mercado_financeiro.csv`](./dataset_mercado_financeiro.csv) contém 36 amostras calibradas a partir de padrões históricos de negociação da B3 e indicadores macroeconômicos do Banco Central (SGS/Bacen / `dados.gov.br`).

| Atributo | Tipo | Descrição | Faixa Típica |
|---|---|---|:---:|
| `volatilidade_atr` | Numérico contínuo | Volatilidade média dos preços (pontos) | 11.5 a 64.5 |
| `adx_tendencia` | Numérico contínuo | Força direcional da tendência | 9.5 a 36.0 |
| `spread_pontos` | Inteiro | Custo de liquidez (bid/ask) | 15 a 105 |
| `retorno_recente_pct` | Numérico contínuo | Retorno acumulado no período (%) | -5.9% a +1.55% |
| `regime_mercado` | Categórico (Rótulo) | Condição estatística do mercado | `favoravel` / `alto_risco` |

---

## 3. Árvore de Decisão e Avaliação do Modelo

Implementada no módulo [`modelo_ml.py`](./modelo_ml.py) através do `DecisionTreeClassifier` da biblioteca `scikit-learn` com limite de profundidade `max_depth=3`:
- **Divisão Treino/Teste:** 27 instâncias de treinamento (75%) e 9 instâncias de teste independente (25%).
- **Acurácia no Teste:** **100,0%** no conjunto de teste independente.
- **Matriz de Confusão:**
  ```text
                Previsto: Favorável   Previsto: Alto Risco
  Real: Favorável         5                    0
  Real: Alto Risco        0                    4
  ```
- **Regras Extraídas da Árvore de Decisão:**
  ```text
  |--- volatilidade_atr <= 27.25
  |   |--- class: favoravel
  |--- volatilidade_atr >  27.25
  |   |--- class: alto_risco
  ```

---

## 4. Base de Conhecimento e Regras SE... ENTÃO... (0,5 pt)

Formalizada em [`regras.py`](./regras.py) com 12 regras organizadas por prioridade decrescente e fundamentadas na **Resolução CVM nº 35/2021** e nos regulamentos da B3:

* **Regra R01 (Circuit Breaker B3 — Prioridade 100):**
  > **SE** `circuit_breaker_bolsa` = *sim*  
  > **ENTÃO** `acao` = *BLOQUEAR_OPERACAO_CIRCUIT_BREAKER_B3*  
  > *Justificativa:* O pregão da B3 acionou o mecanismo oficial de circuit breaker (queda > 10% do Ibovespa). Bloqueio compulsório de novas entradas. (Art. 45 da Resolução CVM nº 35/2021).

* **Regra R02 (Teto de Perda Diária — Prioridade 95):**
  > **SE** `drawdown_diario_excedido` = *sim*  
  > **ENTÃO** `acao` = *BLOQUEAR_OPERACAO_TETO_PERDA_ATINGIDO*  
  > *Justificativa:* O limite máximo de perda financeira diária foi atingido, impedindo o *revenge trading* e preservando o capital do investidor.

* **Regra R03 (Tratamento de Incerteza e Dados Ausentes — Prioridade 90):**
  > **SE** `circuit_breaker_bolsa` = *?* **OU** `spread_dentro_do_limite` = *?* **OU** `horario_operacional_permitido` = *?*  
  > **ENTÃO** `acao` = *SUSPENDER_POR_FALHA_TELEMETRIA*  
  > *Justificativa:* Princípio da Precaução da CVM: havendo desconhecimento sobre variáveis críticas de cotação ou conectividade, o sistema veta qualquer execução autônoma.

* **Regra R04 (Disjuntor Macroeconômico — Prioridade 85):**
  > **SE** `evento_macro_proximo` = *sim*  
  > **ENTÃO** `acao` = *PAUSAR_OPERACAO_DISJUNTOR_MACROECONOMICO*  
  > *Justificativa:* Pausa preventiva em janelas de 15 minutos em torno de comunicados de taxa de juros do Banco Central (Copom SELIC) ou Fed.

* **Regra R05 (Filtro de Spread Excessivo — Prioridade 80):**
  > **SE** `spread_dentro_do_limite` = *não*  
  > **ENTÃO** `acao` = *BLOQUEAR_ENTRADA_SPREAD_EXCESSIVO*

* **Regra R06 (Disjuntor Direcional Consecutivo — Prioridade 75):**
  > **SE** `perdas_consecutivas_mesma_direcao` = *sim* **E** `regime_mercado_ml` = *alto_risco*  
  > **ENTÃO** `acao` = *BLOQUEAR_DIRECAO_DISJUNTOR_CONSECUTIVO*

* **Regra R07 (Redução Defensiva de Lote — Prioridade 70):**
  > **SE** `perdas_consecutivas_mesma_direcao` = *sim* **E** `regime_mercado_ml` = *favoravel*  
  > **ENTÃO** `acao` = *REDUZIR_EXPOSICAO_LOTE_MINIMO*

* **Regra R08 (Filtro de Mercado Lateral Errático — Prioridade 65):**
  > **SE** `regime_mercado_ml` = *alto_risco* **E** `adx_tendencia_forte` = *não*  
  > **ENTÃO** `acao` = *BLOQUEAR_ENTRADA_MERCADO_LATERAL_ERRATICO*

* **Regra R09 (Rompimento com Stop Ampliado — Prioridade 60):**
  > **SE** `regime_mercado_ml` = *alto_risco* **E** `adx_tendencia_forte` = *sim* **E** `spread_dentro_do_limite` = *sim*  
  > **ENTÃO** `acao` = *AUTORIZAR_OPERACAO_STOP_AMPLIADO*

* **Regra R10 (Execução Padrão em Alinhamento Ótimo — Prioridade 50):**
  > **SE** `regime_mercado_ml` = *favoravel* **E** `adx_tendencia_forte` = *sim* **E** `spread_dentro_do_limite` = *sim* **E** `horario_operacional_permitido` = *sim*  
  > **ENTÃO** `acao` = *AUTORIZAR_EXECUCAO_PADRAO*

* **Regra R11 (Mercado Calmo com Realização Parcial — Prioridade 45):**
  > **SE** `regime_mercado_ml` = *favoravel* **E** `adx_tendencia_forte` = *não*  
  > **ENTÃO** `acao` = *AUTORIZAR_COM_REALIZACAO_PARCIAL_PRECOCE*

* **Regra R12 (Fallback / Supervisão Humana do Analista — Prioridade 10):**
  > **SE** nenhuma regra anterior foi satisfeita  
  > **ENTÃO** `acao` = *ENCAMINHAR_REVISAO_GESTOR_RISCO*

---

## ⚙️ 5. Motor de Inferência (0,5 pt)

Implementado no módulo [`motor_inferencia.py`](./motor_inferencia.py):
- **Estratégia:** Encadeamento para Frente (*Forward Chaining*), avaliando premissas a partir dos fatos presentes na memória de trabalho.
- **Resolução de Conflitos:** A regra de maior prioridade válida é selecionada imediatamente, espelhando os sistemas críticos de missão em tempo real.
- **Tratamento do '?' como Incerteza:** A ausência de evidência não é tratada como falsidade. Fatos desconhecidos acionam a regra `R03` de suspensão preventiva.
- **Módulo Explicativo:** Implementa os métodos `explicar_como()` (rastreabilidade dos fatos que sustentam a decisão) e `explicar_por_que()` (fundamentação legal e técnica).
- **Trilha de Auditoria (*Audit Trail*):** Registra o histórico completo de regras testadas, aceitas e rejeitadas para compliance da CVM.

---

## 📊 6. Demonstração de Casos de Teste e Validação

O arquivo [`main.py`](./main.py) implementa a demonstração prática de cinco casos de teste cobrindo todas as categorias de decisão:

1. **Caso 1 (Entrada Regular Autorizada):** ATR = 15.0, ADX = 31.0, Spread = 18 pts, sem circuit breaker e sem perdas.  
   *Predição:* `FAVORAVEL` | *Regra:* `R10` | *Ação:* `AUTORIZAR_EXECUCAO_PADRAO`.
2. **Caso 2 (Circuit Breaker Oficial da B3):** ATR = 58.0, Circuit Breaker = `sim`.  
   *Predição:* `ALTO_RISCO` | *Regra:* `R01` | *Ação:* `BLOQUEAR_OPERACAO_CIRCUIT_BREAKER_B3`.
3. **Caso 3 (Tratamento de Incerteza '?'):** Spread = `?` (falha momentânea de telemetria).  
   *Regra:* `R03` | *Ação:* `SUSPENDER_POR_FALHA_TELEMETRIA`.
4. **Caso 4 (Disjuntor Macroeconômico):** Evento do Banco Central (Copom SELIC) nos próximos 15 min.  
   *Regra:* `R04` | *Ação:* `PAUSAR_OPERACAO_DISJUNTOR_MACROECONOMICO`.
5. **Caso 5 (Circuit Breaker Direcional):** 2 perdas consecutivas em regime de alto risco.  
   *Predição:* `ALTO_RISCO` | *Regra:* `R05/R06` | *Ação:* `BLOQUEAR_DIRECAO_DISJUNTOR_CONSECUTIVO`.

### Bateria de Testes com Pytest
O módulo [`test_sistema_especialista.py`](./test_sistema_especialista.py) conta com **12 testes unitários automatizados** com cobertura de 100% dos fluxos principais:
```bash
$ pytest -v
============================== 12 passed in 0.90s ==============================
```

---

## ⚖️ 7. Declaração de Ética e Impactos da IA (Até 0,5 pt)

A documentação ética completa encontra-se em [`Etica_e_Impactos_da_Inteligencia_Artificial/README.md`](./Etica_e_Impactos_da_Inteligencia_Artificial/README.md), respondendo com rigor aos quesitos da Aula 14 (17/11/2026):
1. **Artigo Científico:** Francisco Pires de Lacerda Júnior (Revista Foco, 2026) — integridade acadêmica, governança e distinção transparente entre apoio de programação e autoria intelectual.
2. **Vídeo IEA-USP:** Minutagem 44:18 — responsabilidade institucional, risco sistêmico e necessidade de disjuntores determinísticos frente à volatilidade algorítmica.
3. **Análise dos Cinco Eixos Éticos:** Privacidade/LGPD (dados 100% anonimizados de mercado), Viés e Equidade (amostragem balanceada), Transparência (XAI e audit trail), Supervisão e Responsabilidade (regra de fallback com o gestor de risco humano) e Impacto Social (prevenção de quebras patrimoniais sistêmicas).
4. **Declarações Oficiais de Uso de IA:**
   - *IA incorporada:* Árvore de Decisão scikit-learn integrada ao motor simbólico.
   - *IA utilizada na elaboração do trabalho:* Utilizada como apoio à programação em Python e organização textual; concepção do projeto, definição das regras e testes permaneceram sob responsabilidade humana exclusiva da equipe.

---

## 📁 8. Estrutura de Arquivos

```text
A1_LFA/
├── dataset_mercado_financeiro.csv           # Base de dados estruturada com 36 amostras
├── modelo_ml.py                             # Treinador da Árvore de Decisão supervisionada
├── regras.py                                # Base de conhecimento com as 12 regras regulatórias
├── motor_inferencia.py                      # Motor de inferência (Forward Chaining + '?')
├── main.py                                  # Script executável com 5 casos de demonstração
├── test_sistema_especialista.py             # Bateria de 12 testes automatizados em pytest
├── notebook_sistema_especialista.ipynb       # Notebook completo pronto para o Google Colab
├── Etica_e_Impactos_da_Inteligencia_Artificial/
│   └── README.md                            # Relatório ético formal da Aula 14
└── README.md                                # Documentação técnica principal da A1
```

---

## 🚀 9. Como Executar

### 1. Executar a Demonstração Principal
```bash
python3 main.py
```

### 2. Rodar a Bateria de Testes Automatizados
```bash
pytest -v
```

### 3. Treinar e Avaliar a Árvore de Decisão Isoladamente
```bash
python3 modelo_ml.py
```
