# Resolução de Exercícios — Autômatos Finitos Determinísticos (AFD)

## Identificação do grupo

| Campo | Preenchimento |
|---|---|
| Turma | N1_3132_-_C.C_(Not) |
| Data | 01/09/2026 |
| Integrante 1 | Danilo Hellu Santos Ramos |
| Integrante 2 | João Paulo De Oliveira Paiva |
| Integrante 3 | Victor Hugo Valadares Mendonça |

---

## Exercício 1 — Entendendo um autômato finito

1. Quantos estados existem?
   **R:** 2 estados.
2. Qual é o estado inicial, considerando que a lâmpada começa apagada?
   **R:** Desligado.
3. Qual entrada provoca uma transição?
   **R:** Pressionar.
4. Partindo de `Desligado`, qual será o estado após um acionamento?
   **R:** Ligado.
5. Partindo de `Desligado`, qual será o estado após dois acionamentos?
   **R:** Desligado.
6. Explique o funcionamento do sistema com suas palavras.
   **R:** O sistema do interruptor funciona de maneira "normal". A cada vez que o interruptor é pressionado, ocorre a troca do estado atual para o estado inverso ("Ligado" para "Desligado", ou "Desligado" para "Ligado"), a fim de acender ou apagar a lâmpada.

## Exercício 3 — Identificando os elementos

1. o alfabeto `Σ`;
   **R:** `Σ = {0, 1}`. É o conjunto finito de símbolos (ou caracteres) de entrada que o autômato é capaz de ler e processar.
2. o conjunto de estados `Q`;
   **R:** `Q = {q0, q1}`. Representa todas as situações (ou configurações) possíveis e finitas nas quais o autômato pode se encontrar durante a sua execução.
3. o estado inicial;
   **R:** `q0`. É o estado de partida, ou seja, o estado em que o autômato sempre inicia a leitura de uma determinada cadeia de entrada.
4. o conjunto de estados finais `F`;
   **R:** `F = {q1}`. É o conjunto de estados de aceitação. Se, após ler toda a cadeia de caracteres, o autômato parar em um desses estados, a palavra é considerada aceita (válida) pela linguagem.
5. os símbolos que podem ser lidos;
   **R:** Os símbolos `0` e `1`. Estes correspondem exatamente aos elementos definidos no alfabeto `Σ`.
6. o significado do círculo duplo em um diagrama;
   **R:** Em um diagrama de transição de estados (grafo), o círculo duplo serve para identificar visualmente um **estado final** (ou estado de aceitação).
7. o significado da seta sem origem apontando para um estado.
   **R:** Indica o **estado inicial** do autômato. É a indicação visual de onde o processamento da cadeia de texto deve começar.

## Exercício 5 — Interpretando uma tabela

1. Qual é o resultado de `δ(q0,0)`?
   **R:** `q0`
2. Qual é o resultado de `δ(q0,1)`?
   **R:** `q1`
3. Qual é o resultado de `δ(q1,0)`?
   **R:** `q2`
4. Qual é o resultado de `δ(q2,1)`?
   **R:** `q1`
5. Qual é o estado de aceitação?
   **R:** O estado de aceitação é o `q1` (logo, `F = {q1}`).
6. Desenhe o diagrama correspondente à tabela.
   **R:**
   ```text
        0
    +-------+
    |       v
 ->(q0) --1--> ((q1)) <--0-- (q2)
                 | ^          ^ ^
                 | |          | |
                 +-1----------+-+ (q2 transita para q1 com 0 e 1)
   ```
7. Justifique por que o autômato é determinístico.
   **R:** Ele é determinístico porque, para cada estado e para cada entrada lida (0 ou 1), existe apenas um único estado de destino possível. O autômato nunca tem ambiguidade para onde ir a partir de uma configuração lendo um símbolo de entrada.

## Exercício 6 — Aceita ou rejeita?

| Cadeia | Caminho percorrido | Estado final | Resultado |
|---|---|---|---|
| `1` | `q0 --1--> q1` | `q1` | ACEITA |
| `0011001` | `q0 --0--> q0 --0--> q0 --1--> q1 --1--> q1 --0--> q2 --0--> q1 --1--> q1` | `q1` | ACEITA |
| `010010` | `q0 --0--> q0 --1--> q1 --0--> q2 --0--> q1 --1--> q1 --0--> q2` | `q2` | REJEITA |
| `1101` | `q0 --1--> q1 --1--> q1 --0--> q2 --1--> q1` | `q1` | ACEITA |
| `000011010` | `q0 --0--> q0 --0--> q0 --0--> q0 --0--> q0 --1--> q1 --1--> q1 --0--> q2 --1--> q1 --0--> q2` | `q2` | REJEITA |

## Exercício 8 — Número par de símbolos `1`

**1. Definição Formal:**
`M = (Σ, Q, δ, q0, F)` onde:
- `Σ = {0, 1}`
- `Q = {q0, q1}`
- `q0` = Estado inicial (representa a quantidade par de `1`s lidos)
- `F = {q0}` (Estado de aceitação)
- `δ` (Função de transição):
  - `δ(q0, 0) = q0`
  - `δ(q0, 1) = q1`
  - `δ(q1, 0) = q1`
  - `δ(q1, 1) = q0`

**2. Tabela de Transição:**

| δ (estado atual) | 0 | 1 |
| :--- | :--- | :--- |
| **-> *q0** | q0 | q1 |
| **q1** | q1 | q0 |

**3. Diagrama do AFD:**
```text
  0                 0
 ┌───┐             ┌───┐
 │   ▼     1       │   ▼
 ►((q0)) ────────► (q1)
   ▲                 │
   │        1        │
   └─────────────────┘
```

**4. Análise e Processamento das Cadeias solicitadas (`ε`, `0`, `1`, `11`, `101`, `1100`, `10101`):**

- **Cadeia: `ε`** (Palavra vazia)
  - Processamento: Inicia e termina em `q0`
  - Resultado: Parou em `q0` -> **ACEITA**

- **Cadeia: `0`**
  - Processamento: `q0 --0--> q0`
  - Resultado: Parou em `q0` -> **ACEITA**

- **Cadeia: `1`**
  - Processamento: `q0 --1--> q1`
  - Resultado: Parou em `q1` -> **REJEITA**

- **Cadeia: `11`**
  - Processamento: `q0 --1--> q1 --1--> q0`
  - Resultado: Parou em `q0` -> **ACEITA**

- **Cadeia: `101`**
  - Processamento: `q0 --1--> q1 --0--> q1 --1--> q0`
  - Resultado: Parou em `q0` -> **ACEITA**

- **Cadeia: `1100`**
  - Processamento: `q0 --1--> q1 --1--> q0 --0--> q0 --0--> q0`
  - Resultado: Parou em `q0` -> **ACEITA**

- **Cadeia: `10101`**
  - Processamento: `q0 --1--> q1 --0--> q1 --1--> q0 --0--> q0 --1--> q1`
  - Resultado: Parou em `q1` -> **REJEITA**

## Exercício 12 — Implementação e testes (AFD do Ex. 7)

**Explicação:** 
Para este exercício, foi implementado o AFD que reconhece a linguagem de todas as cadeias sobre o alfabeto `Σ = {0,1}` que possuem a substring `"00"`. 
- `q0` é o estado inicial (onde a leitura começa).
- `q1` é o estado alcançado após ler o primeiro `0` da sequência.
- `q2` é o estado final/de aceitação, alcançado assim que a cadeia identifica o segundo `0` consecutivo. Ao chegar em `q2`, o autômato permanece lá para qualquer símbolo lido (`0` ou `1`), caracterizando a aceitação da cadeia.

**Print do AFD no JFLAP:**
![Print do AFD no JFLAP](./jflap-ex12.png)

**Tabela de Testes:**

| Cadeia | Resultado esperado | Resultado no JFLAP | Conferência |
|---|---|---|---|
| `100` | Aceita | Accept | OK |
| `0011` | Aceita | Accept | OK |
| `101001` | Aceita | Accept | OK |
| `101` | Rejeitada | Reject | OK |
| `010` | Rejeitada | Reject | OK |
| `1` | Rejeitada | Reject | OK |

---

## Desafio Final

### Problema escolhido
**Controle de Câmbio de um Carro (Automático Simples / Marchas)**
Vamos modelar o sistema de marchas de um carro automático simplificado. O sistema permite aumentar a marcha de Neutro até a 3ª Marcha, ou reduzir. Apenas no Neutro é possível engatar a Ré, e da Ré só é possível voltar ao Neutro.

### Estados e significado
- `N` (Neutro) - Estado em que o carro está desengatado. Estado inicial.
- `M1` (1ª Marcha) - Veículo em primeira marcha.
- `M2` (2ª Marcha) - Veículo em segunda marcha.
- `M3` (3ª Marcha) - Veículo em terceira marcha (marcha máxima neste modelo). Estado de Aceitação (representando, no nosso sistema, a velocidade cruzeiro desejada).
- `R` (Ré) - Veículo em marcha à ré.

### Alfabeto
`Σ = { +, -, r, n }`
- `+` : Aumentar uma marcha
- `-` : Reduzir uma marcha
- `r` : Engatar a ré
- `n` : Desengatar a ré (voltar ao neutro)

### Estado inicial e estados finais
- **Estado Inicial:** `N`
- **Estado Final:** `M3` (Considerando que o nosso objetivo é atingir a velocidade cruzeiro na terceira marcha).

### Tabela de transições

*(Nota: Entradas inválidas para o estado atual simplesmente mantêm o estado)*

| δ | `+` | `-` | `r` | `n` |
|---|---|---|---|---|
| **-> N** | M1 | N | R | N |
| **M1** | M2 | N | M1 | M1 |
| **M2** | M3 | M1 | M2 | M2 |
| **((M3))** | M3 | M2 | M3 | M3 |
| **R** | R | R | R | N |

### Diagrama

```text
       r           n
   ┌─────► [ R ] ─────┐
   │                  ▼
  (N) ──+──► (M1) ──+──► (M2) ──+──► ((M3))
   ▲          │       ▲        │        │
   └───-──────┘       └───-────┘        │
                                        │
    (Em qualquer estado diferente de N, │
     entradas "r" ou "n" são ignoradas) 
```

### Definição formal
`M = (Σ, Q, δ, q0, F)`
- `Σ = {+, -, r, n}`
- `Q = {N, M1, M2, M3, R}`
- `q0 = N`
- `F = {M3}`

### Testes realizados

| Entrada | Resultado esperado | Resultado obtido (Processamento) |
|---|---|---|
| `+`, `+`, `+` | Aceita (Chega na 3ª) | N --+--> M1 --+--> M2 --+--> M3 (ACEITA) |
| `r`, `n`, `+` | Rejeita (Chega na 1ª) | N --r--> R --n--> N --+--> M1 (REJEITA) |
| `+`, `r`, `+` | Rejeita (Chega na 2ª) | N --+--> M1 --r--> M1 --+--> M2 (REJEITA) |
| `+`, `+`, `+`, `+` | Aceita (Limita na 3ª) | N --+--> M1 --+--> M2 --+--> M3 --+--> M3 (ACEITA) |
| `+`, `+`, `-`, `+` | Rejeita (Chega na 2ª) | N --+--> M1 --+--> M2 -----> M1 --+--> M2 (REJEITA) |

### Conclusão
O modelo demonstra como um Autômato Finito Determinístico pode abstrair lógicas mecânicas e eletrônicas cotidianas através de controle de transição de estados. O sistema é determinístico porque, não importando a situação, qualquer ação do motorista (`+`, `-`, `r`, `n`) sempre resultará num único estado definido, impedindo por exemplo o engate da ré durante a locomoção frontal.
