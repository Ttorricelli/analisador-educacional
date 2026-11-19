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
5. As expressões são analisadas respeitando a precedência: sinais unários e parênteses; depois `*`, `/` e `%`; por fim `+` e `-`.
6. Os nós reconhecidos são organizados em uma AST serializável.
7. A API retorna os resultados; a interface apresenta tokens, erros e a AST quando a análise sintática é bem-sucedida.

## Testes

Os testes automatizados do parser cobrem atribuições, chamadas de `print`, precedência, parênteses e situações de erro sintático.

Os sete cenários de teste manual executados na interface estão registrados em [`casos_de_teste.md`](casos_de_teste.md). Os resultados dos testes automatizados e as verificações de integração estão em [`testes.md`](testes.md).

## Limitações

Cada instrução suportada ocupa uma linha. A implementação não reconhece Python completo nem blocos indentados, condicionais, laços, definições de função, listas, dicionários ou chamadas genéricas de função.
