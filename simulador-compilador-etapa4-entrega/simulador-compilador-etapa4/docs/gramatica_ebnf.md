# Gramática EBNF do Subconjunto Educacional de Python

## 1. Escopo

A gramática descreve o subconjunto efetivamente reconhecido pelo parser. Cada instrução deve estar em uma linha. O parser aceita atribuições simples e chamadas de `print`, além de expressões com literais, identificadores, parênteses e operadores aritméticos.

O scanner classifica `print` como `IDENTIFICADOR`; o parser reconhece a chamada pelo lexema `print`.

## 2. Definição da gramática

- **Símbolo inicial:** `PROGRAMA`.
- **Terminais:** identificadores, literais inteiros/reais/string e os lexemas `=`,
  `print`, `(`, `)`, `,`, `+`, `-`, `*`, `/` e `%`.
- **Não terminais:** `PROGRAMA`, `INSTRUCAO`, `ATRIBUICAO`,
  `CHAMADA_PRINT`, `ARGUMENTOS`, `EXPRESSAO`, `TERMO`, `FATOR` e `PRIMARIO`.
- **Separação de instruções:** cada instrução ocupa uma linha física. O scanner
  não emite tokens de quebra de linha; o parser usa a posição `linha` dos tokens
  para separar instruções.

### Correspondência com os tokens do scanner

| Elemento gramatical | Token/lexema produzido pelo scanner |
|---|---|
| `IDENTIFICADOR` | `IDENTIFICADOR` (exceto o lexema `print`, reservado pelo parser como chamada) |
| `LITERAL_INTEIRO` | `LITERAL_INTEIRO` |
| `LITERAL_REAL` | `LITERAL_REAL` |
| `LITERAL_STRING` | `LITERAL_STRING` |
| `=`, `+`, `-`, `*`, `/`, `%` | `OPERADOR`, comparado pelo lexema |
| `(`, `)`, `,` | `DELIMITADOR`, comparado pelo lexema |

Palavras reservadas de Python são reconhecidas pelo scanner, mas não fazem parte
das produções sintáticas suportadas nesta etapa. Por isso, por exemplo, `if`
pode ser tokenizado corretamente e ainda assim ser rejeitado pelo parser.


```ebnf
PROGRAMA       = { INSTRUCAO } ;

INSTRUCAO      = ATRIBUICAO | CHAMADA_PRINT ;

ATRIBUICAO     = IDENTIFICADOR, "=", EXPRESSAO ;

CHAMADA_PRINT  = "print", "(", [ ARGUMENTOS ], ")" ;

ARGUMENTOS     = EXPRESSAO, { ",", EXPRESSAO } ;

EXPRESSAO      = TERMO, { ("+" | "-"), TERMO } ;

TERMO          = FATOR, { ("*" | "/" | "%"), FATOR } ;

FATOR          = { "+" | "-" }, PRIMARIO ;

PRIMARIO       = LITERAL_INTEIRO
               | LITERAL_REAL
               | LITERAL_STRING
               | IDENTIFICADOR
               | "(", EXPRESSAO, ")" ;
```

## 3. Precedência e associatividade

| Maior para menor precedência | Operadores | Associatividade |
|---|---|---|
| Primários | parênteses, literais e identificadores | — |
| Unários | `+`, `-` | da direita para a esquerda |
| Multiplicativos | `*`, `/`, `%` | da esquerda para a direita |
| Aditivos | `+`, `-` | da esquerda para a direita |

Assim, `2 + 3 * 4` é agrupado como `2 + (3 * 4)`, enquanto
`10 - 3 - 2` é agrupado como `(10 - 3) - 2`.

## 4. Observações sobre a implementação

- A análise sintática é feita por um parser descendente recursivo.
- Os tokens são agrupados por número de linha; cada linha é analisada como uma instrução independente.
- A precedência implementada é: parênteses e sinais unários; depois `*`, `/` e `%`; por fim `+` e `-`.
- Os sinais unários `+` e `-` podem ser repetidos antes de um primário.
- `print()` pode ser chamado sem argumentos; também são aceitos um ou mais argumentos separados por vírgula.
- O parser não reconhece expressões distribuídas por várias linhas.

## 5. Exemplos

Atribuições:
```python
x = 10
resultado = 10 + 5 * 2
ajustado = (10 + 5) * 2
resto = 10 % 3
```

Chamadas de `print`:
```python
print(x)
print(x, resultado)
print()
```

Sinais unários:
```python
x = --10
y = +-5
```

## 6. Limitações

Esta gramática não representa Python completo. Não são implementados blocos indentados, condicionais, laços, definições de função, listas, dicionários, chamadas genéricas de função ou operadores relacionais/lógicos na análise sintática.

## 7. Diagnósticos e recuperação

O parser registra `tipo`, `mensagem`, `linha`, `coluna`, `esperado` e
`encontrado` em cada erro sintático. A recuperação é feita por linha: depois
de identificar um erro em uma instrução, o parser continua na próxima linha,
permitindo apresentar mais de um diagnóstico. Se houver qualquer erro, `ast`
é `null`; não é apresentada uma árvore parcial como se o programa inteiro
fosse válido.

Cada nó da AST inclui `linha`, `coluna`, `linha_fim` e `coluna_fim` quando
essas posições podem ser determinadas pelos tokens. A raiz `Programa` agrupa
as instruções válidas.
