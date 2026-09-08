# Lista de Exercícios — Autômatos Finitos Determinísticos (AFD)

> **Disciplina:** Teoria das Linguagens e Autômatos  
> **Tema:** Autômatos Finitos Determinísticos  
> **Modalidade:** Atividade prática em grupo  
> **Objetivo:** identificar, interpretar, construir e testar AFDs.

---

## Identificação do grupo

| Campo | Preenchimento |
|---|---|
| Turma | |
| Data | |
| Integrante 1 | |
| Integrante 2 | |
| Integrante 3 | |
| Integrante 4 | |

## Orientações

- Registre o raciocínio utilizado em cada resposta.
- Nos exercícios com cadeias, apresente o caminho percorrido estado por estado.
- Nos exercícios de construção, entregue a quíntupla, a tabela de transição e o diagrama.
- Use `ε` para representar a cadeia vazia.
- Quando solicitado, implemente e teste o autômato no JFLAP.

---

# Parte 1 — Fundamentos

## Exercício 1 — Entendendo um autômato finito

Uma lâmpada controlada por um interruptor possui os estados `Desligado` e `Ligado`. Sempre que o botão é pressionado, ocorre a mudança:

```text
Desligado --pressionar--> Ligado
Ligado    --pressionar--> Desligado
```

Responda:

1. Quantos estados existem?
2. Qual é o estado inicial, considerando que a lâmpada começa apagada?
3. Qual entrada provoca uma transição?
4. Partindo de `Desligado`, qual será o estado após um acionamento?
5. Partindo de `Desligado`, qual será o estado após dois acionamentos?
6. Explique o funcionamento do sistema com suas palavras.

## Exercício 2 — Porta automática

Uma porta automática possui os estados `Fechado` e `Aberto`. O sensor identifica `pessoa_detectada` ou `nenhuma_pessoa`. Quando uma pessoa é detectada, a porta deve ficar aberta; quando ninguém é detectado, deve ficar fechada.

Complete a tabela:

| Estado atual | Entrada | Próximo estado |
|---|---|---|
| Fechado | pessoa_detectada | Aberto |
| Fechado | nenhuma_pessoa | Fechado |
| Aberto | pessoa_detectada | Aberto |
| Aberto | nenhuma_pessoa | Fechado |

Depois, desenhe o diagrama de estados correspondente e indique o estado inicial.

            pessoa_detectada
        ┌────────────────────────┐
        │                        ▼
   ┌──────────┐              ┌──────────┐
   │ FECHADO  │              │  ABERTO  │
   └──────────┘              └──────────┘
        ▲                        │
        │                        │
        └────────────────────────┘
             nenhuma_pessoa


# Parte 2 — Anatomia e definição formal

## Exercício 3 — Identificando os elementos

Considere um AFD com `Σ = {0,1}`, `Q = {q0,q1}`, estado inicial `q0`, estado final `q1` e as transições abaixo:

| δ | 0 | 1 |
|---|---|---|
| q0 | q0 | q1 |
| q1 | q0 | q1 |

Identifique e explique:

1. o alfabeto `Σ`;
2. o conjunto de estados `Q`;
3. o estado inicial;
4. o conjunto de estados finais `F`;
5. os símbolos que podem ser lidos;
6. o significado do círculo duplo em um diagrama;
7. o significado da seta sem origem apontando para um estado.

## Exercício 4 — A quíntupla do AFD

Um AFD é formalmente representado por:

```text
M = (Σ, Q, δ, q0, F)
```

Complete:

| Elemento | Significado |
|---|---|
| `Σ` | Entrada |
| `Q` | Estados |
| `δ` | 	Mudança de estado |
| `q0` | 	Estado inicial |
| `F` | 	Estados finais |

Explique por que esses cinco elementos são suficientes para definir o funcionamento de um AFD.

Porque eles dizem quais símbolos existem, quais estados existem, como o AFD muda de estado, onde começa e quais estados aceitam a palavra.


# Parte 3 — Tabela de transições e cadeias

## Exercício 5 — Interpretando uma tabela

Considere `Σ = {0,1}`, `Q = {q0,q1,q2}`, estado inicial `q0`, `F = {q1}` e:

| δ | 0 | 1 |
|---|---|---|
| q0 | q0 | q1 |
| q1 | q2 | q1 |
| q2 | q1 | q1 |

Responda:

1. Qual é o resultado de `δ(q0,0)`?
2. Qual é o resultado de `δ(q0,1)`?
3. Qual é o resultado de `δ(q1,0)`?
4. Qual é o resultado de `δ(q2,1)`?
5. Qual é o estado de aceitação?
6. Desenhe o diagrama correspondente à tabela.
7. Justifique por que o autômato é determinístico.

## Exercício 6 — Aceita ou rejeita?

Utilize o AFD do Exercício 5. Determine se cada cadeia é aceita ou rejeitada:

```text
a) 1
b) 0011001
c) 010010
d) 1101
e) 000011010
```

Para cada cadeia, registre todas as transições. Exemplo:

```text
Cadeia: 01
q0 --0--> q0
q0 --1--> q1
Estado final: q1
Resultado: ACEITA
```

| Cadeia | Caminho percorrido | Estado final | Resultado |
|---|---|---|---|
| `1` | | | |
| `0011001` | | | |
| `010010` | | | |
| `1101` | | | |
| `000011010` | | | |

---

# Parte 4 — Construção de AFDs

## Exercício 7 — Cadeias que terminam em `1`

Construa um AFD sobre `Σ = {0,1}` que reconheça todas as cadeias que terminam em `1`.

- Devem ser aceitas: `1`, `01`, `101`, `0001`, `1101`.
- Devem ser rejeitadas: `ε`, `0`, `10`, `100`, `1110`.

Entregue: conjunto de estados, alfabeto, estado inicial, estados finais, tabela, diagrama e teste de pelo menos cinco cadeias.

Q = {q0, q1}

Σ = {0,1}

Estado inicial: q0

Estados finais: F = {q1}

Tabela de transições:

Estado	0	1
→ q0	q0	q1
* q1	q0	q1

Diagrama:

→ q0 --1--> q1*
↑ │
│ │
└---0-----┘

q0 --0--> q0
q1 --1--> q1

Testes:

1 → q0 → q1 → ACEITA
01 → q0 → q0 → q1 → ACEITA
101 → q0 → q1 → q0 → q1 → ACEITA
0001 → q0 → q0 → q0 → q0 → q1 → ACEITA
1101 → q0 → q1 → q1 → q0 → q1 → ACEITA

ε → q0 → REJEITA
0 → q0 → q0 → REJEITA
10 → q0 → q1 → q0 → REJEITA
100 → q0 → q1 → q0 → q0 → REJEITA
1110 → q0 → q1 → q1 → q1 → q0 → REJEITA


## Exercício 8 — Número par de símbolos `1`

Construa um AFD sobre `Σ = {0,1}` que reconheça cadeias com quantidade par de símbolos `1`.

Analise: `ε`, `0`, `1`, `11`, `101`, `1100` e `10101`.

Apresente a definição formal `M = (Σ, Q, δ, q0, F)`, a tabela, o diagrama e o processamento das cadeias. Lembre-se de que basta controlar duas situações: quantidade par ou ímpar de símbolos `1`.

## Exercício 9 — Pelo menos dois zeros consecutivos

Construa um AFD para:

```text
L(M) = {w ∈ {0,1}* | w possui pelo menos dois 0s consecutivos}
```

- Devem ser aceitas: `00`, `001`, `100`, `1001`, `110011`, `0000`.
- Devem ser rejeitadas: `ε`, `0`, `1`, `01`, `10`, `10101`.

  Q = {q0, q1, q2}

Σ = {0,1}

Estado inicial: q0

Estado final: F = {q2}

Tabela de transições:

Estado	0	1
→ q0	q1	q0
q1	q2	q0
* q2	q2	q2

Diagrama:

→ q0 --0--> q1 --0--> q2*
↑ │ │
│ 1 │
└----1-----┘ │
│
0,1 ─┘

Testes:

00 → q0 → q1 → q2 → ACEITA
001 → q0 → q1 → q2 → q2 → ACEITA
100 → q0 → q0 → q1 → q2 → ACEITA
1001 → q0 → q0 → q1 → q2 → q2 → ACEITA
110011 → q0 → q0 → q0 → q1 → q2 → q2 → q2 → ACEITA
0000 → q0 → q1 → q2 → q2 → q2 → ACEITA

ε → q0 → REJEITA
0 → q0 → q1 → REJEITA
1 → q0 → q0 → REJEITA
01 → q0 → q1 → q0 → REJEITA
10 → q0 → q0 → q1 → REJEITA
10101 → q0 → q0 → q1 → q0 → q1 → q0 → REJEITA

Responda antes de construir:

1. O que o estado inicial representa? O estado inicial representa que ainda não encontramos nenhum 0 consecutivo.
2. O que ocorre quando aparece o primeiro `0`? Quando aparece o primeiro 0, o autômato vai para um estado que indica que encontramos um 0
3. O que ocorre quando outro `0` aparece imediatamente depois? Quando outro 0 aparece imediatamente depois, encontramos 00, então o autômato vai para o estado final.
4. Depois de encontrar `00`, a cadeia pode deixar de ser aceita? Não. Depois de encontrar 00, a cadeia continua sendo aceita, independentemente dos símbolos que aparecem depois.
5. Quantos estados são necessários? ão necessários 3 estados: um para nenhum 0, um para um único 0 e um estado final para quando encontramos 00.

Apresente a quíntupla, a tabela, o diagrama e os testes.

Quíntupla:

M = (Q, Σ, δ, q0, F)

Q = {q0, q1, q2}

Σ = {0,1}

q0 = estado inicial

F = {q2}

Tabela de transições:

Estado	0	1
→ q0	q1	q0
q1	q2	q0
* q2	q2	q2

Diagrama:

→ q0 --0--> q1 --0--> q2*
↑ │ │
│ 1 │
└----1-----┘ 0,1
│
↓
q2

Testes:

00 → q0 → q1 → q2 → ACEITA

001 → q0 → q1 → q2 → q2 → ACEITA

100 → q0 → q0 → q1 → q2 → ACEITA

1001 → q0 → q0 → q1 → q2 → q2 → ACEITA

110011 → q0 → q0 → q0 → q1 → q2 → q2 → q2 → ACEITA

0000 → q0 → q1 → q2 → q2 → q2 → ACEITA

ε → q0 → REJEITA

0 → q0 → q1 → REJEITA

1 → q0 → q0 → REJEITA

01 → q0 → q1 → q0 → REJEITA

10 → q0 → q0 → q1 → REJEITA

10101 → q0 → q0 → q1 → q0 → q1 → q0 → REJEITA

# Parte 5 — Desafios de modelagem

## Exercício 10 — Semáforo

Modele um semáforo com os estados `Verde`, `Amarelo` e `Vermelho`. Use a entrada `tempo` e represente o ciclo:

```text
Verde → Amarelo → Vermelho → Verde
```

Entregue o diagrama, a tabela de transições, a definição formal e uma explicação do funcionamento. Discuta se há sentido em definir estados de aceitação nesse modelo e justifique a escolha adotada.

## Exercício 11 — Sistema de login

Modele um sistema com as entradas `senha_correta` e `senha_incorreta`. Uma senha correta autentica o usuário; após três tentativas incorretas, o sistema fica bloqueado.

Determine:

1. todos os estados necessários para contar as tentativas; 
2. o alfabeto de entrada; 
3. o estado inicial; 
4. os estados finais; 
5. todas as transições;
6. o comportamento após a autenticação e após o bloqueio.
  
Responda: apenas os estados `Aguardando`, `Autenticado` e `Bloqueado` são suficientes para controlar três tentativas? Justifique e construa o AFD completo.

Não. Apenas os estados Aguardando, Autenticado e Bloqueado não são suficientes, pois o sistema precisa distinguir entre 1ª, 2ª e 3ª tentativa incorreta. É necessário guardar a quantidade de tentativas para saber quando bloquear o usuário.
Quíntupla:

M = (Q, Σ, δ, q0, F)

Q = {q0, q1, q2, qA, qB}

Onde:

q0 = Aguardando, 0 tentativas incorretas
q1 = Aguardando, 1 tentativa incorreta
q2 = Aguardando, 2 tentativas incorretas
qA = Autenticado
qB = Bloqueado

Σ = {senha_correta, senha_incorreta}

Estado inicial: q0

Estados finais: F = {qA, qB}

Tabela de transições:

Estado	senha_correta	senha_incorreta
→ q0	qA	q1
q1	qA	q2
q2	qA	qB
*qA	qA	qA
*qB	qB	qB

Diagrama:

→ q0 --senha_incorreta--> q1 --senha_incorreta--> q2 --senha_incorreta--> qB*
│ │ │
│ senha_correta │ senha_correta │ senha_correta
↓ ↓ ↓
qA* <────────────────────┴───────────────────────┘

qA --qualquer entrada--> qA

qB --qualquer entrada--> qB

Comportamento:

Uma senha_correta em qualquer estado de tentativa leva para qA (Autenticado).
A 1ª senha incorreta leva de q0 para q1.
A 2ª senha incorreta leva de q1 para q2.
A 3ª senha incorreta leva de q2 para qB (Bloqueado).
Após a autenticação, o sistema permanece autenticado.
Após o bloqueio, o sistema permanece bloqueado.


# Parte 6 — Prática no JFLAP

## Exercício 12 — Implementação e testes

Escolha um dos AFDs dos exercícios 7, 8 ou 9 e implemente-o no JFLAP.

1. Crie os estados.
2. Defina o estado inicial e os estados finais.
3. Crie todas as transições.
4. Teste três cadeias que devem ser aceitas.
5. Teste três cadeias que devem ser rejeitadas.
6. Compare os resultados esperados e obtidos.

Inclua um print do AFD, a tabela de testes e uma breve explicação.

| Cadeia | Resultado esperado | Resultado no JFLAP | Conferência |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

---

# Desafio final

## Exercício 13 — Crie seu próprio problema

Escolha uma situação real representável por estados, como elevador, máquina de vendas, controle de acesso, estacionamento, pedido de delivery, semáforo, porta eletrônica ou protocolo de comunicação.

O grupo deverá:

1. descrever o problema e suas regras;
2. identificar as entradas e os estados;
3. definir o estado inicial e os estados finais;
4. criar a tabela de transições;
5. desenhar o AFD;
6. apresentar `M = (Σ, Q, δ, q0, F)`;
7. testar pelo menos cinco sequências de entrada;
8. explicar por que o modelo é determinístico;
9. apresentar uma conclusão sobre o que foi aprendido.

---

# Entregável

O grupo deverá entregar um único arquivo `README.md`, contendo:

- identificação do grupo;
- respostas dos exercícios indicados pela professora;
- diagramas e tabelas de transição;
- processamento estado por estado das cadeias;
- evidência dos testes no JFLAP;
- conclusão do grupo.

## Modelo para o desafio final

```markdown
## Desafio final

### Problema escolhido

### Estados e significado

### Alfabeto

### Estado inicial e estados finais

### Tabela de transições

### Diagrama

### Definição formal
M = (Σ, Q, δ, q0, F)

### Testes realizados
| Entrada | Resultado esperado | Resultado obtido |
|---|---|---|
| | | |

### Evidência no JFLAP

### Conclusão
```

> **Importante:** não basta apresentar o diagrama. Demonstre como o AFD processa cada cadeia, estado por estado, até decidir pela aceitação ou rejeição.

---

**Profa. Kadidja Valéria**
