# ⚖️ REGISTRO NO GITHUB DA ÉTICA E IMPLICAÇÕES DO PROJETO ESPECIALISTA (0,5 pt A1)
### Disciplina: Inteligência Artificial e LFA — Aula 14 (17/11/2026)
**UDF Centro Universitário**  
**Professora:** Profa. Kadidja Valéria  
**Projeto:** SE-RISK-TRADE — Sistema Especialista Híbrido de Gestão de Risco Operacional na Bolsa de Valores  
**Integrantes:** João Paulo de Oliveira Paiva e Danilo Hellu  

---

## 1. Leitura e Vídeo

### 📖 Artigo Científico (Agosto de 2026)
* **Referência:** LACERDA JÚNIOR, Francisco Pires de. *Da proibição à governança: uso ético da inteligência artificial generativa na educação superior — uma revisão integrativa (2023–2026)*. Revista Foco, v. 19, n. 8, 2026.
* **Questão de integridade acadêmica considerada:**  
  A equipe considerou como diretriz central o princípio da **transparência e governança ativa da autoria**, destacado por Lacerda Júnior (2026). O autor enfatiza que a utilização ética de ferramentas de inteligência artificial em trabalhos acadêmicos exige a clara demarcação entre as atividades de programação/auxílio contextual e a verdadeira autoria e responsabilidade intelectual. Dessa forma, a concepção do problema, o desenho das regras de negócio regulatórias, a validação empírica e a responsabilidade pelas conclusões do sistema são integralmente humanas, cabendo à IA o papel de ferramenta de apoio à codificação, estruturação e refinamento de dados.

### 🎥 Vídeo IEA-USP (Junho de 2026)
* **Referência:** Instituto de Estudos Avançados da USP (IEA-USP). *O Estado da Arte em Ética na Inteligência Artificial*, gravação completa (2h01m).
* **Trecho Selecionado:** Minutagem `44:18` a `48:50` — *"Responsabilidade Institucional, Risco Sistêmico e a Falácia da Autonomia Algorítmica nos Mercados"*.
* **Ideia para debate:**  
  O debatedor destaca que sistemas algorítmicos autônomos que operam sem disjuntores determinísticos (*hard rules*) podem desencadear efeitos de manada e *flash crashes* com severo impacto socioeconômico. A responsabilidade institucional impõe que qualquer automação orientada a decisões financeiras deve subordinar as inferências probabilísticas a travas éticas e regulatórias intransponíveis, com supervisão humana permanente.

---

## 2. Análise Ética do Projeto

### Apresentação do Projeto
O **SE-RISK-TRADE** é uma solução híbrida desenvolvida para apoiar operadores e analistas de risco na mitigação de falhas operacionais e na proteção patrimonial durante a negociação algorítmica de ativos na Bolsa de Valores (B3 / mercado financeiro). O problema abordado é a exposição descontrolada de capital provocada por oscilações abruptas de volatilidade, falhas de telemetria ou insistência emocional em posições perdedoras. O sistema é utilizado por gestores de risco, operadores quantitativos e investidores institucionais, impactando a estabilidade financeira das carteiras geridas. A Inteligência Artificial participa em duas camadas distintas: um modelo supervisionado de **Árvore de Decisão** prevê o fato probabilístico `regime_mercado` ('favoravel' vs 'alto_risco') a partir de séries públicas do Bacen/CVM/B3 (ATR, ADX, spread e retorno); sobre essa previsão, a equipe estruturou um **Motor de Inferência Simbólico** que aplica regras determinísticas estritas baseadas na Resolução CVM nº 35/2021 e no manual de operações da B3, garantindo que nenhuma ordem seja executada se os disjuntores de segurança (circuit breaker, drawdown diário ou dados ausentes '?') forem violados.

### Tabela de Aspectos Éticos

| Aspecto | Pergunta de Orientação | Situação Concreta no Projeto | Quem Pode ser Afetado | Medida Adotada pela Equipe |
|---|---|---|---|---|
| **Privacidade e Dados** | *Quais dados são utilizados? Podem identificar pessoas? É possível alcançar a finalidade com menos dados?* | O sistema utiliza exclusivamente dados e séries públicas e anonimizadas de mercado (cotações, volatilidade ATR, força de tendência ADX, taxas de juros do Banco Central e histórico de ticks da B3). | Operadores e titulares de contas de custódia. | O sistema não solicita nem armazena CPFs, senhas bancárias ou dados pessoais sensíveis, operando estritamente sobre telemetria e métricas financeiras agregadas, em total conformidade com a LGPD (Lei nº 13.709/2018). |
| **Viés e Equidade** | *As regras, os dados ou os rótulos podem prejudicar algum grupo? Como a equipe verificará isso?* | O modelo de Machine Learning poderia apresentar viés estatístico se treinado apenas em momentos atípicos de mercado (ex.: apenas mercado em alta contínua ou apenas crises agudas). | Investidores e participantes da mesa de operações. | A equipe utilizou amostragem balanceada com dados de diferentes regimes de mercado, divisão estratificada (`stratify=y`) e auditoria da base com 12 testes automatizados em pytest para garantir que as decisões de risco sejam aplicadas com equidade técnica. |
| **Transparência** | *Como a pessoa saberá que recebeu uma saída de IA? Que informações ajudarão a entender a recomendação?* | O operador precisa saber exatamente por que uma ordem foi bloqueada ou reduzida, sem respostas opacas de "caixa-preta". | O gestor de risco e o operador da mesa de operações. | Todas as saídas do motor incluem explicabilidade em dois níveis: o método `explicar_como()` (revelando quais fatos satisfizeram a regra) e o método `explicar_por_que()` (informando a justificativa técnica e o fundamento legal da CVM/B3), além da trilha de auditoria completa (*audit trail*). |
| **Supervisão e Responsabilidade** | *Quem revisa uma saída inadequada? Como a pessoa pode corrigir dados ou contestar a recomendação?* | Uma recomendação de bloqueio de entrada pode ocorrer em um momento em que o operador identifique uma oportunidade discricionária de mercado. | O investidor e a equipe de gestão de ativos. | O sistema implementa o princípio da supervisão humana estipulado no Art. 4º da Resolução CVM nº 35/2021: a regra de contingência residual (`R12`) prevê encaminhamento automático para o gestor de risco humano, que retém autoridade irrevogável para intervir ou sobrestar o robô. |
| **Impacto Social** | *Quem se beneficia? Quem pode ser prejudicado se a recomendação estiver errada ou for tratada como definitiva?* | Prevenção de quebras patrimoniais por efeito cascata de ordens automáticas sem disjuntor. Se a regra falhar, o capital do cliente pode ser corroído. | Investidores individuais, fundos e a estabilidade da infraestrutura de mercado. | O sistema trata suas saídas como suporte à decisão com tolerância zero a falhas em disjuntores críticos; qualquer incerteza de telemetria ('?') força a suspensão preventiva de ordens, evitando a propagação de riscos sistêmicos. |

---

## 3. Debate em Sala e Reflexão Individual

### 1. Dilema Ético do Projeto
* **Descrição do Dilema:**  
  Em momentos de extrema volatilidade de mercado (como anúncios inesperados de política monetária do Banco Central ou eventos geopolíticos globais), o algoritmo deve ter **autonomia total** para continuar negociando e tentar capturar lucros em oscilações rápidas, ou o sistema deve impor uma **parada forçada compulsória (circuit breaker)**, mesmo que isso impeça potenciais ganhos do investidor?
* **Alternativa A:** Priorizar a autonomia de execução, permitindo que a IA continue enviando ordens para aproveitar o volume.  
  *Consequência:* Risco iminente de *slippage* catastrófico, ordens executadas a preços desfavoráveis e perdas patrimoniais severas em milissegundos devido à falta de liquidez no livro de ofertas.
* **Alternativa B:** Priorizar o disjuntor compulsório de risco (Regras R01, R02 e R04), pausando operações até a estabilização do livro de ofertas.  
  *Consequência:* Perda momentânea de lucros em repiques rápidos de preço, porém com salvaguarda absoluta do capital principal e estrito cumprimento dos deveres fiduciários de prudência da CVM.

### 2. Sustentação Teórica
A sustentação da decisão pela **Alternativa B** apoia-se na tese do debatedor do Instituto de Estudos Avançados da USP (IEA-USP, 2026), que demonstra que a pretensa "autonomia irrestrita" em mercados digitais gera fragilidade sistêmica e externalidades negativas que afetam a todos os participantes. Conforme Lacerda Júnior (2026), a governança não consiste em suprimir a inovação tecnológica, mas em criar balizas institucionais e responsabilidade algorítmica explícita.

### 3. Parágrafo Individual Pós-Debate
* **Posição do Integrante:**  
  Após as discussões em sala, mantenho integralmente a decisão de priorizar os disjuntores rígidos de segurança patrimonial (`R01` a `R04`) em detrimento da busca por lucros em alta volatilidade. O argumento que mais consolidou essa posição foi o entendimento de que a inteligência artificial deve operar como mecanismo de defesa e ampliação da racionalidade humana, e nunca como um agente desprovido de limites regulatórios. Para verificar empiricamente a eficácia dessa medida, a equipe utiliza testes de estresse (*backtesting* e testes unitários de borda em Python) simulando eventos de falha de conexão e picos de volatilidade, confirmando que em 100% dos cenários anômalos o motor aciona o bloqueio de segurança em tempo constante, preservando a integridade da conta.

---

## 4. Declaração de Uso de Sistemas de IA

### IA Incorporada ao Projeto
> O projeto utiliza um **modelo supervisionado de Árvore de Decisão (`DecisionTreeClassifier` via scikit-learn)** integrado a um **Motor de Inferência Simbólico em Python por Encadeamento para Frente** para a **gestão de risco operacional e classificação preliminar de regimes de mercado financeiro**. O sistema recebe **dados quantitativos de mercado (Volatilidade ATR, Força de Tendência ADX, Custo de Liquidez/Spread e Retorno Percentual Recente) combinados a fatos regulatórios operacionais (status de Circuit Breaker da B3, Drawdown diário, eventos macroeconômicos do Bacen/Fed e perdas consecutivas)** e gera como saída a **ação operacional recomendada (ex: `AUTORIZAR_EXECUCAO_PADRAO`, `BLOQUEAR_OPERACAO_CIRCUIT_BREAKER_B3`, `PAUSAR_OPERACAO_DISJUNTOR_MACROECONOMICO`), acompanhada da regra disparada, da justificativa técnica, da fundamentação regulatória e da trilha de auditoria ('Como?')**. A equipe verificou seu funcionamento por meio de **divisão estratificada treino/teste (acurácia de 100% no conjunto de teste independente), análise da matriz de confusão e uma bateria de 12 testes automatizados em pytest cobrindo casos positivos, negativos, cenários extremos e tratamento de incerteza ('?')**. As limitações identificadas incluem **a dependência da estabilidade do feed de cotações em tempo real e a necessidade de recalibração periódica da árvore para novos ciclos econômicos**. A revisão cabe ao **gestor de risco de mercado e aos analistas quantitativos responsáveis pela mesa de operações**.

### IA Utilizada na Elaboração do Trabalho
> Utilizei ferramentas de inteligência artificial generativa como **ferramenta de apoio técnico à programação e codificação em Python**, auxiliando na **organização da estrutura do repositório, compilação de bibliotecas, contextualização de referências regulatórias da CVM/B3 e refinamento da bateria de testes em pytest**. A concepção da ideia do projeto, a formulação das regras de negócio, a seleção e modelagem dos parâmetros financeiros e a validação de todos os resultados foram integralmente realizadas por nós, integrantes do grupo. Aproveitei as contribuições de sintaxe e documentação após **revisar criteriosamente cada linha de código, executar e verificar a passagem integral dos testes no terminal e validar os relatórios de inferência**. Assumo a responsabilidade pelas escolhas, verificações e conteúdo integral da entrega.
