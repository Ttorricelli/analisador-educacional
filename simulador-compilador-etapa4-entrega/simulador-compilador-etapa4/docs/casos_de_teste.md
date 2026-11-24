# Casos de Teste — Etapa 4

## Objetivo

Registrar os testes manuais executados na interface para verificar a análise sintática, a identificação de erros e a construção da Árvore Sintática Abstrata (AST).

## Casos de teste executados

| ID | Entrada | Resultado esperado | Resultado observado | Status |
|---|---|---|---|---|
| CT01 | `x = 10 + 5`<br>`y = x * 2`<br>`print(y)` | Código aceito; AST com duas atribuições e uma chamada de `print` | Código reconhecido e AST gerada com as três instruções | Aprovado |
| CT02 | `x = 10 +` | Erro sintático por expressão incompleta | Esperado um valor, mas a instrução terminou | Aprovado |
| CT03 | `x = (10 + 5) * 2` | Código aceito e soma agrupada antes da multiplicação | AST representa a soma como operando da multiplicação | Aprovado |
| CT04 | `x = (10 + 5` | Erro sintático por parêntese não fechado | Esperado `)`, mas a instrução terminou | Aprovado |
| CT05 | `print(x` | Erro sintático por chamada incompleta | Esperado `)`, mas a instrução terminou | Aprovado |
| CT06 | `x = * 5` | Erro sintático por operador em posição inválida | Elemento inesperado `*` em uma expressão | Aprovado |
| CT07 | `x = 10 + 5 * 2` | Código aceito e multiplicação agrupada antes da soma | AST apresenta a multiplicação como segundo operando da soma | Aprovado |

## Critérios de avaliação

Um caso de teste é considerado aprovado quando o comportamento observado na interface corresponde ao resultado esperado.

## Observações

Os sete cenários desta tabela foram executados manualmente na interface do simulador. Os resultados observados foram registrados a partir das saídas apresentadas pela aplicação.

Os testes automatizados do backend e do frontend são registrados separadamente em [`testes.md`](testes.md).
