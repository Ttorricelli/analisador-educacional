# Registro de testes — Etapas 3 e 4

## Testes automatizados

Os comandos abaixo foram executados novamente no conteúdo do projeto enviado para revisão.

| Módulo | Comando | Resultado observado |
|---|---|---|
| Backend: scanner, validação, API, parser e AST | `cd backend && python -m pytest -q` | **54 aprovados, 0 reprovados** |
| Frontend: lógica, interface simulada, exemplos, HTML e regressão | `cd frontend && npm test` | **40 aprovados, 0 reprovados** |

**Total: 94 testes automatizados aprovados.**

## Testes manuais da interface

Os sete cenários abaixo foram executados manualmente na interface, com os resultados registrados em [`casos_de_teste.md`](casos_de_teste.md):

- programa com atribuições, operações e chamada de `print`;
- expressão incompleta;
- expressão com parênteses;
- parêntese de fechamento ausente em atribuição;
- parêntese de fechamento ausente em chamada de `print`;
- operador em posição inválida;
- precedência de multiplicação sobre adição.

Todos apresentaram o comportamento esperado.

## Verificação integrada com Docker

Foi executado `docker compose up --build -d` na pasta do projeto. A saída apresentada no terminal indicou:

- imagem do backend construída;
- imagem do frontend construída;
- container do frontend em estado `Running`;
- container do backend em estado `Healthy`.

Também foi realizada uma análise manual pelo navegador em `http://localhost:8080`. A interface apresentou os resultados léxicos, sintáticos e a AST para entradas válidas, além de mensagens de erro sintático para entradas inválidas.

## Observação

Os testes automatizados foram executados no ambiente de revisão. A inicialização com Docker e os testes manuais foram confirmados a partir das saídas compartilhadas durante a validação do projeto. O comportamento pode variar em outro computador conforme a instalação e a configuração do ambiente.
