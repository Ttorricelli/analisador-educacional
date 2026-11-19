# Gramática EBNF do Subconjunto Educacional de Python

## 1. Escopo

A gramática descreve o subconjunto efetivamente reconhecido pelo parser. Cada instrução deve estar em uma linha. O parser aceita atribuições simples e chamadas de `print`, além de expressões com literais, identificadores, parênteses e operadores aritméticos.

O scanner classifica `print` como `IDENTIFICADOR`; o parser reconhece a chamada pelo lexema `print`.

## 2. Definição da gramática

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

## 3. Observações sobre a implementação

- A análise sintática é feita por um parser descendente recursivo.
- Os tokens são agrupados por número de linha; cada linha é analisada como uma instrução independente.
- A precedência implementada é: parênteses e sinais unários; depois `*`, `/` e `%`; por fim `+` e `-`.
- Os sinais unários `+` e `-` podem ser repetidos antes de um primário.
- `print()` pode ser chamado sem argumentos; também são aceitos um ou mais argumentos separados por vírgula.
- O parser não reconhece expressões distribuídas por várias linhas.

## 4. Exemplos

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

## 5. Limitações

Esta gramática não representa Python completo. Não são implementados blocos indentados, condicionais, laços, definições de função, listas, dicionários, chamadas genéricas de função ou operadores relacionais/lógicos na análise sintática.
