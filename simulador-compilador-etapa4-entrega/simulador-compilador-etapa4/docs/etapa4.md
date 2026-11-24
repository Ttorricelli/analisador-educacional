# Etapa 4 — implementação da análise sintática

## Escopo

A Etapa 4 implementa um parser descendente recursivo para um subconjunto didático de Python. Cada instrução é analisada em uma linha independente.

## Gramática

A gramática formal do subconjunto está documentada em [`gramatica_ebnf.md`](gramatica_ebnf.md).

O scanner classifica `print` como `IDENTIFICADOR`; o parser reconhece a chamada pelo lexema `print`.

## Fluxo

1. A API valida a requisição e o código recebido.
2. O scanner converte o código em tokens.
3. Se houver erro léxico, o parser não é executado.
4. O parser agrupa tokens por linha e reconhece atribuições ou chamadas de `print`.
5. As expressões são analisadas respeitando a precedência: parênteses; sinais unários; depois `*`, `/` e `%`; por fim `+` e `-`. Os operadores binários são associativos à esquerda.
6. Os nós reconhecidos são organizados em uma AST serializável, com posições de início e fim.
7. A API retorna tokens, erros léxicos e resultado sintático. A interface apresenta tokens, diagnósticos sintáticos (incluindo esperado/encontrado) e a AST somente quando a análise é bem-sucedida.

## Testes

Os testes automatizados do parser cobrem atribuições, chamadas de `print`, precedência, parênteses e situações de erro sintático.

Os sete cenários de teste manual executados na interface estão registrados em [`casos_de_teste.md`](casos_de_teste.md). Os resultados dos testes automatizados e as verificações de integração estão em [`testes.md`](testes.md).

## Diagnósticos

O parser acumula erros de instruções em linhas diferentes e sincroniza na próxima
linha após um erro. Cada diagnóstico contém linha, coluna, lista de elementos
esperados e lexema encontrado (quando houver). Se existir erro sintático, a API
retorna `ast: null`, evitando apresentar uma árvore parcial como resultado válido.
A análise sintática não é executada quando existem erros léxicos.

## Limitações

Cada instrução suportada ocupa uma linha. A implementação não reconhece Python completo nem blocos indentados, condicionais, laços, definições de função, listas, dicionários ou chamadas genéricas de função.
